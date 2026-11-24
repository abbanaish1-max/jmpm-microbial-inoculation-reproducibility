#!/usr/bin/env python3
"""Report the size and SHA-256 of the official Azarbad & Junker source workbook.

Usage: python verify_source_workbook.py /path/to/supplementary_table_s1_ycae122.xlsx
This checks provenance only; it does not rerun or validate the empirical analysis.
"""
import argparse, hashlib
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument('workbook', help='Path to the downloaded official Supplementary Table S1 workbook')
a=p.parse_args()
f=Path(a.workbook)
if not f.is_file():
    raise SystemExit(f'File not found: {f}')
h=hashlib.sha256()
with f.open('rb') as stream:
    for chunk in iter(lambda: stream.read(1024*1024), b''):
        h.update(chunk)
print(f'file={f.name}')
print(f'size_bytes={f.stat().st_size}')
print(f'sha256={h.hexdigest()}')
print('Historical manifest size: 203093 bytes')
print('Historical manifest SHA-256: 595a888363862e153b30e875e3fa88260dfcc8b862addd2332f205f93d321f03')
