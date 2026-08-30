"""langchain-apex-psi - neutral provenance receipts for LangChain runs.

Opt-in, multi-standard adapters (APEX PSI, OpenTimestamps note, C2PA note).
Part of the APEX PSI reference family: https://github.com/kawal393/psi-seal-spec
License: MIT.

A seal certifies existence, timestamp and integrity of a record - not the
truth of its claims. This package is not legal advice and does not determine
legal compliance.
"""
from .core import (
    C2PANoteAdapter,
    OpenTimestampsAdapter,
    PSIAdapter,
    ProvenanceCallbackHandler,
    VerifierAdapter,
    canonical_json,
    psi_seal,
    seal_text,
)

__version__ = "0.1.0"

__all__ = [
    "ProvenanceCallbackHandler",
    "VerifierAdapter",
    "PSIAdapter",
    "OpenTimestampsAdapter",
    "C2PANoteAdapter",
    "canonical_json",
    "psi_seal",
    "seal_text",
    "__version__",
]
