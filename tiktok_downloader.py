import requests
import re
import json
import os
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from tqdm import tqdm
import argparse

class TikTokDownloader:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.tiktok.com/'
        }
        self.output_dir = "downloaded_videos"
        
        # Buat direktori untuk menyimpan video jika belum ada
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
    
    def clean_url(self, url):
        """Membersihkan URL TikTok dan mendapatkan URL yang valid."""
        if "vm.tiktok.com" in url or "vt.tiktok.com" in url:
            # Jika URL adalah versi pendek, lakukan redirect untuk mendapatkan URL penuh
            session = requests.Session()
            response = session.head(url, allow_redirects=True)
            url = response.url
        
        # Mencari pola URL TikTok yang valid
        pattern = r'https?://(?:www\.)?tiktok\.com/@[\w.-]+/video/\d+'
        match = re.search(pattern, url)
        
        if match:
            return match.group(0)
        else:
            raise ValueError("URL TikTok tidak valid")
    
    def get_video_id(self, url):
        """Mengekstrak ID video dari URL TikTok."""
        parsed_url = urlparse(url)
        path = parsed_url.path
        
        # Path biasanya dalam format: /@username/video/1234567890123456789
        video_id = path.split("/")[-1]
        return video_id
    
    def get_download_url(self, url):
        """Mendapatkan URL unduhan tanpa watermark."""
        try:
            clean_url = self.clean_url(url)
            video_id = self.get_video_id(clean_url)
            
            # Metode 1: Menggunakan ssstik.io
            print("Mencoba menggunakan metode ssstik.io...")
            
            session = requests.Session()
            ssstik_url = "https://ssstik.io/id"
            response = session.get(ssstik_url, headers=self.headers)
            
            if response.status_code != 200:
                print(f"Error mengakses ssstik.io: {response.status_code}")
                # Lanjut ke metode selanjutnya
            else:
                # Dapatkan token CSRF dari halaman
                soup = BeautifulSoup(response.text, "html.parser")
                token_input = soup.find("input", {"name": "tt"})
                
                if token_input:
                    token = token_input.get("value")
                    
                    form_data = {
                        "id": clean_url,
                        "locale": "id",
                        "tt": token
                    }
                    
                    download_page = session.post(
                        "https://ssstik.io/abc?url=dl",
                        headers={
                            **self.headers,
                            "Referer": "https://ssstik.io/id",
                            "Accept": "*/*",
                            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                            "X-Requested-With": "XMLHttpRequest",
                        },
                        data=form_data
                    )
                    
                    if download_page.status_code == 200:
                        download_soup = BeautifulSoup(download_page.text, "html.parser")
                        download_links = download_soup.find_all("a", {"class": "download-link"})
                        
                        for link in download_links:
                            if "Tanpa Watermark" in link.text or "No Watermark" in link.text:
                                return link["href"], video_id
                
            # Metode 2: Menggunakan snaptik.app
            print("Mencoba menggunakan metode snaptik.app...")
            
            snaptik_url = "https://snaptik.app/ID"
            response = session.get(snaptik_url, headers=self.headers)
            
            if response.status_code != 200:
                print(f"Error mengakses snaptik.app: {response.status_code}")
            else:
                # Dapatkan token dari halaman
                soup = BeautifulSoup(response.text, "html.parser")
                token_input = soup.select_one("input[name='token']")
                
                if token_input:
                    token = token_input.get("value")
                    
                    form_data = {
                        "url": clean_url,
                        "token": token
                    }
                    
                    response = session.post(
                        "https://snaptik.app/ID/abc.php",
                        headers={
                            **self.headers,
                            "Referer": "https://snaptik.app/ID",
                            "X-Requested-With": "XMLHttpRequest",
                        },
                        data=form_data
                    )
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.text, "html.parser")
                        download_links = soup.select("a.abutton")
                        
                        for link in download_links:
                            if "Tanpa Watermark" in link.text or "No Watermark" in link.text:
                                return link["href"], video_id
            
            # Metode 3: Menggunakan tikmate.online
            print("Mencoba menggunakan metode tikmate.online...")
            
            tikmate_url = "https://tikmate.online/"
            response = session.get(tikmate_url, headers=self.headers)
            
            if response.status_code != 200:
                print(f"Error mengakses tikmate.online: {response.status_code}")
            else:
                # Membuat permintaan unduhan
                form_data = {
                    "url": clean_url
                }
                
                response = session.post(
                    "https://tikmate.online/abc.php",
                    headers={
                        **self.headers,
                        "Referer": "https://tikmate.online/",
                        "X-Requested-With": "XMLHttpRequest",
                    },
                    data=form_data
                )
                
                if response.status_code == 200:
                    try:
                        result = response.json()
                        if "hd" in result and result["hd"]:
                            download_url = "https://tikmate.online/" + result["hd"]
                            return download_url, video_id
                    except:
                        # Jika tidak berhasil sebagai JSON, coba parse sebagai HTML
                        soup = BeautifulSoup(response.text, "html.parser")
                        download_links = soup.select("a.download-link")
                        
                        for link in download_links:
                            return "https://tikmate.online" + link["href"], video_id
            
            # Metode 4: Menggunakan savetikvideo.org
            print("Mencoba menggunakan metode savetikvideo.org...")
            
            session = requests.Session()
            save_url = "https://savetikvideo.org/"
            response = session.get(save_url, headers=self.headers)
            
            if response.status_code != 200:
                print(f"Error mengakses savetikvideo.org: {response.status_code}")
            else:
                form_data = {
                    "tiktok-url": clean_url,
                    "locale": "id"
                }
                
                response = session.post(
                    "https://savetikvideo.org/wp-json/aio-dl/video-data/",
                    headers={
                        **self.headers,
                        "Referer": "https://savetikvideo.org/",
                        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                        "X-Requested-With": "XMLHttpRequest",
                    },
                    data=form_data
                )
                
                if response.status_code == 200:
                    try:
                        data = response.json()
                        if "medias" in data and len(data["medias"]) > 0:
                            for media in data["medias"]:
                                if "url" in media and "watermark" in media and not media["watermark"]:
                                    return media["url"], video_id
                    except:
                        print("Error parsing savetikvideo.org response")
            
            # Jika semua metode gagal
            print("Semua metode gagal. Tidak dapat menemukan URL unduhan.")
            return None, video_id
            
        except Exception as e:
            print(f"Error saat mendapatkan URL unduhan: {e}")
            return None, None
    
    def download_video(self, url, filename=None):
        """Mengunduh video dari URL yang diberikan."""
        try:
            download_url, video_id = self.get_download_url(url)
            
            if not download_url:
                print("Tidak dapat menemukan URL unduhan video tanpa watermark.")
                return False
            
            if not filename:
                filename = f"{video_id}.mp4"
            
            # Pastikan file memiliki ekstensi .mp4
            if not filename.endswith('.mp4'):
                filename += '.mp4'
            
            output_path = os.path.join(self.output_dir, filename)
            
            print(f"Mengunduh video ke {output_path}...")
            
            # Unduh file dengan progress bar
            response = requests.get(download_url, headers=self.headers, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            
            with open(output_path, 'wb') as f, tqdm(
                desc=filename,
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
            ) as bar:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        size = f.write(chunk)
                        bar.update(size)
            
            print(f"Video berhasil diunduh: {output_path}")
            return True
            
        except Exception as e:
            print(f"Error saat mengunduh video: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description='Unduh video TikTok tanpa watermark')
    parser.add_argument('url', help='URL video TikTok')
    parser.add_argument('-o', '--output', help='Nama file output (opsional)')
    
    args = parser.parse_args()
    
    downloader = TikTokDownloader()
    downloader.download_video(args.url, args.output)

if __name__ == "__main__":
    main()