import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import os
import subprocess
import platform
import webbrowser
import re
import time
import tempfile
import shutil
import requests
import sys

class TikTokBrowserHelper:
    def __init__(self, root):
        self.root = root
        self.root.title("TikTok Video Grabber")
        self.root.geometry("650x650")
        self.root.resizable(True, True)
        
        # Variabel
        self.url_var = tk.StringVar()
        self.output_dir_var = tk.StringVar()
        self.status_var = tk.StringVar()
        
        # Set direktori default
        self.output_dir_var.set(os.path.join(os.getcwd(), "downloaded_videos"))
        
        # Buat frame utama
        main_frame = ttk.Frame(root, padding=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Judul
        ttk.Label(main_frame, text="TikTok Video Grabber", 
                 font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 15))
        
        # URL input
        ttk.Label(main_frame, text="URL Video TikTok:").grid(row=1, column=0, sticky=tk.W, pady=(0, 10))
        url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=50)
        url_entry.grid(row=1, column=1, sticky=tk.EW, pady=(0, 10))
        url_entry.bind('<Return>', lambda e: self.start_process())
        
        # Direktori output
        ttk.Label(main_frame, text="Direktori Output:").grid(row=2, column=0, sticky=tk.W, pady=(0, 10))
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=2, column=1, sticky=tk.EW, pady=(0, 10))
        ttk.Entry(output_frame, textvariable=self.output_dir_var, width=40).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(output_frame, text="Browse", command=self.browse_directory).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Tombol-tombol
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=3, column=0, columnspan=2, pady=(10, 20))
        ttk.Button(btn_frame, text="Paste URL", command=self.paste_url).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="Mulai Proses", command=self.start_process).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="Buka Folder", command=self.open_output_folder).pack(side=tk.LEFT)
        
        # Frame Metode
        method_frame = ttk.LabelFrame(main_frame, text="Metode Unduh")
        method_frame.grid(row=4, column=0, columnspan=2, sticky=tk.NSEW, pady=(0, 15))
        
        # Metode 1
        ttk.Button(method_frame, text="Metode 1: Browser Standar", 
                  command=self.method_standard_browser).pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)
        
        ttk.Label(method_frame, text="Buka browser dan instruksi klik kanan untuk mengunduh video",
                   wraplength=550).pack(anchor=tk.W, padx=30, pady=(0, 10))
        
        # Metode 2 - Ubah jadi SnapTik
        ttk.Button(method_frame, text="Metode 2: SnapTik (Online Downloader)", 
                  command=self.method_online_downloader).pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)
        
        ttk.Label(method_frame, text="Buka SnapTik.com atau downloader online lainnya untuk mengunduh tanpa watermark",
                   wraplength=550).pack(anchor=tk.W, padx=30, pady=(0, 10))
        
        # Metode 3
        ttk.Button(method_frame, text="Metode 3: Screen Recording", 
                  command=self.method_screen_recording).pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)
        
        ttk.Label(method_frame, text="Instruksi untuk merekam layar saat memainkan video TikTok",
                   wraplength=550).pack(anchor=tk.W, padx=30, pady=(0, 10))
        
        # Metode 4 - Dev Tools (ditambahkan kembali sebagai opsi)
        ttk.Button(method_frame, text="Metode 4: Developer Tools (Advanced)", 
                  command=self.method_developer_tools).pack(anchor=tk.W, padx=10, pady=5, fill=tk.X)
        
        ttk.Label(method_frame, text="Buka browser dengan instruksi menggunakan Developer Tools untuk menemukan URL video",
                   wraplength=550).pack(anchor=tk.W, padx=30, pady=(0, 10))
        
        # Status
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var, wraplength=550)
        self.status_label.grid(row=5, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        self.status_var.set("Siap untuk mengunduh video TikTok. Pilih metode yang sesuai.")
        
        # Tab untuk instruksi detail
        notebook = ttk.Notebook(main_frame)
        notebook.grid(row=6, column=0, columnspan=2, sticky=tk.NSEW, pady=(10, 10))
        main_frame.grid_rowconfigure(6, weight=1)
        
        # Tab 1: Instruksi Metode 1
        tab1 = ttk.Frame(notebook)
        notebook.add(tab1, text="Instruksi Metode 1")
        
        instructions1 = (
            "METODE 1: BROWSER STANDAR\n\n"
            "1. Klik 'Metode 1: Browser Standar'\n"
            "2. Tunggu browser terbuka dan video TikTok dimuat\n"
            "3. Klik kanan pada video dan pilih 'Save Video As' atau 'Simpan Video Sebagai'\n"
            "4. Jika klik kanan tidak berfungsi, coba:\n"
            "   - Tekan Ctrl+S (Windows/Linux) atau Command+S (Mac)\n"
            "   - Cari tombol Download/Share di halaman TikTok\n"
            "   - Gunakan ekstensi browser Video Downloader\n"
            "5. Simpan video ke folder yang Anda pilih\n\n"
            "Jika metode ini gagal, coba Metode 2 atau 3."
        )
        
        text1 = tk.Text(tab1, wrap=tk.WORD, height=20, width=70)
        text1.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        text1.insert(tk.END, instructions1)
        text1.config(state=tk.DISABLED)
        
        # Tab 2: Instruksi Metode 2 (SnapTik)
        tab2 = ttk.Frame(notebook)
        notebook.add(tab2, text="Instruksi Metode 2")
        
        instructions2 = (
            "METODE 2: SNAPTIK (ONLINE DOWNLOADER)\n\n"
            "1. Klik 'Metode 2: SnapTik (Online Downloader)'\n"
            "2. Browser akan terbuka dengan website SnapTik.com\n"
            "3. Tunggu halaman SnapTik.com dimuat\n"
            "4. Tempel URL video TikTok ke dalam kotak input SnapTik\n"
            "5. Klik tombol 'Download'\n"
            "6. Tunggu proses selesai, kemudian klik opsi 'Download MP4' atau 'No Watermark'\n"
            "7. Simpan video ke folder yang Anda pilih\n\n"
            "Alternatif Downloader Online Lainnya:\n"
            "- SSSTik.io\n"
            "- SaveTT.cc\n"
            "- TikMate.online\n"
            "- TikDown.org\n"
            "- MusicallyDown.com\n\n"
            "Jika satu situs diblokir atau tidak berfungsi, coba situs lainnya."
        )
        
        text2 = tk.Text(tab2, wrap=tk.WORD, height=20, width=70)
        text2.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        text2.insert(tk.END, instructions2)
        text2.config(state=tk.DISABLED)
        
        # Tab 3: Instruksi Metode 3
        tab3 = ttk.Frame(notebook)
        notebook.add(tab3, text="Instruksi Metode 3")
        
        instructions3 = (
            "METODE 3: SCREEN RECORDING\n\n"
            "1. Klik 'Metode 3: Screen Recording'\n"
            "2. Browser akan terbuka dengan TikTok\n"
            "3. Gunakan alat perekam layar untuk merekam video:\n\n"
            "   WINDOWS:\n"
            "   - Tekan Win+G untuk membuka Game Bar\n"
            "   - Klik tombol rekam untuk mulai merekam\n"
            "   - Atau gunakan Win+Alt+R untuk langsung merekam\n"
            "   - Video tersimpan di folder Videos/Captures\n\n"
            "   MAC:\n"
            "   - Tekan Command+Shift+5\n"
            "   - Pilih area yang ingin direkam\n"
            "   - Klik 'Record'\n"
            "   - Untuk berhenti, klik icon stop di menu bar\n\n"
            "   ANDROID:\n"
            "   - Geser ke bawah panel notifikasi\n"
            "   - Pilih 'Screen Recorder'\n\n"
            "   IPHONE:\n"
            "   - Geser ke atas untuk Control Center\n"
            "   - Tahan tombol rekam (lingkaran dalam lingkaran)\n"
            "   - Pilih 'Screen Recording'\n\n"
            "4. Putar video TikTok dalam mode fullscreen jika memungkinkan\n"
            "5. Berhenti merekam setelah video selesai\n"
            "6. Pindahkan video hasil rekaman ke folder yang Anda pilih"
        )
        
        text3 = tk.Text(tab3, wrap=tk.WORD, height=20, width=70)
        text3.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        text3.insert(tk.END, instructions3)
        text3.config(state=tk.DISABLED)
        
        # Tab 4: Instruksi Metode 4 (Dev Tools)
        tab4 = ttk.Frame(notebook)
        notebook.add(tab4, text="Instruksi Metode 4")
        
        instructions4 = (
            "METODE 4: DEVELOPER TOOLS (ADVANCED)\n\n"
            "1. Klik 'Metode 4: Developer Tools'\n"
            "2. Browser akan terbuka dengan TikTok\n"
            "3. Buka Developer Tools:\n"
            "   - Chrome/Edge: Tekan F12 atau klik kanan > Inspect\n"
            "   - Firefox: Tekan F12 atau klik kanan > Inspect Element\n"
            "4. Klik tab 'Network'\n"
            "5. Reload halaman (F5)\n"
            "6. Putar video TikTok\n"
            "7. Di panel Network, filter dengan '.mp4' atau ketik 'mp4' di kotak filter\n"
            "8. Cari file dengan ukuran besar (biasanya video TikTok)\n"
            "9. Klik kanan file tersebut dan pilih 'Open in new tab' atau 'Copy URL'\n"
            "10. Di tab baru, klik kanan video dan pilih 'Save Video As'\n\n"
            "Catatan: File video biasanya bernama panjang dengan ekstensi .mp4"
        )
        
        text4 = tk.Text(tab4, wrap=tk.WORD, height=20, width=70)
        text4.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)
        text4.insert(tk.END, instructions4)
        text4.config(state=tk.DISABLED)
        
        # Set focus ke URL entry
        url_entry.focus_set()
        
        # Buat folder output jika belum ada
        if not os.path.exists(self.output_dir_var.get()):
            os.makedirs(self.output_dir_var.get())
    
    def browse_directory(self):
        """Membuka dialog untuk memilih direktori output."""
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir_var.set(directory)
            if not os.path.exists(directory):
                os.makedirs(directory)
    
    def paste_url(self):
        """Menempelkan URL dari clipboard."""
        try:
            url = self.root.clipboard_get()
            if url and ('tiktok.com' in url or 'douyin.com' in url):
                self.url_var.set(url)
        except Exception:
            pass
    
    def clean_url(self, url):
        """Membersihkan URL TikTok."""
        # Menangani URL pendek
        if "vm.tiktok.com" in url or "vt.tiktok.com" in url:
            self.status_var.set("Mengonversi URL pendek...")
            try:
                session = requests.Session()
                response = session.head(url, allow_redirects=True, timeout=15)
                url = response.url
                self.status_var.set(f"URL dikonversi: {url}")
            except Exception as e:
                self.status_var.set(f"Gagal mengonversi URL pendek: {e}")
        
        # Membersihkan parameter query
        if '?' in url:
            base_url = url.split('?')[0]
            url = base_url
        
        return url
    
    def start_process(self):
        """Memulai proses awal."""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Masukkan URL TikTok terlebih dahulu!")
            return
        
        # Bersihkan URL
        clean_url = self.clean_url(url)
        self.url_var.set(clean_url)
        
        # Tampilkan informasi
        self.status_var.set(f"URL siap diproses: {clean_url}\nSilakan pilih salah satu metode di atas.")
    
    def method_standard_browser(self):
        """Metode 1: Browser Standar."""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Masukkan URL TikTok terlebih dahulu!")
            return
        
        # Tampilkan instruksi
        messagebox.showinfo("Metode 1: Browser Standar", 
                          "Browser akan terbuka dengan video TikTok.\n\n"
                          "1. Tunggu video dimuat\n"
                          "2. Klik kanan pada video dan pilih 'Save Video As'\n"
                          "3. Jika klik kanan tidak bekerja, coba:\n"
                          "   - Tekan Ctrl+S (Windows) atau Command+S (Mac)\n"
                          "   - Cari tombol Download/Share di halaman\n"
                          "4. Simpan video ke folder yang Anda pilih")
        
        # Buka browser
        self.status_var.set("Membuka browser...")
        threading.Thread(target=self.open_browser, args=(url,), daemon=True).start()
    
    def method_online_downloader(self):
        """Metode 2: SnapTik atau downloader online lain."""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Masukkan URL TikTok terlebih dahulu!")
            return
        
        # Daftar situs downloader
        downloaders = [
            {"name": "SnapTik", "url": "https://snaptik.app/"},
            {"name": "SSSTik", "url": "https://ssstik.io/"},
            {"name": "SaveTT", "url": "https://savett.cc/"},
            {"name": "TikMate", "url": "https://tikmate.online/"},
            {"name": "MusicallyDown", "url": "https://musicallydown.com/"}
        ]
        
        # Dialog pilihan downloader
        downloader_window = tk.Toplevel(self.root)
        downloader_window.title("Pilih Online Downloader")
        downloader_window.geometry("400x300")
        downloader_window.transient(self.root)
        downloader_window.grab_set()
        
        ttk.Label(downloader_window, text="Pilih situs downloader:", font=("Arial", 12)).pack(pady=10)
        
        frame = ttk.Frame(downloader_window, padding=10)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Fungsi untuk membuka downloader
        def open_selected_downloader(downloader_url):
            # Salin URL ke clipboard untuk memudahkan paste
            self.root.clipboard_clear()
            self.root.clipboard_append(url)
            
            # Tampilkan instruksi
            messagebox.showinfo("Petunjuk SnapTik",
                               f"URL TikTok telah disalin ke clipboard.\n\n"
                               f"1. Browser akan terbuka dengan situs downloader\n"
                               f"2. Tempel URL TikTok ke kotak input (Ctrl+V)\n"
                               f"3. Klik tombol download atau proses\n"
                               f"4. Pilih opsi 'No Watermark' atau 'Download MP4'\n"
                               f"5. Simpan video ke folder yang Anda pilih")
            
            # Buka browser dengan URL downloader
            self.status_var.set(f"Membuka browser dengan situs downloader...")
            threading.Thread(target=self.open_browser, args=(downloader_url,), daemon=True).start()
            
            downloader_window.destroy()
        
        # Buat tombol untuk setiap downloader
        for downloader in downloaders:
            btn = ttk.Button(
                frame, 
                text=downloader["name"], 
                command=lambda url=downloader["url"]: open_selected_downloader(url)
            )
            btn.pack(fill=tk.X, pady=5)
        
        ttk.Label(downloader_window, text="Catatan: Jika satu situs diblokir atau tidak\nberfungsi, silakan coba yang lain.", 
                 font=("Arial", 10)).pack(pady=10)
    
    def method_developer_tools(self):
        """Metode 4: Developer Tools."""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Masukkan URL TikTok terlebih dahulu!")
            return
        
        # Tampilkan instruksi
        messagebox.showinfo("Metode 4: Developer Tools", 
                          "Browser akan terbuka dengan video TikTok.\n\n"
                          "1. Tekan F12 untuk membuka Developer Tools\n"
                          "2. Klik tab 'Network'\n"
                          "3. Reload halaman (F5)\n"
                          "4. Putar video\n"
                          "5. Filter dengan '.mp4' atau ketik 'mp4'\n"
                          "6. Cari file dengan ukuran besar\n"
                          "7. Klik kanan dan pilih 'Open in new tab'\n"
                          "8. Di tab baru, pilih 'Save Video As'")
        
        # Buka browser
        self.status_var.set("Membuka browser...")
        threading.Thread(target=self.open_browser, args=(url,), daemon=True).start()
    
    def method_screen_recording(self):
        """Metode 3: Screen Recording."""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Masukkan URL TikTok terlebih dahulu!")
            return
        
        # Tampilkan informasi cara screen recording sesuai OS
        os_name = platform.system()
        
        if os_name == 'Windows':
            recording_instructions = (
                "Cara merekam layar di Windows:\n\n"
                "1. Tekan Win+G untuk membuka Game Bar\n"
                "2. Klik tombol rekam untuk mulai merekam\n"
                "3. Atau gunakan Win+Alt+R untuk langsung merekam\n"
                "4. Putar video TikTok\n"
                "5. Tekan Win+Alt+R lagi untuk berhenti merekam\n"
                "6. Video tersimpan di folder Videos/Captures\n\n"
                "Browser akan terbuka dengan video TikTok setelah Anda menutup pesan ini."
            )
        elif os_name == 'Darwin':  # macOS
            recording_instructions = (
                "Cara merekam layar di Mac:\n\n"
                "1. Tekan Command+Shift+5\n"
                "2. Pilih area yang ingin direkam\n"
                "3. Klik 'Record'\n"
                "4. Putar video TikTok\n"
                "5. Untuk berhenti, klik icon stop di menu bar\n"
                "6. Video akan tersimpan di Desktop\n\n"
                "Browser akan terbuka dengan video TikTok setelah Anda menutup pesan ini."
            )
        else:  # Linux atau lainnya
            recording_instructions = (
                "Cara merekam layar di Linux:\n\n"
                "1. Gunakan aplikasi seperti OBS Studio, SimpleScreenRecorder, atau Kazam\n"
                "2. Atur area rekaman\n"
                "3. Mulai rekaman\n"
                "4. Putar video TikTok\n"
                "5. Berhenti merekam setelah selesai\n\n"
                "Browser akan terbuka dengan video TikTok setelah Anda menutup pesan ini."
            )
        
        messagebox.showinfo("Metode 3: Screen Recording", recording_instructions)
        
        # Buka browser
        self.status_var.set("Membuka browser...")
        threading.Thread(target=self.open_browser, args=(url,), daemon=True).start()
    
    def open_browser(self, url):
        """Membuka browser dengan URL yang diberikan."""
        try:
            if platform.system() == 'Windows':
                # Coba buka dengan Chrome jika tersedia
                try:
                    subprocess.Popen(f'start chrome "{url}"')
                except:
                    webbrowser.open(url)
            else:
                webbrowser.open(url)
            
            self.status_var.set(f"Browser dibuka dengan URL: {url}\nIkuti petunjuk di tab instruksi untuk mengunduh video.")
            
        except Exception as e:
            self.status_var.set(f"Error saat membuka browser: {str(e)}")
            messagebox.showerror("Error", f"Gagal membuka browser: {str(e)}")
    
    def open_output_folder(self):
        """Membuka direktori output."""
        try:
            dir_path = self.output_dir_var.get()
            
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            
            if platform.system() == 'Windows':
                os.startfile(dir_path)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.call(('open', dir_path))
            else:  # Linux
                subprocess.call(('xdg-open', dir_path))
                
            self.status_var.set(f"Folder terbuka: {dir_path}")
                
        except Exception as e:
            self.status_var.set(f"Error saat membuka folder: {str(e)}")
            messagebox.showerror("Error", f"Gagal membuka folder: {str(e)}")

# Main function
def main():
    root = tk.Tk()
    app = TikTokBrowserHelper(root)
    root.mainloop()

if __name__ == "__main__":
    main()