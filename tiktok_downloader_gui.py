import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import os
from tiktok_downloader import TikTokDownloader

class TikTokDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TikTok Video Downloader")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # Gaya
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 12))
        self.style.configure("TLabel", font=("Arial", 12))
        self.style.configure("TEntry", font=("Arial", 12))
        
        # Variabel
        self.url_var = tk.StringVar()
        self.output_dir_var = tk.StringVar()
        self.status_var = tk.StringVar()
        self.progress_var = tk.DoubleVar()
        
        # Set direktori default
        self.output_dir_var.set(os.path.join(os.getcwd(), "downloaded_videos"))
        
        # Buat frame utama
        main_frame = ttk.Frame(root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # URL input
        ttk.Label(main_frame, text="URL Video TikTok:").grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
        ttk.Entry(main_frame, textvariable=self.url_var, width=50).grid(row=0, column=1, sticky=tk.EW, pady=(0, 10))
        
        # Direktori output
        ttk.Label(main_frame, text="Direktori Output:").grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=1, column=1, sticky=tk.EW, pady=(0, 10))
        ttk.Entry(output_frame, textvariable=self.output_dir_var, width=40).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(output_frame, text="Browse", command=self.browse_directory).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Tombol unduh
        ttk.Button(main_frame, text="Unduh Video", command=self.start_download).grid(row=2, column=0, columnspan=2, pady=(10, 20))
        
        # Progress bar
        self.progress = ttk.Progressbar(main_frame, variable=self.progress_var, maximum=100)
        self.progress.grid(row=3, column=0, columnspan=2, sticky=tk.EW, pady=(0, 10))
        
        # Status
        ttk.Label(main_frame, textvariable=self.status_var).grid(row=4, column=0, columnspan=2, sticky=tk.W)
        self.status_var.set("Siap untuk mengunduh")
        
        # Frame untuk hasil
        result_frame = ttk.LabelFrame(main_frame, text="Video yang Diunduh")
        result_frame.grid(row=5, column=0, columnspan=2, sticky=tk.NSEW, pady=(10, 0))
        main_frame.grid_rowconfigure(5, weight=1)
        
        # Listbox untuk menampilkan file yang diunduh
        self.result_listbox = tk.Listbox(result_frame, height=5, width=70)
        self.result_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbar untuk listbox
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 5), pady=5)
        self.result_listbox.config(yscrollcommand=scrollbar.set)
        
        # Bind double-click pada listbox
        self.result_listbox.bind("<Double-1>", self.open_file)
        
        # Inisialisasi downloader
        self.downloader = TikTokDownloader()
        
        # Muat daftar file yang sudah diunduh
        self.load_downloaded_files()
    
    def browse_directory(self):
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir_var.set(directory)
            self.downloader.output_dir = directory
            # Buat direktori jika belum ada
            if not os.path.exists(directory):
                os.makedirs(directory)
            # Refresh daftar file
            self.load_downloaded_files()
    
    def load_downloaded_files(self):
        self.result_listbox.delete(0, tk.END)
        dir_path = self.output_dir_var.get()
        if os.path.exists(dir_path):
            files = [f for f in os.listdir(dir_path) if f.endswith('.mp4')]
            for file in sorted(files, key=lambda x: os.path.getmtime(os.path.join(dir_path, x)), reverse=True):
                self.result_listbox.insert(tk.END, file)
    
    def open_file(self, event):
        try:
            selection = self.result_listbox.curselection()
            if selection:
                file_name = self.result_listbox.get(selection[0])
                file_path = os.path.join(self.output_dir_var.get(), file_name)
                
                # Buka file dengan aplikasi default
                import platform
                import subprocess
                
                if platform.system() == 'Windows':
                    os.startfile(file_path)
                elif platform.system() == 'Darwin':  # macOS
                    subprocess.call(('open', file_path))
                else:  # Linux
                    subprocess.call(('xdg-open', file_path))
        except Exception as e:
            messagebox.showerror("Error", f"Tidak dapat membuka file: {e}")
    
    def update_progress(self, value):
        self.progress_var.set(value)
        self.root.update_idletasks()
    
    def start_download(self):
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Masukkan URL TikTok!")
            return
        
        # Set direktori output ke downloader
        self.downloader.output_dir = self.output_dir_var.get()
        
        # Mulai unduhan dalam thread terpisah
        threading.Thread(target=self.download_thread, args=(url,), daemon=True).start()
    
    def download_thread(self, url):
        try:
            self.status_var.set("Mengambil informasi video...")
            self.update_progress(10)
            
            # Dapatkan URL unduhan dan ID video
            download_url, video_id = self.downloader.get_download_url(url)
            
            if not download_url:
                self.status_var.set("Gagal mendapatkan URL unduhan")
                messagebox.showerror("Error", "Tidak dapat menemukan URL unduhan video tanpa watermark.")
                self.update_progress(0)
                return
            
            filename = f"{video_id}.mp4"
            output_path = os.path.join(self.downloader.output_dir, filename)
            
            self.status_var.set(f"Mengunduh {filename}...")
            self.update_progress(30)
            
            # Unduh video
            response = requests.get(download_url, headers=self.downloader.headers, stream=True)
            total_size = int(response.headers.get('content-length', 0))
            
            # Buat direktori jika belum ada
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            downloaded_size = 0
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=4096):
                    if chunk:
                        f.write(chunk)
                        downloaded_size += len(chunk)
                        progress = min(30 + int(70 * downloaded_size / total_size), 100)
                        self.update_progress(progress)
            
            self.status_var.set(f"Video berhasil diunduh: {filename}")
            self.update_progress(100)
            
            # Refresh daftar file
            self.load_downloaded_files()
            
            # Reset progress setelah beberapa detik
            self.root.after(3000, lambda: self.update_progress(0))
            
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Terjadi kesalahan: {str(e)}")
            self.update_progress(0)

# Main function
def main():
    root = tk.Tk()
    app = TikTokDownloaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()