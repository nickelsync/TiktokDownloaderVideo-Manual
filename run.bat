@echo off
chcp 65001 > nul
cls
echo ===============================================
echo    TIKTOK VIDEO DOWNLOADER (MODE BROWSER)
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

REM Salin file tiktok_downloader.py jika belum ada
if exist tiktok-downloader-simple-final.py (
    echo [INFO] Menyalin file downloader...
    copy /Y tiktok-downloader-simple-final.py tiktok_downloader.py >nul
)

REM Jalankan GUI
echo.
echo [INFO] Memulai TikTok Downloader...
echo.

python tiktok-gui-simplest.py

REM Nonaktifkan virtual environment
call deactivate
echo.
pause