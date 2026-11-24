#!/usr/bin/env python3
"""Download the official Azarbad & Junker Supplementary Table S1 workbook.

This helper uses the PMC public file endpoint. If the endpoint blocks automated
requests, open the article page in a browser and download Supplementary Table S1
manually, then run verify_source_workbook.py on the downloaded file.
"""
from pathlib import Path
import requests

URL = "https://pmc.ncbi.nlm.nih.gov/articles/instance/11538580/bin/supplementary_table_s1_ycae122.xlsx"
OUT = Path("supplementary_table_s1_ycae122.xlsx")
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; research-data-retrieval/1.0)"}
try:
    response = requests.get(URL, headers=HEADERS, timeout=60)
    response.raise_for_status()
    if not response.content.startswith(b"PK"):
        raise RuntimeError("The server response does not appear to be an XLSX ZIP file.")
    OUT.write_bytes(response.content)
    print(f"Downloaded {OUT} ({OUT.stat().st_size} bytes)")
    print("Next: python verify_source_workbook.py supplementary_table_s1_ycae122.xlsx")
except Exception as exc:
    raise SystemExit(
        "Automated download failed. Download the file manually from "
        "https://pmc.ncbi.nlm.nih.gov/articles/PMC11538580/ under Supplementary Material "
        "(Supplementary Table S1), then run verify_source_workbook.py.\n" + str(exc)
    )
