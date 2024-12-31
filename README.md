# YT-DLP GUI

YT-DLP GUI là một ứng dụng giao diện người dùng đơn giản giúp bạn tải xuống video hoặc playlist từ YouTube một cách dễ dàng. Ứng dụng hỗ trợ xác thực thông qua tệp cookies, hiển thị tiến trình tải xuống trong giao diện, và bỏ qua các tệp video đã tồn tại để tránh ghi đè.

## 📋 **Nội Dung**

- [Đặc Tả](#đặc-tả)
- [Yêu Cầu Hệ Thống](#yêu-cầu-hệ-thống)
- [Cài Đặt](#cài-đặt)
- [Sử Dụng Ứng Dụng](#sử-dụng-ứng-dụng)
- [Xây Dựng File EXE](#xây-dựng-file-exe)
  - [Xây Dựng EXE Có Console](#xây-dựng-exe-có-console)
  - [Xây Dựng EXE Không Console](#xây-dựng-exe-không-console)
- [Xuất và Sử Dụng Cookies](#xuất-và-sử-dụng-cookies)
- [Troubleshooting](#troubleshooting)

## 🔍 **Đặc Tả**

YT-DLP GUI được xây dựng bằng Python sử dụng thư viện `yt-dlp` để tải xuống video từ YouTube và `Tkinter` để tạo giao diện người dùng. Ứng dụng hỗ trợ:

- Tải xuống video hoặc toàn bộ playlist.
- Sử dụng tệp cookies để xác thực và tải các video yêu cầu đăng nhập.
- Hiển thị tiến trình tải xuống bao gồm phần trăm, tốc độ, ETA.
- Bỏ qua các tệp đã tồn tại trong thư mục lưu.
- Hiển thị log chi tiết trong giao diện GUI.

## 💻 **Yêu Cầu Hệ Thống**

- **Hệ điều hành:** Windows, macOS, hoặc Linux.
- **Python:** Phiên bản 3.7 trở lên.
- **Thư viện Python:** `yt-dlp`, `tkinter` (thường được cài đặt sẵn với Python).

## 🛠️ **Cài Đặt**

1. **Cài Đặt Python:**

   Đảm bảo rằng bạn đã cài đặt Python 3.7 trở lên. Bạn có thể tải Python từ [trang chính thức](https://www.python.org/downloads/).

2. **Cài Đặt Các Gói Yêu Cầu:**

   Mở Command Prompt (Windows) hoặc Terminal (macOS/Linux) và chạy lệnh sau:

   ```bash
   pip install yt-dlp
   ```

   Thư viện `tkinter` thường được cài đặt sẵn với Python. Nếu không, bạn có thể cài đặt nó theo hướng dẫn của hệ điều hành bạn đang sử dụng.

3. **Tải Mã Nguồn:**

   Tải tệp `yt_dlp_gui.py` từ kho lưu trữ của bạn hoặc tạo tệp mới với nội dung mã nguồn đã được chỉnh sửa.

## 🚀 **Sử Dụng Ứng Dụng**

1. **Chạy Ứng Dụng:**

   Mở Command Prompt hoặc Terminal, điều hướng đến thư mục chứa `yt_dlp_gui.py` và chạy:

   ```bash
   python yt_dlp_gui.py
   ```

2. **Giao Diện Người Dùng:**

   - **Thư Mục Lưu:** Nhấn nút "Chọn..." để chọn thư mục nơi bạn muốn lưu các video đã tải xuống.
   - **Tệp Cookies (txt):** Nhấn nút "Chọn..." để chọn tệp `cookies.txt` đã xuất từ trình duyệt.
   - **URL:** Nhập URL của video hoặc playlist YouTube mà bạn muốn tải xuống.
   - **Tùy Chọn:**
     - **Tải toàn bộ playlist (nếu link là playlist):** Chọn để tải xuống toàn bộ playlist nếu URL là một playlist.
     - **Chỉ tải xuống video (dù link là playlist):** Chọn để chỉ tải một video duy nhất bất kể URL là playlist.
   - **Log:** Khu vực này sẽ hiển thị các thông điệp log từ quá trình tải xuống.
   - **Tiến Trình:** Hiển thị tiêu đề video đang tải, phần trăm tiến trình, tốc độ, ETA, và trạng thái playlist.
   - **Nút "Tải xuống":** Nhấn để bắt đầu quá trình tải xuống.

## 🏗️ **Xây Dựng File EXE**

Để xây dựng ứng dụng thành tệp EXE, bạn có thể sử dụng `PyInstaller`. Dưới đây là hướng dẫn chi tiết cho hai trường hợp: có console và không console.

### 📂 **Bước 1: Cài Đặt PyInstaller**

Nếu chưa cài đặt `PyInstaller`, hãy cài đặt nó bằng pip:

```bash
pip install pyinstaller
```

### 🖥️ **Xây Dựng EXE Có Console**

Mở Command Prompt hoặc Terminal, điều hướng đến thư mục chứa `yt_dlp_gui.py` và chạy lệnh sau:

```bash
pyinstaller --onefile yt_dlp_gui.py
```

- **`--onefile`**: Bao gọn tất cả các thành phần vào một tệp EXE duy nhất.

**Kết Quả:**

Tệp EXE sẽ được tạo trong thư mục `dist`. Khi chạy, cửa sổ console sẽ hiển thị log và thông báo.

### 🔕 **Xây Dựng EXE Không Console**

Để xây dựng EXE mà không hiển thị cửa sổ console, sử dụng tùy chọn `--noconsole`:

```bash
pyinstaller --noconsole --onefile yt_dlp_gui.py
```

- **`--noconsole`**: Không hiển thị cửa sổ console khi chạy EXE.
- **`--onefile`**: Bao gọn tất cả các thành phần vào một tệp EXE duy nhất.

**Kết Quả:**

Tệp EXE sẽ được tạo trong thư mục `dist`. Khi chạy, chỉ có giao diện GUI mà không có cửa sổ console.

## 📑 **Xuất và Sử Dụng Cookies**

Để `yt-dlp` có thể tải xuống các video yêu cầu xác thực, bạn cần xuất cookies từ trình duyệt của mình.

### 🔄 **Bước 1: Xuất Cookies Từ Trình Duyệt**

1. **Cài Đặt Tiện Ích Mở Rộng (Extension) để Xuất Cookies:**

   - **Cho Chrome:**
     - [Get cookies.txt](https://chrome.google.com/webstore/detail/get-cookiestxt/nhfgmdpfpioojkacmpjopnhnnkiknmce)
   - **Cho Firefox:**
     - [Export Cookies](https://addons.mozilla.org/en-US/firefox/addon/export-cookies-txt/)

2. **Xuất Cookies:**

   - **Sau khi cài đặt tiện ích mở rộng:**
     - Mở trình duyệt và đăng nhập vào tài khoản YouTube của bạn.
     - Sử dụng tiện ích mở rộng để xuất cookies và lưu tệp `cookies.txt` vào một vị trí dễ nhớ trên máy tính của bạn.

   **Lưu Ý:**

   - Đảm bảo rằng tệp `cookies.txt` chứa thông tin xác thực hợp lệ.
   - Bạn có thể mở tệp `cookies.txt` bằng trình soạn thảo văn bản để kiểm tra nội dung.

### 🔗 **Bước 2: Sử Dụng Cookies Trong Ứng Dụng GUI**

1. **Chọn Tệp Cookies:**

   - Trong giao diện GUI, nhấn nút "Chọn..." bên cạnh trường "Tệp cookies (txt)".
   - Chọn tệp `cookies.txt` đã xuất từ trình duyệt.

2. **Bắt Đầu Tải Xuống:**

   - Nhập URL của video hoặc playlist.
   - Chọn tùy chọn tải xuống.
   - Nhấn nút "Tải xuống" để bắt đầu quá trình.

## 🛠️ **Troubleshooting**

### ❌ **Lỗi Yêu Cầu Xác Thực**

- **Mô Tả Lỗi:**

  ```
  ERROR: [youtube] ZMymukzJYfA: Sign in to confirm you’re not a bot. Use --cookies-from-browser or --cookies for the authentication.
  ```

- **Giải Pháp:**

  1. **Kiểm Tra Tệp Cookies:**
     - Đảm bảo rằng tệp `cookies.txt` được xuất đúng cách và chứa thông tin xác thực hợp lệ.
     - Mở tệp `cookies.txt` bằng trình soạn thảo văn bản và kiểm tra các dòng có định dạng đúng không.

  2. **Cập Nhật `yt-dlp`:**
     - Đảm bảo bạn đang sử dụng phiên bản mới nhất của `yt-dlp`:
       ```bash
       pip install -U yt-dlp
       ```

  3. **Kiểm Tra Đường Dẫn Tệp Cookies:**
     - Đảm bảo rằng đường dẫn đến tệp `cookies.txt` được truyền đúng cách trong giao diện GUI.

  4. **Thử Tải Bằng Command Line:**
     - Trước khi sử dụng GUI, hãy thử tải xuống video qua command line:
       ```bash
       yt-dlp --cookies "C:\Đường\Dẫn\Đến\cookies.txt" "https://www.youtube.com/watch?v=ZMymukzJYfA"
       ```
     - Nếu lệnh này hoạt động, vấn đề có thể nằm trong mã nguồn GUI của bạn.

### 📂 **Lỗi Ghi Cache (`FileNotFoundError`)**

- **Giải Pháp:**

  1. **Kiểm Tra Đường Dẫn Cache:**
     - Đảm bảo rằng đường dẫn cache (`cachedir`) được đặt đúng và thư mục đó có quyền ghi.

  2. **Kiểm Tra Quyền Truy Cập:**
     - Đảm bảo rằng thư mục lưu và thư mục cache có quyền truy cập đầy đủ.

  3. **Tạo Thư Mục Cache Thủ Công:**
     - Nếu cần, tạo thư mục cache bằng tay và đảm bảo rằng nó tồn tại trước khi chạy ứng dụng.

### 📄 **Các Video Bị Bỏ Qua**

- **Mô Tả:**
  - Với tùy chọn `no_overwrites`, các video đã tồn tại trong thư mục lưu sẽ bị bỏ qua.

- **Giải Pháp:**
  - Kiểm tra thư mục lưu để xác nhận các video đã được tải xuống.
  - Nếu bạn muốn tải lại video, hãy xóa tệp đã tồn tại hoặc thay đổi tên tệp.

---

**Chúc bạn thành công với YT-DLP GUI!**

```
