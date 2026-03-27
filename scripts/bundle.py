#!/usr/bin/env python3
"""
Bundle all repo files into a single text file for email transport.
Skips .git/, node_modules/, binary files, and lockfiles.

Usage:
  python scripts/bundle.py                    # writes repo_bundle.txt
  python scripts/bundle.py -o my_bundle.txt   # custom output name
  python scripts/bundle.py --unbundle repo_bundle.txt  # reconstruct files

Reconstruct on the other end:
  python scripts/bundle.py --unbundle repo_bundle.txt
"""

import argparse
import os
from pathlib import Path

SEPARATOR = "=-=-=-"

SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv", "venv", "dist", "build"}
SKIP_FILES = {"package-lock.json", ".DS_Store", "Thumbs.db"}
BINARY_EXTENSIONS = {
    ".png", ".jpg", ".jpeg", ".gif", ".ico", ".webp", ".bmp", ".svg",
    ".woff", ".woff2", ".ttf", ".eot", ".otf",
    ".zip", ".tar", ".gz", ".bz2", ".7z", ".rar",
    ".exe", ".dll", ".so", ".dylib",
    ".pdf", ".doc", ".docx", ".xls", ".xlsx",
    ".mp3", ".mp4", ".wav", ".avi", ".mov",
    ".pyc", ".pyo", ".class", ".o",
}


def should_skip(path: Path, repo_root: Path) -> bool:
    rel = path.relative_to(repo_root)
    parts = rel.parts
    if any(p in SKIP_DIRS for p in parts):
        return True
    if path.name in SKIP_FILES:
        return True
    if path.suffix.lower() in BINARY_EXTENSIONS:
        return True
    return False


def bundle(repo_root: Path, output: Path):
    files = sorted(
        f for f in repo_root.rglob("*")
        if f.is_file() and not should_skip(f, repo_root)
    )

    with open(output, "w", encoding="utf-8", errors="replace") as out:
        out.write(f"# Repo bundle created from: {repo_root.name}\n")
        out.write(f"# Files: {len(files)}\n")
        out.write(f"# Reconstruct with: python scripts/bundle.py --unbundle {output.name}\n\n")

        for f in files:
            rel = f.relative_to(repo_root).as_posix()
            try:
                content = f.read_text(encoding="utf-8")
            except (UnicodeDecodeError, PermissionError):
                content = f"[BINARY OR UNREADABLE FILE — {f.stat().st_size} bytes]"

            out.write(f"{SEPARATOR} {rel} {SEPARATOR}\n")
            out.write(content)
            if not content.endswith("\n"):
                out.write("\n")

    print(f"Bundled {len(files)} files into {output}")
    print(f"Size: {output.stat().st_size / 1024:.1f} KB")


def unbundle(bundle_path: Path, output_dir: Path):
    text = bundle_path.read_text(encoding="utf-8")
    lines = text.splitlines(keepends=True)

    current_path = None
    current_lines: list[str] = []
    count = 0

    def flush():
        nonlocal count
        if current_path:
            out = output_dir / current_path
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text("".join(current_lines), encoding="utf-8")
            count += 1

    for line in lines:
        stripped = line.strip()
        if stripped.startswith(SEPARATOR) and stripped.endswith(SEPARATOR) and len(stripped) > len(SEPARATOR) * 2:
            flush()
            current_path = stripped[len(SEPARATOR):].strip()
            current_path = current_path[:-(len(SEPARATOR))].strip()
            current_lines = []
        elif current_path is not None:
            current_lines.append(line)

    flush()
    print(f"Reconstructed {count} files into {output_dir}/")


def main():
    parser = argparse.ArgumentParser(description="Bundle/unbundle repo for email transport")
    parser.add_argument("-o", "--output", default="repo_bundle.txt", help="Output bundle filename")
    parser.add_argument("--unbundle", metavar="FILE", help="Reconstruct files from a bundle")
    parser.add_argument("--output-dir", default="unbundled", help="Directory for unbundled files")
    args = parser.parse_args()

    if args.unbundle:
        unbundle(Path(args.unbundle), Path(args.output_dir))
    else:
        repo_root = Path(__file__).resolve().parent.parent
        bundle(repo_root, Path(args.output))


if __name__ == "__main__":
    main()
