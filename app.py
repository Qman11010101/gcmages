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

    for index, music in enumerate(musics_data):
        title = music["title"]
        filename = music[game_data["image_key"]]
        image_url = game_data["image_base"]
        save_path = args.dir + f"/{game_name}"
        full_filepath_local = save_path + f"/{filename}"
        full_filepath_remote = image_url + filename
        dryrun_sign = "[Dry-Run] " if args.dry_run else ""
        download_message_prefix = f"{dryrun_sign}({index + 1} / {len(musics_data)}) "

        # ファイルの存在確認（ディレクトリごとない場合もある）
        is_target_exists = os.path.isfile(full_filepath_local)

        if is_target_exists:
            if args.overwrite:
                downloading_message_body = (
                    f"OVERWRITING '{title}' from {full_filepath_remote}"
                )
            else:
                downloading_message_body = (
                    f"SKIPPING '{title}' from {full_filepath_remote}"
                )
        else:
            downloading_message_body = f"Saving '{title}' from {full_filepath_remote}"
        print(download_message_prefix + downloading_message_body)

        if args.dry_run or is_target_exists:
            continue

        # 保存先ディレクトリがなければ作成
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
