# psi-seal-spec

**Apex PSI - Universal Verification Layer.**

Apex PSI — Universal Verification Layer. Proposed open standard under active development. Verification free forever (MIT). IETF drafts are individual submissions, not formally endorsed. Verify everything yourself.

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

## Verify the Verifier

Every line here is MIT. Audit it. Report a divergence: you are credited in
SECURITY.md and merged into the record. The math must survive its maker.

Companion implementations:
- TypeScript verifier: https://github.com/kawal393/apex-psi-verify
- Python verifier: https://github.com/kawal393/apex-verify-python

## License

MIT - free forever, for everyone, no permission required.
