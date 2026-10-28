"""Offline checks for the repository-level uv configuration."""
import importlib.util
from pathlib import Path
import tomllib
import unittest


ROOT = Path(__file__).resolve().parents[1]


class RepositoryDependencies(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project = tomllib.loads((ROOT / "pyproject.toml").read_text())
        cls.lock = tomllib.loads((ROOT / "uv.lock").read_text())

    def test_single_lockfile_and_only_package_metadata_remains_nested(self):
        # Only inspect tracked source directories, not installed .venv packages.
        chapters = sorted(ROOT.glob("Chapter *"))
        self.assertFalse([p for chapter in chapters for p in chapter.rglob("uv.lock")])
        self.assertEqual(
            [p.relative_to(ROOT).as_posix() for chapter in chapters
             for p in chapter.rglob("pyproject.toml")],
            ["Chapter 11/pyproject.toml"],
        )

    def test_python_baseline_and_no_default_lab_install(self):
        self.assertEqual((ROOT / ".python-version").read_text().strip(), "3.12")
        self.assertEqual(self.project["project"]["requires-python"], ">=3.12,<3.13")
        self.assertEqual(self.project["tool"]["uv"]["default-groups"], [])
        self.assertFalse(self.project["tool"]["uv"]["package"])

    def test_all_chapters_and_notebooks_have_profiles(self):
        groups = self.project["dependency-groups"]
        for chapter in range(1, 13):
            prefix = f"chapter-{chapter}"
            self.assertTrue(any(g == prefix or g.startswith(prefix + "-") for g in groups))
        self.assertIn("notebooks", groups)
        self.assertIn("dev", groups)
        for framework in ["langchain", "google-adk", "crewai", "autogen",
                          "openai-agents", "llamaindex", "anthropic", "mistral",
                          "pydantic-ai", "claude-agent-sdk", "bakeoff-mistral"]:
            self.assertIn(f"chapter-3-{framework}", groups)

    def test_profiles_are_mutually_exclusive_but_notebook_tooling_is_shared(self):
        conflicts = self.project["tool"]["uv"]["conflicts"]
        exclusive = {entry["group"] for entry in conflicts[0]}
        expected = set(self.project["dependency-groups"]) - {"notebooks", "chapter-11-production"}
        self.assertEqual(exclusive, expected)
        self.assertIn({"include-group": "chapter-11"},
                      self.project["dependency-groups"]["chapter-11-production"])

    def test_lock_contains_all_profiles_and_local_harness(self):
        root = next(p for p in self.lock["package"]
                    if p["name"] == self.project["project"]["name"])
        self.assertEqual(set(root["dev-dependencies"]), set(self.project["dependency-groups"]))
        harness = next(p for p in self.lock["package"] if p["name"] == "kyc-eval-harness")
        self.assertEqual(harness["source"], {"editable": "Chapter 11"})

    def test_ci_uses_root_project_and_tracks_dependency_changes(self):
        spec = importlib.util.spec_from_file_location("change_scope", ROOT / "Chapter 11/ci/change_scope.py")
        scope = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(scope)
        for path in [b"pyproject.toml", b"uv.lock", b".python-version",
                     b"Chapter 11/src/models.py", b".github/workflows/kyc.yml"]:
            self.assertTrue(scope.relevant([path]))
        self.assertFalse(scope.relevant([b"README.md", b"Chapter 3/common.py"]))
        workflow = (ROOT / "Chapter 11/ci/github_actions.yml").read_text()
        self.assertIn('python-version: "3.12"', workflow)
        self.assertIn('cache-dependency-glob: "uv.lock"', workflow)
        self.assertIn("uv sync --project .. --locked --group chapter-11", workflow)
        self.assertNotIn("Chapter 11/uv.lock", workflow)


if __name__ == "__main__":
    unittest.main()
