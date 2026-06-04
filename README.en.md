# Skill Routing Kit

Skill Routing Kit is a local-first Codex plugin for improving skill and plugin hit rate without adding a slow or invasive runtime layer.

It provides:

- an always-on routing guard as a short `AGENTS.md` snippet
- a local registry of skill/plugin capability cards
- a manual diagnostic command for routing a request
- explicit registry refresh and health-check commands
- clear removal steps

The kit is designed for users whose primary work lives in local repositories and local files, while external connectors are used only when explicitly named, clearly required, or confirmed.

## Design Principles

1. **Improve hit rate without noise**  
   The routing guard is a silent micro-check. It should improve selection of process skills, artifact skills, and connector plugins without printing a routing report for every ordinary task.

2. **Local-first by default**  
   Local files, repositories, browser verification, and build/test commands are preferred. External connectors are elevated only when the user names them, the source of truth clearly lives there, or the user confirms access.

3. **Fast lookup, no per-turn scanning**  
   The registry is a local JSON index. It is refreshed manually or on demand, not rebuilt during every conversation turn.

4. **Conservative connectors**  
   Registry generation does not read Gmail, Slack, Notion, Drive, or any connector content. Connector cards only indicate possible relevance and never prove access.

5. **Easy removal**  
   The kit does not install hooks, telemetry, background scanners, or runtime interception. Removing the AGENTS snippet, generated registry, and plugin directory restores normal Codex behavior.

## Implementation Logic

The system has three layers:

```text
Always-on Routing Guard
  Short AGENTS.md rule that silently classifies task/source/artifact/process need.

Registry
  Local layered capability index: process, source, artifact, domain, risk.

Diagnostic Plugin
  Manual tools to route a request, inspect stale registry state, and debug skill descriptions.
```

The routing guard is the part that improves daily hit rate. The registry and diagnostic script help it stay maintainable and explainable.

## Installation

### Recommended: ask Codex to install it

If you are not comfortable with terminals, directory structures, or plugin setup, paste this into Codex:

```text
Please install the Skill Routing Kit plugin from https://github.com/juew/Skill-Routing-Kit into the global Codex plugin directory, normally ~/.codex/plugins/skill-routing-kit. Do not install the plugin into the current project. Only enable the routing guard in the current project's AGENTS.md. Do not ask me to create directories manually; use the repository installer and verify the plugin after installation.
```

Codex should handle:

- downloading or cloning the repository
- creating local directories
- installing plugin files
- adding the `AGENTS.md` routing guard when requested
- running basic validation

You should not need to manually create `.codex-plugin`, `skills`, or `registry` directories.

### One-command install

If you are comfortable running one terminal command:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/juew/Skill-Routing-Kit/main/scripts/install.sh)" -- --install-agents
```

By default, this installs the plugin to:

```text
~/.codex/plugins/skill-routing-kit
```

and writes the routing guard to:

```text
~/.codex/AGENTS.md
```

To install only the plugin without writing `AGENTS.md`:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/juew/Skill-Routing-Kit/main/scripts/install.sh)"
```

To write the routing guard into a specific project:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/juew/Skill-Routing-Kit/main/scripts/install.sh)" -- --install-agents --agents "/path/to/project/AGENTS.md"
```

Restart Codex or reload plugins if the new plugin does not appear immediately.

### Advanced: manual install

The plugin layout is shown here only for maintainers and advanced troubleshooting:

```text
skill-routing-kit/
├── .codex-plugin/plugin.json
├── skills/skill-router/SKILL.md
├── scripts/
├── registry/
├── examples/
└── assets/
```

The always-on routing guard lives at:

```text
assets/agents-routing-snippet.md
```

The snippet is marked so it can be removed safely:

```text
BEGIN Skill Routing Kit
END Skill Routing Kit
```

## Daily Usage

Most of the time, do nothing special. Ask Codex normally.

The AGENTS snippet makes Codex silently check:

- task type
- source location
- final artifact
- process skill need
- connector relevance

Ordinary tasks should not show a routing report.

For complex, ambiguous, multi-artifact, or long-running tasks, Codex may show a brief routing check:

```text
Primary skill: ...
Helper skills: ...
Source: ...
Verification path: ...
```

## Route A Request Manually

Use the diagnostic script when you want to inspect routing explicitly:

```bash
python3 scripts/route_request.py "Turn this PDF into a slide deck"
```

Debug mode:

```bash
python3 scripts/route_request.py --debug "Fix this frontend error"
```

Check registry health:

```bash
python3 scripts/route_request.py --check-registry
```

Refresh then route:

```bash
python3 scripts/route_request.py --refresh "Analyze this CSV and create an Excel report"
```

## Update The Registry

Refresh the generated registry after installing, removing, or editing skills/plugins:

```bash
python3 scripts/build_registry.py --yes
```

Dry run:

```bash
python3 scripts/build_registry.py --dry-run
```

Custom output:

```bash
python3 scripts/build_registry.py --output registry/capabilities.generated.json --yes
```

The builder:

- reads only local metadata files
- does not use the network
- does not read connector content
- does not check connector authorization
- writes only the registry output file

Each capability card includes provenance and timestamps so stale or incorrect cards can be traced.

## Registry Health

`route_request.py` warns when:

- the registry is missing
- the registry is older than 7 days
- `schema_version` is not supported
- a source path no longer exists

Use:

```bash
python3 scripts/route_request.py --check-registry --debug
```

to inspect card provenance.

## Removal

To remove Skill Routing Kit:

1. Remove the `AGENTS.md` block between:

```text
BEGIN Skill Routing Kit
END Skill Routing Kit
```

2. Delete generated registry files if desired:

```bash
rm registry/capabilities.generated.json
```

3. Uninstall or delete the plugin directory through your normal Codex plugin workflow.

There are no hooks, telemetry, background scanners, or runtime interception paths to clean up.

## Limitations

- The registry is a hint index, not the source of truth.
- Connector cards do not prove access or authentication.
- The v1 router uses conservative keyword/category matching, not embeddings.
- Dynamic registry rebuild, connector availability probing, stale diffs, and richer conflict diagnostics are v2 features.

## Validation

Run:

```bash
python3 -m unittest discover -s tests
python3 scripts/route_request.py --check-registry
python3 scripts/build_registry.py --dry-run
```
