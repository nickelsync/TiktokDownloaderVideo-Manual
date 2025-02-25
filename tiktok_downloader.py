import requests
import re
import os
import webbrowser
import random
import time
import subprocess
import platform
import argparse
from urllib.parse import urlparse

class TikTokDownloader:
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/121.0.6167.171 Mobile/15E148 Safari/604.1'
        ]
        
        self.output_dir = "downloaded_videos"
        
        # Buat direktori untuk menyimpan video jika belum ada
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def clean_url(self, url):
        """Membersihkan URL TikTok dan mendapatkan URL yang valid."""
        try:
            # Menangani URL pendek
            if "vm.tiktok.com" in url or "vt.tiktok.com" in url:
                print("Mengonversi URL pendek ke URL lengkap...")
                custom_headers = {
                    'User-Agent': random.choice(self.user_agents),
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                }
                try:
                    session = requests.Session()
                    response = session.head(url, headers=custom_headers, allow_redirects=True, timeout=15)
                    url = response.url
                    print(f"URL lengkap: {url}")
                except Exception as e:
                    print(f"Gagal mengonversi URL pendek: {e}")
            
            # Membersihkan parameter query yang tidak perlu
            if '?' in url:
                base_url = url.split('?')[0]
                url = base_url
            
            return url
        except Exception as e:
            print(f"Error saat membersihkan URL: {e}")
            return url
    
    def get_video_id(self, url):
        """Mengekstrak ID video dari URL TikTok."""
        try:
            match = re.search(r'/video/(\d+)', url)
            if match:
                return match.group(1)
            return url.split('/')[-1]
        except Exception as e:
            print(f"Error saat mendapatkan ID video: {e}")
            return f"tiktok_{int(time.time())}"
    
    def extract_username(self, url):
        """Mengekstrak username dari URL TikTok."""
        try:
            match = re.search(r'@([\w.-]+)', url)
            if match:
                return match.group(1)
            return "user"
        except Exception as e:
            print(f"Error saat mendapatkan username: {e}")
            return "user"
    
    def open_browser_and_download(self, url, output_path=None):
        """Membuka browser untuk mengunduh video secara manual."""
        print("\nMembuka browser untuk mengunduh video...")
        
        # Buka browser dengan URL TikTok
        if platform.system() == 'Windows':
            # Tambahkan parameter untuk otomatis download di Chrome (jika Chrome adalah browser default)
            # Ini tidak selalu berhasil, tergantung pada pengaturan browser
            try:
                subprocess.Popen(f'start chrome "{url}"')
            except:
                webbrowser.open(url)
        else:
            webbrowser.open(url)
        
        print("Browser dibuka. Silakan ikuti langkah-langkah ini:")
        print("1. Tunggu video dimuat")
        print("2. Klik kanan pada video")
        print("3. Pilih 'Save Video As' atau 'Simpan Video Sebagai'")
        if output_path:
            print(f"4. Simpan video ke: {output_path}")
        else:
            print(f"4. Simpan video ke folder 'downloaded_videos'")
        
        return True
    
    def download_video(self, url, filename=None):
        """Download video TikTok - menggunakan metode browser."""
        try:
            print("\nMemulai proses download video TikTok...")
            
            # Bersihkan URL dan dapatkan ID video
            clean_url = self.clean_url(url)
            video_id = self.get_video_id(clean_url)
            username = self.extract_username(clean_url)
            
            print(f"URL yang dibersihkan: {clean_url}")
            print(f"ID Video: {video_id}")
            print(f"Username: {username}")
            
            # Siapkan nama file output
            if not filename:
                filename = f"{username}_{video_id}.mp4"
            if not filename.endswith('.mp4'):
                filename += '.mp4'
            
            output_path = os.path.join(self.output_dir, filename)
            
            # Buat folder jika belum ada
            if not os.path.exists(self.output_dir):
                os.makedirs(self.output_dir)
            
            # Buka browser untuk download manual
            self.open_browser_and_download(clean_url, output_path)
            
            print(f"\nSilakan download video ke: {output_path}")
            
            manual_choice = input("\nApakah Anda berhasil mengunduh video? (y/n): ").lower()
            if manual_choice == 'y':
                print("Video berhasil diunduh secara manual.")
                return True
            else:
                print("Unduhan manual dibatalkan atau gagal.")
                return False
            
        except Exception as e:
            print(f"Error saat proses download: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description='Unduh video TikTok dengan watermark')
    parser.add_argument('url', nargs='?', help='URL video TikTok')
    parser.add_argument('-o', '--output', help='Nama file output (opsional)')
    
    args = parser.parse_args()
    
    downloader = TikTokDownloader()
    
    if args.url:
        # Jika URL diberikan sebagai argumen
        downloader.download_video(args.url, args.output)
    else:
        # Mode interaktif jika tidak ada URL yang diberikan
        print("=" * 50)
        print("TIKTOK VIDEO DOWNLOADER (DENGAN WATERMARK)")
        print("=" * 50)
        print("Aplikasi ini akan membantu Anda mengunduh video TikTok.")
        print("Masukkan URL video TikTok untuk memulai unduhan.")
        print("Ketik 'exit' untuk keluar.")
        print("-" * 50)
        
        while True:
            url = input("\nMasukkan URL TikTok: ").strip()
            
            if url.lower() == 'exit':
                print("Terima kasih telah menggunakan TikTok Downloader!")
                break
            
            if url:
                custom_filename = input("Masukkan nama file (opsional, tekan Enter untuk default): ").strip()
                filename = custom_filename if custom_filename else None
                
                downloader.download_video(url, filename)
                
                print("\nSiap untuk mengunduh video lain.")
            else:
                print("URL tidak boleh kosong! Coba lagi.")

if __name__ == "__main__":
    main()