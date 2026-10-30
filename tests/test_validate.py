import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.validate import ROOT, validate


class ValidationTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name) / "repo"
        self.root.mkdir()
        for path in [*ROOT.glob("*.md"), ROOT / "LICENSE"]:
            shutil.copyfile(path, self.root / path.name)
        for directory in ("references", "evals"):
            shutil.copytree(ROOT / directory, self.root / directory)

    def test_repository_is_valid(self):
        self.assertEqual(validate(self.root), [])

    def test_missing_bundled_reference_is_rejected(self):
        (self.root / "references/configuration.md").unlink()
        self.assertTrue(any("configuration.md" in error for error in validate(self.root)))

    def test_broken_readme_link_is_rejected(self):
        with (self.root / "README.md").open("a", encoding="utf-8") as document:
            document.write("\n[Missing guide](missing.md)\n")
        self.assertTrue(any("missing.md" in error for error in validate(self.root)))

    def test_eval_cannot_read_outside_the_repository(self):
        (self.root.parent / "outside.md").write_text("private", encoding="utf-8")
        path = self.root / "evals/evals.json"
        suite = json.loads(path.read_text(encoding="utf-8"))
        suite["evals"][0]["files"] = ["../outside.md"]
        path.write_text(json.dumps(suite), encoding="utf-8")
        self.assertTrue(any("out-of-tree" in error for error in validate(self.root)))

    def test_duplicate_eval_ids_are_rejected(self):
        path = self.root / "evals/evals.json"
        suite = json.loads(path.read_text(encoding="utf-8"))
        suite["evals"][1]["id"] = suite["evals"][0]["id"]
        path.write_text(json.dumps(suite), encoding="utf-8")
        self.assertTrue(any("unique integers" in error for error in validate(self.root)))

    def test_invalid_yaml_fixture_is_rejected(self):
        path = self.root / "evals/fixtures/model-scope/project-config.yml"
        path.write_text("tools: [\n", encoding="utf-8")
        self.assertTrue(any(error.startswith("evals:") for error in validate(self.root)))

    def test_nonmapping_frontmatter_is_rejected(self):
        (self.root / "SKILL.md").write_text("---\n- invalid\n---\n", encoding="utf-8")
        self.assertTrue(any("frontmatter must be a mapping" in error for error in validate(self.root)))


if __name__ == "__main__":
    unittest.main()
