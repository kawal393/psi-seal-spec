"""Core module: canonicalisation, sealing, adapters, LangChain callback handler."""
from __future__ import annotations

import hashlib
import json
import time
from typing import Any, Callable, Dict, List, Optional

from langchain_core.callbacks.base import BaseCallbackHandler
from langchain_core.outputs import LLMResult

DEFAULT_VERIFY_BASE = "https://www.ai-governance-standard.com"


def canonical_json(obj: Any) -> bytes:
    """RFC 8785-style canonical serialisation: sorted keys, compact separators, UTF-8."""
    return json.dumps(
        obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False
    ).encode("utf-8")


def psi_seal(payload: Dict[str, Any]) -> str:
    """Deterministic seal: SHA-256 over the canonical record."""
    return hashlib.sha256(canonical_json(payload)).hexdigest()


def seal_text(text: str, **meta: Any) -> Dict[str, Any]:
    """Seal an arbitrary text blob (convenience for non-LangChain use)."""
    payload: Dict[str, Any] = {
        "output_sha256": hashlib.sha256(text.encode("utf-8")).hexdigest(),
        "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "kind": "text",
    }
    payload.update(meta)
    seal = psi_seal(payload)
    return {
        "seal": seal,
        "payload": payload,
        "verify_url": f"{DEFAULT_VERIFY_BASE}/verify?hash={seal}",
    }


class VerifierAdapter:
    """Neutral interface: any provenance standard can plug in."""

    name = "base"

    def attest(self, seal: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError


class PSIAdapter(VerifierAdapter):
    """APEX PSI: deterministic seal + public, free, account-free verification."""

    name = "apex-psi"

    def __init__(self, verify_base: str = DEFAULT_VERIFY_BASE):
        self.verify_base = verify_base.rstrip("/")

    def attest(self, seal: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "standard": self.name,
            "seal": seal,
            "verify_url": f"{self.verify_base}/verify?hash={seal}",
        }


class OpenTimestampsAdapter(VerifierAdapter):
    """Note adapter: Bitcoin anchoring happens externally; receipt attaches to seal."""

    name = "opentimestamps"

    def attest(self, seal: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "standard": self.name,
            "seal": seal,
            "note": "anchor externally via opentimestamps.org; OTS receipt attaches to this seal",
        }


class C2PANoteAdapter(VerifierAdapter):
    """Note adapter: embed the seal as a claim inside a C2PA manifest pipeline."""

    name = "c2pa-note"

    def attest(self, seal: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "standard": self.name,
            "seal": seal,
            "note": "embed this seal as a C2PA claim in your manifest pipeline",
        }


class ProvenanceCallbackHandler(BaseCallbackHandler):
    """Opt-in handler: seals every LLM output; adapters attest each seal.

    Default OFF everywhere. Nothing is transmitted by this handler; adapters
    only emit local attestations (URLs / notes) unless you wire one to submit.
    """

    def __init__(
        self,
        adapters: Optional[List[VerifierAdapter]] = None,
        include_input_digest: bool = False,
        on_receipt: Optional[Callable[[Dict[str, Any]], None]] = None,
    ):
        super().__init__()
        self.adapters: List[VerifierAdapter] = adapters or [PSIAdapter()]
        self.include_input_digest = include_input_digest
        self.on_receipt = on_receipt
        self.receipts: List[Dict[str, Any]] = []

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> None:
        for gens in response.generations:
            for g in gens:
                text = getattr(g, "text", None) or str(getattr(g, "message", ""))
                payload: Dict[str, Any] = {
                    "output_sha256": hashlib.sha256(
                        text.encode("utf-8")
                    ).hexdigest(),
                    "ts": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "kind": "llm-output",
                }
                if self.include_input_digest and kwargs.get("inputs") is not None:
                    payload["input_sha256"] = hashlib.sha256(
                        canonical_json(kwargs["inputs"])
                    ).hexdigest()
                seal = psi_seal(payload)
                receipt = {
                    "seal": seal,
                    "payload": payload,
                    "attestations": [a.attest(seal, payload) for a in self.adapters],
                }
                self.receipts.append(receipt)
                if self.on_receipt is not None:
                    self.on_receipt(receipt)

    def latest(self) -> Optional[Dict[str, Any]]:
        return self.receipts[-1] if self.receipts else None
