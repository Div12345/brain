#!/usr/bin/env python3
"""Import papers into Zotero via the local connector API.

Usage:
    # By DOI (fetches metadata from CrossRef):
    python zotero-import.py --doi "10.1371/journal.pone.0224365"

    # Multiple DOIs:
    python zotero-import.py --doi "10.1093/biomet/asn034" "10.1111/j.1467-9868.2005.00490.x"

    # By arXiv ID:
    python zotero-import.py --arxiv "2201.00494" "2106.02521"

    # Manual item (when CrossRef doesn't have it):
    python zotero-import.py --manual --title "My Paper" --authors "Smith,John;Doe,Jane" --year 2022

    # With tags:
    python zotero-import.py --doi "10.1234/example" --tags "stability-selection,feature-selection"

Requires: Zotero desktop running (connector at localhost:23119)
"""

import argparse
import json
import sys
import urllib.request
import urllib.error


import xml.etree.ElementTree as ET

CONNECTOR_URL = "http://localhost:23119/connector/saveItems"
CROSSREF_URL = "https://api.crossref.org/works/{}"
ARXIV_URL = "https://export.arxiv.org/api/query?id_list={}"


def fetch_crossref(doi: str) -> dict | None:
    """Fetch metadata from CrossRef for a DOI."""
    url = CROSSREF_URL.format(doi)
    req = urllib.request.Request(url, headers={"User-Agent": "ZoteroImport/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read())
            return data.get("message", {})
    except (urllib.error.URLError, json.JSONDecodeError) as e:
        print(f"  CrossRef lookup failed for {doi}: {e}", file=sys.stderr)
        return None


def crossref_to_zotero(cr: dict, extra_tags: list[str] = None) -> dict:
    """Convert CrossRef metadata to Zotero saveItems format."""
    # Extract authors
    creators = []
    for author in cr.get("author", []):
        creators.append({
            "firstName": author.get("given", ""),
            "lastName": author.get("family", ""),
            "creatorType": "author",
        })

    # Extract date
    date_parts = cr.get("published", cr.get("created", {})).get("date-parts", [[]])
    date = "-".join(str(p) for p in date_parts[0]) if date_parts[0] else ""

    # Build item
    item = {
        "itemType": "journalArticle",
        "title": cr.get("title", [""])[0] if isinstance(cr.get("title"), list) else cr.get("title", ""),
        "creators": creators,
        "date": date,
        "DOI": cr.get("DOI", ""),
        "url": cr.get("URL", ""),
        "publicationTitle": cr.get("container-title", [""])[0] if isinstance(cr.get("container-title"), list) else cr.get("container-title", ""),
        "volume": cr.get("volume", ""),
        "issue": cr.get("issue", ""),
        "pages": cr.get("page", ""),
        "abstractNote": cr.get("abstract", ""),
    }

    # Tags
    tags = extra_tags or []
    item["tags"] = tags

    return item


def fetch_arxiv(arxiv_id: str) -> dict | None:
    """Fetch metadata from arXiv API."""
    clean_id = arxiv_id.replace("arXiv:", "").strip()
    url = ARXIV_URL.format(clean_id)
    req = urllib.request.Request(url, headers={"User-Agent": "ZoteroImport/1.0"})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            root = ET.fromstring(resp.read())
            ns = {"a": "http://www.w3.org/2005/Atom"}
            entry = root.find("a:entry", ns)
            if entry is None:
                return None
            return {
                "title": (entry.findtext("a:title", "", ns) or "").strip().replace("\n", " "),
                "authors": [
                    a.findtext("a:name", "", ns)
                    for a in entry.findall("a:author", ns)
                ],
                "summary": (entry.findtext("a:summary", "", ns) or "").strip(),
                "published": (entry.findtext("a:published", "", ns) or "")[:10],
                "arxiv_id": clean_id,
                "url": f"https://arxiv.org/abs/{clean_id}",
                "doi": entry.findtext("{http://arxiv.org/schemas/atom}doi", ""),
            }
    except (urllib.error.URLError, ET.ParseError) as e:
        print(f"  arXiv lookup failed for {arxiv_id}: {e}", file=sys.stderr)
        return None


def arxiv_to_zotero(ax: dict, extra_tags: list[str] = None) -> dict:
    """Convert arXiv metadata to Zotero saveItems format."""
    creators = []
    for name in ax.get("authors", []):
        parts = name.rsplit(" ", 1)
        if len(parts) == 2:
            creators.append({"firstName": parts[0], "lastName": parts[1], "creatorType": "author"})
        else:
            creators.append({"lastName": name, "firstName": "", "creatorType": "author"})

    item = {
        "itemType": "journalArticle",
        "title": ax["title"],
        "creators": creators,
        "date": ax["published"],
        "DOI": ax.get("doi", ""),
        "url": ax["url"],
        "publicationTitle": "arXiv preprint",
        "abstractNote": ax.get("summary", ""),
        "extra": f"arXiv:{ax['arxiv_id']}",
        "tags": extra_tags or [],
    }
    return item


def import_by_arxiv(arxiv_ids: list[str], tags: list[str] = None):
    """Import papers by arXiv ID."""
    for aid in arxiv_ids:
        print(f"Importing arXiv:{aid}...")
        ax = fetch_arxiv(aid)
        if not ax:
            print(f"  FAILED: Could not fetch metadata for arXiv:{aid}")
            continue

        item = arxiv_to_zotero(ax, tags)
        title = item.get("title", "Unknown")[:60]
        print(f"  Found: {title}")

        if save_to_zotero([item]):
            print(f"  OK: Created in Zotero")
        else:
            print(f"  FAILED: Could not save to Zotero")


def save_to_zotero(items: list[dict]) -> bool:
    """Send items to Zotero via connector saveItems endpoint."""
    payload = {
        "items": items,
        "uri": items[0].get("url", "https://crossref.org"),
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        CONNECTOR_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            if resp.status == 201:
                return True
            print(f"  Unexpected status: {resp.status}", file=sys.stderr)
            return False
    except urllib.error.URLError as e:
        print(f"  Zotero connector error: {e}", file=sys.stderr)
        print("  Is Zotero running?", file=sys.stderr)
        return False


def import_by_doi(dois: list[str], tags: list[str] = None):
    """Import papers by DOI."""
    for doi in dois:
        print(f"Importing {doi}...")
        cr = fetch_crossref(doi)
        if not cr:
            print(f"  FAILED: Could not fetch metadata for {doi}")
            continue

        item = crossref_to_zotero(cr, tags)
        title = item.get("title", "Unknown")[:60]
        print(f"  Found: {title}")

        if save_to_zotero([item]):
            print(f"  OK: Created in Zotero")
        else:
            print(f"  FAILED: Could not save to Zotero")


def import_manual(title: str, authors_str: str, year: str, doi: str = "",
                  journal: str = "", tags: list[str] = None):
    """Import a manually specified paper."""
    creators = []
    if authors_str:
        for author in authors_str.split(";"):
            parts = author.strip().split(",")
            if len(parts) == 2:
                creators.append({
                    "lastName": parts[0].strip(),
                    "firstName": parts[1].strip(),
                    "creatorType": "author",
                })
            else:
                creators.append({
                    "lastName": parts[0].strip(),
                    "firstName": "",
                    "creatorType": "author",
                })

    item = {
        "itemType": "journalArticle",
        "title": title,
        "creators": creators,
        "date": year,
        "DOI": doi,
        "publicationTitle": journal,
        "tags": tags or [],
    }

    print(f"Importing: {title}...")
    if save_to_zotero([item]):
        print(f"  OK: Created in Zotero")
    else:
        print(f"  FAILED: Could not save to Zotero")


def main():
    parser = argparse.ArgumentParser(description="Import papers into Zotero")
    parser.add_argument("--doi", nargs="+", help="DOI(s) to import")
    parser.add_argument("--arxiv", nargs="+", help="arXiv ID(s) to import")
    parser.add_argument("--manual", action="store_true", help="Manual entry mode")
    parser.add_argument("--title", help="Paper title (manual mode)")
    parser.add_argument("--authors", help="Authors as 'Last,First;Last,First' (manual mode)")
    parser.add_argument("--year", help="Publication year (manual mode)")
    parser.add_argument("--journal", default="", help="Journal name (manual mode)")
    parser.add_argument("--tags", help="Comma-separated tags")

    args = parser.parse_args()
    tags = [t.strip() for t in args.tags.split(",")] if args.tags else []

    if args.doi:
        import_by_doi(args.doi, tags)
    elif args.arxiv:
        import_by_arxiv(args.arxiv, tags)
    elif args.manual:
        if not args.title:
            print("Error: --title required for manual mode", file=sys.stderr)
            sys.exit(1)
        import_manual(args.title, args.authors or "", args.year or "", tags=tags)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
