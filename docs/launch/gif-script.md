# 30-Second GIF Script

Goal: show the value without explaining the whole architecture.

## Storyboard

### Scene 1: Plugin Is Installed

Show Codex plugin list with `Skill Routing Kit` enabled.

Caption:

```text
Skill Routing Kit installed
```

### Scene 2: Routing Diagnostic

Terminal:

```bash
python3 scripts/route_request.py "为什么 pdf skill 没有命中这个请求"
```

Highlight:

```text
Recommended skill/plugin:
- Skill Router (skill-router)
```

Caption:

```text
Routing questions should use the router, not the mentioned domain skill.
```

### Scene 3: Final Artifact Routing

Terminal:

```bash
python3 scripts/route_request.py "把这个 PDF 整理成一份 PPT"
```

Highlight:

```text
Recommended skill/plugin:
- Presentations (presentations)

Helper skills/plugins:
- PDF (pdf)
```

Caption:

```text
Route by final artifact. PDF is input; PPT is output.
```

### Scene 4: Safety

Show README safety bullets.

Caption:

```text
Local-first. No connector content reads. No background scanner.
```

## Recording Tips

- Keep the terminal width around 100 columns.
- Use a large font.
- Use a clean shell prompt.
- Hide unrelated local paths if they are visually noisy.
- Keep final GIF under 30 seconds.

## Suggested Commands

From the repository root:

```bash
python3 scripts/route_request.py "为什么 pdf skill 没有命中这个请求"
python3 scripts/route_request.py "把这个 PDF 整理成一份 PPT"
python3 scripts/route_request.py --check-registry
```

## Optional Script For Recording

```bash
clear
echo '$ python3 scripts/route_request.py "为什么 pdf skill 没有命中这个请求"'
python3 scripts/route_request.py "为什么 pdf skill 没有命中这个请求"
sleep 2
clear
echo '$ python3 scripts/route_request.py "把这个 PDF 整理成一份 PPT"'
python3 scripts/route_request.py "把这个 PDF 整理成一份 PPT"
sleep 2
clear
echo '$ python3 scripts/route_request.py --check-registry'
python3 scripts/route_request.py --check-registry
```

## Output File Names

- `assets/demo-routing-diagnostic.gif`
- `assets/demo-final-artifact-routing.gif`
- `assets/demo-full-30s.gif`
