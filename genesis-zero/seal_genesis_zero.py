"""GENESIS ZERO sealing ceremony â€” 29 August 2026.
Canonical document -> SHA-256 -> live public notarize (APEX PSI ledger,
Ed25519 + LMS-W4-SHA256 PQ layer) -> public verify-hash round-trip -> manifest.
Deterministic and repeatable: the document bytes alone fix the digest."""
import hashlib, json, os, urllib.request
from datetime import datetime, timezone

DOC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "GENESIS_ZERO.md")
NOTARIZE = "https://qhtntebpcribjiwrdtdd.supabase.co/functions/v1/notarize"
VERIFY = "https://qhtntebpcribjiwrdtdd.supabase.co/functions/v1/verify-hash"

raw = open(DOC_PATH, "rb").read()
digest = hashlib.sha256(raw).hexdigest()
print("GENESIS ZERO document bytes:", len(raw))
print("GENESIS ZERO sha256:", digest)


def post(url, obj, timeout=120):
    req = urllib.request.Request(
        url, data=json.dumps(obj).encode("utf-8"),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


print("== STEP 1: NOTARIZE (live public endpoint) ==")
payload = {
    "decision": ("NOTARIZE: GENESIS ZERO - APEX PSI REFERENCE IMPLEMENTATION v1.0. "
                 "Canonical declaration of the Apex PSI verification layer: RFC 8785 "
                 "canonicalisation, SHA-256 digest, Ed25519 + LMS-W4-SHA256 hybrid "
                 "signature, Bitcoin chain-tip anchoring, public ledger receipt. "
                 "Free and open protocol; correction public if the math breaks; money "
                 "buys process, never outcome. Document digest sha256:" + digest),
    "predicate": "GENESIS_ZERO",
    "context": {
        "title": "Genesis Zero - APEX PSI Reference Implementation v1.0",
        "source": "genesis-zero/GENESIS_ZERO.md (this repository)",
        "category": "genesis-reference",
        "document_sha256": digest,
        "document_bytes": len(raw),
        "operator": "ROCKYFILMS888 PTY LTD ABN 71 672 237 795",
        "issued": "2026-08-29",
    },
}
res = post(NOTARIZE, payload)
print(json.dumps(res, indent=1)[:1600])

led = res.get("ledger_hash") or res.get("hash") or res.get("sha256")
commit = res.get("commit_id") or res.get("receipt_id")
print("RECEIPT:", commit, "LEDGER HASH:", led)

verified = None
if led:
    print("== STEP 2: PUBLIC VERIFY ROUND-TRIP ==")
    req = urllib.request.Request(VERIFY + "?hash=" + led)
    with urllib.request.urlopen(req, timeout=60) as r:
        v = json.loads(r.read().decode("utf-8"))
    verified = v.get("verified")
    print("verified:", verified, "| found:", v.get("found"),
          "| phase:", v.get("phase"), "| status:", v.get("status"),
          "| pq_verified:", v.get("pq_verified"), "| commit:", v.get("commit_id"))

manifest = {
    "genesis_zero": True,
    "title": "APEX PSI - Reference Implementation v1.0",
    "sealed_at_utc": datetime.now(timezone.utc).isoformat(),
    "document": "genesis-zero/GENESIS_ZERO.md",
    "document_sha256": digest,
    "document_bytes": len(raw),
    "receipt": commit,
    "ledger_hash": led,
    "public_verify": verified,
    "verify_url": ("https://apex-infrastructure.com/verify/" + led) if led else None,
    "notarize_response": res,
}
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "GENESIS_ZERO_MANIFEST.json")
json.dump(manifest, open(out, "w", encoding="utf-8"), indent=2)
print("MANIFEST SAVED:", out)

