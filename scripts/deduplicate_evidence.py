#!/usr/bin/env python3
"""Deterministiska hjälpoperationer för evidens-URL:er och dubblettgrupper.

Scriptet gör medvetet inte semantisk deduplicering automatiskt. Det producerar
signaler som GPT:n eller en människa kan använda tillsammans med proveniens.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit

TRACKING_PREFIXES = ("utm_",)
TRACKING_KEYS = {"gclid", "fbclid", "mc_cid", "mc_eid"}


def canonicalize_url(url: str) -> str:
    parts = urlsplit(url.strip())
    host = (parts.hostname or "").lower()
    netloc = host
    if parts.port:
        netloc += f":{parts.port}"
    if parts.username:
        # Preserve unusual authenticated URLs rather than silently rewriting identity.
        netloc = parts.netloc.lower()
    query = []
    for key, value in parse_qsl(parts.query, keep_blank_values=True):
        lk = key.lower()
        if lk in TRACKING_KEYS or any(lk.startswith(prefix) for prefix in TRACKING_PREFIXES):
            continue
        query.append((key, value))
    query.sort()
    return urlunsplit((parts.scheme.lower(), netloc, parts.path or "/", urlencode(query, doseq=True), ""))


def fingerprint(value: str, prefix: str) -> str:
    digest = hashlib.sha256(value.encode("utf-8")).hexdigest()[:20]
    return f"{prefix}-{digest}"


def document_fingerprint(url: str) -> str:
    return fingerprint(canonicalize_url(url), "doc")


def claim_fingerprint(agency_id: str, technology_target_id: str, usage_semantics: str, origin_key: str) -> str:
    normalized = "|".join(part.strip().lower() for part in (agency_id, technology_target_id, usage_semantics, origin_key))
    return fingerprint(normalized, "claim")


def process_record(record: dict) -> dict:
    out = dict(record)
    url = record.get("source_url")
    if url:
        out["canonical_source_url"] = canonicalize_url(url)
        out["document_fingerprint"] = document_fingerprint(url)
    if all(record.get(k) for k in ("agency_id", "technology_target_id", "usage_semantics", "origin_key")):
        out["claim_fingerprint"] = claim_fingerprint(
            record["agency_id"], record["technology_target_id"], record["usage_semantics"], record["origin_key"]
        )
    return out


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", nargs="?", help="JSON-fil med ett objekt eller en lista")
    parser.add_argument("--url", help="Normalisera endast en URL")
    args = parser.parse_args()
    if args.url:
        print(json.dumps({"canonical_url": canonicalize_url(args.url), "document_fingerprint": document_fingerprint(args.url)}, ensure_ascii=False, indent=2))
        return 0
    if not args.input:
        parser.error("ange input eller --url")
    data = json.loads(Path(args.input).read_text(encoding="utf-8"))
    result = [process_record(x) for x in data] if isinstance(data, list) else process_record(data)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
