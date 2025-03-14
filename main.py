import os
import sys
import subprocess

# Активация виртуального окружения (если не запущено)
venv_path = os.path.join(os.path.dirname(__file__), "venv", "Scripts" if os.name == "nt" else "bin", "activate")
if not getattr(sys, "base_prefix", sys.prefix) == sys.prefix and os.path.exists(venv_path):
    os.system(f'"{venv_path}"')

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

def download_audio(video_url, audio_format="flac", output_folder="downloads"):
    """Скачивает аудио с YouTube и конвертирует его в указанный формат."""
    os.makedirs(output_folder, exist_ok=True)

    yt_dlp_path = os.path.abspath("yt-dlp.exe" if os.name == "nt" else "yt-dlp")
    if not os.path.exists(yt_dlp_path):
        raise FileNotFoundError("yt-dlp не найден. Убедитесь, что он в папке со скриптом.")

    output_template = os.path.join(output_folder, "%(title)s.%(ext)s")

    command = [
        yt_dlp_path,
        "-f", "bestaudio",
        "--extract-audio",
        "--audio-format", audio_format,
        "-o", output_template,
        video_url
    ]

    subprocess.run(command)

if __name__ == "__main__":
    language = choose_option(["ru", "en"], "Выберите язык / Choose language:")
    
    texts = {
        "ru": {
            "enter_url": "Введите URL видео:",
            "choose_format": "Выберите формат аудио:",
            "chosen_format": "## Выбранный формат:",
            "success": "## Аудио успешно скачано в формате",
            "error": "## Ошибка"
        },
        "en": {
            "enter_url": "Enter video URL:",
            "choose_format": "Select audio format:",
            "chosen_format": "## Selected format:",
            "success": "## Audio successfully downloaded in",
            "error": "## Error"
        }
    }

    video_url = input(f"\n{texts[language]['enter_url']} ")
    audio_format = choose_option(["mp3", "wav", "flac"], texts[language]["choose_format"])
    
    print(f"\n{texts[language]['chosen_format']} {audio_format.upper()}\n")

    try:
        download_audio(video_url, audio_format)
        print(f"{texts[language]['success']} {audio_format}!")
    except Exception as e:
        print(f"{texts[language]['error']}: {e}")
