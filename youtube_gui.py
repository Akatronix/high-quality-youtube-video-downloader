# import os
# import threading
# import yt_dlp
# import tkinter as tk
# from tkinter import filedialog, ttk
# from PIL import Image, ImageTk
# import requests
# from io import BytesIO

# format_map = {
#     "1080p MP4": "bestvideo[height<=1080]+bestaudio/best",
#     "720p MP4": "bestvideo[height<=720]+bestaudio/best",
#     "480p MP4": "bestvideo[height<=480]+bestaudio/best",
#     "360p MP4": "bestvideo[height<=360]+bestaudio/best",
#     "Audio Only": "bestaudio",
#     "MP3 Audio": "bestaudio",
#     "best (Auto)": "best"
# }
# def clear_ui(self):
#     self.progress['value'] = 0
#     self.url_entry.delete(0, tk.END)
#     self.folder_var.set(self.default_folder)
#     self.info_label.config(text="")
#     self.thumbnail_label.config(image="", text="")
#     self.thumbnail_label.image = None

# class YouTubeDownloaderGUI:
#     def __init__(self, root):
#         self.default_folder = os.path.join(os.path.expanduser("~"), "Downloads")
#         self.root = root
#         self.root.title("YouTube Downloader")
#         self.root.resizable(False, False)

#         try:
#             image = Image.open("logo.jpg")
#             photo = ImageTk.PhotoImage(image)
#             root.iconphoto(False, photo)
#         except:
#             pass

#         tk.Label(root, text="YouTube URL:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
#         self.url_entry = tk.Entry(root, width=50)
#         self.url_entry.grid(row=0, column=1, padx=5, pady=5)

#         tk.Label(root, text="Format:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
#         self.format_var = tk.StringVar()
#         self.format_dropdown = ttk.Combobox(root, textvariable=self.format_var, width=47, state="readonly")
#         self.format_dropdown['values'] = list(format_map.keys())
#         self.format_dropdown.current(0)
#         self.format_dropdown.grid(row=1, column=1, padx=5, pady=5)

#         tk.Label(root, text="Save to Folder:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
#         self.folder_var = tk.StringVar(value=self.default_folder)
#         tk.Entry(root, textvariable=self.folder_var, width=50).grid(row=2, column=1, padx=5, pady=5)
#         tk.Button(root, text="Browse", command=self.browse_folder).grid(row=2, column=2, padx=5)

#         self.download_btn = tk.Button(root, text="Download", width=20, height=2, command=self.start_download)
#         self.download_btn.grid(row=3, column=1, pady=15)

#         self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
#         self.progress.grid(row=4, column=1, pady=10)

#         self.info_label = tk.Label(root, text="", wraplength=400, justify="center")
#         self.info_label.grid(row=5, column=1)

#         self.thumbnail_label = tk.Label(root)
#         self.thumbnail_label.grid(row=6, column=1, pady=10)

#     def browse_folder(self):
#         folder = filedialog.askdirectory()
#         if folder:
#             self.folder_var.set(folder)

#     def start_download(self):
#         self.clear_ui()
#         self.download_btn.config(state="disabled")
#         threading.Thread(target=self.download).start()





#     def download(self):
#         try:
#             url = self.url_entry.get().strip()
#             folder = self.folder_var.get().strip() or self.default_folder
#             selected_format = self.format_var.get()
#             format_code = format_map.get(selected_format, "best")

#             if not url:
#                 self.info_label.config(text="❌ Please enter a YouTube URL.")
#                 self.download_btn.config(state="normal")
#                 return

#             ydl_opts = {
#                 'format': format_code,
#                 'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
#                 'progress_hooks': [self.progress_hook],
#                 'quiet': True,
#                 'ignoreerrors': True,
#             }

#             if selected_format == "MP3 Audio":
#                 ydl_opts['postprocessors'] = [{
#                     'key': 'FFmpegExtractAudio',
#                     'preferredcodec': 'mp3',
#                     'preferredquality': '192',
#                 }]
#                 ydl_opts['outtmpl'] = os.path.join(folder, '%(title)s.%(ext)s')
#             else:
#                 ydl_opts['merge_output_format'] = 'mp4'

#             with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                 info = ydl.extract_info(url, download=False)
#                 self.show_thumbnail(info.get("thumbnail"))
#                 self.info_label.config(text=f"🎬 Title: {info.get('title')}\n⏱ Duration: {info.get('duration')}s")
#                 ydl.download([url])

#             self.info_label.config(text="✅ Download Complete!")
#             clear_ui()
#         except Exception as e:
#             self.info_label.config(text=f"❌ Error: {e}")
#         finally:
#             self.download_btn.config(state="normal")

#     def clear_ui(self):
#         self.progress['value'] = 0
#         self.info_label.config(text="")
#         self.thumbnail_label.config(image="", text="")
#         self.thumbnail_label.image = None

#     def show_thumbnail(self, url):
#         try:
#             response = requests.get(url)
#             img_data = Image.open(BytesIO(response.content)).resize((320, 180))
#             img = ImageTk.PhotoImage(img_data)
#             self.thumbnail_label.config(image=img, text="")
#             self.thumbnail_label.image = img
#         except:
#             self.thumbnail_label.config(text="No Thumbnail")

#     def progress_hook(self, d):
#         if d['status'] == 'downloading':
#             total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
#             downloaded = d.get('downloaded_bytes', 0)
#             percent = int(downloaded / total_bytes * 100) if total_bytes else 0
#             self.progress['value'] = percent
#             self.info_label.config(
#                 text=f"⬇️ Downloading: {percent}% — {round(downloaded / 1_000_000, 2)}MB of {round(total_bytes / 1_000_000, 2)}MB"
#             )


# if __name__ == "__main__":
#     root = tk.Tk()
#     app = YouTubeDownloaderGUI(root)
#     root.mainloop()



import os
import threading
import yt_dlp
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO

# Format map to convert user-friendly labels to yt-dlp format strings
format_map = {
    "1080p MP4": "bestvideo[height<=1080]+bestaudio/best",
    "720p MP4": "bestvideo[height<=720]+bestaudio/best",
    "480p MP4": "bestvideo[height<=480]+bestaudio/best",
    "360p MP4": "bestvideo[height<=360]+bestaudio/best",
    "Audio Only": "bestaudio",
    "MP3 Audio": "bestaudio",
    "best (Auto)": "best"
}

class YouTubeDownloaderGUI:
    def __init__(self, root):
        self.default_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        self.root = root
        self.root.title("YouTube Downloader")
        self.root.resizable(False, False)

        # Set favicon (optional)
        try:
            image = Image.open("logo.jpg")
            photo = ImageTk.PhotoImage(image)
            root.iconphoto(False, photo)
        except:
            pass

        # YouTube URL input
        tk.Label(root, text="YouTube URL:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.url_entry = tk.Entry(root, width=50)
        self.url_entry.grid(row=0, column=1, padx=5, pady=5)

        # Format dropdown
        tk.Label(root, text="Format:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.format_var = tk.StringVar()
        self.format_dropdown = ttk.Combobox(root, textvariable=self.format_var, width=47, state="readonly")
        self.format_dropdown['values'] = list(format_map.keys())
        self.format_dropdown.current(0)
        self.format_dropdown.grid(row=1, column=1, padx=5, pady=5)

        # Folder select
        tk.Label(root, text="Save to Folder:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.folder_var = tk.StringVar(value=self.default_folder)
        tk.Entry(root, textvariable=self.folder_var, width=50).grid(row=2, column=1, padx=5, pady=5)
        tk.Button(root, text="Browse", command=self.browse_folder).grid(row=2, column=2, padx=5)

        # Download button
        self.download_btn = tk.Button(root, text="Download", width=20, height=2, command=self.start_download)
        self.download_btn.grid(row=3, column=1, pady=15)

        # Progress bar
        self.progress = ttk.Progressbar(root, orient="horizontal", length=400, mode="determinate")
        self.progress.grid(row=4, column=1, pady=10)

        # Info label
        self.info_label = tk.Label(root, text="", wraplength=400, justify="center")
        self.info_label.grid(row=5, column=1)

        # Thumbnail display
        self.thumbnail_label = tk.Label(root)
        self.thumbnail_label.grid(row=6, column=1, pady=10)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_var.set(folder)

    def start_download(self):
        self.download_btn.config(state="disabled")
        threading.Thread(target=self.download).start()

    def download(self):
        try:
            url = self.url_entry.get().strip()
            folder = self.folder_var.get().strip() or self.default_folder
            format_label = self.format_var.get()
            format_code = format_map.get(format_label, "best")

            if not url:
                self.info_label.config(text="❌ Please enter a YouTube URL.")
                self.download_btn.config(state="normal")
                return

            ydl_opts = {
                'format': format_code,
                'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
                'progress_hooks': [self.progress_hook],
                'quiet': True,
            }

            if format_label == "MP3 Audio":
                ydl_opts['postprocessors'] = [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }]
                ydl_opts['outtmpl'] = os.path.join(folder, '%(title)s.%(ext)s')
            else:
                ydl_opts['merge_output_format'] = 'mp4'

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                self.show_thumbnail(info.get("thumbnail"))
                self.info_label.config(text=f"Title: {info.get('title')}\nDuration: {info.get('duration')}s")
                ydl.download([url])

            self.info_label.config(text="✅ Download Complete!")
            self.clear_ui()

        except Exception as e:
            self.info_label.config(text=f"❌ Error: {e}")
        finally:
            self.download_btn.config(state="normal")

    def show_thumbnail(self, url):
        try:
            response = requests.get(url)
            img_data = Image.open(BytesIO(response.content)).resize((320, 180))
            img = ImageTk.PhotoImage(img_data)
            self.thumbnail_label.config(image=img, text="")
            self.thumbnail_label.image = img
        except:
            self.thumbnail_label.config(image="", text="No Thumbnail")
            self.thumbnail_label.image = None

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            total_bytes = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            downloaded = d.get('downloaded_bytes', 0)
            percent = int(downloaded / total_bytes * 100) if total_bytes else 0
            self.progress['value'] = percent
            self.info_label.config(
                text=f"Downloading: {percent}% - {round(downloaded / 1_000_000, 2)}MB of {round(total_bytes / 1_000_000, 2)}MB"
            )

    def clear_ui(self):
        self.progress['value'] = 0
        self.url_entry.delete(0, tk.END)
        self.info_label.config(text=" Download Complete!")
        self.thumbnail_label.config(image="", text="")
        self.thumbnail_label.image = None


# Launch GUI
if __name__ == "__main__":
    root = tk.Tk()
    app = YouTubeDownloaderGUI(root)
    root.mainloop()
