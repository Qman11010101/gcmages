import argparse
from typing import Literal

from consts import GAMES, JACKET_PATH_DEFAULT

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
    # ここに処理を実装
    games = GAMES if args.game == "all" else [args.game]
    print(f"Games: {games}")
    print(f"Directory: {args.dir}")
    print(f"Format: {args.format}")
    print(f"Dry Run: {args.dry_run}")
    print(f"Overwrite: {args.overwrite}")
    print(f"Interval: {args.interval}")


if __name__ == "__main__":
    main()
