#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TikTok Video Grabber
Aplikasi untuk mengunduh video TikTok dengan berbagai metode
"""

import argparse
import sys
import tkinter as tk
import os
import webbrowser
from tiktok_downloader import TikTokDownloader

def main():
    # Parse argumen command line
    parser = argparse.ArgumentParser(description='TikTok Video Grabber')
    parser.add_argument('--cli', action='store_true', help='Jalankan dalam mode CLI (Command Line Interface)')
    parser.add_argument('--url', help='URL video TikTok (diperlukan dalam mode CLI)')
    parser.add_argument('--output', help='Nama file output (opsional, hanya untuk mode CLI)')
    parser.add_argument('--method', choices=['browser', 'snaptik', 'record'], 
                      default='browser', help='Metode unduhan (browser, snaptik, record)')
    
    args = parser.parse_args()
    
    # Jika mode CLI
    if args.cli:
        if not args.url:
            print("Error: URL diperlukan dalam mode CLI")
            parser.print_help()
            sys.exit(1)
        
        # Jalankan downloader
        downloader = TikTokDownloader()
        
        if args.method == 'snaptik':
            print("Membuka SnapTik dengan URL TikTok...")
            webbrowser.open(f"https://snaptik.app/")
            print("URL TikTok Anda:", args.url)
            print("Tempel URL ke dalam kotak input SnapTik untuk mengunduh video")
            sys.exit(0)
        elif args.method == 'browser':
            print("Membuka browser dengan URL TikTok...")
            downloader.clean_url(args.url)  # Bersihkan URL
            webbrowser.open(args.url)
            print("Klik kanan pada video dan pilih 'Save Video As' atau gunakan Ctrl+S")
            sys.exit(0)
        else:
            # Method record - beri instruksi perekaman layar
            if sys.platform == 'win32':
                print("Untuk merekam layar di Windows:")
                print("1. Tekan Win+G untuk membuka Game Bar")
                print("2. Klik tombol rekam atau tekan Win+Alt+R")
            elif sys.platform == 'darwin':
                print("Untuk merekam layar di macOS:")
                print("1. Tekan Command+Shift+5")
                print("2. Pilih area dan klik 'Record'")
            else:
                print("Gunakan aplikasi perekam layar di sistem Anda")
            
            # Buka URL TikTok di browser
            webbrowser.open(args.url)
            print("URL TikTok dibuka di browser. Mulai rekam layar dan putar video.")
            sys.exit(0)
    
    # Jika mode GUI (default)
    else:
        # Cek file yang tersedia dan prioritaskan
        if os.path.exists("tiktok-video-grabber-online.py"):
            # Jika file tiktok-video-grabber-online.py tersedia, gunakan itu
            try:
                import importlib.util
                spec = importlib.util.spec_from_file_location("tiktok_grabber", "tiktok-video-grabber-online.py")
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                root = tk.Tk()
                app = module.TikTokBrowserHelper(root)
                root.mainloop()
                return
            except Exception as e:
                print(f"Error saat memuat tiktok-video-grabber-online.py: {e}")
                # Lanjut ke metode berikutnya jika gagal
        
        # Coba import dari tiktok-gui-simplest.py
        if os.path.exists("tiktok-gui-simplest.py"):
            try:
                import importlib.util
                spec = importlib.util.spec_from_file_location("tiktok_gui", "tiktok-gui-simplest.py")
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                root = tk.Tk()
                app = module.TikTokDownloaderApp(root)
                root.mainloop()
                return
            except Exception as e:
                print(f"Error saat memuat tiktok-gui-simplest.py: {e}")
                # Lanjut ke metode berikutnya jika gagal
        
        # Jika kedua file tidak ditemukan, gunakan metode fallback
        try:
            from tiktok_downloader import TikTokDownloader
            # Buat aplikasi GUI sederhana
            root = tk.Tk()
            root.title("TikTok Video Downloader (Simple)")
            root.geometry("550x400")
            
            def open_browser():
                url = url_entry.get().strip()
                if not url:
                    tk.messagebox.showerror("Error", "Masukkan URL TikTok terlebih dahulu!")
                    return
                
                # Buka SnapTik.app atau URL TikTok di browser
                if method_var.get() == "snaptik":
                    # Salin URL ke clipboard
                    root.clipboard_clear()
                    root.clipboard_append(url)
                    # Buka SnapTik
                    webbrowser.open("https://snaptik.app/")
                    status_label.config(text="SnapTik.app dibuka di browser. URL TikTok disalin ke clipboard.")
                else:
                    # Buka URL TikTok
                    downloader = TikTokDownloader()
                    clean_url = downloader.clean_url(url)
                    webbrowser.open(clean_url)
                    status_label.config(text="Browser dibuka dengan URL TikTok.")
            
            # Frame utama
            main_frame = tk.Frame(root, padx=20, pady=20)
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            # URL input
            tk.Label(main_frame, text="URL Video TikTok:").grid(row=0, column=0, sticky=tk.W, pady=(0, 10))
            url_entry = tk.Entry(main_frame, width=50)
            url_entry.grid(row=0, column=1, sticky=tk.EW, pady=(0, 10))
            
            # Metode unduhan
            method_var = tk.StringVar(value="browser")
            method_frame = tk.LabelFrame(main_frame, text="Metode Unduhan", padx=10, pady=10)
            method_frame.grid(row=1, column=0, columnspan=2, sticky=tk.EW, pady=(10, 20))
            
            tk.Radiobutton(method_frame, text="Browser Standar", variable=method_var, value="browser").pack(anchor=tk.W)
            tk.Radiobutton(method_frame, text="SnapTik (Tanpa Watermark)", variable=method_var, value="snaptik").pack(anchor=tk.W)
            
            # Tombol
            button_frame = tk.Frame(main_frame)
            button_frame.grid(row=2, column=0, columnspan=2, pady=(0, 20))
            
            paste_button = tk.Button(button_frame, text="Paste URL", command=lambda: url_entry.insert(0, root.clipboard_get()))
            paste_button.pack(side=tk.LEFT, padx=(0, 10))
            
            open_button = tk.Button(button_frame, text="Buka di Browser", command=open_browser)
            open_button.pack(side=tk.LEFT)
            
            # Status
            status_label = tk.Label(main_frame, text="Masukkan URL TikTok dan pilih metode unduhan", wraplength=500)
            status_label.grid(row=3, column=0, columnspan=2, sticky=tk.W)
            
            # Instruksi
            instructions = (
                "Cara Menggunakan:\n\n"
                "1. Tempel URL video TikTok ke dalam kotak di atas\n"
                "2. Pilih metode unduhan\n"
                "3. Klik 'Buka di Browser'\n\n"
                "Untuk Browser Standar:\n"
                "- Klik kanan pada video dan pilih 'Save Video As'\n"
                "- Atau tekan Ctrl+S (Windows) / Command+S (Mac)\n\n"
                "Untuk SnapTik:\n"
                "- Tempel URL TikTok ke dalam kotak input SnapTik\n"
                "- Klik tombol download dan pilih 'No Watermark'"
            )
            
            tk.Label(main_frame, text=instructions, justify=tk.LEFT, wraplength=500).grid(row=4, column=0, columnspan=2, sticky=tk.W, pady=(20, 0))
            
            root.mainloop()
            return
        
        except Exception as e:
            # Jika semua metode gagal, tampilkan pesan error
            print(f"Error saat memulai aplikasi GUI: {e}")
            print("Membuka browser dengan URL TikTok...")
            url = input("Masukkan URL TikTok: ")
            if url:
                webbrowser.open(url)
                print("Browser dibuka. Klik kanan pada video dan pilih 'Save Video As'")
            sys.exit(1)

if __name__ == "__main__":
    main()