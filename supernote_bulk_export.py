#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#   "supernotelib",
# ]
# ///
import argparse
import hashlib
import shutil
import subprocess
import sys
from pathlib import Path


def build_parser():
    parser = argparse.ArgumentParser(
        description="Bulk export Supernote .note files to PDF using supernote-tool."
    )
    parser.add_argument(
        "input_dir",
        help="Directory containing .note files (searched recursively).",
    )
    parser.add_argument(
        "--pdf-type",
        choices=["raster", "vector"],
        default="raster",
        help="PDF output type. Default: raster",
    )
    parser.add_argument(
        "-j",
        "--workers",
        type=int,
        default=None,
        help="Number of worker threads for supernote-tool.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing PDFs.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print commands without running conversions.",
    )
    parser.add_argument(
        "--no-verify-unchanged",
        action="store_true",
        help="Skip hashing .note files to verify they were not modified.",
    )
    return parser


def find_note_files(root: Path):
    return sorted(root.rglob("*.note"))


def ensure_tool_available():
    if shutil.which("supernote-tool") is None:
        print(
            "supernote-tool not found in PATH. Install with: pip install supernotelib",
            file=sys.stderr,
        )
        return False
    return True


def build_command(note_path: Path, output_path: Path, pdf_type: str, workers: int | None):
    cmd = [
        "supernote-tool",
        "convert",
        "-t",
        "pdf",
        "-a",
    ]
    if pdf_type == "vector":
        cmd.extend(["--pdf-type", "vector"])
    if workers is not None:
        cmd.extend(["-j", str(workers)])
    cmd.extend([str(note_path), str(output_path)])
    return cmd


def sha256_file(path: Path):
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def main():
    parser = build_parser()
    args = parser.parse_args()

    input_dir = Path(args.input_dir).expanduser().resolve()
    output_dir = Path.cwd().resolve()

    if not input_dir.exists() or not input_dir.is_dir():
        print(f"Input directory does not exist: {input_dir}", file=sys.stderr)
        return 2

    if not ensure_tool_available():
        return 2

    note_files = find_note_files(input_dir)
    if not note_files:
        print("No .note files found.")
        return 0

    converted = 0
    skipped = 0
    failed = 0

    for note_path in note_files:
        rel_path = note_path.relative_to(input_dir)
        output_path = output_dir / rel_path.with_suffix(".pdf")
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if output_path.exists() and not args.overwrite:
            skipped += 1
            continue

        pre_hash = None
        if not args.no_verify_unchanged and not args.dry_run:
            pre_hash = sha256_file(note_path)

        cmd = build_command(note_path, output_path, args.pdf_type, args.workers)
        if args.dry_run:
            print(" ".join(cmd))
            converted += 1
            continue

        try:
            subprocess.run(cmd, check=True)
            if pre_hash is not None:
                post_hash = sha256_file(note_path)
                if post_hash != pre_hash:
                    print(
                        f"ERROR: source file changed during conversion: {note_path}",
                        file=sys.stderr,
                    )
                    failed += 1
                    continue
            converted += 1
        except subprocess.CalledProcessError:
            failed += 1

    print(
        f"Done. Converted: {converted}, skipped: {skipped}, failed: {failed}."
    )
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
