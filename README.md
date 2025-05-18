# gcmages

English version available at [README_EN.md](README_EN.md).

## 概要
gcmagesは、SEGAの音楽ゲーム3機種「CHUNITHM」「オンゲキ」「maimai」の楽曲ジャケット画像をダウンロードするためのツールです。

## 環境構築
実行にはPython3系が必要です。[uv](https://docs.astral.sh/uv/)で環境を構築することをお勧めします。

```bash
uv sync
```

## 使い方
`main.py`を実行することで、楽曲ジャケット画像をダウンロードできます。
デフォルトでは、3機種全ての画像がダウンロードされます。
```
python main.py [chunithm|ongeki|maimai] [--dir DIR_PATH] [--format (png|jpg|webp)] [--overwrite] [--interval INTERVAL] [--dry-run] 
```

### 引数
- `chunithm` : CHUNITHMの楽曲ジャケット画像をダウンロードします。
- `ongeki` : オンゲキの楽曲ジャケット画像をダウンロードします。
- `maimai` : maimaiの楽曲ジャケット画像をダウンロードします。
- `--dir DIR_PATH` : ダウンロード先のディレクトリを指定します。デフォルトは`./jacket/[chunithm|ongeki|maimai]`です。
- `--format (png|jpg|webp)` : ダウンロードする画像のフォーマットを指定します。デフォルトは`webp`です。
  - `png` : PNG形式でダウンロードします。
  - `jpg` : JPEG形式でダウンロードします。
  - `webp` : WebP形式でダウンロードします。
- `--dry-run` : 実際にはダウンロードせず、ダウンロードするファイル名を表示します。
- `--overwrite` : キャッシュを無視して、全ての楽曲ジャケット画像をダウンロードします。
- `--interval INTERVAL` : ダウンロード間隔を指定します。デフォルトは1秒です。1秒未満の値は指定できません。