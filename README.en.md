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

## Routing Methodology

Skill Routing Kit improves hit rate through a small retrieval-and-ranking loop:

1. **Describe when to use a capability**  
   Every skill/plugin should answer: what task, input, and final artifact should trigger me? This maps to `use_when`, `inputs`, and `outputs` in registry cards, and to trigger language in skill descriptions.

2. **Use layered routing**  
   Classify first by `process/source/artifact/domain/risk`, then select a primary capability plus helper capabilities. For example, “turn this PDF into a slide deck” should route primarily to Presentations because the final artifact is slides; PDF handling is a helper.

3. **Add negative examples**  
   Every card needs `avoid_when`: when not to use the capability. Negative examples reduce false positives, such as not elevating connectors unless the user names them or treating PDF as the primary skill when PDF is only an input.

4. **Recall, then rerank**  
   The router recalls broad candidates, then reranks by final artifact, source location, task action, and risk/permission requirements. v1 uses conservative keyword/category matching; the registry shape is designed so embedding or stronger rerankers can be added later without rewriting capability cards.

These pieces map to the implementation:

- `SKILL.md` descriptions tell the model when to consider a skill.
- `registry/*.json` stores searchable `use_when/categories/avoid_when`.
- `scripts/route_request.py` performs recall, scoring, reranking, and diagnostics.
- the `AGENTS.md` snippet makes routing a default daily guardrail.

## Installation

### Recommended: ask Codex to install it

If you are not comfortable with terminals, directory structures, or plugin setup, paste this into Codex:

```text
Please install the Skill Routing Kit plugin from https://github.com/juew/Skill-Routing-Kit. Install the plugin source globally at ~/plugins/skill-routing-kit, register it in ~/.agents/plugins/marketplace.json, run codex plugin add skill-routing-kit@personal, and enable the routing guard globally in ~/.codex/AGENTS.md by default, so all projects can benefit. Do not install it into the current project. Do not ask me to create directories manually; use the repository installer and verify the plugin after installation.
```

Codex should handle:

- downloading or cloning the repository
- creating local directories
- installing plugin files
- registering the personal marketplace entry
- enabling the plugin with `codex plugin add skill-routing-kit@personal`
- adding the global `~/.codex/AGENTS.md` routing guard by default
- running basic validation

You should not need to manually create `.codex-plugin`, `skills`, or `registry` directories.

### One-command install

If you are comfortable running one terminal command:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/juew/Skill-Routing-Kit/main/scripts/install.sh)" -- --install-agents --codex-add
```

By default, this installs the plugin to:

```text
~/plugins/skill-routing-kit
```

registers it in:

```text
~/.agents/plugins/marketplace.json
```

and writes the routing guard to:

```text
~/.codex/AGENTS.md
```

Default scope:

- plugin source: global, `~/plugins/skill-routing-kit`
- marketplace: personal, `~/.agents/plugins/marketplace.json`
- routing guard: global, `~/.codex/AGENTS.md`
- project-level routing: optional advanced mode with `--agents /path/to/project/AGENTS.md`

To install only the plugin without writing `AGENTS.md`:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/juew/Skill-Routing-Kit/main/scripts/install.sh)" -- --codex-add
```

To write the routing guard into a specific project:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/juew/Skill-Routing-Kit/main/scripts/install.sh)" -- --install-agents --agents "/path/to/project/AGENTS.md" --codex-add
```

Restart Codex or reload plugins if the new plugin does not appear immediately.

## Updating

### Recommended: ask Codex to update it

If you are not comfortable with terminals, paste this into Codex:

```text
Please update the Skill Routing Kit plugin from https://github.com/juew/Skill-Routing-Kit. Keep the plugin source globally at ~/plugins/skill-routing-kit, keep it registered in ~/.agents/plugins/marketplace.json, run codex plugin add skill-routing-kit@personal, keep the routing guard enabled globally in ~/.codex/AGENTS.md, refresh the registry, verify the plugin, and do not ask me to manually create or copy directories.
```

Codex should handle:

- fetching the latest version from GitHub
- backing up the current local version
- reinstalling into `~/plugins/skill-routing-kit`
- updating `~/.agents/plugins/marketplace.json`
- rerunning `codex plugin add skill-routing-kit@personal`
- updating the routing guard between `BEGIN/END Skill Routing Kit` in `~/.codex/AGENTS.md`
- refreshing the registry
- running plugin validation and basic tests

### One-command update

The installer also works as an updater:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/juew/Skill-Routing-Kit/main/scripts/install.sh)" -- --install-agents --codex-add
```

Existing versions are backed up to:

```text
~/plugins/.backups/
```

Restart Codex or reload plugins if the updated plugin does not appear immediately.

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
