"""Extract Altrincham athletes from a Hale10k PDF results file.

Usage:
    python hale_script.py --pdf /path/to/Hale10k_results.pdf --out altrincham_hale.csv

Dependencies:
    pip install pdfplumber

The script searches for lines containing 'Altrincham' (case-insensitive), then
attempts to extract a chip time and a reasonably-formed athlete name. The
output is a CSV with two columns (no header): name,chip_time
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from typing import List, Optional, Tuple

try:
    import pdfplumber
except Exception as e:  # pragma: no cover - runtime dependency
    raise SystemExit(
        "pdfplumber is required. Install with: pip install pdfplumber"
    ) from e


TIME_RE = re.compile(r"\b\d{1,2}:\d{2}:\d{2}\b|\b\d{1,2}:\d{2}\b")
CLUB_RE = re.compile(r"altrincham", re.I)
NAME_RE = re.compile(r"[A-Z][a-z\-']+(?: [A-Z][a-z\-']+){0,4}")


def extract_lines_from_pdf(path: str) -> List[str]:
    lines: List[str] = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            for l in text.splitlines():
                l = l.strip()
                if l:
                    lines.append(l)
    return lines


def extract_name_and_time(line: str) -> Optional[Tuple[str, str]]:
    if not CLUB_RE.search(line):
        return None
    
    time_start_idx = line.find('AC')+3
    chip_time = line[time_start_idx:time_start_idx+5]

    # find the club match index and consider the left side of the line first
    club_m = CLUB_RE.search(line)
    club_idx = club_m.start() if club_m else len(line)
    left = line[:club_idx]

    # remove times and obvious bib/placings from the left part
    left_clean = TIME_RE.sub("", left)
    left_clean = re.sub(r"^\s*\d+[\).]?\s*", "", left_clean)  # leading bib/pos
    left_clean = re.sub(r"\b\d{1,4}\b", "", left_clean)  # stray numbers
    left_clean = re.sub(r"\s{2,}", " ", left_clean).strip()

    # try to find name candidates on the cleaned left part
    candidates = list(NAME_RE.finditer(left_clean))
    if candidates:
        # choose the candidate closest to the club (i.e., the last one)
        name = candidates[-1].group(0)
        return name, chip_time

    # fallback: search whole line for a name-like token
    candidates = list(NAME_RE.finditer(line))
    if candidates:
        # choose candidate nearest to the chip time if available
        if chip_time:
            chip_idx = line.rfind(chip_time)
            best = min(candidates, key=lambda m: abs(m.start() - chip_idx))
            return best.group(0), chip_time
        return candidates[0].group(0), chip_time

    return None


def process(pdf_path: str, out_csv: str) -> None:
    lines = extract_lines_from_pdf(pdf_path)
    matches: List[Tuple[str, str]] = []
    for ln in lines:
        if CLUB_RE.search(ln):
            res = extract_name_and_time(ln)
            if res:
                matches.append(res)

    if not matches:
        print("No Altrincham athletes found in the PDF (or parsing failed).")

    # write CSV without header, one athlete per row: name,chip_time
    with open(out_csv, "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        for name, chip in matches:
            writer.writerow([name, chip])

    print(f"Wrote {len(matches)} rows to {out_csv}")


def main(argv: Optional[List[str]] = None) -> int:
    p = argparse.ArgumentParser(description="Extract Altrincham athletes from a Hale10k PDF")
    p.add_argument("--pdf", required=True, help="Path to Hale10k_results.pdf")
    p.add_argument("--out", default="altrincham_hale.csv", help="Output CSV file")
    args = p.parse_args(argv)

    process(args.pdf, args.out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
