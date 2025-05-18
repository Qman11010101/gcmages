# gcmages

日本語版は[README.md](README.md)をご覧ください。(Japanese version is available at [README.md](README.md))

## Overview
gcmages is a tool for downloading song jacket images from three SEGA music games: "CHUNITHM", "ONGEKI", and "maimai".

## Setup
Python 3.x is required to run this tool. It is recommended to set up the environment using [uv](https://docs.astral.sh/uv/).

```bash
uv sync
```

## Usage
You can download song jacket images by running `main.py`.
By default, images from all three games will be downloaded.
```
python main.py [GAME] [--dir DIR_PATH] [--format (png|jpg|webp)] [--overwrite] [--interval INTERVAL] [--dry-run] 
```

Once downloaded, images are stored as cache.
If cache exists, images will not be downloaded again unless the `--overwrite` option is specified.

### Arguments
- `GAME` : Specify which game's jacket images to download.
  - `chunithm` : Download CHUNITHM song jacket images.
  - `ongeki` : Download ONGEKI song jacket images.
  - `maimai` : Download maimai song jacket images.
  - `all` : Download song jacket images from all games.
- `--dir DIR_PATH` : Specify the download directory. Default is `./jacket/[chunithm|ongeki|maimai]`.
- `--format (png|jpg|webp)` : Specify the image format for download. Default is `webp`.
  - `png` : Download in PNG format.
  - `jpg` : Download in JPEG format.
  - `webp` : Download in WebP format.
- `--dry-run` : Display filenames that would be downloaded without actually downloading.
- `--overwrite` : Download all song jacket images ignoring the cache.
- `--interval INTERVAL` : Specify the interval between downloads. Default is 1 second. Values less than 1 second are not allowed.

## Notes
### About SSL Certificate Errors
When downloading maimai song jacket images, SSL certificate errors may occur.
In this case, please follow the steps on [this site](https://rakuraku-engineer.com/posts/python-request-get-error-ssl/) to add the SSL certificate for `maimaidx.jp` to cacert.pem.
cacert.pem can be found in the installation directory of `certifi`, which can be shown by running `uv pip show certifi`.

### About Download Intervals
To avoid putting excessive load on SEGA's servers, the download interval is set to a minimum of 1 second.
While you can change the interval using the `--interval` option, values less than 1 second are not allowed.
Setting shorter intervals may result in issues such as having your connection blocked.

## License
This project is distributed under the MIT License. See [LICENSE](LICENSE) for details.
