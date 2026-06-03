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

## Install

For non-technical users, the recommended path is to ask Codex to install it:

```text
Please install the Skill Routing Kit plugin from https://github.com/juew/Skill-Routing-Kit and enable the routing guard in the current project's AGENTS.md. Do not ask me to create directories manually; use the repository installer and verify the plugin after installation.
```

不熟悉命令行的用户，可以直接把下面这句话复制给 Codex：

```text
请从 https://github.com/juew/Skill-Routing-Kit 安装 Skill Routing Kit 插件，并把路由规则启用到当前项目的 AGENTS.md。不要让我手动创建目录；请使用仓库里的安装脚本完成安装，并在安装后验证插件。
```

One-command install:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/juew/Skill-Routing-Kit/main/scripts/install.sh)" -- --install-agents
```

This creates the needed directories automatically.

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
