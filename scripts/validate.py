"""Validate the skill, local documentation links, and synthetic eval inputs offline."""

import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

import yaml

ROOT = Path(__file__).resolve().parents[1]
FRONTMATTER_KEYS = {
    "name", "description", "license", "compatibility", "metadata",
    "allowed-tools", "disable-model-invocation",
}


def local_file(root, owner, target):
    path = (owner.parent / unquote(target)).resolve()
    if not path.is_relative_to(root.resolve()) or not path.is_file():
        raise ValueError(f"missing or out-of-tree local file: {target}")
    return path


def validate(root=ROOT):
    errors = []
    skill = root / "SKILL.md"
    try:
        text = skill.read_text(encoding="utf-8")
        match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)", text, re.S)
        if not match:
            raise ValueError("missing YAML frontmatter")
        metadata = yaml.safe_load(match.group(1))
        if not isinstance(metadata, dict):
            raise ValueError("frontmatter must be a mapping")
        if metadata.get("name") != "customize-omp":
            raise ValueError("name must be customize-omp")
        if not isinstance(metadata.get("description"), str) or not metadata["description"].strip():
            raise ValueError("description must be a nonempty string")
        if metadata.keys() - FRONTMATTER_KEYS:
            raise ValueError("unsupported frontmatter fields")
        version = metadata.get("metadata", {}).get("version")
        if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+", version):
            raise ValueError("metadata.version must be an OMP release string")
        if metadata.get("license") != "MIT" or not (root / "LICENSE").is_file():
            raise ValueError("MIT metadata and LICENSE file must both be present")
        if len(text.splitlines()) >= 500:
            raise ValueError("keep SKILL.md below 500 lines; move detail into references")
        references = set(re.findall(r"`(references/[^`\s]+\.md)`", text))
        if not references:
            raise ValueError("SKILL.md must route to bundled references")
        for reference in references:
            local_file(root, skill, reference)
    except (OSError, ValueError, AttributeError, yaml.YAMLError) as exc:
        errors.append(f"SKILL.md: {exc}")

    markdown_files = [*root.glob("*.md"), *root.glob("references/*.md")]
    for document in markdown_files:
        try:
            body = document.read_text(encoding="utf-8")
            if body.count("```") % 2:
                raise ValueError("unclosed code fence")
            for target in re.findall(r"\[[^\]]*\]\(([^)\s]+)\)", body):
                url = urlsplit(target)
                if not url.scheme and url.path:
                    local_file(root, document, url.path)
        except (OSError, ValueError) as exc:
            errors.append(f"{document.relative_to(root)}: {exc}")

    try:
        evaluation_file = root / "evals/evals.json"
        suite = json.loads(evaluation_file.read_text(encoding="utf-8"))
        if not isinstance(suite, dict) or suite.get("skill_name") != "customize-omp":
            raise ValueError("skill_name must be customize-omp")
        cases = suite.get("evals")
        if not isinstance(cases, list) or not cases:
            raise ValueError("evals must be a nonempty list")
        ids = set()
        for case in cases:
            if not isinstance(case, dict):
                raise ValueError("each eval must be an object")
            case_id = case.get("id")
            if type(case_id) is not int or case_id in ids:
                raise ValueError("eval IDs must be unique integers")
            ids.add(case_id)
            for field in ("prompt", "expected_output"):
                if not isinstance(case.get(field), str) or not case[field].strip():
                    raise ValueError(f"eval {case_id}: {field} must be nonempty text")
            for field in ("files", "expectations"):
                value = case.get(field)
                if not isinstance(value, list) or not value or not all(isinstance(item, str) and item.strip() for item in value):
                    raise ValueError(f"eval {case_id}: {field} must contain nonempty strings")
            for filename in case["files"]:
                local_file(root, root / "SKILL.md", filename)
        for fixture in (root / "evals/fixtures").rglob("*"):
            if fixture.suffix == ".json":
                json.loads(fixture.read_text(encoding="utf-8"))
            elif fixture.suffix in (".yml", ".yaml"):
                if not isinstance(yaml.safe_load(fixture.read_text(encoding="utf-8")), dict):
                    raise ValueError(f"fixture must be a YAML mapping: {fixture.relative_to(root)}")
    except (OSError, ValueError, yaml.YAMLError) as exc:
        errors.append(f"evals: {exc}")
    return errors


if __name__ == "__main__":
    problems = validate()
    for problem in problems:
        print(problem, file=sys.stderr)
    if not problems:
        print("Skill metadata, bundled references, local links, and eval fixtures are valid.")
    sys.exit(bool(problems))
