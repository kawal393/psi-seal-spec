# langchain-apex-psi

Neutral provenance receipts for LangChain runs. Opt-in, zero network calls by
default, multi-standard by design: APEX PSI is one adapter among equals
(OpenTimestamps and C2PA note adapters ship in the box).

Part of the APEX PSI reference family:
https://github.com/kawal393/psi-seal-spec (MIT).

## What it does

Every LLM output that passes through the handler is sealed:

1. `output_sha256` = SHA-256 of the exact output bytes.
2. Record (digest + UTC timestamp + kind, optional input digest) is
   canonicalised RFC 8785-style and sealed: `seal = SHA-256(canonical record)`.
3. Each configured adapter attests the seal (verification URL for APEX PSI,
   anchoring note for OpenTimestamps, manifest note for C2PA).

The seal is deterministic: identical bytes produce an identical seal on any
machine, and anyone can recompute it. That is the whole point - a provenance
claim you can check, not a label you must trust.

## Usage

```python
from langchain_apex_psi import (
    ProvenanceCallbackHandler, PSIAdapter, OpenTimestampsAdapter, C2PANoteAdapter,
)

handler = ProvenanceCallbackHandler(
    adapters=[PSIAdapter(), OpenTimestampsAdapter(), C2PANoteAdapter()]
)

# any LangChain runnable:
result = chain.invoke(inputs, config={"callbacks": [handler]})

receipt = handler.latest()
print(receipt["seal"])
print(receipt["attestations"][0]["verify_url"])
```

Default is OFF everywhere. Nothing is transmitted unless you wire an adapter
to submit receipts to a ledger of your choice.

## EU AI Act Article 50

A recomputable, timestamped seal per output is the kind of machine-readable
evidence Article 50(2) of Regulation (EU) 2024/1689 names: effective,
interoperable, robust and reliable. See the companion technical note
`docs/APEX_ARTICLE50_TECHNICAL_NOTE.pdf` in the repository root. This package
is not legal advice and does not determine legal compliance.

## Fences

- A seal certifies existence, timestamp and integrity of a record - not the
  truth of its claims.
- Verification is free, account-free, and licensed for perpetual public use.
- If two public verification doors ever disagree, the correction is public and
  the finder is credited.

## Test

```
python tests/test_smoke.py
```
