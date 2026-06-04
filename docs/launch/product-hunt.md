# Product Hunt

Use this after the repository has a demo GIF or screenshot.

## Name

```text
Skill Routing Kit
```

## Tagline

```text
Make Codex pick the right skill or plugin more often
```

## Description

```text
Skill Routing Kit is a local-first Codex plugin that improves skill/plugin hit rate with a routing guard, capability registry, and explainable diagnostics. It helps Codex choose the primary skill, keep helper plugins contextual, and avoid tempting but wrong routes.
```

## Maker Comment

```text
Hi Product Hunt,

I built Skill Routing Kit after running into a practical problem with AI coding agents: the more skills and plugins I installed, the more important routing became.

This plugin adds a small local-first routing layer for Codex:

- a skill-router skill for diagnostics
- a local capability registry
- an AGENTS.md routing guard
- request routing explanations
- registry health checks

It is intentionally conservative: no background scanner, no telemetry, no connector content reads, and no network by default.

The core idea is simple: route by final artifact, source of truth, task process, and permission risk.

I would love feedback from people building with Codex skills, MCP tools, or agent workflows.
```

## Gallery Suggestions

1. Plugin list screenshot showing Skill Routing Kit installed.
2. Terminal demo: routing diagnostic selects `skill-router`.
3. Terminal demo: PDF to PPT selects `presentations`, PDF as helper.
4. Architecture diagram from README.
5. Safety model slide: local-first, no connector reads, removable.
