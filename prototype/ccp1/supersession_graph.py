from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Iterable, Mapping, Optional, Tuple
import copy

from prototype.ccp0.ccp import ValidationError


class SupersessionGraphError(ValidationError):
    """Raised when a scoped supersession graph would become ambiguous or cyclic."""


@dataclass(frozen=True)
class SupersessionEdge:
    prior: str
    superseding: str
    key: str
    reason: str
    authority: str


@dataclass(frozen=True)
class ResolvedKey:
    key: str
    value: Any
    terminal_claim: str
    chain: Tuple[str, ...]


@dataclass(frozen=True)
class ClaimResolution:
    root_claim: str
    resolved: Mapping[str, ResolvedKey]

    @property
    def values(self) -> Dict[str, Any]:
        return {
            key: copy.deepcopy(item.value)
            for key, item in sorted(self.resolved.items())
        }

    @property
    def provenance(self) -> Dict[str, Tuple[str, ...]]:
        return {
            key: item.chain
            for key, item in sorted(self.resolved.items())
        }

    def compact_summary(self) -> Dict[str, Any]:
        """Current-state summary whose width depends on resolved keys, not graph size."""
        return {
            "root_claim": self.root_claim,
            "values": self.values,
            "terminals": {
                key: item.terminal_claim
                for key, item in sorted(self.resolved.items())
            },
        }


class ScopedSupersessionGraph:
    """Deterministic per-subclaim supersession graph.

    For each (prior claim, key), at most one outgoing replacement is permitted.
    That means a current value can be followed deterministically without using
    event ordering to resolve same-scope forks.
    """

    def __init__(self) -> None:
        self._claims: Dict[str, Dict[str, Any]] = {}
        self._successor: Dict[Tuple[str, str], SupersessionEdge] = {}

    @property
    def claims(self) -> Dict[str, Dict[str, Any]]:
        return copy.deepcopy(self._claims)

    @property
    def edge_count(self) -> int:
        return len(self._successor)

    def register_claim(self, claim_id: str, value: Mapping[str, Any]) -> None:
        if not claim_id:
            raise ValidationError("claim_id is required")
        if not isinstance(value, Mapping):
            raise ValidationError("scoped supersession requires mapping-valued claims")
        normalized = copy.deepcopy(dict(value))
        existing = self._claims.get(claim_id)
        if existing is not None:
            if existing == normalized:
                return
            raise ValidationError(
                f"claim {claim_id!r} is immutable and already bound differently"
            )
        self._claims[claim_id] = normalized

    def _next(self, claim_id: str, key: str) -> Optional[SupersessionEdge]:
        return self._successor.get((claim_id, key))

    def _would_cycle(self, prior: str, superseding: str, key: str) -> bool:
        current = superseding
        seen = {prior}
        while True:
            if current in seen:
                return True
            seen.add(current)
            edge = self._next(current, key)
            if edge is None:
                return False
            current = edge.superseding

    def add_edge(
        self,
        *,
        prior: str,
        superseding: str,
        keys: Iterable[str],
        reason: str,
        authority: str,
    ) -> Tuple[SupersessionEdge, ...]:
        if prior not in self._claims:
            raise SupersessionGraphError(f"unknown prior claim {prior!r}")
        if superseding not in self._claims:
            raise SupersessionGraphError(f"unknown superseding claim {superseding!r}")
        if prior == superseding:
            raise SupersessionGraphError("self-supersession is forbidden")
        if not reason or not authority:
            raise ValidationError("supersession reason and authority are required")

        scoped_keys = tuple(sorted(set(keys)))
        if not scoped_keys:
            raise SupersessionGraphError("supersession requires at least one key")

        # Validate the whole proposed edge-set before mutating the graph.
        for key in scoped_keys:
            if key not in self._claims[superseding]:
                raise SupersessionGraphError(
                    f"replacement claim {superseding!r} does not contain key {key!r}"
                )
            existing = self._successor.get((prior, key))
            if existing is not None:
                if existing.superseding == superseding:
                    raise SupersessionGraphError(
                        f"duplicate supersession for {prior!r}/{key!r} already exists"
                    )
                raise SupersessionGraphError(
                    f"ambiguous same-key fork for {prior!r}/{key!r}: "
                    f"{existing.superseding!r} vs {superseding!r}"
                )
            if self._would_cycle(prior, superseding, key):
                raise SupersessionGraphError(
                    f"supersession would create cycle for key {key!r}"
                )

        created = []
        for key in scoped_keys:
            edge = SupersessionEdge(
                prior=prior,
                superseding=superseding,
                key=key,
                reason=reason,
                authority=authority,
            )
            self._successor[(prior, key)] = edge
            created.append(edge)
        return tuple(created)

    def resolve_key(self, root_claim: str, key: str) -> ResolvedKey:
        if root_claim not in self._claims:
            raise KeyError(root_claim)
        if key not in self._claims[root_claim]:
            raise KeyError(f"{root_claim}:{key}")

        chain = [root_claim]
        current = root_claim
        seen = {root_claim}

        while True:
            edge = self._next(current, key)
            if edge is None:
                break
            current = edge.superseding
            if current in seen:
                # Defensive check: graph construction should already prevent this.
                raise SupersessionGraphError(
                    f"cycle encountered during resolution for key {key!r}"
                )
            seen.add(current)
            chain.append(current)

        return ResolvedKey(
            key=key,
            value=copy.deepcopy(self._claims[current][key]),
            terminal_claim=current,
            chain=tuple(chain),
        )

    def resolve_claim(self, root_claim: str) -> ClaimResolution:
        if root_claim not in self._claims:
            raise KeyError(root_claim)
        resolved = {
            key: self.resolve_key(root_claim, key)
            for key in sorted(self._claims[root_claim])
        }
        return ClaimResolution(root_claim=root_claim, resolved=resolved)
