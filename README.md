# TikTok Downloader (Dengan Watermark)

Aplikasi Python untuk mengunduh video TikTok dengan watermark. Aplikasi ini menyediakan cara yang mudah dan cepat untuk menyimpan video TikTok ke komputer Anda. Tersedia dalam versi Command Line Interface (CLI) dan Graphical User Interface (GUI).

## Fitur

- Unduh video TikTok dengan watermark
- Antarmuka pengguna grafis (GUI) mudah digunakan
- Mode command line (CLI) untuk penggunaan cepat
- Mendukung URL TikTok pendek dan panjang
- Progress bar untuk memantau proses unduhan
- Mengelola video yang diunduh

## Persyaratan

- Python 3.6 atau lebih baru
- Paket yang diperlukan:
  - requests
  - beautifulsoup4
  - tqdm
  - tkinter (sudah termasuk dalam sebagian besar instalasi Python)

## Instalasi

### Di Windows dengan File Batch (Termudah)

1. Install Python dari [python.org](https://www.python.org/downloads/) (centang "Add Python to PATH" saat instalasi)
2. Download semua file project ini ke satu folder
3. Double-click file `run-tiktok-downloader.bat` untuk menjalankan aplikasi

### Instalasi Manual

1. Install Python jika belum terinstal
2. Buka Command Prompt dan navigasi ke direktori project
3. Buat virtual environment:
   ```
   python -m venv venv
   ```
4. Aktifkan virtual environment:
   ```
   venv\Scripts\activate
   ```
5. Install dependensi:
   ```
   pip install requests beautifulsoup4 tqdm
   ```

## Penggunaan

### Mode GUI

Untuk menjalankan aplikasi dengan antarmuka pengguna grafis:

1. Double-click file `run-tiktok-downloader.bat`, atau
2. Jalankan perintah dari Command Prompt:
   ```
   python tiktok-gui-watermark.py
   ```

### Mode CLI

Untuk mengunduh video menggunakan command line:

```
python tiktok-watermark.py "URL_VIDEO_TIKTOK"
```

Atau gunakan mode interaktif:

```
python tiktok-watermark.py
```

## Contoh Penggunaan

1. **Salin URL video TikTok** dari aplikasi TikTok atau browser
   - Format: `https://www.tiktok.com/@username/video/1234567890123456789`
   - Atau URL pendek: `https://vm.tiktok.com/XXXXX/`

2. **Tempel URL** ke dalam aplikasi dan klik "Unduh Video"

3. **Video akan disimpan** ke folder "downloaded_videos"

## Kemungkinan Masalah dan Solusi

### URL Tidak Valid

- Pastikan URL dalam format yang benar
- Pastikan video TikTok tidak diprivat atau dihapus

### Kegagalan Unduh

- Periksa koneksi internet Anda
- Coba URL video TikTok yang berbeda
- Jika download otomatis gagal, aplikasi akan menawarkan metode manual:
  1. Browser akan terbuka dengan URL TikTok
  2. Klik kanan pada video dan pilih "Save Video As"
  3. Simpan ke folder "downloaded_videos"

### File Hasil Unduhan Terlalu Kecil

- Aplikasi akan otomatis memeriksa apakah file yang diunduh valid
- Jika file bukan video (misalnya HTML), aplikasi akan menghapusnya dan menampilkan pesan error

## Mengapa Dengan Watermark?

Aplikasi ini mengunduh video TikTok dengan watermark asli karena:

1. **Lebih andal** - Tidak perlu menggunakan layanan pihak ketiga yang sering diblokir oleh ISP Indonesia
2. **Lebih cepat** - Unduh langsung dari server TikTok
3. **Lebih aman** - Tidak ada risiko menggunakan layanan tidak resmi
4. **Legal** - Menghormati hak cipta dan ketentuan layanan TikTok

## Catatan Penting

- Aplikasi ini dibuat untuk tujuan pendidikan dan penggunaan pribadi
- Hormati hak cipta pembuat konten saat mengunduh video
- Jangan mendistribusikan ulang video yang diunduh tanpa izin dari pemilik konten

## Kontribusi

Kontribusi, masalah, dan permintaan fitur dipersilakan. Jangan ragu untuk memeriksa halaman masalah jika Anda ingin berkontribusi.

## Penafian

Aplikasi ini tidak berafiliasi dengan TikTok atau ByteDance Ltd. Semua merek dagang yang disebutkan adalah milik dari pemiliknya masing-masing.