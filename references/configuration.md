# OMP Configuration Reference

Use this file for settings, scope, profiles, precedence, migration, and reload
questions. Confirm exact fields with the installed `omp` version because the
registry is versioned and unknown keys are not a substitute for registered
settings.

## Paths and scope

The default profile's native agent directory is `~/.omp/agent`:

| Resource | Global | Project |
|---|---|---|
| Persistent settings | `~/.omp/agent/config.yml` (or existing `config.yaml`) | `<cwd>/.omp/config.yml` plus legacy `<cwd>/.omp/settings.json` |
| Models | `~/.omp/agent/models.yml` / `models.yaml` | Use project settings or an explicit `--config`/registry path as supported |
| MCP | `~/.omp/agent/mcp.json` or `.mcp.json` | `<cwd>/.omp/mcp.json` or `.omp/.mcp.json` |
| Keybindings | `~/.omp/agent/keybindings.yml` | Project keybinding sources are version-sensitive; confirm discovery before creating one |
| Skills | `~/.omp/agent/skills/<name>/SKILL.md` | `<ancestor>/.omp/skills/<name>/SKILL.md` |
| Commands | `~/.omp/agent/commands/*.md` | `<cwd>/.omp/commands/*.md` |
| Prompts | `~/.omp/agent/prompts/*.md` | `<cwd>/.omp/prompts/*.md` |
| Rules | `~/.omp/agent/rules/*.{md,mdc}` | `<cwd>/.omp/rules/*.{md,mdc}` |
| Hooks | `~/.omp/agent/hooks/pre/*`, `hooks/post/*` | `<cwd>/.omp/hooks/pre/*`, `hooks/post/*` |
| Extensions | `~/.omp/agent/extensions/` | `<cwd>/.omp/extensions/` |
| Themes | `~/.omp/agent/themes/<name>.json` | Confirm project theme discovery before relying on it |

Top-level prompt/context files include `AGENTS.md`, `RULES.md`, `SYSTEM.md`,
`SYSTEM_TEMPLATE.md`, `APPEND_SYSTEM.md`, `TITLE_SYSTEM.md`, and
`PERSONALITY.md`. The active profile changes the global root. External-tool
bases such as `~/.claude` are not profile-scoped.

`PI_CODING_AGENT_DIR` relocates the default-profile agent directory. Named
profiles derive their own directory and do not inherit that override. Use
`omp --profile <name> config path` to see the active path. `omp config init-xdg`
initializes supported XDG data/state/cache directories on macOS and Linux; it
does not migrate existing files or set environment variables.

## Precedence

The normal effective-setting order is:

```text
built-in defaults <- global config <- project config <- --config overlays
  <- runtime overrides <- setting environment variables
```

Repeated `--config` overlays load in order, with later files winning. Objects
deep-merge. Scalars and arrays replace the lower layer wholesale; a project
array does not append to the global array. A configured `null` usually means
unset and allows the default, except where a feature documents tombstones or
project model-role fallback.

The active profile scopes native settings, models, MCP, sessions, caches, and
auth. Keybindings are a deliberate exception: a named profile reads the default
profile keybindings first and lets the active profile override individual
bindings.

Project-native settings are scoped to the process cwd and are not discovered by
walking arbitrary ancestors for settings. Context files and system-prompt files
have their own nearest non-empty `.omp` walk; do not infer one discovery rule
from another.

## Inspect and edit settings

Use the management CLI for schema-aware changes:

```bash
omp config list
omp config list --json
omp config list --scope global --json
omp config list --scope project --json
omp config get theme.dark
omp config get theme.dark --json
omp config set compaction.enabled false
omp config set defaultThinkingLevel medium
omp config reset steeringMode
omp config path
```

`omp config set` writes the global main YAML file. It parses booleans, numbers,
enums, arrays as JSON arrays, records as JSON objects, and strings according to
the target setting schema. It cannot create arbitrary project keys. Edit a
project `.omp/config.yml` directly when a project-only override is required;
model-role storage is a documented exception when `modelRoleStorage: project`.

Before a direct edit:

1. Read the existing YAML and identify the exact setting path.
2. Preserve comments, unrelated keys, unknown intent, and array semantics where
   the chosen editor allows it.
3. Prefer a nested mapping for dotted keys, for example:

```yaml
theme:
  dark: titanium
  light: light
tools:
  approvalMode: write
  approval:
    bash: prompt
    read: allow
```

4. Validate with `omp config list --json` or `omp config get <key> --json`.

Never put secrets in a project config, an overlay that will be committed, or a
skill. Environment values and command-resolved values are not written back by
`omp config`.

## Live reload and restart

Interactive and RPC hosts watch the main global file, project settings sources,
and config overlays. A valid change is reloaded after a short debounce; an
invalid layer keeps its last good values and logs a warning. Reloading updates
settings consumed by later work, but does not rerun startup-only work, restart
already-running subagents, or switch a healthy active session's model.

Use `/settings` for interactive setting edits. Start a new session when a
setting is startup-only, when the active session captured a model/tool choice,
or when a resource's discovery is not live. Newly enabled extension modules
that were not imported at startup require a process restart. Explicitly verify
rather than promising that a generic reload is enough.

## Migration and diagnosis

When no global YAML exists, OMP can migrate legacy `settings.json` to
`config.yml`; after a successful non-empty migration it preserves the old file
as a backup. Do not manually delete legacy files during a migration request.

For a no-effect report, gather:

```bash
omp --version
omp config path
omp config list --json
omp config list --scope global --json
omp config list --scope project --json
```

Then inspect `--config` arguments, `PI_CONFIG_FILES`, setting environment
variables, the launch cwd, and profile selection. Explain which layer wins
before proposing a change.

## Authoritative references

Checked at OMP `v18.14.0`; use the installed version before applying exact keys.

- [Settings, CLI writes, merge rules and watchers](https://github.com/can1357/oh-my-pi/blob/v18.14.0/docs/settings.md)
- [Discovery, profiles and config roots](https://github.com/can1357/oh-my-pi/blob/v18.14.0/docs/config-usage.md)
- [Environment selectors](https://github.com/can1357/oh-my-pi/blob/v18.14.0/docs/environment-variables.md)
- `omp config list --json` exposes the current registered settings. For types and
  defaults, inspect the owning `register(...)` definitions collected by
  `packages/coding-agent/src/config/all-settings.ts`.
