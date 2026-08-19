#!/usr/bin/env python3
"""Hello PSI - Python reference seed (stdlib only).

Apex PSI — Universal Verification Layer. Proposed open standard under active development. Verification free forever (MIT). IETF drafts are individual submissions, not formally endorsed. Verify everything yourself.

Implements rules R1-R10 of PSI-SEAL/1. Run:  python hello_psi.py
"""
import hashlib
import json
import sys
import unicodedata

# Schema digest pinned 2026-08-20 from the live canonical schema at
# https://ai-governance-standard.com/.well-known/psi-schema.json
# (SHA-256 over RFC 8785 JCS of the parsed document). The seed is fully
# deterministic and offline by design; run with --check-live to recompute
# from the network and confirm the pin is current.
PINNED_SCHEMA_DIGEST = "454743698e1b23d5eddb7fc4a97ae1c8c33047921ef360d8e6c86d61f2fe9e77"
SCHEMA_URL = "https://ai-governance-standard.com/.well-known/psi-schema.json"
SEALED_AT = "2026-08-20T00:00:00.000Z"  # R6, pinned for reproducible vectors

VECTORS = [
    ("vector-0", ""),
    ("vector-1", "Hello, PSI."),
    ("vector-2", '{"model":"example","output":"The seal is the math."}'),
]


def jcs(value):
    """R1 - RFC 8785 JSON Canonicalization Scheme (PSI subset: no floats)."""
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, int):
        return str(value)
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=False)
    if isinstance(value, list):
        return "[" + ",".join(jcs(v) for v in value) + "]"
    if isinstance(value, dict):
        keys = sorted(value.keys(), key=lambda k: k.encode("utf-16-be"))
        return "{" + ",".join(
            json.dumps(k, ensure_ascii=False) + ":" + jcs(value[k]) for k in keys
        ) + "}"
    raise TypeError("unsupported type in PSI envelope: %r" % type(value))


def schema_digest(doc):
    return hashlib.sha256(jcs(doc).encode("utf-8")).hexdigest()


def live_schema_digest():
    import urllib.request

    try:
        with urllib.request.urlopen(SCHEMA_URL, timeout=10) as r:
            return schema_digest(json.loads(r.read().decode("utf-8")))
    except Exception:
        return None


def seal(text, name, sealed_at=SEALED_AT, sd=None):
    raw = text.encode("utf-8")
    h = hashlib.sha256(raw).hexdigest()                                    # R5
    leaf = hashlib.sha256(("PSI1:" + h).encode("ascii")).hexdigest()       # R9
    envelope = {                                                           # R3 order
        "schema": "PSI-SEAL/1.0.0",
        "schema_digest": sd if sd else "0" * 64,
        "sealed_at": sealed_at,                                            # R6
        "subject": {                                                       # R7
            "name": unicodedata.normalize("NFC", name),
            "size_bytes": len(raw),
        },
        "hash": h,                                                         # R4/R5
        "merkle": {"leaf": leaf, "root": leaf},                            # R8
    }
    seal_hash = hashlib.sha256(jcs(envelope).encode("utf-8")).hexdigest()  # R10
    return envelope, seal_hash


def main():
    sd = PINNED_SCHEMA_DIGEST
    print("language: python")
    print("schema_digest:", sd)
    if "--check-live" in sys.argv:
        live = live_schema_digest()
        print("live_digest  :", live if live else "UNREACHABLE")
        print("pin_current  :", "yes" if live == sd else "no")
    for name, text in VECTORS:
        envelope, sh = seal(text, name, sd=sd)
        print("---", name)
        print("hash      :", envelope["hash"])
        print("leaf      :", envelope["merkle"]["leaf"])
        print("seal_hash :", sh)
        print("envelope  :", jcs(envelope))


if __name__ == "__main__":
    main()
