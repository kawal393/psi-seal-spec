"""Smoke test: determinism, handler wiring, multi-standard attestations."""
import hashlib
import sys

from langchain_core.outputs import Generation, LLMResult

from langchain_apex_psi import (
    C2PANoteAdapter,
    OpenTimestampsAdapter,
    PSIAdapter,
    ProvenanceCallbackHandler,
    canonical_json,
    psi_seal,
    seal_text,
)

TEXT = "The ledger does not judge. It remembers."


def main() -> int:
    handler = ProvenanceCallbackHandler(
        adapters=[PSIAdapter(), OpenTimestampsAdapter(), C2PANoteAdapter()]
    )
    response = LLMResult(generations=[[Generation(text=TEXT)]])
    handler.on_llm_end(response)

    assert len(handler.receipts) == 1, "expected exactly one receipt"
    r = handler.latest()

    # determinism: recompute the seal from the payload, must match
    assert psi_seal(r["payload"]) == r["seal"], "seal not deterministic"

    # output digest matches the raw text
    assert r["payload"]["output_sha256"] == hashlib.sha256(
        TEXT.encode("utf-8")
    ).hexdigest(), "output digest mismatch"

    # three standards attested
    names = [a["standard"] for a in r["attestations"]]
    assert names == ["apex-psi", "opentimestamps", "c2pa-note"], names

    # verify url carries the seal
    url = r["attestations"][0]["verify_url"]
    assert url.endswith("hash=" + r["seal"]), url

    # different text -> different seal
    other = seal_text("other bytes")
    assert other["seal"] != r["seal"], "collision on distinct input"

    # canonical json is stable across key order
    a = canonical_json({"x": 1, "y": 2})
    b = canonical_json({"y": 2, "x": 1})
    assert a == b, "canonicalisation not order-stable"

    print("SEAL", r["seal"])
    print("VERIFY", url)
    print("SMOKE PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
