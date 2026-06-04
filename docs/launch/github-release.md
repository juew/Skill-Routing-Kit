# GitHub Release And Repo Setup

## Repository Topics

Add these topics in GitHub repository settings:

- `codex`
- `codex-plugin`
- `ai-agents`
- `agent-workflows`
- `skill-routing`
- `local-first`
- `developer-tools`
- `llm-tools`

## Release Title

```text
Skill Routing Kit v0.1.0: local-first routing for Codex skills and plugins
```

## Release Body

````md
Skill Routing Kit is a local-first Codex plugin that improves skill/plugin hit rate with a routing guard, capability registry, and explainable diagnostics.

Codex can have many skills and plugins installed, but the right one does not always trigger. This release focuses on making routing decisions more explicit: what should be primary, what should be helper context, and when a tempting skill should not be used.

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

## Demo

```bash
python3 scripts/route_request.py "为什么 pdf skill 没有命中这个请求"
```

Expected:

```text
Recommended skill/plugin:
- Skill Router (skill-router)

Helper skills/plugins:
- PDF (pdf)
```

## Known limitations

- v1 uses conservative keyword/category scoring, not embeddings.
- Connector cards are routing hints, not proof of authentication.
- Registry refresh is explicit instead of automatic.
- Demo GIF and UI screenshots are planned next.
````

## Discussion Post

Create a GitHub Discussion titled:

```text
Share your missed skill-routing cases
```

Body:

````md
Skill Routing Kit is built around a practical question:

> When did Codex pick the wrong skill or plugin, and what signal should have routed it correctly?

If you have a missed-routing case, please share:

- User request
- Expected primary skill/plugin
- Actual or likely wrong route
- Why the wrong route was tempting
- Any negative example that would help

Useful examples may become routing regression tests.
````
