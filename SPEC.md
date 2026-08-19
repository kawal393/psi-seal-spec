# PSI-SEAL/1 - Normative Specification

Apex PSI — Universal Verification Layer. Proposed open standard under active development. Verification free forever (MIT). IETF drafts are individual submissions, not formally endorsed. Verify everything yourself.

Canonical machine-readable copy: https://ai-governance-standard.com/.well-known/psi-schema.json

## Envelope field set (closed, R2)

| Field | Type | Rule |
|---|---|---|
| schema | string | "PSI-SEAL/1.0.0" |
| schema_digest | string | SHA-256 over JCS of the canonical schema document, lowercase hex (R4) |
| sealed_at | string | RFC 3339 UTC, three fractional digits, literal Z (R6) |
| subject | object | name (NFC UTF-8), size_bytes (exact octet length) (R7) |
| hash | string | SHA-256 over raw octet stream of subject (R5) |
| merkle | object | leaf = SHA-256("PSI1:" || hash) (R9); root per R8 |
| signature | object | Ed25519 over ASCII seal_hash; optional hybrid LMS-W4-SHA256 (R11) |
| licence | object | issuance licence reference |

## Normative rules

R1  Envelope serialisation: RFC 8785 JSON Canonicalization Scheme (JCS), UTF-8, no BOM.
R2  Field set is closed. Unknown top-level fields render a seal non-conformant.
R3  Field order in the emitted receipt: schema, schema_digest, sealed_at, subject, hash, merkle, signature, licence.
R4  Digests: lowercase hexadecimal, exactly 64 characters, no 'sha256:' prefix inside the envelope.
R5  Hash algorithm: SHA-256 over the raw octet stream of the subject; no transport encoding, no trailing padding.
R6  sealed_at: RFC 3339 UTC with exactly three fractional digits and a literal 'Z' (e.g. 2026-08-17T09:00:00.000Z).
R7  subject.size_bytes: non-negative integer, exact octet length. subject.name: NFC-normalised UTF-8 string.
R8  Merkle assembly: binary tree over leaf digests in submission order; each parent = SHA-256(left_bytes || right_bytes) over 32-byte raw digests; an odd node is promoted, never duplicated.
R9  merkle.leaf = SHA-256 of the ASCII string 'PSI1:' || hash. Domain separation is mandatory.
R10 seal_hash = SHA-256(JCS(envelope minus the signature and licence members)).
R11 Signature suite: Ed25519 over the ASCII seal_hash; optional hybrid post-quantum LMS-W4-SHA256 (NIST SP 800-208).
R12 Every seal MUST carry schema and schema_digest. Only schema-conformant seals are considered PSI-compliant.

## Conformance

Only schema-conformant seals are considered PSI-compliant. Outputs that deviate
from this specification fail verification even if functionally similar. Seals
are deterministic mathematical statements about byte state and time. They are
never a personal certification or a statement of fact about the sealed content.

## Licensing

- Verification: MIT - free forever, for everyone, no permission required.
- Issuance: APEX PSI Sealing Engine Licence v1 (personal use free; commercial
  use PSI-05 royalty terms).
