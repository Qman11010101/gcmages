import argparse
from typing import Literal

import requests

from consts import GAMES, GAMES_DATA, JACKET_PATH_DEFAULT

ImageFormat = Literal["png", "jpg", "webp"]


def parse_args():
    parser = argparse.ArgumentParser(
        description="A tool to download jacket images from three SEGA rhythm games"
    )
    parser.add_argument(
        "game",
        nargs="?",  # optional
        choices=GAMES + ["all"],
        help="Target game to download (all: download for all games)",
        default="all",
    )
    parser.add_argument(
        "--dir",
        help=f"Download destination directory (default: {JACKET_PATH_DEFAULT}[game])",
        default=JACKET_PATH_DEFAULT,
    )
    parser.add_argument(
        "--format",
        choices=["png", "jpg", "webp"],
        default="webp",
        help="Image format (default: webp)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Display filenames only without actually downloading",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Re-download all images ignoring cache",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=1.0,
        help="Download interval in seconds (default: 1.0)",
    )

    args = parser.parse_args()

    # 間隔が1秒未満の場合はエラー
    if args.interval < 1.0:
        parser.error("--interval must be 1.0 seconds or greater")

    return args


def main():
    args = parse_args()
    for game in GAMES:
        if args.game == "all" or args.game == game:
            music_data = requests.get(GAMES_DATA[game]["music_data"]).json()

            # ここで実際にダウンロード処理を行う関数を呼び出す
            # download_jackets(g, args.dir, args.format, args.dry_run, args.overwrite, args.interval)
            print(
                f"Downloading jackets for {game} to {args.dir} in {args.format} format."
            )
            print(
                f"Dry run: {args.dry_run}, Overwrite: {args.overwrite}, Interval: {args.interval}s"
            )
            # 実際のダウンロード処理は省略


if __name__ == "__main__":
    main()
