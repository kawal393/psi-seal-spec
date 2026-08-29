"""CASE 001 ROW 1 sealing ceremony - Uber written acknowledgment of APP 12 request.
Canonical artifact -> SHA-256 -> live public notarize (APEX PSI ledger,
Ed25519 + LMS-W4-SHA256 PQ layer) -> public verify-hash round-trip -> manifest.
Same ceremony as GENESIS ZERO (seal_genesis_zero.py)."""
import hashlib, json, urllib.request
from datetime import datetime, timezone

DOC_PATH = r"c:\Users\apex1\.openhands\case-001\ROW1_UBER_ACKNOWLEDGMENT_2026-08-17.md"
NOTARIZE = "https://qhtntebpcribjiwrdtdd.supabase.co/functions/v1/notarize"
VERIFY = "https://qhtntebpcribjiwrdtdd.supabase.co/functions/v1/verify-hash"

raw = open(DOC_PATH, "rb").read()
digest = hashlib.sha256(raw).hexdigest()
print("ROW 1 artifact bytes:", len(raw))
print("ROW 1 sha256:", digest)


def post(url, obj, timeout=120):
    req = urllib.request.Request(
        url, data=json.dumps(obj).encode("utf-8"),
        headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


print("== STEP 1: NOTARIZE (live public endpoint) ==")
payload = {
    "decision": ("NOTARIZE: CASE 001 ROW 1 - THE FIRST SEALED WORKER RECORD. "
                 "FACT: On 17 August 2026 at 00:46 AEST, Uber Support (agent "
                 "'Mahak', Uber Pacific Pty Ltd, Sydney) acknowledged in writing "
                 "receipt of the worker's notice and APP 12 access request and "
                 "stated it would be processed in accordance with applicable "
                 "privacy laws. Verdict: none. The ledger does not judge. "
                 "Document digest sha256:" + digest),
    "predicate": "CASE_001_ROW_1",
    "context": {
        "title": "Case 001 Row 1 - Uber acknowledgment of APP 12 request",
        "source": "case-001/ROW1_UBER_ACKNOWLEDGMENT_2026-08-17.md",
        "category": "worker-record-row",
        "case": "CASE_001",
        "row": 1,
        "event_date": "2026-08-17T00:46+10:00",
        "document_sha256": digest,
        "document_bytes": len(raw),
        "worker": "Kawaljeet Singh",
        "operator": "ROCKYFILMS888 PTY LTD ABN 71 672 237 795",
        "issued": "2026-08-29",
    },
}
res = post(NOTARIZE, payload)
print(json.dumps(res, indent=1)[:1600])

led = res.get("decision_hash") or res.get("ledger_hash") or res.get("hash")
commit = res.get("receipt_id") or res.get("commit_id")
leaf = res.get("merkle_leaf")
print("RECEIPT:", commit, "DECISION HASH:", led, "LEAF:", leaf)

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
    "case": "CASE_001",
    "row": 1,
    "title": "Uber acknowledgment of APP 12 request (17 Aug 2026)",
    "sealed_at_utc": datetime.now(timezone.utc).isoformat(),
    "document": "case-001/ROW1_UBER_ACKNOWLEDGMENT_2026-08-17.md",
    "document_sha256": digest,
    "document_bytes": len(raw),
    "receipt": commit,
    "decision_hash": led,
    "merkle_leaf": leaf,
    "public_verify": verified,
    "verify_url": ("https://apex-infrastructure.com/verify/" + led) if led else None,
    "notarize_response": res,
}
out = r"c:\Users\apex1\.openhands\case-001\ROW1_MANIFEST.json"
json.dump(manifest, open(out, "w", encoding="utf-8"), indent=2)
print("MANIFEST SAVED:", out)
