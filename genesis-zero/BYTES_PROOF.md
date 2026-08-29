# BYTES PROOF — GENESIS ZERO

The sealed digest binds EXACTLY these bytes (2032 bytes, CRLF newlines, UTF-8, no BOM):

```
f91ba473ee1e88b349d3a4dee18a27d9d8adbc3e1ef1e32aadcd94960a7b7b9b
```

## Recompute from this repository, byte-exact

A `.gitattributes` rule (`-text`) stores the sealed file with zero newline
normalisation. Download the raw file and hash it:

```powershell
# Windows
curl.exe -s https://raw.githubusercontent.com/kawal393/psi-seal-spec/main/genesis-zero/GENESIS_ZERO.md -o GENESIS_ZERO.md
certutil -hashfile GENESIS_ZERO.md SHA256
```

```bash
# Linux/macOS
curl -s https://raw.githubusercontent.com/kawal393/psi-seal-spec/main/genesis-zero/GENESIS_ZERO.md -o GENESIS_ZERO.md
sha256sum GENESIS_ZERO.md
```

Both must print `f91ba473ee1e88b349d3a4dee18a27d9d8adbc3e1ef1e32aadcd94960a7b7b9b`.

Or, after `git clone`, read the committed blob directly:

```python
import subprocess, hashlib
blob = subprocess.check_output(["git", "show", "HEAD:genesis-zero/GENESIS_ZERO.md"])
print(hashlib.sha256(blob).hexdigest())
# must print: f91ba473ee1e88b349d3a4dee18a27d9d8adbc3e1ef1e32aadcd94960a7b7b9b
```

If you get a different digest, publish the divergence — the correction
protocol is part of the standard.

## Live public receipt

- Receipt: APEX-NTR-C29D90C714C99F96 (VERIFIED / APPROVED, PQ-signed)
- https://apex-infrastructure.com/verify/d60e050719f8be3223c5e51e1cc80a990fad552a4b1692fb2c042097e626e04e
- https://ai-governance-standard.com/verify?hash=d60e050719f8be3223c5e51e1cc80a990fad552a4b1692fb2c042097e626e04e
