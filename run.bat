@echo off
chcp 65001 > nul
cls
echo ===============================================
echo    TIKTOK VIDEO DOWNLOADER (DENGAN WATERMARK)
echo ===============================================
echo.

REM Cek apakah Python terinstal
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python tidak ditemukan.
    echo Silakan instal Python dari https://www.python.org/downloads/
    echo PASTIKAN untuk mencentang "Add Python to PATH" saat instalasi.
    echo.
    pause
    exit /b
)

REM Cek koneksi internet
echo [INFO] Memeriksa koneksi internet...
ping -n 1 www.google.com >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Koneksi internet mungkin bermasalah.
    echo Aplikasi masih akan dilanjutkan, tetapi mungkin ada masalah saat mengunduh.
    echo.
)

REM Cek apakah virtual environment sudah ada, jika belum buat baru
if not exist venv (
    echo [INFO] Membuat virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo [ERROR] Gagal membuat virtual environment.
        echo Pastikan Python diinstal dengan benar.
        pause
        exit /b
    )
)

REM Aktifkan virtual environment
echo [INFO] Mengaktifkan virtual environment...
call venv\Scripts\activate

REM Upgrade pip
python -m pip install --upgrade pip >nul 2>&1

REM Instal dependensi jika belum
echo [INFO] Memeriksa dan menginstal dependensi...
pip show requests >nul 2>&1
if %errorlevel% neq 0 (
    pip install requests
)

pip show beautifulsoup4 >nul 2>&1
if %errorlevel% neq 0 (
    pip install beautifulsoup4
)

pip show tqdm >nul 2>&1
if %errorlevel% neq 0 (
    pip install tqdm
)

REM Jalankan downloader dalam mode interaktif
echo.
echo [INFO] Memulai TikTok Downloader...
echo.

REM Rename file jika tiktok-watermark.py yang ada
if exist tiktok-watermark.py (
    copy /Y tiktok-watermark.py tiktok_downloader.py >nul
)

python tiktok_downloader.py

REM Nonaktifkan virtual environment
call deactivate
echo.
pause