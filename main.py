import os
import threading
import yt_dlp
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image
import requests
from io import BytesIO


format_map = {
    "1080p MP4": "bestvideo[height<=1080]+bestaudio/best",
    "720p MP4": "bestvideo[height<=720]+bestaudio/best",
    "480p MP4": "bestvideo[height<=480]+bestaudio/best",
    "360p MP4": "bestvideo[height<=360]+bestaudio/best",
    "Audio Only": "bestaudio",
    "MP3 Audio": "bestaudio",
    "best (Auto)": "best"
}


class SplashScreen(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.overrideredirect(True)
        self.configure(bg="black")

        width, height = 700, 400
        self.update_idletasks()
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2 + 120
        y = (screen_height - height) // 2
        self.geometry(f"{width}x{height}+{x}+{y}")

        container = ctk.CTkFrame(self, fg_color="transparent")
        container.pack(expand=True)

        try:
            logo = Image.open("logo.jpg").resize((100, 100))
            self.logo_img = ctk.CTkImage(light_image=logo, size=(100, 100))
            logo_label = ctk.CTkLabel(container, image=self.logo_img, text="")
            logo_label.pack(pady=(30, 10))
        except Exception as e:
            print(f"Logo load failed: {e}")

        ctk.CTkLabel(container, text="HQ-YouTube Downloader", font=ctk.CTkFont(size=18, weight="bold")).pack()
        ctk.CTkLabel(container, text="by Zyrex Robotics", font=ctk.CTkFont(size=14)).pack()

        self.after(3000, self.destroy)


class YouTubeDownloaderApp(ctk.CTk):
    def __init__(self):
        self.default_folder = os.path.join(os.path.expanduser("~"), "Downloads")
        super().__init__()
        self.title("ZyrexRobotics - HQ-YouTube Downloader")
        self.geometry("680x530")
        self.resizable(False, False)
        ctk.set_appearance_mode("System")
        self.iconbitmap("logo.ico")

        ctk.CTkLabel(self, text="YouTube URL:").grid(row=0, column=0, padx=(20, 5), pady=10, sticky="e")
        self.url_entry = ctk.CTkEntry(self, width=400)
        self.url_entry.grid(row=0, column=1, columnspan=2, padx=(0, 20), pady=10, sticky="w")

        ctk.CTkLabel(self, text="Format:").grid(row=1, column=0, padx=(20, 5), pady=10, sticky="e")
        self.format_option = ctk.CTkComboBox(self, values=list(format_map.keys()))
        self.format_option.set("720p MP4")
        self.format_option.grid(row=1, column=1, columnspan=2, padx=(0, 20), pady=10, sticky="w")

        ctk.CTkLabel(self, text="Save Folder:").grid(row=2, column=0, padx=(20, 5), pady=10, sticky="e")
        self.folder_path = ctk.CTkEntry(self, width=400)
        self.folder_path.grid(row=2, column=1, padx=(0, 10), pady=10, sticky="w")
        ctk.CTkButton(self, text="Browse", command=self.browse_folder).grid(row=2, column=2, padx=(0, 20), pady=10, sticky="w")

        self.download_btn = ctk.CTkButton(self, text="Download", command=self.start_download, height=50, width=200, font=ctk.CTkFont(size=16, weight="bold"))
        self.download_btn.grid(row=3, column=1, pady=20)

        self.progress = ctk.CTkProgressBar(self, width=400)
        self.progress.grid(row=4, column=1)
        self.progress.set(0)

        self.video_info_label = ctk.CTkLabel(self, text="", justify="left")
        self.video_info_label.grid(row=5, column=1, pady=5, sticky="w")

        self.progress_label = ctk.CTkLabel(self, text="", justify="left")
        self.progress_label.grid(row=6, column=1, pady=2, sticky="w")

        self.thumbnail_label = ctk.CTkLabel(self, text="")
        self.thumbnail_label.grid(row=7, column=1, pady=10)

    def browse_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_path.delete(0, "end")
            self.folder_path.insert(0, folder)

    def start_download(self):
        self.download_btn.configure(state="disabled")
        threading.Thread(target=self.download).start()

    def download(self):
        try:
            url = self.url_entry.get()
            folder = self.folder_path.get()
            folder = self.folder_path.get().strip() or self.default_folder
            selected_format = self.format_option.get()
            format_code = format_map.get(selected_format, "best")

            ydl_opts = {
                'format': format_code,
                'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
                'merge_output_format': 'mp4',
                'progress_hooks': [self.progress_hook],
                'quiet': True,
                'ignoreerrors': True,
                'noplaylist': False,
            }

            # Special handling for MP3 extraction
            if selected_format == "MP3 Audio":
                ydl_opts.update({
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                    'outtmpl': os.path.join(folder, '%(title)s.%(ext)s'),
                })

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                entries = info.get("entries")
                if entries:
                    for entry in entries:
                        if not entry:
                            continue
                        self.display_info(entry)
                        ydl.download([entry["webpage_url"]])
                else:
                    self.display_info(info)
                    ydl.download([url])

            self.progress_label.configure(text="✅ Download complete!")

            # 🔁 Reset GUI
            self.url_entry.delete(0, "end")
            self.video_info_label.configure(text="")
            self.thumbnail_label.configure(image=None, text="")
            self.thumbnail_label.image = None
            self.progress.set(0)
        except Exception as e:
            self.progress_label.configure(text=f"❌ Error: {e}")
        finally:
            self.download_btn.configure(state="normal")

    def display_info(self, info):
        title = info.get('title', 'N/A')
        duration = info.get('duration', 'N/A')
        thumbnail_url = info.get('thumbnail')
        self.video_info_label.configure(text=f"🎬 Title: {title}\n⏱ Duration: {duration}s")
        self.progress_label.configure(text="")
        self.show_thumbnail(thumbnail_url)

    def show_thumbnail(self, url):
        try:
            response = requests.get(url)
            img_data = Image.open(BytesIO(response.content)).resize((320, 180))
            ctk_img = ctk.CTkImage(light_image=img_data, size=(320, 180))
            self.thumbnail_label.configure(image=ctk_img, text="")
            self.thumbnail_label.image = ctk_img
        except:
            self.thumbnail_label.configure(text="No Thumbnail")

    def progress_hook(self, d):
        if d['status'] == 'downloading':
            total = d.get("total_bytes") or d.get("total_bytes_estimate", 0)
            downloaded = d.get("downloaded_bytes", 0)
            percent = downloaded / total if total else 0
            self.progress.set(percent)
            self.progress_label.configure(
                text=f"⬇️ Downloading: {int(percent * 100)}% ({round(downloaded / 1_000_000, 2)}MB / {round(total / 1_000_000, 2)}MB)"
            )


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    app = YouTubeDownloaderApp()
    splash = SplashScreen(app)
    app.wait_window(splash)
    app.mainloop()
