#!/usr/bin/env python3
import subprocess
import sys
import tempfile
import unittest
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ROUTE = ROOT / "scripts" / "route_request.py"
REGISTRY = ROOT / "registry" / "core-capabilities.json"
INSTALL = ROOT / "scripts" / "install.py"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def run_route(request: str, *args: str) -> str:
    result = subprocess.run(
        [sys.executable, str(ROUTE), "--registry", str(REGISTRY), *args, request],
        cwd=str(ROOT),
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=True,
    )
    return result.stdout


def recommended_block(output: str) -> str:
    return output.split("Recommended skill/plugin:", 1)[1].split("Helper skills/plugins:", 1)[0]


class RouteRequestTests(unittest.TestCase):
    def test_pdf_to_ppt_routes_to_presentations(self):
        output = run_route("把这个 PDF 整理成一份 PPT")
        self.assertIn("Presentations", recommended_block(output))
        self.assertIn("PDF", output)

    def test_frontend_bug_routes_to_debugging(self):
        output = run_route("帮我修这个前端页面的控制台 error 并验证页面")
        self.assertIn("Systematic Debugging", recommended_block(output))
        self.assertIn("Frontend", output)

    def test_github_needs_confirmation(self):
        output = run_route("帮我把 GitHub PR 评论修掉")
        self.assertIn("GitHub", output)
        self.assertIn("Needs confirmation", output)

    def test_routing_diagnostic_routes_to_skill_router(self):
        output = run_route("为什么 pdf skill 没有命中这个请求")
        self.assertIn("Skill Router", recommended_block(output))

    def test_registry_check(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = Path(tmp) / "registry.json"
            registry.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "generated_at": "2999-01-01T00:00:00+00:00",
                        "capabilities": [],
                    }
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, str(ROUTE), "--registry", str(registry), "--check-registry"],
                cwd=str(ROOT),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        self.assertEqual(result.returncode, 0)
        self.assertIn("Capabilities:", result.stdout)

    def test_core_registry_check_reports_staleness_when_old(self):
        result = subprocess.run(
            [sys.executable, str(ROUTE), "--registry", str(REGISTRY), "--check-registry"],
            cwd=str(ROOT),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertIn(result.returncode, {0, 1})
        self.assertIn("Capabilities:", result.stdout)

    def test_debug_output_shows_candidates_but_default_does_not(self):
        default_output = run_route("帮我把 PDF 变成 PPT")
        self.assertNotIn("Debug candidates:", default_output)
        self.assertNotRegex(default_output, r"\n-\s+\d+\s+")

        debug_output = run_route("帮我把 PDF 变成 PPT", "--debug")
        self.assertIn("Debug candidates:", debug_output)
        self.assertRegex(debug_output, r"\n-\s+\d+\s+")

    def test_missing_registry_is_reported_without_traceback(self):
        with tempfile.TemporaryDirectory() as tmp:
            missing = Path(tmp) / "missing.json"
            result = subprocess.run(
                [sys.executable, str(ROUTE), "--registry", str(missing), "--check-registry"],
                cwd=str(ROOT),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        self.assertEqual(result.returncode, 1)
        self.assertIn("Registry not found", result.stdout)
        self.assertNotIn("Traceback", result.stderr)

    def test_registry_warnings_for_stale_schema_and_missing_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = Path(tmp) / "registry.json"
            registry.write_text(
                json.dumps(
                    {
                        "schema_version": "0.1",
                        "generated_at": "2020-01-01T00:00:00+00:00",
                        "capabilities": [
                            {
                                "id": "fake",
                                "name": "Fake",
                                "kind": "skill",
                                "categories": [],
                                "provenance": {
                                    "source_type": "skill",
                                    "path": str(Path(tmp) / "missing" / "SKILL.md"),
                                },
                            }
                        ],
                    }
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [sys.executable, str(ROUTE), "--registry", str(registry), "--check-registry"],
                cwd=str(ROOT),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        self.assertEqual(result.returncode, 1)
        self.assertIn("stale", result.stdout)
        self.assertIn("schema_version", result.stdout)
        self.assertIn("source path", result.stdout)

    def test_generated_like_registry_routes_diagnostics_to_skill_router(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = Path(tmp) / "registry.json"
            registry.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "generated_at": "2999-01-01T00:00:00+00:00",
                        "capabilities": [
                            {
                                "id": "pdf",
                                "name": "pdf",
                                "kind": "skill",
                                "categories": ["artifact", "local", "pdf", "skill"],
                                "use_when": "Use when tasks involve reading, creating, or reviewing PDF files.",
                                "provenance": {
                                    "source_type": "core_static",
                                    "path": "registry/core-capabilities.json",
                                },
                            },
                            {
                                "id": "skill-routing-kit",
                                "name": "skill-routing-kit",
                                "kind": "plugin",
                                "categories": ["local", "plugin", "process", "routing"],
                                "use_when": "Local-first skill routing guard and diagnostics.",
                                "provenance": {
                                    "source_type": "core_static",
                                    "path": "registry/core-capabilities.json",
                                },
                            },
                            {
                                "id": "skill-router",
                                "name": "skill-router",
                                "kind": "skill",
                                "categories": ["local", "skill"],
                                "use_when": "Use when the user asks to diagnose skill/plugin routing.",
                                "provenance": {
                                    "source_type": "core_static",
                                    "path": "registry/core-capabilities.json",
                                },
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROUTE),
                    "--registry",
                    str(registry),
                    "为什么 pdf skill 没有命中这个请求",
                ],
                cwd=str(ROOT),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
        self.assertIn("skill-router", recommended_block(result.stdout))

    def test_domain_specific_rps_skill_does_not_match_generic_business_testing(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = Path(tmp) / "registry.json"
            registry.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "generated_at": "2999-01-01T00:00:00+00:00",
                        "capabilities": [
                            {
                                "id": "generic-testing",
                                "name": "Generic Testing",
                                "kind": "skill",
                                "categories": ["local", "process", "skill", "testing"],
                                "use_when": "Use for generic business testing.",
                                "provenance": {"source_type": "core_static"},
                            },
                            {
                                "id": "rps-web-ui-testing",
                                "name": "rps-web-ui-testing",
                                "kind": "skill",
                                "categories": [
                                    "domain",
                                    "local",
                                    "process",
                                    "rps",
                                    "skill",
                                    "testing",
                                ],
                                "use_when": "Use for formal RPS software web UI testing.",
                                "provenance": {"source_type": "core_static"},
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROUTE),
                    "--registry",
                    str(registry),
                    "帮我做业务测试",
                ],
                cwd=str(ROOT),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
        self.assertIn("Generic Testing", recommended_block(result.stdout))
        self.assertNotIn("rps-web-ui-testing", result.stdout)

    def test_domain_specific_rps_skill_matches_explicit_rps_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = Path(tmp) / "registry.json"
            registry.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "generated_at": "2999-01-01T00:00:00+00:00",
                        "capabilities": [
                            {
                                "id": "generic-testing",
                                "name": "Generic Testing",
                                "kind": "skill",
                                "categories": ["local", "process", "skill", "testing"],
                                "use_when": "Use for generic business testing.",
                                "provenance": {"source_type": "core_static"},
                            },
                            {
                                "id": "rps-web-ui-testing",
                                "name": "rps-web-ui-testing",
                                "kind": "skill",
                                "categories": [
                                    "domain",
                                    "local",
                                    "process",
                                    "rps",
                                    "skill",
                                    "testing",
                                ],
                                "use_when": "Use for formal RPS software web UI testing.",
                                "provenance": {"source_type": "core_static"},
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROUTE),
                    "--registry",
                    str(registry),
                    "帮我做RPS产品测试",
                ],
                cwd=str(ROOT),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
        self.assertIn("rps-web-ui-testing", recommended_block(result.stdout))

    def test_domain_specific_rps_skill_is_excluded_for_non_rps_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = Path(tmp) / "registry.json"
            registry.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "generated_at": "2999-01-01T00:00:00+00:00",
                        "capabilities": [
                            {
                                "id": "generic-testing",
                                "name": "Generic Testing",
                                "kind": "skill",
                                "categories": ["local", "process", "skill", "testing"],
                                "use_when": "Use for generic business testing.",
                                "provenance": {"source_type": "core_static"},
                            },
                            {
                                "id": "rps-web-ui-testing",
                                "name": "rps-web-ui-testing",
                                "kind": "skill",
                                "categories": [
                                    "domain",
                                    "local",
                                    "process",
                                    "rps",
                                    "skill",
                                    "testing",
                                ],
                                "use_when": "Use for formal RPS software web UI testing.",
                                "provenance": {"source_type": "core_static"},
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROUTE),
                    "--registry",
                    str(registry),
                    "帮我做非RPS产品的业务测试",
                ],
                cwd=str(ROOT),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
        self.assertIn("Generic Testing", recommended_block(result.stdout))
        self.assertNotIn("rps-web-ui-testing", result.stdout)

    def test_multi_evidence_regression_routes_to_subagent_orchestration(self):
        with tempfile.TemporaryDirectory() as tmp:
            registry = Path(tmp) / "registry.json"
            registry.write_text(
                json.dumps(
                    {
                        "schema_version": "1.0",
                        "generated_at": "2999-01-01T00:00:00+00:00",
                        "capabilities": [
                            {
                                "id": "subagent-orchestration",
                                "name": "subagent-orchestration",
                                "kind": "skill",
                                "categories": [
                                    "local",
                                    "multi_agent",
                                    "orchestration",
                                    "process",
                                    "skill",
                                    "testing",
                                ],
                                "use_when": "Use for long-running multi-agent evidence testing.",
                                "provenance": {"source_type": "core_static"},
                            },
                            {
                                "id": "rps-web-ui-testing",
                                "name": "rps-web-ui-testing",
                                "kind": "skill",
                                "categories": [
                                    "domain",
                                    "local",
                                    "orchestration",
                                    "process",
                                    "rps",
                                    "skill",
                                    "testing",
                                ],
                                "use_when": "Use for formal RPS software web UI testing.",
                                "provenance": {"source_type": "core_static"},
                            },
                        ],
                    }
                ),
                encoding="utf-8",
            )
            result = subprocess.run(
                [
                    sys.executable,
                    str(ROUTE),
                    "--registry",
                    str(registry),
                    "做服务器页面回归，需要主控拆分 UI、API、日志、截图、JSON 证据，多个子 Agent 返回后验收",
                ],
                cwd=str(ROOT),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
        self.assertIn("subagent-orchestration", recommended_block(result.stdout))
        self.assertNotIn("rps-web-ui-testing", result.stdout)

    def test_build_registry_dry_run_and_refresh_custom_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "custom-registry.json"
            dry = subprocess.run(
                [
                    sys.executable,
                    str(ROOT / "scripts" / "build_registry.py"),
                    "--output",
                    str(output),
                    "--dry-run",
                ],
                cwd=str(ROOT),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
            self.assertIn("registry summary", dry.stdout)
            self.assertFalse(output.exists())

            refreshed = subprocess.run(
                [
                    sys.executable,
                    str(ROUTE),
                    "--registry",
                    str(output),
                    "--refresh",
                    "--check-registry",
                ],
                cwd=str(ROOT),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )
            self.assertTrue(output.exists())
            self.assertIn("Warnings: none", refreshed.stdout)

    def test_installer_creates_target_and_agents_snippet(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "plugins" / "skill-routing-kit"
            marketplace = Path(tmp) / ".agents" / "plugins" / "marketplace.json"
            agents = Path(tmp) / "AGENTS.md"

            subprocess.run(
                [
                    sys.executable,
                    str(INSTALL),
                    "--target",
                    str(target),
                    "--install-agents",
                    "--agents",
                    str(agents),
                    "--marketplace",
                    str(marketplace),
                ],
                cwd=str(ROOT),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )

            self.assertTrue((target / ".codex-plugin" / "plugin.json").exists())
            self.assertTrue((target / "skills" / "skill-router" / "SKILL.md").exists())
            self.assertFalse((target / ".git").exists())
            self.assertIn("BEGIN Skill Routing Kit", agents.read_text(encoding="utf-8"))
            marketplace_payload = load_json(marketplace)
            entries = [
                entry
                for entry in marketplace_payload["plugins"]
                if entry.get("name") == "skill-routing-kit"
            ]
            self.assertEqual(len(entries), 1)
            self.assertEqual(entries[0]["source"]["path"], "./plugins/skill-routing-kit")

            subprocess.run(
                [
                    sys.executable,
                    str(INSTALL),
                    "--target",
                    str(target),
                    "--install-agents",
                    "--agents",
                    str(agents),
                    "--marketplace",
                    str(marketplace),
                ],
                cwd=str(ROOT),
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                check=True,
            )

            agents_text = agents.read_text(encoding="utf-8")
            self.assertEqual(agents_text.count("BEGIN Skill Routing Kit"), 1)
            marketplace_payload = load_json(marketplace)
            entries = [
                entry
                for entry in marketplace_payload["plugins"]
                if entry.get("name") == "skill-routing-kit"
            ]
            self.assertEqual(len(entries), 1)

    def test_manifest_exposes_skills_directory(self):
        manifest = load_json(ROOT / ".codex-plugin" / "plugin.json")
        self.assertEqual(manifest.get("skills"), "./skills/")

    def test_installer_rejects_target_inside_repository(self):
        target = ROOT / "tmp-install-target"
        result = subprocess.run(
            [sys.executable, str(INSTALL), "--target", str(target)],
            cwd=str(ROOT),
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("cannot be inside", result.stderr)


if __name__ == "__main__":
    unittest.main()
