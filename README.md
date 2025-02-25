# TikTok Downloader Tanpa Watermark

Aplikasi Python untuk mengunduh video TikTok tanpa watermark. Tersedia dalam versi Command Line Interface (CLI) dan Graphical User Interface (GUI).

## Fitur

- Unduh video TikTok tanpa watermark
- Antarmuka pengguna grafis (GUI) mudah digunakan
- Mode command line (CLI) untuk otomatisasi
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

### Menggunakan pip

```bash
pip install tiktok-downloader-no-watermark
```

### Menggunakan source code

1. Clone repositori atau download source code
2. Buka terminal dan navigasi ke direktori project
3. Jalankan perintah:

```bash
pip install -e .
```

## Penggunaan

### Mode GUI

Untuk menjalankan aplikasi dengan antarmuka pengguna grafis:

```bash
python main.py
```

Atau jika diinstal menggunakan pip:

```bash
tiktok-downloader
```

### Mode CLI

Untuk mengunduh video menggunakan command line:

```bash
python main.py --cli --url "URL_VIDEO_TIKTOK" [--output "NAMA_FILE_OUTPUT"]
```

Atau jika diinstal menggunakan pip:

```bash
tiktok-downloader --cli --url "URL_VIDEO_TIKTOK" [--output "NAMA_FILE_OUTPUT"]
```

## Contoh

```bash
# Mengunduh video dengan URL TikTok
python main.py --cli --url "https://www.tiktok.com/@username/video/1234567890123456789"

# Mengunduh video dengan nama file output kustom
python main.py --cli --url "https://www.tiktok.com/@username/video/1234567890123456789" --output "video_saya.mp4"
```

## Struktur Project

```
tiktok-downloader-no-watermark/
├── main.py                  # File utama untuk menjalankan aplikasi
├── tiktok_downloader.py     # Implementasi downloader TikTok
├── tiktok_downloader_gui.py # Implementasi GUI
├── setup.py                 # File setup untuk instalasi
├── README.md                # Dokumentasi
└── downloaded_videos/       # Direktori default untuk video yang diunduh
```

## Catatan Penting

- Aplikasi ini dibuat untuk tujuan pendidikan.
- Penggunaan aplikasi ini harus mematuhi kebijakan TikTok dan hukum hak cipta yang berlaku.
- Aplikasi ini menggunakan layanan pihak ketiga yang mungkin berubah sewaktu-waktu.

## Lisensi

Proyek ini dilisensikan di bawah lisensi MIT - lihat file LICENSE untuk detailnya.

## Kontribusi

Kontribusi, masalah, dan permintaan fitur dipersilakan. Jangan ragu untuk memeriksa halaman masalah jika Anda ingin berkontribusi.

## Penafian

Aplikasi ini tidak berafiliasi dengan TikTok atau ByteDance Ltd.