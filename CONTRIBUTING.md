# Contributing

Keep `SKILL.md` focused on routing and workflow; put topic-specific details in
the matching `references/` file. Preserve source links and version caveats.

## Validate a change

Requires Python 3.12 and the dependency in `requirements-dev.txt`:

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python -m unittest discover -s tests -v
```

The validator checks frontmatter, reference paths, local Markdown links, and
evaluation input syntax. It runs offline and does not launch OMP, connect MCP
servers, execute fixture commands, or call a model.

When changing version-specific advice, record `omp --version` and verify it
against installed docs or the matching upstream release. Update the affected
reference first, then `SKILL.md`, both READMEs, and the changelog.
`metadata.version` tracks the OMP release being documented; it is not a claim
that every integration has been tested.

## Evaluate behavior

Use the prompts and synthetic inputs in `evals/evals.json`. Supply the fixtures
read-only and give every execution its own output sandbox outside this checkout.
Never use a real home configuration or live credentials as evaluation input.

For a comparison, launch independent with-skill and without-skill runs using the
same model and task. The baseline must not access this skill or its references.
Do not reveal target paths or answers through extra execution instructions.
Report artifact correctness separately from discovery, model routing, and live
connectivity; exclude contaminated runs from efficacy conclusions.

The fixtures contain deliberate overrides to test preservation of unrelated
configuration. Treat them as test data, not ready-to-install user defaults.

## Public reports

Include the OMP version, OS, relevant resource path/scope, expected behavior,
observed behavior, and a minimal reproduction. Use synthetic values. Keep API
keys, OAuth material, session transcripts, account data, and machine-specific
paths out of commits and issue reports.

## Before publishing

Run validation and inspect `git diff --cached --check` and
`git diff --cached --stat`. Confirm that only documentation, validation code,
and synthetic fixtures are staged. CI requires no OMP credentials or repository
secrets. Use a GitHub noreply address for public commits when keeping a personal
email private.
