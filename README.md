# TikTok Downloader (Mode Browser)

Aplikasi sederhana untuk membantu mengunduh video TikTok dengan menggunakan browser Anda. Aplikasi ini dirancang untuk situasi di mana downloader otomatis tidak berfungsi karena pemblokiran API atau masalah koneksi.

## Cara Kerja

Aplikasi ini:
1. Membantu membersihkan URL TikTok
2. Membuka browser dengan URL video TikTok
3. Menampilkan petunjuk langkah demi langkah untuk mengunduh video secara manual
4. Mengelola video yang telah diunduh

## Fitur

- Antarmuka pengguna grafis yang sederhana dan mudah digunakan
- Tombol "Paste URL" untuk cepat menempelkan URL dari clipboard
- Daftar video yang telah diunduh dengan kemampuan pengelolaan
- Instruksi jelas untuk mengunduh video secara manual
- Tidak bergantung pada API pihak ketiga yang sering diblokir oleh ISP

## Persyaratan

- Python 3.6 atau lebih baru
- Paket Python yang diperlukan:
  - requests
  - tkinter (biasanya sudah termasuk dalam instalasi Python)

## Instalasi

### Di Windows dengan File Batch (Termudah)

1. Install Python dari [python.org](https://www.python.org/downloads/) (centang "Add Python to PATH" saat instalasi)
2. Download semua file project ini ke satu folder
3. Double-click file `run-simplest.bat` untuk menjalankan aplikasi

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
   pip install requests
   ```

## Cara Menggunakan

1. **Jalankan aplikasi** menggunakan `run-simplest.bat` atau dengan perintah:
   ```
   python tiktok-gui-simplest.py
   ```

2. **Salin URL video TikTok** dari aplikasi TikTok atau browser
   - Format: `https://www.tiktok.com/@username/video/1234567890123456789`
   - Atau URL pendek: `https://vm.tiktok.com/XXXXX/`

3. **Tempel URL** ke dalam aplikasi (atau gunakan tombol "Paste URL")

4. **Klik "Buka di Browser"**
   - Browser akan terbuka dengan URL video TikTok
   - Ikuti instruksi yang ditampilkan:
     1. Tunggu video dimuat di browser
     2. Klik kanan pada video
     3. Pilih "Save Video As" atau "Simpan Video Sebagai"
     4. Simpan ke folder "downloaded_videos"

5. **Klik "Refresh"** untuk melihat video yang telah diunduh dalam daftar

6. **Kelola video yang diunduh**:
   - Double-click untuk membuka video
   - Klik kanan untuk opsi lainnya (Buka Folder, Hapus File, dll.)

## Pemecahan Masalah

### Tidak Dapat Melihat Opsi "Save Video As"

- Periksa jika Anda menggunakan browser yang didukung (Chrome, Firefox, Edge)
- Coba gunakan browser desktop, bukan mobile
- Beberapa versi TikTok mungkin mencegah klik kanan; coba gunakan shortcut keyboard:
  - Windows/Linux: Ctrl+S
  - Mac: Command+S

### Browser Tidak Terbuka

- Pastikan Anda memiliki browser default yang ditetapkan di sistem
- Coba buka URL secara manual jika browser tidak terbuka otomatis

### Video Tidak Muncul di Daftar Setelah Diunduh

- Klik tombol "Refresh" untuk memperbarui daftar
- Pastikan Anda menyimpan video ke folder "downloaded_videos" yang benar
- Verifikasi bahwa file berekstensi .mp4

## Catatan Penting

- Aplikasi ini mengunduh video dengan watermark TikTok asli
- Video diunduh secara manual melalui browser untuk menghindari pemblokiran API
- Hormati hak cipta pembuat konten saat mengunduh video
- Aplikasi ini dibuat untuk tujuan pendidikan dan penggunaan pribadi
