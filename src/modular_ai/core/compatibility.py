"""Reference manifest compatibility checks, independent of any model framework.

This is a design-time validator, not a model loader or proof of numerical safety.
Registry definitions own their ports and artifact fingerprints; workflows own wiring.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


@dataclass(frozen=True)
class Diagnostic:
    code: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {"code": self.code, "message": self.message}


@dataclass(frozen=True)
class CompatibilityReport:
    status: str
    diagnostics: tuple[Diagnostic, ...]
    connections: tuple[dict[str, str | bool], ...] = ()

    def as_dict(self) -> dict[str, Any]:
        return {"status": self.status, "diagnostics": [x.as_dict() for x in self.diagnostics],
                "connections": list(self.connections)}


def validate_manifest(manifest: Mapping[str, Any], registry: Mapping[str, Any]) -> CompatibilityReport:
    """Check declared structure, semantic ports and artifact fingerprints.

    Statuses: compatible, unverified, migration, incompatible. An unresolved
    external checkpoint always yields unverified, never claims executable safety.
    """
    modules = registry["modules"]
    diagnostics: list[Diagnostic] = []
    ranks = {"compatible": 0, "unverified": 1, "migration": 2, "incompatible": 3}
    severity = "compatible"
    connections: list[dict[str, str | bool]] = []

    def flag(status: str, code: str, message: str) -> None:
        nonlocal severity
        diagnostics.append(Diagnostic(code, message))
        if ranks[status] > ranks[severity]:
            severity = status

    workflow = manifest.get("workflow", {})
    if not isinstance(workflow, dict):
        return CompatibilityReport("incompatible", (Diagnostic("workflow", "Workflow must be an object"),))
    workflow_id = workflow.get("use")
    definition = modules.get(workflow_id)
    if not definition or definition.get("category") != "workflow":
        return CompatibilityReport("incompatible", (Diagnostic("workflow", f"Unknown workflow: {workflow_id}"),))
    slots = workflow.get("slots", {})
    if not isinstance(slots, dict):
        return CompatibilityReport("incompatible", (Diagnostic("slots", "Slots must be an object"),))
    allowed = definition["slots"] + definition.get("optional_slots", [])
    for slot in definition["slots"]:
        if slot not in slots:
            flag("incompatible", "missing-slot", f"Missing required slot: {slot}")
    for slot, module_id in slots.items():
        if slot not in allowed:
            flag("incompatible", "unexpected-slot", f"Unknown slot: {slot}")
        elif module_id not in modules or modules[module_id].get("category") == "workflow":
            flag("incompatible", "unknown-module", f"Unknown module: {module_id} in {slot}")
        elif modules[module_id].get("category") != definition["slot_categories"][slot]:
            flag("incompatible", "wrong-category", f"Slot {slot} requires {definition['slot_categories'][slot]}, not {modules[module_id]['category']}")

    if severity == "incompatible":
        return CompatibilityReport(severity, tuple(diagnostics), tuple(connections))

    for link in definition["links"]:
        condition = link.get("when_present")
        excluded = link.get("when_absent")
        if condition and condition not in slots:
            continue
        if excluded and excluded in slots:
            continue
        from_slot, from_port = link["from"].split(".", 1)
        to_slot, to_port = link["to"].split(".", 1)
        if from_slot not in slots or to_slot not in slots:
            flag("incompatible", "missing-link-slot", f"Cannot resolve link {link['from']} → {link['to']}")
            continue
        output = modules[slots[from_slot]].get("output", {}).get(from_port)
        expected = modules[slots[to_slot]].get("input", {}).get(to_port)
        connections.append({"from": link["from"], "to": link["to"],
                            "actual": output or "missing", "expected": expected or "missing",
                            "matches": bool(output and expected and output == expected)})
        if output is None or expected is None or output != expected:
            flag("incompatible", "port-mismatch", f"{from_slot}.{from_port} ({output or 'missing'}) → {to_slot}.{to_port} ({expected or 'missing'})")

    provided: dict[str, tuple[str, str]] = {}
    for slot, module_id in slots.items():
        for key, fingerprint in modules[module_id].get("provides", {}).items():
            if key in provided and provided[key][0] != fingerprint:
                flag("migration", "ambiguous-artifact", f"Conflicting {key} fingerprints from {provided[key][1]} and {slot}")
            else:
                provided[key] = (fingerprint, slot)
    for slot, module_id in slots.items():
        for key, fingerprint in modules[module_id].get("requires", {}).items():
            actual = provided.get(key)
            if actual is None:
                flag("unverified", "missing-artifact-binding", f"{slot} requires {key}={fingerprint}; no provider declared")
            elif actual[0] != fingerprint:
                flag("migration", "artifact-mismatch", f"{slot} requires {key}={fingerprint}, but {actual[1]} provides {actual[0]}")

    artifacts = manifest.get("artifacts", {})
    if not isinstance(artifacts, dict):
        flag("incompatible", "artifacts", "Artifacts must be an object")
    else:
        for name, ref in artifacts.items():
            if not isinstance(ref, str) or ref.startswith("unresolved:"):
                flag("unverified", "unresolved-artifact", f"{name}: a validated artifact is not available")

    return CompatibilityReport(severity, tuple(diagnostics), tuple(connections))
