# TikTok Video Grabber

Aplikasi sederhana untuk membantu mengunduh video TikTok menggunakan berbagai metode yang mudah dan efektif. Aplikasi ini dirancang untuk mengatasi berbagai batasan dalam mengunduh video TikTok.

## Fitur Utama

- **Multiple Metode Unduhan**: 4 cara berbeda untuk mengunduh video TikTok
- **Integrasi dengan SnapTik dan Downloader Online**: Akses mudah ke layanan populer pengunduh TikTok
- **Antarmuka Pengguna yang Intuitif**: Mudah digunakan dengan petunjuk jelas untuk setiap metode
- **Cross-Platform**: Berfungsi di Windows, macOS, dan Linux
- **Instruksi Detail**: Panduan langkah demi langkah untuk setiap metode

## Metode yang Tersedia

### Metode 1: Browser Standar
Metode tradisional menggunakan browser dan klik kanan untuk mengunduh video.

### Metode 2: SnapTik (Online Downloader)
Menggunakan layanan online seperti SnapTik, SSSTik, SaveTT, dan lainnya untuk mengunduh video TikTok, bahkan tanpa watermark.

### Metode 3: Screen Recording
Petunjuk untuk merekam layar saat memainkan video TikTok, berfungsi di semua platform.

### Metode 4: Developer Tools (Advanced)
Metode lanjutan menggunakan Developer Tools browser untuk menemukan URL video langsung.

## Persyaratan

- Python 3.6 atau lebih baru
- Paket Python yang diperlukan:
  - requests
  - tkinter (biasanya sudah termasuk dalam instalasi Python)

## Instalasi

### Di Windows dengan File Batch

1. Install Python dari [python.org](https://www.python.org/downloads/) (centang "Add Python to PATH" saat instalasi)
2. Download semua file project ini ke satu folder
3. Double-click file `run.bat` untuk menjalankan aplikasi

### Instalasi Manual

1. Install Python jika belum terinstal
2. Buka Command Prompt dan navigasi ke direktori project
3. Buat virtual environment:
   ```
   python -m venv venv
   ```
4. Aktifkan virtual environment:
   ```
   venv\Scripts\activate   # Windows
   source venv/bin/activate  # macOS/Linux
   ```
5. Install dependensi:
   ```
   pip install requests
   ```
6. Klik 2 kali pada run.bat

## Cara Menggunakan

1. **Jalankan aplikasi** menggunakan file batch atau perintah python
2. **Tempel URL video TikTok** ke dalam aplikasi (atau gunakan tombol "Paste URL")
3. **Pilih salah satu metode** yang tersedia:

### Cara Menggunakan Metode 1 (Browser Standar)
- Klik "Metode 1: Browser Standar"
- Browser akan terbuka dengan video TikTok
- Coba klik kanan pada video dan pilih "Save Video As"
- Jika tidak berfungsi, coba shortcut Ctrl+S (Windows) atau Command+S (Mac)

### Cara Menggunakan Metode 2 (SnapTik)
- Klik "Metode 2: SnapTik (Online Downloader)"
- Pilih layanan downloader yang ingin digunakan (SnapTik, SSSTik, dll)
- URL TikTok akan otomatis disalin ke clipboard
- Tempel URL ke dalam kotak input pada situs downloader
- Klik tombol download dan simpan video

### Cara Menggunakan Metode 3 (Screen Recording)
- Klik "Metode 3: Screen Recording"
- Ikuti petunjuk untuk merekam layar sesuai sistem operasi Anda
- Mainkan video TikTok
- Simpan hasil rekaman

### Cara Menggunakan Metode 4 (Developer Tools)
- Klik "Metode 4: Developer Tools"
- Tekan F12 untuk membuka Developer Tools
- Buka tab Network
- Filter dengan ".mp4"
- Temukan dan unduh file video

## Mengatasi Masalah Umum

### Klik Kanan Tidak Berfungsi
- Gunakan Metode 2 (SnapTik) sebagai alternatif terbaik
- Jika satu situs downloader diblokir, coba situs lainnya

### Situs Downloader Diblokir
- Coba gunakan VPN
- Coba situs downloader alternatif lainnya dari daftar
- Gunakan Metode 3 (Screen Recording) sebagai pilihan terakhir

### Browser Tidak Terbuka
- Pastikan Anda memiliki browser default yang ditetapkan di sistem
- Buka URL secara manual jika browser tidak terbuka otomatis

## Catatan Penting

- Aplikasi ini dibuat untuk tujuan pendidikan dan penggunaan pribadi
- Hormati hak cipta pembuat konten saat mengunduh video
- Beberapa metode menghasilkan video dengan watermark, sementara metode lain (seperti SnapTik) dapat menghilangkan watermark
- Aplikasi ini tidak melakukan penyimpanan atau pelacakan atas video yang diunduh
