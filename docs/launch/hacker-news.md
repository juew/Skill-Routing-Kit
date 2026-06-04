# Hacker News

## Title

```text
Show HN: Skill Routing Kit – local-first routing for Codex skills and plugins
```

## Body

```text
Hi HN,

I built Skill Routing Kit, a small local-first Codex plugin for improving skill/plugin hit rate.

The problem: once you install many Codex skills and plugins, the correct one does not always trigger. A PDF input can be mistaken for the final artifact, a routing diagnostic can be handled by the domain skill that was merely mentioned, and external connectors can become tempting even when the task is local.

Skill Routing Kit adds:

- a `skill-router` skill for routing diagnostics;
- a local capability registry;
- an AGENTS.md routing guard;
- explainable request routing;
- registry freshness/provenance checks.

It is intentionally conservative: no background scanner, no telemetry, no connector content reads, and no network by default.

Example:

`python3 scripts/route_request.py "为什么 pdf skill 没有命中这个请求"`

recommends `skill-router`, with `PDF` only as helper context.

Repo:
https://github.com/juew/Skill-Routing-Kit

I am especially interested in missed-routing cases from people building Codex skills, MCP tools, or agent workflows.
```

## First Comment

```text
Implementation note: v0.1.0 uses conservative keyword/category scoring rather than embeddings. The registry format is structured around use_when, avoid_when, categories, provenance, and helper/primary selection so it can later support a stronger reranker without changing the authoring model.
```
