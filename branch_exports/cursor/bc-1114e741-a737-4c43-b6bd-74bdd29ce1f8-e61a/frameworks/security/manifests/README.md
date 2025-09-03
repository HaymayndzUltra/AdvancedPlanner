# Handoff Manifests

Sealed manifests record immutable handoffs for each cycle. Do not modify sealed manifests.

- Include: manifest_version, cycle, snapshot_rev, rulebook_hash, artifacts with sha256, quality_gates, signing, sealed flag
- Any change requires a new manifest under a new cycle path