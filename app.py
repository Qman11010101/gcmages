import os
import sys
import time
from argparse import Namespace
from io import BytesIO

import requests
import urllib3
from PIL import Image
from urllib3.exceptions import InsecureRequestWarning

from consts import GAMES_DATA

# InsecureRequestWarning を抑制
urllib3.disable_warnings(category=InsecureRequestWarning)


def _replace_ext(filename: str, new_ext: str) -> str:
    base, _ = os.path.splitext(filename)
    return f"{base}.{new_ext}"


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
        # 保存時の拡張子を引数のformatに置き換える
        filename_save = _replace_ext(filename, args.format)
        save_path = args.dir + f"/{game_name}"
        full_filepath_local = save_path + f"/{filename_save}"
        full_filepath_remote = game_data["image_base"] + filename
        is_target_exists = os.path.isfile(full_filepath_local)
        if not is_target_exists or args.overwrite:
            download_count += 1
            download_list.append(f"{title} ({filename_save}) from {full_filepath_remote}")
        else:
            skip_list.append(f"{title} ({filename_save}) from {full_filepath_remote}")

    print(f"[{game_name}] Download: {download_count} / {download_count + len(skip_list)}")
    if args.dry_run:
        for index, item in enumerate(download_list):
            print(f"[Dry-Run] ({index + 1} / {download_count}) {item}")
        return

    download_items = [(music, title, filename) for music in musics_data for title in [music["title"]] for filename in [music[game_data["image_key"]]] if any(f"{title} (" in item and music[game_data["image_key"]].split(".")[0] in item for item in download_list)]

    for index, (music, title, filename_orig) in enumerate(download_items):
        image_url = game_data["image_base"]
        save_path = args.dir + f"/{game_name}"
        filename_save = _replace_ext(filename_orig, args.format)
        full_filepath_local = save_path + f"/{filename_save}"
        full_filepath_remote = image_url + filename_orig
        remaining_count = download_count - index - 1
        remaining_time_seconds = remaining_count * args.interval
        minutes = int(remaining_time_seconds // 60)
        seconds = int(remaining_time_seconds % 60)
        time_str = f"{minutes:02d}m{seconds:02d}s"
        download_message_prefix = f"[{time_str}] ({index + 1} / {download_count}) "
        downloading_message_body = f"Saving '{title}' from {full_filepath_remote}" if not os.path.isfile(full_filepath_local) else f"OVERWRITING '{title}' from {full_filepath_remote}"
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

        # ダウンロード -> Pillowで指定フォーマットに変換して保存
        try:
            response = requests.get(full_filepath_remote, verify=False)
            response.raise_for_status()
            image_bytes = BytesIO(response.content)
            with Image.open(image_bytes) as im:
                im.load()
                params = {}
                fmt = args.format.lower()
                if fmt == "jpg":
                    fmt_save = "JPEG"
                    params = {"quality": 95, "optimize": True}
                elif fmt == "png":
                    fmt_save = "PNG"
                    params = {"optimize": True}
                else:  # webp
                    fmt_save = "WEBP"
                    params = {"quality": 90, "method": 6}
                # JPEG/WEBPでRGBAの場合は自動で変換（透過を白で埋めるなどはせず、Pillowに任せる）
                if fmt_save in ("JPEG", "WEBP") and im.mode in ("RGBA", "LA"):
                    background = Image.new("RGB", im.size, (255, 255, 255))
                    background.paste(im, mask=im.split()[-1])
                    im_to_save = background
                elif fmt_save == "JPEG" and im.mode != "RGB":
                    im_to_save = im.convert("RGB")
                else:
                    im_to_save = im
                im_to_save.save(full_filepath_local, format=fmt_save, **params)
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] Error downloading {filename_orig}: {e}", file=sys.stderr)
            continue
        except Exception as e:  # Pillow変換エラー
            print(f"[ERROR] Error converting {filename_orig} to {args.format}: {e}", file=sys.stderr)
            continue
        finally:
            time.sleep(args.interval)
