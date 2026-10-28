"""Execute Chapter 1 credential cells offline without reading real credentials."""
import contextlib
import json
import os
from pathlib import Path
import sys
import tempfile
from types import ModuleType, SimpleNamespace
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


def credential_cells():
    for path in sorted((ROOT / "Chapter 1").glob("*.ipynb")):
        notebook = json.loads(path.read_text())
        for cell in notebook["cells"]:
            source = "".join(cell.get("source", []))
            if cell["cell_type"] == "code" and "from google.colab import userdata" in source:
                keys = [key for key in ("OPENAI_API_KEY", "GOOGLE_API_KEY",
                                       "ANTHROPIC_API_KEY", "NEWS_API_KEY")
                        if f"userdata.get('{key}')" in source]
                yield path.name, source, keys


class Chapter1Environment(unittest.TestCase):
    def test_root_dotenv_loaded_from_root_and_chapter_working_directories(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            chapter = root / "Chapter 1"
            chapter.mkdir()
            (root / ".env").write_text(
                "OPENAI_API_KEY=file-openai\nGOOGLE_API_KEY=file-google\n"
                "ANTHROPIC_API_KEY=file-anthropic\nNEWS_API_KEY=file-news\n"
            )
            for cwd in (root, chapter):
                for name, source, keys in credential_cells():
                    with self.subTest(notebook=name, cwd=cwd.name, keys=keys):
                        with contextlib.chdir(cwd), patch.dict(os.environ, {}, clear=True), \
                                patch.dict(sys.modules, {"google.colab": None}):
                            namespace = {}
                            exec(source, namespace)
                            for key in keys:
                                self.assertEqual(namespace[key], os.environ[key])
                                self.assertTrue(namespace[key].startswith("file-"))

    def test_exported_environment_takes_precedence_over_dotenv(self):
        with tempfile.TemporaryDirectory() as directory, contextlib.chdir(directory):
            Path(".env").write_text("OPENAI_API_KEY=file-value\nGOOGLE_API_KEY=file-value\n"
                                    "ANTHROPIC_API_KEY=file-value\nNEWS_API_KEY=file-value\n")
            for name, source, keys in credential_cells():
                with self.subTest(notebook=name, keys=keys):
                    values = {key: "exported-value" for key in keys}
                    with patch.dict(os.environ, values, clear=True), \
                            patch.dict(sys.modules, {"google.colab": None}):
                        namespace = {}
                        exec(source, namespace)
                        for key in keys:
                            self.assertEqual(namespace[key], "exported-value")

    def test_colab_keeps_using_secrets_without_importing_dotenv(self):
        colab = ModuleType("google.colab")
        colab.userdata = SimpleNamespace(get=lambda key: f"colab-{key}")
        for name, source, keys in credential_cells():
            with self.subTest(notebook=name, keys=keys):
                with patch.dict(os.environ, {}, clear=True), \
                        patch.dict(sys.modules, {"google.colab": colab, "dotenv": None}):
                    namespace = {}
                    exec(source, namespace)
                    for key in keys:
                        self.assertEqual(namespace[key], f"colab-{key}")
                        self.assertNotIn(key, os.environ)


if __name__ == "__main__":
    unittest.main()
