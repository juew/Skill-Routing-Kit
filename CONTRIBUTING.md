# Contributing To Skill Routing Kit

Thanks for helping improve Codex skill/plugin routing.

## Good Contributions

- Better routing examples with clear expected output.
- Safer negative examples for when a skill should not trigger.
- Registry cards for high-value local-first workflows.
- Tests for missed-routing regressions.
- Documentation that makes installation or removal easier.

## Design Rules

- Keep routing local-first by default.
- Do not add background scanning.
- Do not read connector content during registry generation.
- Do not assume connector authentication.
- Prefer explainable scoring over opaque behavior.
- Keep the `AGENTS.md` guard short enough to be used globally.

## Development

Run validation before opening a pull request:

```bash
python3 /Users/zhonghao/.codex/skills/.system/plugin-creator/scripts/validate_plugin.py .
python3 -B -m unittest discover -s tests
python3 scripts/build_registry.py --dry-run
python3 scripts/route_request.py --check-registry
```

If you change routing behavior, add or update a regression test in `tests/test_route_request.py`.

## Pull Request Checklist

- The change is local-first and does not add hidden network behavior.
- Plugin validation passes.
- Unit tests pass.
- New routing behavior has a test or demo case.
- Documentation is updated when commands or install paths change.

## Security And Privacy

Do not include private skill registries, connector data, access tokens, local machine secrets, or user-specific paths in examples unless they are clearly placeholders.
