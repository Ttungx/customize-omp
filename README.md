# customize-omp

[简体中文](README.zh-CN.md)

An Agent Skill for configuring, extending, and troubleshooting
[oh-my-pi (OMP)](https://github.com/can1357/oh-my-pi). It helps a coding agent
choose the right mechanism and scope, preserve existing configuration, and
verify what OMP actually loads.

Inspired by [customize-pi](https://github.com/Ttungx/customize-pi), this is a
community-maintained skill for OMP. It follows the same workflow: diagnose
first, use the smallest suitable mechanism, load detailed references on demand,
and keep changes reversible. Reviews and diagnoses stay read-only unless an
edit is requested.

## Coverage and compatibility

- YAML settings, profiles, precedence, environment variables, and migration.
- Models, provider endpoints, model roles, authentication, and credentials.
- MCP servers, transports, OAuth, tools, eval, and approval policies.
- Skills, commands, prompts, rules, context files, and system prompts.
- Themes, keybindings, hooks, extensions, plugins, and Windows behavior.

The references target **OMP 18.14.0**, checked against the local CLI and
[upstream v18.14.0](https://github.com/can1357/oh-my-pi/tree/v18.14.0)
(commit `31147f9d1a76608549821c3759f8487b4d66c72d`). Each reference links to its
source. `metadata.version` in `SKILL.md` tracks the documented OMP release.
Recheck affected fields and commands when the installed OMP version differs.

## Install

Requires OMP and Git for the clone method. Python is only needed for repository
validation; using the skill requires no Python dependency.

Find the active agent directory:

```bash
omp config path
# For a named profile:
omp --profile work config path
```

For the default profile, clone into its skills directory:

```bash
# Run only when the target directory does not already exist.
git clone https://github.com/Ttungx/customize-omp.git ~/.omp/agent/skills/customize-omp
```

For a named profile or a custom agent directory, replace `~/.omp/agent` with the
path reported above. For project-only use, run this from the project root:

```bash
git clone https://github.com/Ttungx/customize-omp.git .omp/skills/customize-omp
```

You can also copy `SKILL.md`, `references/`, and `LICENSE` into the same
`customize-omp` directory. Keep their relative layout. For reproducible installs,
check out a reviewed commit in the clone.

Start a new OMP session from the intended project, then invoke:

```text
/skill:customize-omp
```

Check that OMP discovers the skill and its bundled references:

```bash
omp read skill://customize-omp
omp read skill://customize-omp/references/configuration.md
```

If discovery fails, check the active profile, `skills.enabled`, include/ignore
filters, `--no-skills`, and name collisions.

## Use

```text
/skill:customize-omp set a project-only default model without affecting other repositories
/skill:customize-omp diagnose why .omp/mcp.json is ignored; report findings before editing
/skill:customize-omp create an on-demand release checklist for this project
```

The model can also select the skill from ordinary OMP customization requests.
Automatic selection depends on the model; explicit invocation is available.
Installing the files does not edit OMP settings or credentials.

## Layout

| File | Purpose |
|---|---|
| [SKILL.md](SKILL.md) | Mechanism selection, diagnosis, and change workflow |
| [Configuration](references/configuration.md) | Paths, profiles, precedence, and reload |
| [MCP and tools](references/mcp-and-tools.md) | Servers, secret indirection, eval, and approvals |
| [Resources](references/resources.md) | Skills, prompts, rules, themes, and plugins |
| [Runtime](references/runtime.md) | Models, providers, auth, extensions, and sessions |
| [Security and Windows](references/security-and-windows.md) | Permissions, credentials, shells, and terminals |
| [Evaluations](evals/evals.json) | Synthetic task prompts, fixtures, and expected outcomes |

## Validation and maintenance

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python -m unittest discover -s tests -v
```

CI runs these checks on Linux and Windows. They validate frontmatter, reference
paths, local Markdown links, fixture syntax, and evaluation inputs. The earlier
isolated OMP 18.14.0 smoke check confirmed settings precedence and skill/reference
URI reads. These checks do not establish live MCP connectivity, exhaustive SDK
compatibility, or automatic routing accuracy.

See [CONTRIBUTING.md](CONTRIBUTING.md) for updating references and running
behavior evaluations. Session transcripts, credentials, machine-specific
configuration, and evaluation outputs should remain outside the repository.

## License

[MIT](LICENSE). See [CHANGELOG.md](CHANGELOG.md) for changes.
