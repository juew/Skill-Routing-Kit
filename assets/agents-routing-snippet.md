<!-- BEGIN Skill Routing Kit -->
## Skill Routing Guard

Before acting on any non-trivial request, silently perform a brief skill routing micro-check:

- classify task type: explain, create, edit, debug, analyze, test, review, deploy
- classify source: local files/repo, web, GitHub, Gmail, Drive, Notion, Slack, Figma, Linear
- classify artifact: code, document, spreadsheet, presentation, PDF, image, webpage, report
- classify process need: planning, debugging, TDD, verification, review, orchestration

For requests that produce a concrete deliverable or artifact, route through `superpowers:using-superpowers` first. Use the refreshed registry and skill descriptions to surface likely process helpers, orchestration helpers, and artifact-specific helpers; SRK should not replace the process skill's decision.

If a skill clearly applies, use it before acting or briefly state why it is not appropriate.

Default to local files, local repositories, local browser verification, and local build/test commands. Use external connectors only when the user explicitly names the app, the source of truth clearly lives there, or the user confirms using that connector.

Show a brief routing check only for complex, ambiguous, multi-skill, multi-artifact, long-running, or user-requested routing tasks.

When skills/plugins are installed, removed, or routing seems stale, suggest refreshing the Skill Routing Kit registry.
<!-- END Skill Routing Kit -->
