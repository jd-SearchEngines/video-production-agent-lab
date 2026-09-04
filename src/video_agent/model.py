"""Model boundary used by v0.3 without requiring an external provider."""

from __future__ import annotations

from typing import Any, Dict, Protocol


class ModelProtocol(Protocol):
    def respond(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]: ...


class ScriptedModel:
    """Deterministic stand-in for a model; it never calls a provider."""

    provider = None
    model = None

    def respond(self, prompt: str, context: Dict[str, Any]) -> Dict[str, Any]:
        return {"prompt": prompt, "context_keys": sorted(context), "provider": None, "model": None}
