#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
TikTok Downloader No Watermark
Aplikasi untuk mengunduh video TikTok tanpa watermark
"""

import argparse
import sys
import tkinter as tk
from tiktok_downloader import TikTokDownloader
from tiktok_downloader_gui import TikTokDownloaderApp

def main():
    # Parse argumen command line
    parser = argparse.ArgumentParser(description='TikTok Downloader No Watermark')
    parser.add_argument('--cli', action='store_true', help='Jalankan dalam mode CLI (Command Line Interface)')
    parser.add_argument('--url', help='URL video TikTok (diperlukan dalam mode CLI)')
    parser.add_argument('--output', help='Nama file output (opsional, hanya untuk mode CLI)')
    
    args = parser.parse_args()
    
    # Jika mode CLI
    if args.cli:
        if not args.url:
            print("Error: URL diperlukan dalam mode CLI")
            parser.print_help()
            sys.exit(1)
        
        # Jalankan downloader
        downloader = TikTokDownloader()
        success = downloader.download_video(args.url, args.output)
        
        if success:
            sys.exit(0)
        else:
            sys.exit(1)
    
    # Jika mode GUI (default)
    else:
        root = tk.Tk()
        app = TikTokDownloaderApp(root)
        root.mainloop()

if __name__ == "__main__":
    main()