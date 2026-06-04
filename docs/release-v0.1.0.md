# Skill Routing Kit v0.1.0

Skill Routing Kit is a local-first Codex plugin that improves skill/plugin hit rate with a routing guard, capability registry, and explainable diagnostics.

## Highlights

- Installable Codex plugin with `skill-router`.
- Personal marketplace registration for Codex Desktop.
- Global `AGENTS.md` routing guard.
- Local registry builder and health checks.
- Explainable request routing with helper skills and negative examples.
- No background scanner, telemetry, connector reads, or network dependency by default.

## Install

Ask Codex:

```text
Please install the Skill Routing Kit plugin from https://github.com/juew/Skill-Routing-Kit. Install the plugin source globally at ~/plugins/skill-routing-kit, register it in ~/.agents/plugins/marketplace.json, run codex plugin add skill-routing-kit@personal, and enable the routing guard globally in ~/.codex/AGENTS.md. Do not install it into the current project. Do not ask me to create directories manually; use the repository installer and verify the plugin after installation.
```

Or run:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/juew/Skill-Routing-Kit/main/scripts/install.sh)" -- --install-agents --codex-add
```

## Validation

```bash
python3 /Users/zhonghao/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
python3 -B -m unittest discover -s tests
python3 scripts/build_registry.py --dry-run
```

## Known Limitations

- v1 uses conservative keyword/category scoring, not embeddings.
- Connector cards are routing hints, not proof of authentication.
- Registry refresh is explicit instead of automatic.
- Demo GIF and UI screenshots are planned for a future release.
