# psi-seal-spec

**Apex PSI - Universal Verification Layer.**

Apex PSI — Universal Verification Layer. Proposed open standard under active development. Verification free forever (MIT). IETF drafts are individual submissions, not formally endorsed. Verify everything yourself.

## GENESIS ZERO — sealed 29 August 2026

The reference implementation declaration, sealed live against the public APEX PSI ledger:

- Document: `genesis-zero/GENESIS_ZERO.md`
- Document SHA-256: `f91ba473ee1e88b349d3a4dee18a27d9d8adbc3e1ef1e32aadcd94960a7b7b9b`
- Receipt: `APEX-NTR-C29D90C714C99F96` (VERIFIED / APPROVED, PQ-signed LMS-W4-SHA256)
- Sealed decision hash: `d60e050719f8be3223c5e51e1cc80a990fad552a4b1692fb2c042097e626e04e`
- Merkle leaf: `b9895d1bd7ce676c46d251a72544f5b6463e501a6fd173626b2199c0a2fe0480`

Verify it yourself:

```
certutil -hashfile genesis-zero\GENESIS_ZERO.md SHA256   # Windows
sha256sum genesis-zero/GENESIS_ZERO.md                   # Linux/macOS
```

Match the printed digest against the live public receipt:

- https://apex-infrastructure.com/verify/d60e050719f8be3223c5e51e1cc80a990fad552a4b1692fb2c042097e626e04e
- https://ai-governance-standard.com/verify?hash=d60e050719f8be3223c5e51e1cc80a990fad552a4b1692fb2c042097e626e04e

The sealing ceremony is reproducible: `genesis-zero/seal_genesis_zero.py`
(canonical bytes → SHA-256 → live public notarize → public verify round-trip).
If the math breaks, the correction is public. Money buys process, never outcome.

## CASE 001 — THE FIRST SEALED WORKER RECORD (live)

The reference applied to a worker: every row is one fact + one document hash +
one timestamp + one public seal. Facts only — no verdict is rendered.

ROW 1 — sealed 29 August 2026:

- Fact: on 17 Aug 2026, 00:46 AEST, Uber Support (agent 'Mahak',
  Uber Pacific Pty Ltd, Sydney) acknowledged in writing receipt of the worker's
  notice and APP 12 access request.
- Artifact: `case-001/ROW1_UBER_ACKNOWLEDGMENT_2026-08-17.md`
- Artifact SHA-256: `f57d4b3e7e558480f828dc5b20ba8878418ad049ee4134d35f97893c9352d10b`
- Receipt: `APEX-NTR-20E2092FA5304F81` (VERIFIED / APPROVED, PQ-signed)
- Sealed decision hash: `ee74bacdbef9e4dce922f9cba0d253e4084564ba6efe59fd7ee20b223917a2ef`
- Merkle leaf: `c445a235185cea8879b323dad8988b6efb35e3960da129543947704260b77533`

Verify: recompute the artifact digest, then match against the live receipt:

```
certutil -hashfile case-001\ROW1_UBER_ACKNOWLEDGMENT_2026-08-17.md SHA256
```

- https://apex-infrastructure.com/verify/ee74bacdbef9e4dce922f9cba0d253e4084564ba6efe59fd7ee20b223917a2ef
- https://ai-governance-standard.com/verify?hash=ee74bacdbef9e4dce922f9cba0d253e4084564ba6efe59fd7ee20b223917a2ef

The record grows every time evidence lands. The ledger does not judge. It remembers.

## Prove it in 60 seconds

A seal is deterministic math. Two implementations, two languages, zero shared
code - identical bytes.

```
python hello-psi/hello_psi.py  > py.out
node   hello-psi/hello-psi.js  > js.out
fc /b py.out js.out            # Windows   (use diff on Linux/macOS)
```

No differences = the protocol is real. That is the entire pitch. Both seeds
run fully offline: the schema digest is pinned in both files
(`454743...fe9e77`, computed 2026-08-20 from the live canonical schema).
To confirm the pin is still current:

```
python hello-psi/hello_psi.py --check-live
node   hello-psi/hello-psi.js --check-live
```

Both must print `pin_current : yes`.

## Layout

- `SPEC.md` - PSI-SEAL/1 normative rules R1-R12 (mirrors the live
  `/.well-known/psi-schema.json`)
- `hello-psi/hello_psi.py` - Python reference seed (stdlib only)
- `hello-psi/hello-psi.js` - JavaScript reference seed (Node 18+, zero deps)
- `hello-psi/vectors.json` - machine-readable test vectors, generated from the
  actual identical output of both seeds - never hand-typed
- `genesis-zero/` - Genesis Zero declaration, sealed receipt manifest, and the
  reproducible sealing script (29 Aug 2026)
- `case-001/` - The First Sealed Worker Record: row artifacts, sealed receipt
  manifests, and reproducible row-sealing scripts

## Verify the Verifier

Every line here is MIT. Audit it. Report a divergence: you are credited in
SECURITY.md and merged into the record. The math must survive its maker.

Companion implementations:
- TypeScript verifier: https://github.com/kawal393/apex-psi-verify
- Python verifier: https://github.com/kawal393/apex-verify-python

## License

MIT - free forever, for everyone, no permission required.
