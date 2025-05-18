import os
from argparse import Namespace

import requests

from consts import GAMES_DATA


def download(game_name: str, args: Namespace):
    game_data = GAMES_DATA[game_name]
    musics_data = requests.get(game_data["music_data"]).json()

    for index, music in enumerate(musics_data):
        title = music["title"]
        filename = music[game_data["image_key"]]
        image_url = game_data["image_base"]
        save_path = args.dir + f"/{game_name}"
        full_filepath = save_path + f"/{filename}"
        dryrun_sign = "[Dry-Run] " if args.dry_run else ""
        print(
            f"{dryrun_sign}({index + 1} / {len(musics_data)}) Saving '{title}' to '{full_filepath}' from {image_url + filename}"
        )

        if args.dry_run:
            continue

        # 保存先ディレクトリがなければ作成
        os.makedirs(save_path, exist_ok=True)
