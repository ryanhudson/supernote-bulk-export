# Supernote Bulk Export

Bulk export Supernote `.note` files to PDF using `supernote-tool`.

## Prerequisites

- Python 3.10+
- `uv` installed

## Usage

Run it from the destination folder for PDFs, and pass the source `.note` folder.
Because this script uses a PEP 723 header, `uv` will auto-install `supernotelib`:

```bash
cd /path/to/exports
uv run /Users/ryan/development/cdex/supernote-bulk-export/supernote_bulk_export.py \
  /path/to/notes
```

Options:

- `--pdf-type raster|vector` (default: raster)
- `-j, --workers N` (number of threads for conversion)
- `--overwrite` (overwrite existing PDFs)
- `--dry-run` (print commands without running)
- `--no-verify-unchanged` (skip hashing to confirm sources stayed unchanged)

## Example

```bash
cd ~/Supernote/PDF
uv run /Users/ryan/development/cdex/supernote-bulk-export/supernote_bulk_export.py \
  ~/Supernote/EXPORT --pdf-type vector -j 4
```

## One-liner via GitHub Gist

This script is designed to work as a one-shot tool with `uv run` and a raw Gist URL.
Run it from your destination folder:

```bash
cd ~/Supernote/PDF
uv run https://gist.githubusercontent.com/ryanhudson/2b412c961228a5413dc001c1fd77ee03/raw/supernote_bulk_export.py \
  ~/Supernote/EXPORT
```

## Notes

- The script never writes to the source `.note` files. By default it hashes each file before and after conversion and fails if any source file changes.
