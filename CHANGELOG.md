# Changelog

## 0.1.0

Initial public release of Skill Routing Kit.

### Added

- Codex plugin manifest with `skill-router` skill exposure.
- Local-first installer for `~/plugins/skill-routing-kit`.
- Personal marketplace registration in `~/.agents/plugins/marketplace.json`.
- Optional `codex plugin add skill-routing-kit@personal` activation.
- Global `AGENTS.md` routing guard installer.
- Local capability registry and generated registry builder.
- Request routing diagnostics with explainable scoring.
- Registry health checks for staleness, schema mismatch, and missing provenance.
- Product logo and composer icon assets.
- Bilingual documentation.

### Fixed

- Personal marketplace install path now matches Codex Desktop plugin discovery.
- Routing diagnostics now prefer `skill-router` over a domain skill that is merely mentioned.
- Helper candidates now filter weak matches while preserving useful negative examples.
