#!/usr/bin/env python3
"""Construit arma.json en scannant les fichiers XLS/XLSX ARMA locaux."""
import json
import re
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent
OUT = ROOT / "arma.json"

def extract_year(fname):
    m = re.search(r'(20[12]\d)', fname)
    return int(m.group(1)) if m else 0

def build_title(year):
    return f"Звіт про виконання паспорта бюджетної програми на {year} рік"

def build():
    candidates = list(ROOT.glob("*.xls")) + list(ROOT.glob("*.xlsx"))
    resources = []
    for fpath in candidates:
        if fpath.name.startswith("~") or fpath.name.startswith("."):
            continue
        year = extract_year(fpath.name)
        if year == 0:
            print(f"⚠️  pas d'annee detectee : {fpath.name}")
            continue
        ext = fpath.suffix.lower()
        fmt = "xlsx" if ext in (".xls", ".xlsx") else "other"
        resources.append({
            "title": build_title(year),
            "url": fpath.name,
            "format": fmt,
            "size": fpath.stat().st_size,
            "year": year,
        })

    resources.sort(key=lambda r: r["year"])

    dataset = {
        "id": "arma-budget-program-reports",
        "title": "Звіти про виконання паспортів бюджетних програм АРМА",
        "description": (
            "Сукупність річних звітів про виконання паспортів бюджетних програм "
            "Національного агентства України з питань виявлення, розшуку та управління "
            "активами, одержаними від корупційних та інших злочинів (АРМА). "
            "Джерело : data.gov.ua"
        ),
        "organization": {"name": "Національне агентство України з питань виявлення, розшуку та управління активами (АРМА)"},
        "tags": ["arma", "бюджет", "паспорт бюджетної програми", "звіт"] + [str(r["year"]) for r in resources],
        "last_update": "2026-02-09",
        "url": "https://data.gov.ua/",
        "popularity": 0,
        "resources": resources,
        "source": "data.gov.ua",
    }

    out = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "source": "local",
        "count": 1,
        "results": [dataset],
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK : {len(resources)} ressources -> {OUT}")
    for r in resources:
        print(f"   - {r['year']} : {r['title']} ({r['size']} o) [{r['url']}]")

if __name__ == "__main__":
    build()
