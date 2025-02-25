import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
import os
import webbrowser
import subprocess
import platform
import time
from tiktok_downloader import TikTokDownloader

class TikTokDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TikTok Video Downloader (dengan Watermark)")
        self.root.geometry("600x450")
        self.root.resizable(True, True)
        
        # Gaya
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 11))
        self.style.configure("TLabel", font=("Arial", 11))
        self.style.configure("TEntry", font=("Arial", 11))
        self.style.configure("Bold.TLabel", font=("Arial", 11, "bold"))
        
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
        ttk.Label(main_frame, text="TikTok Video Downloader", 
                 font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, sticky=tk.W, pady=(0, 15))
        
        ttk.Label(main_frame, text="Mode Manual Dengan Browser", 
                 font=("Arial", 12)).grid(row=1, column=0, columnspan=2, sticky=tk.W, pady=(0, 20))
        
        # URL input
        ttk.Label(main_frame, text="URL Video TikTok:").grid(row=2, column=0, sticky=tk.W, pady=(0, 10))
        url_entry = ttk.Entry(main_frame, textvariable=self.url_var, width=50)
        url_entry.grid(row=2, column=1, sticky=tk.EW, pady=(0, 10))
        url_entry.bind('<Return>', lambda e: self.start_download())  # Tekan Enter untuk download
        
        # Direktori output
        ttk.Label(main_frame, text="Direktori Output:").grid(row=3, column=0, sticky=tk.W, pady=(0, 10))
        output_frame = ttk.Frame(main_frame)
        output_frame.grid(row=3, column=1, sticky=tk.EW, pady=(0, 10))
        ttk.Entry(output_frame, textvariable=self.output_dir_var, width=40).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(output_frame, text="Browse", command=self.browse_directory).pack(side=tk.RIGHT, padx=(5, 0))
        
        # Tombol-tombol
        btn_frame = ttk.Frame(main_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=(10, 20))
        ttk.Button(btn_frame, text="Buka di Browser", command=self.start_download).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="Buka Folder", command=self.open_output_folder).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(btn_frame, text="Paste URL", command=self.paste_url).pack(side=tk.LEFT)
        
        # Informasi manual
        info_frame = ttk.LabelFrame(main_frame, text="Cara Mengunduh")
        info_frame.grid(row=5, column=0, columnspan=2, sticky=tk.NSEW, pady=(10, 20))
        
        instructions = (
            "1. Masukkan URL video TikTok dan klik 'Buka di Browser'\n"
            "2. Tunggu video dimuat di browser\n"
            "3. Klik kanan pada video, pilih 'Save Video As' atau 'Simpan Video Sebagai'\n"
            "4. Simpan ke folder 'downloaded_videos'\n"
            "5. Klik 'Refresh' untuk melihat video yang diunduh"
        )
        
        ttk.Label(info_frame, text=instructions, wraplength=550, justify=tk.LEFT).pack(
            fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Status
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var, wraplength=550)
        self.status_label.grid(row=6, column=0, columnspan=2, sticky=tk.W, pady=(0, 10))
        self.status_var.set("Siap untuk membantu mengunduh video TikTok")
        
        # Frame untuk hasil
        result_frame = ttk.LabelFrame(main_frame, text="Video yang Diunduh")
        result_frame.grid(row=7, column=0, columnspan=2, sticky=tk.NSEW, pady=(0, 10))
        main_frame.grid_rowconfigure(7, weight=1)
        
        # Listbox untuk menampilkan file yang diunduh
        self.result_listbox = tk.Listbox(result_frame, height=5, width=70, font=("Arial", 10))
        self.result_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Scrollbar untuk listbox
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, padx=(0, 5), pady=5)
        self.result_listbox.config(yscrollcommand=scrollbar.set)
        
        # Frame tombol tambahan
        bottom_frame = ttk.Frame(main_frame)
        bottom_frame.grid(row=8, column=0, columnspan=2, sticky=tk.E, pady=(0, 0))
        ttk.Button(bottom_frame, text="Refresh", command=self.load_downloaded_files).pack(side=tk.RIGHT)
        
        # Context menu untuk listbox
        self.context_menu = tk.Menu(self.result_listbox, tearoff=0)
        self.context_menu.add_command(label="Buka File", command=self.open_selected_file)
        self.context_menu.add_command(label="Buka Folder", command=self.open_file_location)
        self.context_menu.add_separator()
        self.context_menu.add_command(label="Hapus dari Daftar", command=self.remove_selected)
        self.context_menu.add_command(label="Hapus File", command=self.delete_selected_file)
        
        # Bind double-click dan right-click pada listbox
        self.result_listbox.bind("<Double-1>", self.open_file)
        self.result_listbox.bind("<Button-3>", self.show_context_menu)
        
        # Inisialisasi downloader
        self.downloader = TikTokDownloader()
        self.downloader.output_dir = self.output_dir_var.get()
        
        # Muat daftar file yang sudah diunduh
        self.load_downloaded_files()
        
        # Event handler untuk perubahan direktori output
        self.output_dir_var.trace_add("write", self.on_output_dir_change)
        
        # Set focus ke URL entry
        url_entry.focus_set()
    
    def on_output_dir_change(self, *args):
        """Handler untuk perubahan direktori output."""
        self.downloader.output_dir = self.output_dir_var.get()
    
    def browse_directory(self):
        """Membuka dialog untuk memilih direktori output."""
        directory = filedialog.askdirectory()
        if directory:
            self.output_dir_var.set(directory)
            # Buat direktori jika belum ada
            if not os.path.exists(directory):
                os.makedirs(directory)
            # Refresh daftar file
            self.load_downloaded_files()
    
    def paste_url(self):
        """Menempelkan URL dari clipboard."""
        try:
            url = self.root.clipboard_get()
            if url and ('tiktok.com' in url or 'douyin.com' in url):
                self.url_var.set(url)
        except Exception:
            pass
    
    def load_downloaded_files(self):
        """Memuat daftar file yang sudah diunduh."""
        self.result_listbox.delete(0, tk.END)
        dir_path = self.output_dir_var.get()
        if os.path.exists(dir_path):
            files = [f for f in os.listdir(dir_path) if f.endswith('.mp4')]
            for file in sorted(files, key=lambda x: os.path.getmtime(os.path.join(dir_path, x)), reverse=True):
                self.result_listbox.insert(tk.END, file)
    
    def open_file(self, event):
        """Membuka file yang dipilih dengan aplikasi default."""
        self.open_selected_file()
    
    def open_selected_file(self):
        """Membuka file yang dipilih dengan aplikasi default."""
        try:
            selection = self.result_listbox.curselection()
            if selection:
                file_name = self.result_listbox.get(selection[0])
                file_path = os.path.join(self.output_dir_var.get(), file_name)
                self.open_file_with_default_app(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Tidak dapat membuka file: {e}")
    
    def open_file_location(self):
        """Membuka lokasi file di file explorer."""
        try:
            selection = self.result_listbox.curselection()
            if selection:
                file_name = self.result_listbox.get(selection[0])
                file_path = os.path.join(self.output_dir_var.get(), file_name)
                self.open_folder_with_file_selected(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Tidak dapat membuka lokasi file: {e}")
    
    def remove_selected(self):
        """Menghapus file yang dipilih dari daftar (tidak menghapus file)."""
        try:
            selection = self.result_listbox.curselection()
            if selection:
                self.result_listbox.delete(selection[0])
        except Exception as e:
            messagebox.showerror("Error", f"Tidak dapat menghapus dari daftar: {e}")
    
    def delete_selected_file(self):
        """Menghapus file yang dipilih dari disk."""
        try:
            selection = self.result_listbox.curselection()
            if selection:
                file_name = self.result_listbox.get(selection[0])
                file_path = os.path.join(self.output_dir_var.get(), file_name)
                
                confirm = messagebox.askyesno("Konfirmasi", f"Anda yakin ingin menghapus file ini?\n{file_name}")
                if confirm:
                    os.remove(file_path)
                    self.result_listbox.delete(selection[0])
                    messagebox.showinfo("Info", "File berhasil dihapus.")
        except Exception as e:
            messagebox.showerror("Error", f"Tidak dapat menghapus file: {e}")
    
    def show_context_menu(self, event):
        """Menampilkan menu konteks saat klik kanan pada listbox."""
        try:
            # Pilih item di bawah kursor
            index = self.result_listbox.nearest(event.y)
            if index >= 0:
                self.result_listbox.selection_clear(0, tk.END)
                self.result_listbox.selection_set(index)
                self.result_listbox.activate(index)
                self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()
    
    def open_file_with_default_app(self, file_path):
        """Membuka file dengan aplikasi default."""
        import platform
        import subprocess
        
        try:
            if platform.system() == 'Windows':
                os.startfile(file_path)
            elif platform.system() == 'Darwin':  # macOS
                subprocess.call(('open', file_path))
            else:  # Linux
                subprocess.call(('xdg-open', file_path))
        except Exception as e:
            messagebox.showerror("Error", f"Tidak dapat membuka file: {e}")
    
    def open_folder_with_file_selected(self, file_path):
        """Membuka folder yang berisi file."""
        import platform
        import subprocess
        
        try:
            folder_path = os.path.dirname(file_path)
            
            if platform.system() == 'Windows':
                # Untuk Windows, buka Explorer dengan file terseleksi
                subprocess.Popen(f'explorer /select,"{file_path}"')
            elif platform.system() == 'Darwin':  # macOS
                # Untuk macOS, buka Finder
                subprocess.call(('open', folder_path))
            else:  # Linux
                # Untuk Linux, buka file manager
                subprocess.call(('xdg-open', folder_path))
        except Exception as e:
            messagebox.showerror("Error", f"Tidak dapat membuka folder: {e}")
    
    def open_output_folder(self):
        """Membuka direktori output."""
        import platform
        import subprocess
        
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
        except Exception as e:
            messagebox.showerror("Error", f"Tidak dapat membuka folder: {e}")
    
    def start_download(self):
        """Memulai proses download."""
        url = self.url_var.get().strip()
        if not url:
            messagebox.showerror("Error", "Masukkan URL TikTok!")
            return
        
        # Set direktori output ke downloader
        self.downloader.output_dir = self.output_dir_var.get()
        
        # Tampilkan instruksi
        clean_url = self.downloader.clean_url(url)
        video_id = self.downloader.get_video_id(clean_url)
        username = self.downloader.extract_username(clean_url)
        
        filename = f"{username}_{video_id}.mp4"
        output_path = os.path.join(self.downloader.output_dir, filename)
        
        # Buat folder jika belum ada
        if not os.path.exists(self.downloader.output_dir):
            os.makedirs(self.downloader.output_dir)
        
        # Tampilkan informasi
        messagebox.showinfo("Petunjuk Download", 
                          f"Browser akan dibuka dengan TikTok.\n\n"
                          f"Ikuti langkah-langkah ini:\n"
                          f"1. Tunggu video dimuat\n"
                          f"2. Klik kanan pada video\n"
                          f"3. Pilih 'Save Video As' atau 'Simpan Video Sebagai'\n"
                          f"4. Simpan video ke: \n{output_path}\n\n"
                          f"Setelah selesai, klik 'Refresh' untuk melihat video dalam daftar.")
        
        # Buka browser
        threading.Thread(target=self.open_browser_thread, args=(clean_url,), daemon=True).start()
    
    def open_browser_thread(self, url):
        """Thread untuk membuka browser."""
        try:
            self.status_var.set("Membuka browser...")
            
            # Buka browser
            if platform.system() == 'Windows':
                # Tambahkan parameter untuk otomatis download di Chrome (jika Chrome adalah browser default)
                try:
                    subprocess.Popen(f'start chrome "{url}"')
                except:
                    webbrowser.open(url)
            else:
                webbrowser.open(url)
            
            self.status_var.set("Browser dibuka. Silakan unduh video secara manual.")
            
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Terjadi kesalahan saat membuka browser: {str(e)}")

# Main function
def main():
    root = tk.Tk()
    app = TikTokDownloaderApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()