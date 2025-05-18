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
python main.py [GAME] [--dir DIR_PATH] [--format (png|jpg|webp)] [--overwrite] [--interval INTERVAL] [--dry-run] 
```

一度ダウンロードした画像は、キャッシュとして保存されます。
キャッシュが存在する場合、`--overwrite`オプションを指定しない限り、再度ダウンロードされることはありません。

### 引数
- `GAME` : ダウンロードするゲームを指定します。
  - `chunithm` : CHUNITHMの楽曲ジャケット画像をダウンロードします。
  - `ongeki` : オンゲキの楽曲ジャケット画像をダウンロードします。
  - `maimai` : maimaiの楽曲ジャケット画像をダウンロードします。
  - `all` : 全てのゲームの楽曲ジャケット画像をダウンロードします。
- `--dir DIR_PATH` : ダウンロード先のディレクトリを指定します。デフォルトは`./jacket/[chunithm|ongeki|maimai]`です。
- `--format (png|jpg|webp)` : ダウンロードする画像のフォーマットを指定します。デフォルトは`webp`です。
  - `png` : PNG形式でダウンロードします。
  - `jpg` : JPEG形式でダウンロードします。
  - `webp` : WebP形式でダウンロードします。
- `--dry-run` : 実際にはダウンロードせず、ダウンロードするファイル名を表示します。
- `--overwrite` : キャッシュを無視して、全ての楽曲ジャケット画像をダウンロードします。
- `--interval INTERVAL` : ダウンロード間隔を指定します。デフォルトは1秒です。1秒未満の値は指定できません。

## 注意
### SSL証明書のエラーについて
maimaiの楽曲ジャケット画像をダウンロードする際に、SSL証明書のエラーが発生する場合があります。
この場合、[こちらのサイト](https://rakuraku-engineer.com/posts/python-request-get-error-ssl/)に掲載されている手順を参考に、`maimaidx.jp`のSSL証明書をcacert.pemに追加してください。
cacert.pemは`uv pip show certifi`で表示される`certifi`のインストール先ディレクトリ内にあります。

### インターバルについて
SEGAのサーバーに負荷をかけないため、ダウンロード間隔を1秒以上に設定しています。
`--interval`オプションを指定することで、ダウンロード間隔を変更できますが、1秒未満の値は指定できません。
短い間隔でダウンロードを行うと、通信がブロックされるなどの問題が発生する可能性があります。

## ライセンス
MITライセンスのもとで配布されています。詳しくは[LICENSE](LICENSE)をご覧ください。