#!/usr/bin/env python3
"""
Génère arma.json à partir de l'API CKAN de data.europa.eu
ou du portail ukrainien data.gov.ua.

Usage:
    python build_arma_json.py --source eu    --out arma.json
    python build_arma_json.py --source ua    --out arma.json
    python build_arma_json.py --source local --in raw/ --out arma.json
"""
import argparse
import json
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin

try:
    import requests
except ImportError:
    sys.exit("pip install requests")

# --- Portails CKAN ---
PORTALS = {
    "eu": "https://data.europa.eu/api/hub/search/",
    "ua": "https://data.gov.ua/api/3/action/",
}

# --- Requêtes de recherche ARMA ---
ARMA_QUERIES = [
    "ARMA",
    "АРМА",
    "Національне агентство України з питань виявлення, розшуку та управління активами",
    "agency asset recovery ukraine",
    "бюджетна програма",
]

# --- Formats reconnus ---
FMT_MAP = {
    "csv": "csv",
    "json": "json",
    "xls": "xlsx", "xlsx": "xlsx", "excel": "xlsx",
}


def log(msg):
    print(f"[{datetime.now():%H:%M:%S}] {msg}", file=sys.stderr)


def fetch_ckan_package_search(base_url, query, rows=100, start=0):
    """Interroge package_search CKAN."""
    url = urljoin(base_url, "action/package_search")
    params = {"q": query, "rows": rows, "start": start}
    r = requests.get(url, params=params, timeout=30)
    r.raise_for_status()
    return r.json()


def normalize_resource(res, base_url):
    """Normalise une ressource CKAN."""
    fmt = (res.get("format") or "").lower()
    fmt = FMT_MAP.get(fmt, "other")
    url = res.get("url") or res.get("access_url") or ""
    if url and not url.startswith("http"):
        url = urljoin(base_url, url)
    return {
        "title": res.get("name") or res.get("title") or res.get("description") or "",
        "url": url,
        "format": fmt,
        "size": res.get("size"),
        "last_modified": res.get("last_modified") or res.get("created"),
    }


def normalize_package(pkg, base_url):
    """Normalise un dataset CKAN au format attendu par le dashboard."""
    # Titre : CKAN utilise title ou name
    title = pkg.get("title") or pkg.get("name") or ""
    # Description : notes
    description = pkg.get("notes") or ""
    # Organisation
    org = ""
    if isinstance(pkg.get("organization"), dict):
        org = pkg["organization"].get("title") or pkg["organization"].get("name") or ""
    elif pkg.get("organization"):
        org = str(pkg["organization"])
    # Tags
    tags = [t.get("name") or t.get("display_name") or "" for t in pkg.get("tags", [])]
    tags = [t for t in tags if t]
    # Dates
    last_update = (pkg.get("metadata_modified") or
                   pkg.get("last_update") or
                   pkg.get("date_updated") or
                   pkg.get("modified") or "")
    created = pkg.get("metadata_created") or pkg.get("created") or ""
    # URL
    url = pkg.get("url") or pkg.get("landing_page") or ""
    if url and not url.startswith("http"):
        url = urljoin(base_url, url)
    # Ressources
    resources = [normalize_resource(r, base_url) for r in pkg.get("resources", [])]
    # Popularité (CKAN tracking)
    tracking = pkg.get("tracking_summary") or {}
    popularity = tracking.get("total") or pkg.get("views") or 0

    return {
        "id": pkg.get("id") or pkg.get("name"),
        "title": title,
        "description": description,
        "organization": {"name": org},
        "tags": tags,
        "last_update": last_update,
        "created": created,
        "url": url,
        "popularity": popularity,
        "resources": resources,
        "source": base_url,
    }


def collect_from_portal(portal_key, queries, max_per_query=200):
    """Collecte tous les datasets ARMA depuis un portail CKAN."""
    base_url = PORTALS[portal_key]
    all_packages = {}
    for q in queries:
        log(f"Recherche « {q} » sur {base_url}")
        start = 0
        rows = 100
        while True:
            try:
                data = fetch_ckan_package_search(base_url, q, rows=rows, start=start)
            except Exception as e:
                log(f"  ⚠️  Erreur: {e}")
                break
            result = data.get("result", {})
            pkgs = result.get("results", [])
            count = result.get("count", 0)
            if not pkgs:
                break
            for pkg in pkgs:
                norm = normalize_package(pkg, base_url)
                if norm["id"]:
                    all_packages[norm["id"]] = norm
            start += rows
            log(f"  → {len(all_packages)} uniques / {count} total")
            if start >= min(count, max_per_query):
                break
            time.sleep(0.3)  # rate limit
    return list(all_packages.values())


def collect_from_local(input_dir):
    """Charge des fichiers arma*.json déjà téléchargés."""
    all_packages = {}
    for path in Path(input_dir).glob("*.json"):
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
            pkgs = data.get("results") or data.get("result", {}).get("results") or data
            if isinstance(pkgs, dict):
                pkgs = [pkgs]
            for pkg in pkgs:
                if "id" in pkg:
                    all_packages[pkg["id"]] = pkg
        except Exception as e:
            log(f"⚠️  {path}: {e}")
    return list(all_packages.values())


def dedupe_and_merge(datasets):
    """Fusionne les doublons et déduplique les ressources."""
    seen = {}
    for d in datasets:
        key = d.get("id")
        if key not in seen:
            seen[key] = d
        else:
            # Fusionne les ressources
            existing_urls = {r["url"] for r in seen[key].get("resources", [])}
            for r in d.get("resources", []):
                if r["url"] not in existing_urls:
                    seen[key]["resources"].append(r)
    return list(seen.values())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", choices=["eu", "ua", "local"], required=True)
    ap.add_argument("--in", dest="input_dir", default=None)
    ap.add_argument("--out", default="arma.json")
    ap.add_argument("--max-per-query", type=int, default=200)
    args = ap.parse_args()

    if args.source == "local":
        if not args.input_dir:
            sys.exit("--in requis avec --source local")
        datasets = collect_from_local(args.input_dir)
    else:
        datasets = collect_from_portal(args.source, ARMA_QUERIES, args.max_per_query)

    datasets = dedupe_and_merge(datasets)
    datasets.sort(key=lambda d: d.get("last_update") or "", reverse=True)

    output = {
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "source": args.source,
        "count": len(datasets),
        "results": datasets,
    }
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    total_res = sum(len(d.get("resources", [])) for d in datasets)
    log(f"✅ {len(datasets)} datasets, {total_res} ressources → {args.out}")


if __name__ == "__main__":
    main()