# Supernote Bulk Export

Bulk export Supernote `.note` files to PDF using `supernote-tool`.

Quick Start (one-liner)

Run from the folder you want the PDFs to be written into:

```bash
cd /path/to/pdf-output
uv run https://gist.githubusercontent.com/ryanhudson/2b412c961228a5413dc001c1fd77ee03/raw/supernote_bulk_export.py \
  /path/to/your/notes
```

This will:
- Read `.note` files from the source folder (recursively).
- Write PDFs into the current folder, mirroring subfolders.
- Verify source files never change (hash before/after).

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
`~/Supernote/EXPORT` is the folder containing your `.note` files (copied from the Supernote device).
`~/Supernote/PDF` is the output folder where you want PDFs to be written.
Run it from your destination/output folder so the PDFs land there:

```bash
cd ~/Supernote/PDF
uv run https://gist.githubusercontent.com/ryanhudson/2b412c961228a5413dc001c1fd77ee03/raw/supernote_bulk_export.py \
  ~/Supernote/EXPORT
```

If your folders are named differently, just replace those paths. For example:

```bash
cd /path/to/pdf-output
uv run https://gist.githubusercontent.com/ryanhudson/2b412c961228a5413dc001c1fd77ee03/raw/supernote_bulk_export.py \
  /path/to/note-files
```

## Notes

- The script never writes to the source `.note` files. By default it hashes each file before and after conversion and fails if any source file changes.
