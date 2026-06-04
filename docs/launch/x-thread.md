# X Thread

## Thread

1.
```text
I open-sourced Skill Routing Kit.

It makes Codex pick the right skill or plugin more often.

Repo: https://github.com/juew/Skill-Routing-Kit
```

2.
```text
The problem:

Codex can have many skills/plugins installed, but the correct one does not always trigger.

A PDF input can be mistaken for the final artifact.
A routing question can be handled by the wrong domain skill.
A connector can be considered when the task is local.
```

3.
```text
Skill Routing Kit adds:

- a skill-router skill
- a local capability registry
- an AGENTS.md routing guard
- explainable route diagnostics
- registry health checks
```

4.
```text
Example:

"为什么 pdf skill 没有命中这个请求"

The primary route should be skill-router.
PDF is only helper context.
```

5.
```text
Another example:

"把这个 PDF 整理成一份 PPT"

The primary route should be Presentations.
PDF is an input, not the final artifact.
```

6.
```text
The method:

1. describe when to use
2. classify by process/source/artifact/domain/risk
3. describe when not to use
4. recall broad candidates, then rerank
```

7.
```text
It is local-first by design:

- no background scanner
- no telemetry
- no connector content reads
- no network by default
- explicit registry refresh
```

8.
```text
If you build Codex skills, MCP tools, or agent workflows, I would love feedback on missed routing cases.

Repo:
https://github.com/juew/Skill-Routing-Kit
```

## Short Single Post

```text
I open-sourced Skill Routing Kit: a local-first Codex plugin that improves skill/plugin hit rate with a routing guard, capability registry, and explainable diagnostics.

It helps decide what should be primary, what is helper context, and when a tempting skill should not be used.

https://github.com/juew/Skill-Routing-Kit
```
