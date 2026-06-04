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

## Routing Methodology

Skill Routing Kit improves hit rate by turning skill/plugin selection into a small retrieval-and-ranking loop:

- describe **when to use** each capability;
- classify capabilities into layered routing categories such as `process/source/artifact/domain/risk`;
- describe **when not to use** each capability with negative examples;
- recall broad candidates first, then rerank by final artifact, source, task action, and risk.

中文完整说明见 [README.zh-CN.md](README.zh-CN.md) 的“设计原理与实现逻辑”。

## Install

For non-technical users, the recommended path is to ask Codex to install it:

```text
Please install the Skill Routing Kit plugin from https://github.com/juew/Skill-Routing-Kit. Install the plugin source globally at ~/plugins/skill-routing-kit, register it in ~/.agents/plugins/marketplace.json, run codex plugin add skill-routing-kit@personal, and enable the routing guard globally in ~/.codex/AGENTS.md. Do not install it into the current project. Do not ask me to create directories manually; use the repository installer and verify the plugin after installation.
```

不熟悉命令行的用户，可以直接把下面这句话复制给 Codex：

```text
请从 https://github.com/juew/Skill-Routing-Kit 安装 Skill Routing Kit 插件。插件源请全局安装到 ~/plugins/skill-routing-kit，注册到 ~/.agents/plugins/marketplace.json，执行 codex plugin add skill-routing-kit@personal，并默认把路由规则启用到 ~/.codex/AGENTS.md。不要把插件安装到当前项目目录。不要让我手动创建目录；请使用仓库里的安装脚本完成安装，并在安装后验证插件。
```

One-command install:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/juew/Skill-Routing-Kit/main/scripts/install.sh)" -- --install-agents --codex-add
```

This creates the needed directories automatically.

Default scope:

- plugin source: global, `~/plugins/skill-routing-kit`
- marketplace entry: `~/.agents/plugins/marketplace.json`
- routing guard: global, `~/.codex/AGENTS.md`
- project-level routing: optional advanced mode with `--agents /path/to/project/AGENTS.md`

## Update

For non-technical users, update it the same way: ask Codex to do it.

```text
Please update the Skill Routing Kit plugin from https://github.com/juew/Skill-Routing-Kit. Keep the plugin source globally at ~/plugins/skill-routing-kit, keep it registered in ~/.agents/plugins/marketplace.json, run codex plugin add skill-routing-kit@personal, keep the routing guard enabled globally in ~/.codex/AGENTS.md, refresh the registry, verify the plugin, and do not ask me to manually create or copy directories.
```

不熟悉命令行的用户，可以直接把下面这句话复制给 Codex：

```text
请从 https://github.com/juew/Skill-Routing-Kit 更新 Skill Routing Kit 插件。插件源继续安装在全局目录 ~/plugins/skill-routing-kit，继续注册在 ~/.agents/plugins/marketplace.json，执行 codex plugin add skill-routing-kit@personal，路由规则继续全局启用在 ~/.codex/AGENTS.md。请备份旧版本、刷新 registry、验证插件，不要让我手动创建或复制目录。
```

Codex can use the same installer for updates; existing installs are backed up automatically.

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
