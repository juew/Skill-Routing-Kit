# Skill Routing Kit Demo

These examples show the core promise: route by final artifact, source of truth, process need, and risk.

## 1. Routing Diagnostics Should Use Skill Router

```bash
python3 scripts/route_request.py "为什么 pdf skill 没有命中这个请求"
```

Expected:

```text
Recommended skill/plugin:
- Skill Router (skill-router)

Helper skills/plugins:
- PDF (pdf)

Why:
- routing diagnostic request prefers the skill-router capability
- local-first preference
```

Why this matters: the user is asking about routing behavior. The mentioned `pdf` skill is context, not the primary route.

## 2. PDF To PPT Should Route By Final Artifact

```bash
python3 scripts/route_request.py "把这个 PDF 整理成一份 PPT"
```

Expected:

```text
Recommended skill/plugin:
- Presentations (presentations)

Helper skills/plugins:
- PDF (pdf)
```

Why this matters: the PDF is an input. The final artifact is a presentation.

## 3. Local Debugging Should Stay Local

```bash
python3 scripts/route_request.py "帮我调试这个本地项目的测试失败"
```

Expected:

```text
Recommended skill/plugin:
- frontend-testing-debugging or systematic-debugging
```

Why this matters: local test failures should not route to an external connector unless the user explicitly names one.

## 4. Registry Health

```bash
python3 scripts/route_request.py --check-registry
```

Expected:

```text
Schema: 1.0
Capabilities: ...
Warnings: none
```

If the registry is missing, stale, or points to deleted files, the script tells you what to refresh.

## 5. Refresh Registry

```bash
python3 scripts/build_registry.py --dry-run
python3 scripts/build_registry.py --yes
```

The builder scans local metadata only. It does not read connector content or use the network.
