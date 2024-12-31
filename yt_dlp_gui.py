import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import threading
import os
import yt_dlp
import math

class YTDLProgressHook:
    """
    Lớp này sẽ được yt-dlp gọi lại mỗi khi bắt đầu tải 1 video,
    đang tải, hoặc tải xong 1 video. Ta lợi dụng để cập nhật GUI.
    """

    def __init__(
        self, 
        title_label,         # Hiển thị title video đang tải
        progress_label,      # Hiển thị % tiến trình, tốc độ, ETA
        progress_bar,        # Thanh progress bar
        file_status_label,   # Hiển thị "Item X of Y"
        downloaded_count_label
    ):
        self.title_label = title_label
        self.progress_label = progress_label
        self.progress_bar = progress_bar
        self.file_status_label = file_status_label
        self.downloaded_count_label = downloaded_count_label

        self.total_files = 0       # Tổng số video (nếu là playlist)
        self.downloaded_files = 0  # Đã tải xong bao nhiêu video

    def format_bytes(self, n_bytes):
        """Đổi byte -> dạng KiB, MiB, GiB,... để hiển thị đẹp."""
        if n_bytes == 0:
            return "0B"
        units = ["B", "KiB", "MiB", "GiB", "TiB"]
        idx = 0
        while n_bytes >= 1024 and idx < len(units) - 1:
            n_bytes /= 1024
            idx += 1
        return f"{n_bytes:.2f}{units[idx]}"

    def format_eta(self, sec):
        """Đổi giây -> mm:ss, hoặc hh:mm:ss nếu >= 1 giờ."""
        try:
            sec = int(sec)
        except (ValueError, TypeError):
            return "Unknown"
        
        if sec < 60:
            return f"0:{sec:02d}"
        elif sec < 3600:
            m, s = divmod(sec, 60)
            return f"{m}:{s:02d}"
        else:
            h, r = divmod(sec, 3600)
            m, s = divmod(r, 60)
            return f"{h}:{m:02d}:{s:02d}"

    def __call__(self, d):
        """Hook được gọi mỗi khi yt-dlp có trạng thái mới (downloading/finished/error)."""
        status = d.get('status')
        
        # Lấy về playlist_count (nếu có, hoặc mặc định = 1)
        playlist_count = d.get('playlist_count', 1)
        # Lấy về playlist_index (nếu có, hoặc mặc định = 1)
        playlist_index = d.get('playlist_index', 1)

        # Nếu d['info_dict'] tồn tại, ta lấy title video
        info_dict = d.get('info_dict', {})
        current_title = info_dict.get('title', 'No Title')

        if status == 'downloading':
            # Lấy các thông tin cần thiết
            downloaded_bytes = d.get('downloaded_bytes', 0)
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate') or 0
            speed = d.get('speed') or 0  # byte/s
            eta = d.get('eta') or 0      # giây

            # Tính phần trăm
            if total_bytes > 0:
                percent = downloaded_bytes / total_bytes * 100
            else:
                percent = 0

            # Cập nhật progress bar
            self.progress_bar['value'] = percent

            # Định dạng chuỗi hiển thị
            downloaded_str = self.format_bytes(downloaded_bytes)
            total_str = self.format_bytes(total_bytes)
            speed_str = self.format_bytes(speed) + "/s" if speed else "0B/s"
            eta_str = self.format_eta(eta)

            # Ví dụ: "21.7% of 211.60MiB at 1.91MiB/s ETA 01:26"
            progress_text = (f"{percent:.1f}% of {total_str} "
                             f"at {speed_str} ETA {eta_str}")

            self.progress_label.config(text=progress_text)
            self.title_label.config(text=f"Video đang tải: {current_title}")

            # Cập nhật tổng số file
            self.total_files = max(self.total_files, playlist_count)
            
            # Hiển thị "item X of Y"
            if playlist_count > 1:
                self.file_status_label.config(
                    text=f"Đang tải item {playlist_index} of {playlist_count}"
                )
            else:
                self.file_status_label.config(text="")

        elif status == 'finished':
            # Khi 1 video tải xong
            self.progress_label.config(text="Hoàn tất 1 video!")
            self.progress_bar['value'] = 100

            self.downloaded_files += 1
            if self.total_files > 1:
                self.downloaded_count_label.config(
                    text=f"Đã tải {self.downloaded_files}/{self.total_files} file(s)"
                )
            else:
                self.downloaded_count_label.config(
                    text="Đã tải xong 1 video!"
                )

def choose_directory():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        folder_path.set(folder_selected)

def choose_cookies():
    cookies_selected = filedialog.askopenfilename(
        title="Chọn tệp cookies.txt",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )
    if cookies_selected:
        cookies_path.set(cookies_selected)

def start_download():
    """
    Chạy yt-dlp trong thread riêng để không khóa giao diện Tkinter.
    """
    url = url_entry.get().strip()
    folder = folder_path.get().strip()
    cookies = cookies_path.get().strip()

    if not url:
        messagebox.showwarning("Thiếu URL", "Vui lòng nhập URL video hoặc playlist.")
        return

    if not folder:
        messagebox.showwarning("Thiếu thư mục", "Vui lòng chọn thư mục lưu.")
        return

    # Khóa nút Tải xuống
    download_button.config(state=tk.DISABLED)

    # Tùy chọn "yes_playlist" hay "no_playlist"
    if playlist_option.get() == "yes_playlist":
        # Cho phép tải playlist
        ydl_opts = {
            'outtmpl': os.path.join(folder, '%(playlist_title)s', '%(title)s.%(ext)s'),
            'noplaylist': False,  # Để tải playlist
            'ignoreerrors': True,
            'no_overwrites': True,  # Bỏ qua các file đã tồn tại
            'verbose': False,  # Để tránh quá nhiều log trong terminal
            'cachedir': os.path.join(folder, '.cache', 'yt-dlp'),  # Đặt cache trong thư mục lưu
        }
    else:
        # Chỉ tải 1 video
        ydl_opts = {
            'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
            'noplaylist': True,  # Để chỉ tải một video
            'ignoreerrors': True,
            'no_overwrites': True,  # Bỏ qua các file đã tồn tại
            'verbose': False,  # Để tránh quá nhiều log trong terminal
            'cachedir': os.path.join(folder, '.cache', 'yt-dlp'),  # Đặt cache trong thư mục lưu
        }

    # Nếu có cookies, thêm vào ydl_opts
    if cookies:
        ydl_opts['cookies'] = cookies

    # Đảm bảo thư mục cache tồn tại
    cache_dir = ydl_opts.get('cachedir')
    if cache_dir:
        try:
            os.makedirs(cache_dir, exist_ok=True)
        except Exception as e:
            print(f"Không thể tạo thư mục cache: {cache_dir}. Lỗi: {e}")

    # Tạo object hook để cập nhật tiến độ
    progress_hook = YTDLProgressHook(
        title_label=current_title_label,
        progress_label=progress_label,
        progress_bar=progress_bar,
        file_status_label=file_status_label,
        downloaded_count_label=downloaded_count_label
    )

    ydl_opts['progress_hooks'] = [progress_hook]

    def run_download():
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            # Khi tải xong toàn bộ => báo cho người dùng
            window.after(
                0, 
                lambda: messagebox.showinfo("Thành công", "Đã tải xong!")
            )
        except Exception as e:
            window.after(
                0, 
                lambda: messagebox.showerror("Lỗi", str(e))
            )
        finally:
            # Mở lại nút Tải xuống
            window.after(0, lambda: download_button.config(state=tk.NORMAL))

    # Tạo luồng và chạy
    t = threading.Thread(target=run_download)
    t.daemon = True
    t.start()

# ------------------------ Giao diện tkinter ------------------------

window = tk.Tk()
window.title("YT-DLP GUI")

# Biến lưu trữ đường dẫn
folder_path = tk.StringVar()
# Biến lưu trữ đường dẫn cookies
cookies_path = tk.StringVar()
# Biến lưu trữ tuỳ chọn tải Playlist
playlist_option = tk.StringVar(value="yes_playlist")

# Chọn folder
folder_frame = tk.Frame(window)
folder_frame.pack(pady=5, padx=5, fill="x")

tk.Label(folder_frame, text="Thư mục lưu:").pack(side="left")
tk.Entry(folder_frame, textvariable=folder_path, width=50).pack(side="left", padx=5)
tk.Button(folder_frame, text="Chọn...", command=choose_directory).pack(side="left")

# Chọn tệp cookies
cookies_frame = tk.Frame(window)
cookies_frame.pack(pady=5, padx=5, fill="x")

tk.Label(cookies_frame, text="Tệp cookies (txt):").pack(side="left")
tk.Entry(cookies_frame, textvariable=cookies_path, width=50).pack(side="left", padx=5)
tk.Button(cookies_frame, text="Chọn...", command=choose_cookies).pack(side="left")

# Nhập URL
url_frame = tk.Frame(window)
url_frame.pack(pady=5, padx=5, fill="x")

tk.Label(url_frame, text="URL:").pack(side="left")
url_entry = tk.Entry(url_frame, width=60)
url_entry.pack(side="left", padx=5)

# Tuỳ chọn (yes_playlist / no_playlist)
option_frame = tk.LabelFrame(window, text="Tùy chọn")
option_frame.pack(pady=5, padx=5, fill="x")

tk.Radiobutton(
    option_frame,
    text="Tải toàn bộ playlist (nếu link là playlist)",
    variable=playlist_option,
    value="yes_playlist"
).pack(anchor="w")

tk.Radiobutton(
    option_frame,
    text="Chỉ tải xuống video (dù link là playlist)",
    variable=playlist_option,
    value="no_playlist"
).pack(anchor="w")

# Khu vực hiển thị tiến trình
progress_frame = tk.Frame(window)
progress_frame.pack(pady=5, padx=5, fill="x")

current_title_label = tk.Label(progress_frame, text="Video đang tải: (chưa bắt đầu)")
current_title_label.pack(anchor="w", pady=2)

progress_label = tk.Label(progress_frame, text="Chưa tải")
progress_label.pack(anchor="w", pady=2)

progress_bar = ttk.Progressbar(progress_frame, length=400, mode='determinate')
progress_bar.pack(anchor="w", pady=2)

file_status_label = tk.Label(progress_frame, text="")
file_status_label.pack(anchor="w", pady=2)

downloaded_count_label = tk.Label(progress_frame, text="")
downloaded_count_label.pack(anchor="w", pady=2)

# Nút Tải xuống
download_button = tk.Button(window, text="Tải xuống", command=start_download, bg="#4CAF50", fg="white")
download_button.pack(pady=10)

window.mainloop()
