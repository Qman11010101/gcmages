import os
import sys
import time
from argparse import Namespace
from io import BytesIO

import requests

from consts import GAMES_DATA


def download(game_name: str, args: Namespace):
    game_data = GAMES_DATA[game_name]
    try:
        musics_data = requests.get(game_data["music_data"]).json()
    except requests.exceptions.RequestException as e:
        print(f"Error downloading music data: {e}")
        return

    download_count = 0
    download_list: list[str] = []
    skip_list: list[str] = []
    for music in musics_data:
        title = music["title"]
        filename = music[game_data["image_key"]]
        save_path = args.dir + f"/{game_name}"
        full_filepath_local = save_path + f"/{filename}"
        full_filepath_remote = game_data["image_base"] + filename
        is_target_exists = os.path.isfile(full_filepath_local)
        if not is_target_exists or args.overwrite:
            download_count += 1
            download_list.append(f"{title} ({filename}) from {full_filepath_remote}")
        else:
            skip_list.append(f"{title} ({filename}) from {full_filepath_remote}")

    print(
        f"[{game_name}] Download: {download_count} / {download_count + len(skip_list)}"
    )
    if args.dry_run:
        for index, item in enumerate(download_list):
            print(f"[Dry-Run] ({index + 1} / {download_count}) {item}")
        return

    download_items = [
        (music, title, filename)
        for music in musics_data
        for title in [music["title"]]
        for filename in [music[game_data["image_key"]]]
        if any(f"{title} ({filename})" in item for item in download_list)
    ]

    for index, (music, title, filename) in enumerate(download_items):
        image_url = game_data["image_base"]
        save_path = args.dir + f"/{game_name}"
        full_filepath_local = save_path + f"/{filename}"
        full_filepath_remote = image_url + filename
        remaining_count = download_count - index - 1
        remaining_time_seconds = remaining_count * args.interval
        minutes = int(remaining_time_seconds // 60)
        seconds = int(remaining_time_seconds % 60)
        time_str = f"{minutes:02d}m{seconds:02d}s"
        download_message_prefix = f"[{time_str}] ({index + 1} / {download_count}) "
        downloading_message_body = (
            f"Saving '{title}' from {full_filepath_remote}"
            if not os.path.isfile(full_filepath_local)
            else f"OVERWRITING '{title}' from {full_filepath_remote}"
        )
        full_message = download_message_prefix + downloading_message_body
        try:
            terminal_width = os.get_terminal_size().columns
            display_width = sum(2 if ord(c) > 127 else 1 for c in full_message)
            if display_width > terminal_width:
                current_width = 0
                truncated = ""
                for c in full_message:
                    char_width = 2 if ord(c) > 127 else 1
                    if current_width + char_width > terminal_width - 3:
                        break
                    truncated += c
                    current_width += char_width
                full_message = truncated + "..."
            else:
                padding_width = terminal_width - display_width
                full_message = full_message + " " * padding_width
        except OSError:
            pass
        print(f"\r{full_message}", end="")

        if args.dry_run:
            continue

        os.makedirs(save_path, exist_ok=True)

        # ダウンロード
        try:
            response = requests.get(full_filepath_remote)
            response.raise_for_status()
            image = BytesIO(response.content)
            with open(full_filepath_local, "wb") as f:
                f.write(image.read())
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Error downloading {filename}: {e}", file=sys.stderr)
            continue
        finally:
            time.sleep(args.interval)
