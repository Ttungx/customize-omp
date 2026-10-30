---
name: customize-omp
description: >-
  Customize oh-my-pi (OMP), the omp terminal coding agent: route requests to the
  correct config file, scope, resource, CLI surface, and verification step.
  Use this skill whenever the user asks to configure, migrate, diagnose, review,
  explain, or extend OMP settings, profiles, models, providers, MCP servers,
  skills, commands, prompts, rules, themes, keybindings, hooks, extensions,
  plugins, eval tools, approvals, or project discovery, even when they only say
  that omp is ignoring a setting or a resource is missing.
license: MIT
compatibility: Requires oh-my-pi (`omp`); exact schemas and defaults are version-sensitive.
metadata:
  version: "18.14.0"
---

# Customize OMP

Oh My Pi is a terminal coding agent whose behavior is assembled from settings,
profiles, project discovery, models, MCP servers, skills, prompts, rules,
themes, keybindings, hooks, extensions, and plugins. This skill routes a
customization request to the smallest mechanism that OMP will actually load,
then verifies the effective surface instead of trusting a file edit.

The design goal is reversible, inspectable customization. Identify the resource
and scope first, preserve unrelated user intent, keep secrets out of copied
configuration, and prefer the documented `omp` management surface over manual
rewrites. OMP is not Pi with a renamed directory: its canonical settings are
YAML, MCP remains JSON, and OMP capability discovery has its own precedence and
reload behavior.

## Version discipline

This skill targets `omp 18.14.0`, checked against the upstream `v18.14.0` docs
(commit `31147f9d1a76608549821c3759f8487b4d66c72d`). OMP changes quickly, so
confirm exact keys, defaults, commands, and paths when the installed version
differs. Start with:

```bash
omp --version
omp config path
omp config list --json
```

The `metadata.version` entry identifies the OMP release documented here. When
the installed version differs, confirm the affected reference against the
installed OMP docs or the matching upstream release before editing. Prefer docs
bundled with the installed package; binary installs may have none. Fall back to
`https://github.com/can1357/oh-my-pi/tree/v<installed-version>/docs` and its
source/schema files. Use `main` only when no matching release is available and
state that limitation. Each reference links to the release used here.
Keep the version assumption visible in the final report.

## Progressive disclosure

1. Identify the resource: setting, model, MCP server, skill, command, prompt,
   rule, context file, theme, keybinding, hook, extension, plugin, or runtime
   policy.
2. Read the matching reference under `references/`; it contains the working
   schema and OMP-specific caveats.
3. Confirm the exact behavior against the installed binary and docs. Use
   `omp --help`, `omp <command> --help`, `/settings`, `/hotkeys`, `/mcp`, and
   `omp config` as applicable.
4. Inspect the existing file and effective scopes before changing it. Preserve
   unknown keys and unrelated intent; do not replace a whole YAML or JSON file
   to change one value.
5. Before writing, state the target path/scope, the smallest change, and whether
   live reload, `/reload`, a new session, or a process restart is required.
6. Apply the documented surface where one exists, then verify the loaded result.

Reference map:

- `references/configuration.md`: paths, profiles, YAML settings, precedence,
  merge rules, `omp config`, project discovery, reload, and migration.
- `references/mcp-and-tools.md`: MCP JSON, transports, OAuth, secret
  indirection, tool selection, approvals, eval, browser, LSP, and tasks.
- `references/resources.md`: skills, commands, prompts, rules, context files,
  system prompts, themes, hooks, extensions, and plugins.
- `references/runtime.md`: models, providers, auth, `models.yml`, model roles,
  extensions, custom tools, sessions, and runtime APIs.
- `references/security-and-windows.md`: trust boundaries, credentials,
  profiles, shell/PTY behavior, Windows notes, and review risks.

## Choose the mechanism

Choose the least powerful mechanism that fully satisfies the goal:

| Goal | OMP surface | Reason |
|---|---|---|
| Persistent project or user instructions | `.omp/AGENTS.md`, `AGENTS.md`, or `.omp/RULES.md` / `RULES.md` | Context or sticky rules, without executable code |
| Replace or append system-prompt behavior | `SYSTEM.md`, `SYSTEM_TEMPLATE.md`, `APPEND_SYSTEM.md` | Prompt customization without an extension |
| A repeatable knowledge/workflow pack | `skills/<name>/SKILL.md` | Model-readable capability with optional assets |
| A user-invoked slash command or prompt | `.omp/commands/*.md` or `.omp/prompts/*.md` | Text template/command, no runtime code |
| Preference, provider selection, approval, or tool policy | `config.yml`, edited with `omp config` where supported | Schema-aware persistent settings |
| Model/provider definition | `models.yml` | Catalog and transport configuration |
| MCP server | `.omp/mcp.json` or `~/.omp/agent/mcp.json` | OMP-native MCP discovery and management |
| Keyboard behavior or theme | `keybindings.yml`, `themes/<name>.json` | Declarative TUI customization |
| Event-driven or executable behavior | hook/extension module or plugin | Requires OMP runtime APIs and user permissions |
| Installable bundle for other users | OMP plugin/marketplace package | Declares and ships resources together |
| One-run experiment | `--config <file>`, `--profile <name>`, `-e/--extension` | Isolated or explicit loading without mutating defaults |

When two surfaces can work, prefer the one earlier in this table: it is easier
to review, undo, and explain. Do not turn a setting or prompt request into an
extension merely because an extension can do it.

## Diagnose before changing

Treat "OMP ignores this" as a scope, discovery, load, or precedence problem:

| Symptom | Check first | Common cause |
|---|---|---|
| A setting has no effect | `omp config list --json`, `omp config get <key>`, project config, `--config`, and setting env vars | A higher-precedence project, overlay, runtime, or environment value wins; arrays replace rather than append |
| A project setting is ignored | Current `cwd`, `<cwd>/.omp/config.yml`, and whether the process was launched from the intended directory | Native settings are cwd-scoped; some context/system resources use nearest non-empty `.omp` discovery |
| A skill is absent or never routes | `--no-skills`, `--skills`, `skills.enabled`, path/layout, frontmatter, `/skill:<name>` | Wrong one-level layout, missing description, collision namespace, include/ignore filter, or disabled provider |
| A command, prompt, rule, hook, or extension is absent | Effective resource settings, startup diagnostics, resource path, `--no-extensions`, `--extension`, `disabledExtensions` | Root was empty, source was disabled, explicit paths were omitted, or a newly enabled module needs a restart |
| MCP has no tools | `/mcp list`, `/mcp reload`, `/mcp test <name>`, source file, transport fields, env resolution | Wrong JSON shape, disabled or shadowed server, missing command/URL, auth failure, or project MCP disabled |
| A model is missing | `omp models`, `omp models --help`, auth state, `models.yml`, `enabledProviders`/`disabledProviders` | No credential, provider disabled, malformed custom model, or a role points at an unavailable model |
| Approval is surprising | `tools.approvalMode`, `tools.approval`, `tools.restrictedFolders`, `--approval-mode`, `--auto-approve` | Tier policy, explicit deny/prompt, restricted folder, or runtime override wins |
| A theme or keybinding is not active | `/hotkeys`, theme setting, exact file name/schema, active profile | `keybindings.yml` is separate from `config.yml`; a strict theme failed validation; profile inheritance differs |
| A reload did not fix it | Re-check startup-only behavior and the active session's runtime overrides | Some changes apply to new sessions or require a process restart; reload does not undo every runtime choice |

A report, diagnosis, or review is read-only. Show evidence, paths, effective
values, a proposed diff, and residual risks; do not modify files unless the
user asks for the edit.

## Scope and safety invariants

- Global native configuration normally lives under `~/.omp/agent`; named
  profiles use `~/.omp/profiles/<name>/agent`. `PI_CODING_AGENT_DIR` relocates
  the default profile, and `OMP_PROFILE`/`PI_PROFILE` select a profile.
- Project-native settings live under `<cwd>/.omp`. Project files are not a
  sandbox: commands, MCP servers, hooks, extensions, plugins, and tools can run
  with the user's OS permissions.
- Settings precedence is generally built-in defaults, global config, project
  config, `--config` overlays, runtime flags, then setting environment variables.
  Later overlays win; objects deep-merge, while arrays and scalars replace.
- Put credentials in OMP auth storage, provider login flows, environment
  variables, or command-resolved values. Never paste tokens into project
  config, skills, prompts, MCP files, reports, or committed plugin metadata.
- Review executable extension/plugin/MCP code before enabling it. A profile
  isolates configuration, sessions, auth, and caches; it is not an OS sandbox.
- After an edit, report the exact paths changed, backup/diff status, validation
  performed, reload/new-session/restart requirement, version assumption, and
  remaining security or compatibility risks.
