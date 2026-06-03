# Skill Routing Kit

[中文说明](README.zh-CN.md) | [English Documentation](README.en.md)

Skill Routing Kit is a Codex plugin for improving skill and plugin hit rate. It adds a lightweight, local-first routing layer that helps Codex decide when to use a skill, when not to use it, and how to diagnose missed routing.

Skill Routing Kit 是一个用于提升 Codex skill/plugin 命中率的插件。它通过本地优先的 routing registry、静默路由规则、诊断脚本和可维护的索引机制，让 Codex 更容易在合适的时机调用合适的能力。

## What It Provides

- A `skill-router` skill for routing diagnosis and registry maintenance.
- A capability registry with use cases, negative examples, categories, and provenance.
- Local scripts for request routing, registry scanning, freshness checks, and diagnostics.
- An `AGENTS.md` snippet that can make routing a default silent guardrail.
- Bilingual documentation for installation, daily use, updates, and removal.

## Quick Start

Validate the plugin:

```bash
python3 /Users/zhonghao/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
```

Run the routing tests:

```bash
python3 -B -m unittest discover -s tests
```

Try a routing diagnosis:

```bash
python3 scripts/route_request.py "帮我把这个 PDF 做成 PPT 并保留版式"
```

Build a local generated registry:

```bash
python3 scripts/build_registry.py --dry-run
python3 scripts/build_registry.py --yes
```

## Documentation

Use the Chinese README if you want the full design rationale and operating model in Chinese:

- [README.zh-CN.md](README.zh-CN.md)

Use the English README for the same installation and maintenance guide in English:

- [README.en.md](README.en.md)
