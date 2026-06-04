# Reddit Posts

## r/opensource

Title:

```text
I built a local-first routing kit for Codex skills and plugins
```

Body:

```text
I open-sourced Skill Routing Kit:
https://github.com/juew/Skill-Routing-Kit

It is a Codex plugin that improves skill/plugin hit rate with a routing guard, local capability registry, and explainable diagnostics.

The problem it tries to solve: once you install many AI agent capabilities, the right one does not always trigger. A mentioned PDF skill may be context, not the primary task. A connector may be tempting, but the work may be local. A routing/debugging question should use a routing diagnostic skill, not the domain skill mentioned in the question.

The project is intentionally local-first:

- no background scanner
- no telemetry
- no connector content reads
- no network by default
- explicit registry refresh

I would appreciate feedback on the README, install flow, and whether the routing examples make the problem clear.
```

## r/ChatGPTCoding

Title:

```text
How are you handling skill/plugin routing as Codex capabilities grow?
```

Body:

```text
I have been running into a practical issue: the more skills/plugins I install for Codex, the more important routing becomes.

I built a small local-first plugin for this:
https://github.com/juew/Skill-Routing-Kit

It adds a `skill-router` skill, a local registry, an AGENTS.md routing guard, and a route_request.py diagnostic script.

Example:

`python3 scripts/route_request.py "把这个 PDF 整理成一份 PPT"`

The route should be Presentations as primary, with PDF as helper context, because the final artifact is PPT.

I am curious: what missed skill/plugin trigger cases have you seen in coding-agent workflows?
```

## r/LocalLLaMA

Title:

```text
Local-first capability routing for Codex skills/plugins
```

Body:

```text
This is not a model release, but it may be relevant to people thinking about agent routing.

I built Skill Routing Kit:
https://github.com/juew/Skill-Routing-Kit

It is a local-first routing layer for Codex skills/plugins. It uses a local registry with use_when, avoid_when, categories, and provenance, then performs simple recall/rerank to select a primary skill and helper capabilities.

v0.1.0 uses conservative keyword/category matching, not embeddings. The goal is to make routing explainable first, then potentially swap in a stronger reranker later.

No background scanner, no telemetry, no connector content reads, no network by default.

Interested in feedback from people building local agent stacks: how do you represent negative examples and "do not use" cases in capability routing?
```
