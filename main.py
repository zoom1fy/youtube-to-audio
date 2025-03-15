import os
import sys
import subprocess

# Активация виртуального окружения (если не запущено)
venv_path = os.path.join(os.path.dirname(__file__), "venv", "Scripts" if os.name == "nt" else "bin", "activate")
if not getattr(sys, "base_prefix", sys.prefix) == sys.prefix and os.path.exists(venv_path):
    subprocess.run([venv_path], shell=True, check=True)

try:
    import readchar  # Локальная зависимость
except ImportError:
    print("Устанавливаю зависимости...")
    subprocess.run([sys.executable, "-m", "pip", "install", "readchar", "yt-dlp"], check=True)
    import readchar  # Повторный импорт

def choose_option(options, title):
    """Меню выбора опции (язык, формат) с управлением стрелками."""
    index = 0
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print(f"{title}\n")
        for i, option in enumerate(options):
            print(f"{'>' if i == index else ' '} {option}")

        key = readchar.readkey()
        if key == readchar.key.UP and index > 0:
            index -= 1
        elif key == readchar.key.DOWN and index < len(options) - 1:
            index += 1
        elif key == readchar.key.ENTER:
            return options[index]

def download_media(video_url, format_choice="mp3", output_folder="downloads"):
    """Скачивает аудио или видео с YouTube в указанном формате."""
    os.makedirs(output_folder, exist_ok=True)

    yt_dlp_path = os.path.abspath("yt-dlp.exe" if os.name == "nt" else "yt-dlp")
    if not os.path.exists(yt_dlp_path):
        raise FileNotFoundError("yt-dlp не найден. Убедитесь, что он в папке со скриптом.")

    output_template = os.path.join(output_folder, "%(title)s.%(ext)s")

    if format_choice == "mp4":
        command = [yt_dlp_path, "-f", "bestvideo+bestaudio", "-o", output_template, video_url]
    else:
        command = [
            yt_dlp_path,
            "-f", "bestaudio",
            "--extract-audio",
            "--audio-format", format_choice,
            "-o", output_template,
            video_url
        ]

    subprocess.run(command)

if __name__ == "__main__":
    language = choose_option(["ru", "en"], "Выберите язык / Choose language:")
    
    texts = {
        "ru": {
            "enter_url": "Введите URL видео:",
            "choose_format": "Выберите формат (аудио/видео):",
            "chosen_format": "## Выбранный формат:",
            "success": "## Файл успешно скачан в формате",
            "error": "## Ошибка"
        },
        "en": {
            "enter_url": "Enter video URL:",
            "choose_format": "Select format (audio/video):",
            "chosen_format": "## Selected format:",
            "success": "## File successfully downloaded in",
            "error": "## Error"
        }
    }

    video_url = input(f"\n{texts[language]['enter_url']} ")
    format_choice = choose_option(["mp3", "wav", "flac", "mp4"], texts[language]["choose_format"])
    
    print(f"\n{texts[language]['chosen_format']} {format_choice.upper()}\n")

    try:
        download_media(video_url, format_choice)
        print(f"{texts[language]['success']} {format_choice}!")
    except Exception as e:
        print(f"{texts[language]['error']}: {e}")
