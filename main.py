import os
import sys
import subprocess
import threading
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
from pathlib import Path

class YouTubeDownloader:
    def __init__(self):
        self.setup_environment()

    def setup_environment(self):
        """Установка и проверка окружения (попытка установить yt-dlp, если отсутствует)"""
        try:
            import yt_dlp  # noqa: F401
        except ImportError:
            print("Установка зависимостей...")
            try:
                subprocess.run(
                    [sys.executable, "-m", "pip", "install", "yt-dlp"],
                    check=True,
                    capture_output=True,
                )
                print("Зависимости успешно установлены")
            except subprocess.CalledProcessError as e:
                print(f"Ошибка установки зависимостей: {e}")
                sys.exit(1)

    def download_media(self, video_url, format_choice="mp3", output_folder="downloads", progress_callback=None):
        """Скачивание медиа с прогрессом"""
        try:
            import yt_dlp
        except ImportError:
            raise ImportError("yt-dlp не установлен")

        Path(output_folder).mkdir(exist_ok=True)

        ydl_opts = {
            "outtmpl": os.path.join(output_folder, "%(title)s.%(ext)s"),
            "progress_hooks": [progress_callback] if progress_callback else [],
        }

        if format_choice == "mp4":
            ydl_opts["format"] = "bestvideo[height<=1080]+bestaudio/best[height<=1080]"
        else:
            ydl_opts.update(
                {
                    "format": "bestaudio/best",
                    "postprocessors": [
                        {
                            "key": "FFmpegExtractAudio",
                            "preferredcodec": format_choice,
                            "preferredquality": "192" if format_choice == "mp3" else "0",
                        }
                    ],
                }
            )

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([video_url])
            return True, "Success"
        except Exception as e:
            return False, str(e)


class ModernYouTubeDownloaderApp:
    def __init__(self, root):
        self.root = root
        self.downloader = YouTubeDownloader()

        # мультиязычные тексты
        self.language = "ru"
        self.texts = {
            "ru": {
                "title": "YouTube Media Downloader",
                "url_label": "Ссылка на видео:",
                "format_label": "Формат файла",
                "folder_label": "Папка для сохранения:",
                "download_btn": "Скачать",
                "browse_btn": "Обзор",
                "language_label": "Язык / Language:",
                "success": "Успех",
                "error": "Ошибка",
                "success_msg": "Файл успешно скачан!",
                "empty_url": "Введите ссылку на видео",
                "preparing": "Подготовка к загрузке...",
                "processing": "Обработка файла...",
                "downloading": "Загрузка: {}",
                "formats": [
                    ("MP3 (Аудио)", "mp3"),
                    ("WAV (Аудио)", "wav"),
                    ("FLAC (Аудио)", "flac"),
                    ("MP4 (Видео 1080p)", "mp4"),
                ],
            },
            "en": {
                "title": "YouTube Media Downloader",
                "url_label": "Video URL:",
                "format_label": "File Format",
                "folder_label": "Save to folder:",
                "download_btn": "Download",
                "browse_btn": "Browse",
                "language_label": "Language / Язык:",
                "success": "Success",
                "error": "Error",
                "success_msg": "File downloaded successfully!",
                "empty_url": "Please enter video URL",
                "preparing": "Preparing to download...",
                "processing": "Processing file...",
                "downloading": "Downloading: {}",
                "formats": [
                    ("MP3 (Audio)", "mp3"),
                    ("WAV (Audio)", "wav"),
                    ("FLAC (Audio)", "flac"),
                    ("MP4 (Video 1080p)", "mp4"),
                ],
            },
        }

        self.setup_window()
        self.setup_styles()
        self.setup_ui()

    def setup_window(self):
        """Настройка главного окна"""
        self.root.title(self.texts[self.language]["title"])
        self.root.geometry("550x600")
        self.root.minsize(500, 450)
        self.root.configure(bg="#f5f5f5")

        # Центрирование окна
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() - self.root.winfo_reqwidth()) // 2
        y = (self.root.winfo_screenheight() - self.root.winfo_reqheight()) // 2
        self.root.geometry(f"+{x}+{y}")

    def setup_styles(self):
        """Настройка стилей"""
        self.style = ttk.Style()
        try:
            self.style.theme_use("clam")
        except Exception:
            pass

        if sys.platform == "win32":
            default_font = "Segoe UI"
        elif sys.platform == "darwin":
            default_font = "SF Pro"
        else:
            default_font = "DejaVu Sans"

        self.colors = {
            "primary": "#2E86AB",
            "secondary": "#A23B72",
            "success": "#28a745",
            "warning": "#ffc107",
            "danger": "#dc3545",
            "light": "#f8f9fa",
            "dark": "#343a40",
            "background": "#f5f5f5",
        }

        self.style.configure("TFrame", background=self.colors["background"])
        self.style.configure("TLabel", background=self.colors["background"], font=(default_font, 10))
        self.style.configure("Title.TLabel", font=(default_font, 14, "bold"), foreground=self.colors["primary"])
        self.style.configure("TButton", font=(default_font, 10))
        self.style.configure("Accent.TButton", background=self.colors["primary"], foreground="white")
        self.style.configure("Secondary.TButton", background=self.colors["secondary"], foreground="white")
        self.style.configure("TRadiobutton", background=self.colors["background"], font=(default_font, 9))
        self.style.configure("TEntry", font=(default_font, 10))

    # ---------------- paste utilities ----------------
    def _paste_clipboard(self, widget):
        try:
            txt = widget.clipboard_get()
            widget.insert(tk.INSERT, txt)
        except tk.TclError:
            pass

    def _bind_paste(self, widget):
        """
        Универсальная привязка для вставки:
        - ловим <Control-Key> и внутри проверяем keysym/char для 'v' или 'в'
        - поддерживаем Shift-Insert, Ctrl-Insert
        - добавляем контекстное меню (правый клик) с пунктом Вставить
        """
        def on_control_key(event):
            ks = (event.keysym or "").lower()
            ch = (event.char or "").lower()

            # если похожая на V/В клавиша — вставляем
            if ks == "v" or ks == "в" or ch == "v" or ch == "в":
                try:
                    txt = widget.clipboard_get()
                    widget.insert(tk.INSERT, txt)
                except tk.TclError:
                    pass
                return "break"  # остановить дальнейшую обработку

            # иначе — не обрабатываем здесь
            return None

        widget.bind("<Control-Key>", on_control_key)       # ловит Ctrl + любая клавиша
        widget.bind("<Control-v>", lambda e: self._paste_clipboard(widget))
        widget.bind("<Control-V>", lambda e: self._paste_clipboard(widget))
        widget.bind("<Shift-Insert>", lambda e: self._paste_clipboard(widget))
        widget.bind("<Control-Insert>", lambda e: self._paste_clipboard(widget))

        # macOS: иногда Command (Meta) используется
        try:
            widget.bind("<Command-Key-v>", lambda e: self._paste_clipboard(widget))
            widget.bind("<Command-v>", lambda e: self._paste_clipboard(widget))
        except Exception:
            # если KeySym не поддерживается — просто игнорируем
            pass

        # контекстное меню (правый клик)
        menu = tk.Menu(widget, tearoff=0)
        menu.add_command(label="Вставить", command=lambda: self._paste_clipboard(widget))

        def show_context_menu(event):
            try:
                menu.tk_popup(event.x_root, event.y_root)
            finally:
                menu.grab_release()
            return "break"

        widget.bind("<Button-3>", show_context_menu)  # Windows/Linux правый клик
        widget.bind("<Button-2>", show_context_menu)  # macOS/альтернативы

    # -------------------------------------------------

    def setup_ui(self):
        """Создание интерфейса"""
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        title_label = ttk.Label(main_frame, text=self.texts[self.language]["title"], style="Title.TLabel")
        title_label.pack(pady=(0, 15))

        # язык
        language_frame = ttk.Frame(main_frame)
        language_frame.pack(fill=tk.X, pady=5)
        ttk.Label(language_frame, text=self.texts[self.language]["language_label"]).pack(anchor=tk.W)

        lang_btn_frame = ttk.Frame(language_frame)
        lang_btn_frame.pack(fill=tk.X, pady=(5, 0))

        ttk.Button(
            lang_btn_frame,
            text="Русский",
            command=lambda: self.change_language("ru"),
            style="Secondary.TButton" if self.language == "ru" else "TButton",
        ).pack(side=tk.LEFT, padx=(0, 5))

        ttk.Button(
            lang_btn_frame,
            text="English",
            command=lambda: self.change_language("en"),
            style="Secondary.TButton" if self.language == "en" else "TButton",
        ).pack(side=tk.LEFT)

        # URL
        url_frame = ttk.Frame(main_frame)
        url_frame.pack(fill=tk.X, pady=10)

        ttk.Label(url_frame, text=self.texts[self.language]["url_label"]).pack(anchor=tk.W)
        self.url_entry = ttk.Entry(url_frame)
        self.url_entry.pack(fill=tk.X, pady=(5, 0), ipady=4)
        self.url_entry.bind("<Return>", lambda e: self.start_download())

        # Форматы
        format_frame = ttk.LabelFrame(main_frame, text=self.texts[self.language]["format_label"], padding=10)
        format_frame.pack(fill=tk.X, pady=10)

        self.format_var = tk.StringVar(value="mp3")
        for text, value in self.texts[self.language]["formats"]:
            ttk.Radiobutton(format_frame, text=text, value=value, variable=self.format_var).pack(anchor=tk.W, pady=2)

        # Папка
        folder_frame = ttk.Frame(main_frame)
        folder_frame.pack(fill=tk.X, pady=10)

        ttk.Label(folder_frame, text=self.texts[self.language]["folder_label"]).pack(anchor=tk.W)

        folder_input_frame = ttk.Frame(folder_frame)
        folder_input_frame.pack(fill=tk.X, pady=(5, 0))

        self.folder_var = tk.StringVar(value="downloads")
        folder_entry = ttk.Entry(folder_input_frame, textvariable=self.folder_var)
        folder_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4, padx=(0, 5))

        ttk.Button(folder_input_frame, text=self.texts[self.language]["browse_btn"], command=self.browse_folder, style="TButton").pack(side=tk.RIGHT)

        # применяем универсальную привязку вставки к полям
        self._bind_paste(self.url_entry)
        self._bind_paste(folder_entry)

        # Прогресс
        self.progress_frame = ttk.Frame(main_frame)
        self.progress_frame.pack(fill=tk.X, pady=15)

        self.progress = ttk.Progressbar(self.progress_frame, mode="indeterminate")
        self.status_label = ttk.Label(self.progress_frame, text="")

        # Кнопка загрузки
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        self.download_btn = ttk.Button(button_frame, text=self.texts[self.language]["download_btn"], command=self.start_download, style="Accent.TButton")
        self.download_btn.pack(ipady=10, ipadx=30, pady=10)

    def browse_folder(self):
        folder = filedialog.askdirectory(title=self.texts[self.language]["folder_label"])
        if folder:
            self.folder_var.set(folder)

    def change_language(self, lang):
        self.language = lang
        self.update_ui_texts()

    def update_ui_texts(self):
        # пересоздаём UI с новым языком
        for widget in self.root.winfo_children():
            widget.destroy()
        self.setup_ui()

    def start_download(self):
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror(self.texts[self.language]["error"], self.texts[self.language]["empty_url"])
            return

        self.progress.pack(fill=tk.X, pady=(0, 5))
        self.status_label.pack()
        self.progress.start(10)
        self.status_label.config(text=self.texts[self.language]["preparing"])
        self.download_btn.config(state="disabled")

        thread = threading.Thread(target=self.download_thread, args=(url,))
        thread.daemon = True
        thread.start()

    def download_thread(self, url):
        def progress_hook(d):
            if d.get("status") == "downloading":
                percent = d.get("_percent_str", "0%")
                self.root.after(0, lambda: self.status_label.config(text=self.texts[self.language]["downloading"].format(percent)))
            elif d.get("status") == "finished":
                self.root.after(0, lambda: self.status_label.config(text=self.texts[self.language]["processing"]))

        try:
            success, message = self.downloader.download_media(url, self.format_var.get(), self.folder_var.get(), progress_hook)
            self.root.after(0, self.download_finished, success, message)
        except Exception as e:
            self.root.after(0, self.download_finished, False, str(e))

    def download_finished(self, success, message):
        self.progress.stop()
        self.progress.pack_forget()
        self.status_label.pack_forget()
        self.download_btn.config(state="normal")

        if success:
            messagebox.showinfo(self.texts[self.language]["success"], self.texts[self.language]["success_msg"])
            self.url_entry.delete(0, tk.END)
        else:
            messagebox.showerror(self.texts[self.language]["error"], f"{self.texts[self.language]['error']}:\n{message}")


def main():
    try:
        root = tk.Tk()
        app = ModernYouTubeDownloaderApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Ошибка запуска приложения: {e}")
        input("Нажмите Enter для выхода...")


if __name__ == "__main__":
    main()
