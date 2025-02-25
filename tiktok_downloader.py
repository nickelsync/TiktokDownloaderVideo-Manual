import requests
import re
import json
import os
import time
import random
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from tqdm import tqdm
import argparse
import webbrowser

class TikTokDownloader:
    def __init__(self):
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/121.0.6167.171 Mobile/15E148 Safari/604.1'
        ]
        
        self.headers = {
            'User-Agent': random.choice(self.user_agents),
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com/'
        }
        
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
            
            # Pola URL TikTok
            patterns = [
                r'https?://(?:www\.)?tiktok\.com/@[\w.-]+/video/\d+',
                r'https?://(?:www\.)?tiktok\.com/\w+/video/\d+',
                r'https?://(?:www\.)?tiktok\.com/.*/video/\d+'
            ]
            
            for pattern in patterns:
                match = re.search(pattern, url)
                if match:
                    return match.group(0)
            
            # Ekstrak ID video saja jika tidak ada pola yang cocok
            video_id_match = re.search(r'/video/(\d+)', url)
            if video_id_match:
                video_id = video_id_match.group(1)
                # Coba rekonstruksi URL dengan username jika ada
                username_match = re.search(r'@([\w.-]+)', url)
                if username_match:
                    username = username_match.group(1)
                    return f"https://www.tiktok.com/@{username}/video/{video_id}"
                else:
                    return f"https://www.tiktok.com/video/{video_id}"
            
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
    
    def get_video_url_from_tiktok(self, url):
        """Mendapatkan URL video langsung dari TikTok."""
        try:
            print("Mendapatkan video langsung dari TikTok...")
            
            # Request dengan beberapa header berbeda untuk menghindari deteksi
            headers = {
                'User-Agent': random.choice(self.user_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Cache-Control': 'max-age=0'
            }
            
            session = requests.Session()
            response = session.get(url, headers=headers, timeout=20)
            
            if response.status_code != 200:
                print(f"Gagal mengakses TikTok: {response.status_code}")
                return None
            
            # Cari URL video dalam konten HTML
            html_content = response.text
            
            # Metode 1: Cari __UNIVERSAL_DATA_FOR_REHYDRATION__
            universal_pattern = r'window\[\'UNIVERSAL_DATA_FOR_REHYDRATION\'\]\s*=\s*({.+?});'
            universal_match = re.search(universal_pattern, html_content, re.DOTALL)
            
            if universal_match:
                try:
                    json_data = json.loads(universal_match.group(1))
                    route_params = json_data.get('__DEFAULT_SCOPE__', {}).get('webapp.video-detail', {}).get('videoData', {})
                    
                    if route_params:
                        video_url = route_params.get('itemInfo', {}).get('itemStruct', {}).get('video', {}).get('downloadAddr', '')
                        if not video_url:
                            video_url = route_params.get('itemInfo', {}).get('itemStruct', {}).get('video', {}).get('playAddr', '')
                        if video_url:
                            return video_url
                except Exception as e:
                    print(f"Error parsing UNIVERSAL_DATA: {e}")
            
            # Metode 2: Cari SIGI_STATE
            sigi_pattern = r'<script id="SIGI_STATE" type="application/json">(.+?)</script>'
            sigi_match = re.search(sigi_pattern, html_content, re.DOTALL)
            
            if sigi_match:
                try:
                    json_data = json.loads(sigi_match.group(1))
                    item_id = self.get_video_id(url)
                    
                    # Cari URL video dalam JSON
                    if 'ItemModule' in json_data and item_id in json_data['ItemModule']:
                        item_data = json_data['ItemModule'][item_id]
                        video_url = item_data.get('video', {}).get('downloadAddr', '')
                        if not video_url:
                            video_url = item_data.get('video', {}).get('playAddr', '')
                        if video_url:
                            return video_url
                except Exception as e:
                    print(f"Error parsing SIGI_STATE: {e}")
            
            # Metode 3: Cari URL video langsung di HTML
            video_pattern = r'<video[^>]*src="([^"]*)"'
            video_match = re.search(video_pattern, html_content)
            
            if video_match:
                video_url = video_match.group(1).replace('&amp;', '&')
                if video_url:
                    return video_url
            
            # Metode 4: Cari pola URL di dalam script dengan regex
            url_pattern = r'(https://v\d+\.tiktokcdn\.com/[^"\']+\.mp4)'
            url_matches = re.findall(url_pattern, html_content)
            
            if url_matches:
                for url_match in url_matches:
                    if '.mp4' in url_match:
                        return url_match
            
            print("Tidak dapat menemukan URL video dari TikTok langsung.")
            return None
        except Exception as e:
            print(f"Error saat mendapatkan video dari TikTok: {e}")
            return None
    
    def download_video(self, url, filename=None):
        """Mengunduh video TikTok dengan watermark."""
        try:
            print("\nMemulai proses download video TikTok dengan watermark...")
            
            # Bersihkan URL dan dapatkan ID video
            clean_url = self.clean_url(url)
            video_id = self.get_video_id(clean_url)
            username = self.extract_username(clean_url)
            
            print(f"URL yang dibersihkan: {clean_url}")
            print(f"ID Video: {video_id}")
            print(f"Username: {username}")
            
            # Dapatkan URL video langsung dari TikTok
            video_url = self.get_video_url_from_tiktok(clean_url)
            
            if not video_url:
                print("\nTidak dapat menemukan URL video secara otomatis.")
                print("Mencoba metode manual...")
                
                # Buat nama file default
                if not filename:
                    filename = f"{username}_{video_id}.mp4"
                if not filename.endswith('.mp4'):
                    filename += '.mp4'
                
                output_path = os.path.join(self.output_dir, filename)
                
                print("\nLANGKAH-LANGKAH MANUAL:")
                print("1. URL TikTok berikut akan dibuka di browser default Anda")
                print("2. Di browser, klik kanan pada video dan pilih 'Save Video As' atau 'Simpan Video Sebagai'")
                print("3. Simpan video ke folder 'downloaded_videos' di direktori yang sama dengan aplikasi ini")
                
                # Buka URL di browser default
                webbrowser.open(clean_url)
                
                print(f"\nURL TikTok: {clean_url}")
                print(f"Simpan video sebagai: {filename}")
                
                manual_choice = input("\nApakah Anda berhasil mengunduh video secara manual? (y/n): ").lower()
                if manual_choice == 'y':
                    print("Video berhasil diunduh secara manual.")
                    return True
                else:
                    print("Unduhan manual dibatalkan.")
                    return False
            
            # Siapkan nama file output
            if not filename:
                filename = f"{username}_{video_id}.mp4"
            if not filename.endswith('.mp4'):
                filename += '.mp4'
            
            output_path = os.path.join(self.output_dir, filename)
            
            print(f"Mengunduh video ke {output_path}...")
            print(f"URL video: {video_url}")
            
            # Header untuk download
            download_headers = {
                'User-Agent': random.choice(self.user_agents),
                'Accept': '*/*',
                'Accept-Encoding': 'gzip, deflate, br',
                'Referer': 'https://www.tiktok.com/',
                'Connection': 'keep-alive'
            }
            
            # Download dengan progress bar
            with requests.get(video_url, headers=download_headers, stream=True, timeout=30) as response:
                if response.status_code != 200:
                    print(f"Error saat mengunduh video: Status code {response.status_code}")
                    return False
                
                total_size = int(response.headers.get('content-length', 0))
                
                with open(output_path, 'wb') as f, tqdm(
                    desc=filename,
                    total=total_size,
                    unit='B',
                    unit_scale=True,
                    unit_divisor=1024,
                ) as bar:
                    for chunk in response.iter_content(chunk_size=8192):
                        if chunk:
                            size = f.write(chunk)
                            bar.update(size)
            
            # Verifikasi file
            file_size = os.path.getsize(output_path)
            if file_size < 10000:  # Jika kurang dari 10KB
                print("Warning: File yang diunduh terlalu kecil, memeriksa konten...")
                
                with open(output_path, 'r', errors='ignore') as f:
                    content = f.read(1000)
                    if '<html' in content.lower() or '<!doctype html' in content.lower():
                        print("File yang diunduh adalah HTML, bukan video!")
                        os.remove(output_path)
                        return False
            
            print(f"\nVideo berhasil diunduh: {output_path}")
            print(f"Ukuran file: {file_size / (1024*1024):.2f} MB")
            return True
            
        except Exception as e:
            print(f"Error saat mengunduh video: {e}")
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
        print("Aplikasi ini mengunduh video TikTok dengan watermark asli.")
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