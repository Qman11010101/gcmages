import argparse
from typing import Literal

ImageFormat = Literal["png", "jpg", "webp"]


def parse_args():
    parser = argparse.ArgumentParser(
        description="SEGAの音楽ゲーム3機種のジャケット画像をダウンロードするツール"
    )
    parser.add_argument(
        "game",
        nargs="?",  # 引数を省略可能にする
        choices=["chunithm", "ongeki", "maimai", "all"],
        help="ダウンロードする対象のゲーム (all: 全てのゲーム)",
        default="all",
    )
    parser.add_argument(
        "--dir", help="ダウンロード先のディレクトリ (デフォルト: ./jacket/[game])"
    )
    parser.add_argument(
        "--format",
        choices=["png", "jpg", "webp"],
        default="webp",
        help="画像フォーマット (デフォルト: webp)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="実際にはダウンロードせず、ファイル名のみを表示",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="キャッシュを無視して全ての画像を再ダウンロード",
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=1.0,
        help="ダウンロード間隔（秒、デフォルト: 1.0）",
    )

    args = parser.parse_args()

    # 間隔が1秒未満の場合はエラー
    if args.interval < 1.0:
        parser.error("--interval は1秒以上を指定してください")

    return args


def main():
    args = parse_args()
    # ここに処理を実装
    games = ["chunithm", "ongeki", "maimai"] if args.game == "all" else [args.game]
    print(f"Games: {games}")
    print(f"Directory: {args.dir}")
    print(f"Format: {args.format}")
    print(f"Dry Run: {args.dry_run}")
    print(f"Overwrite: {args.overwrite}")
    print(f"Interval: {args.interval}")


if __name__ == "__main__":
    main()
