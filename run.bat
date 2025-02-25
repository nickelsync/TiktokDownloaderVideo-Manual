@echo off
echo Menjalankan TikTok Downloader...
echo ==============================

REM Cek apakah Python terinstal
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python tidak ditemukan.
    echo Silakan instal Python dari https://www.python.org/downloads/
    echo PASTIKAN untuk mencentang "Add Python to PATH" saat instalasi.
    echo.
    pause
    exit /b
)

REM Cek apakah virtual environment sudah ada, jika belum buat baru
if not exist venv (
    echo Membuat virtual environment...
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ERROR: Gagal membuat virtual environment.
        echo Pastikan Python diinstal dengan benar.
        pause
        exit /b
    )
)

REM Aktifkan virtual environment
call venv\Scripts\activate

REM Instal dependensi jika belum
pip show requests >nul 2>&1
if %errorlevel% neq 0 (
    echo Menginstal dependensi...
    pip install requests beautifulsoup4 tqdm
)

REM Jalankan aplikasi
echo.
echo Memulai TikTok Downloader...
echo.
python main.py

REM Nonaktifkan virtual environment
call deactivate
pause