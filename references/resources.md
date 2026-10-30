# OMP Resources Reference

Use this file for skills, slash commands, prompts, rules, context files,
system-prompt customization, themes, hooks, extensions, and plugins.

## Native resource layout

For the default profile, OMP-native user resources live below `~/.omp/agent`;
project resources live below `<cwd>/.omp`. A named profile changes the active
user root. Native directory sources for commands, prompts, rules, hooks, tools,
extensions, and settings must normally exist and be non-empty before they are
admitted. Skills are the notable exception: OMP scans each ancestor's
`.omp/skills` tree and the user skills tree even when the surrounding `.omp`
directory is otherwise empty.

```text
~/.omp/agent/                         # active global root
  AGENTS.md                            # user context
  RULES.md                             # user sticky rule
  SYSTEM.md                            # plain custom system block
  SYSTEM_TEMPLATE.md                   # Handlebars system template
  APPEND_SYSTEM.md                     # append text
  TITLE_SYSTEM.md                      # title-generation prompt
  PERSONALITY.md                       # personality replacement
  config.yml                           # settings
  models.yml                           # providers and models
  mcp.json                             # MCP servers
  keybindings.yml                      # action -> chord mapping
  skills/<name>/SKILL.md
  commands/*.md
  prompts/*.md
  rules/*.{md,mdc}
  hooks/pre/*
  hooks/post/*
  extensions/*.{ts,js}
  themes/<name>.json

<repo>/.omp/
  AGENTS.md
  RULES.md
  SYSTEM.md / SYSTEM_TEMPLATE.md
  APPEND_SYSTEM.md
  commands/*.md, prompts/*.md, rules/*.{md,mdc}
  skills/<name>/SKILL.md
  hooks/pre/*, hooks/post/*
  extensions/*.{ts,js}
  config.yml, mcp.json
```

The native project context provider uses the nearest non-empty `.omp` directory
for `.omp/AGENTS.md`, `RULES.md`, and system-prompt files. Standalone ancestor
`AGENTS.md`/`CLAUDE.md` files are discovered by their own providers. Do not
assume every resource walks ancestors in the same way.

## Skills

Use one directory per skill with explicit frontmatter:

```markdown
---
name: release-check
description: Check release metadata and run the project's release validation.
---

# Release Check
...
```

The conventional path is `<skills-root>/<name>/SKILL.md`, one level below
`skills/`; nested groups are not recursively discovered unless
`skills.customDirectories` points at the nested parent. Native OMP skills require
a meaningful description for reliable routing.

Important behavior:

- `description` is the primary routing signal; make it specific and pushy
  enough to cover the real trigger branches.
- `globs` and `alwaysApply` are metadata, not automatic invocation controls in
  the normal OMP skill loader.
- `hide`/`disableModelInvocation` can hide a skill from the advertised list
  while leaving it reachable through `skill://` and `/skill:<name>`.
- `skills.includeSkills`, `skills.ignoredSkills`, `--skills`, and
  `disabledExtensions` can filter skills.
- A differing same-name skill keeps the bare name at higher precedence; other
  copies remain reachable under a namespace such as `plugin/name`. Identical
  copies collapse.
- Use `/skill:<name>` for an explicit smoke test. It can also appear as a token
  in normal prose when skill commands are enabled.
- Keep referenced scripts/assets inside the skill directory and resolve them
  through `skill://<name>/...` or the injected skill directory.

## Commands, prompts, and rules

A Markdown file in `commands/` becomes a slash command. A Markdown file in
`prompts/` is a reusable prompt template. File commands support `description`
and `argument-hint` frontmatter, `$1`, `$2`, `$ARGUMENTS` / `$@`, and 1-based
slices such as `$@[2:3]`. Missing positional arguments become empty strings.
Inspect the installed command and prompt docs before using template-specific
syntax; the command pipeline and a system-prompt Handlebars template are
different routes.

Normal rules live in `rules/*.{md,mdc}` and may use rule metadata such as
`globs`, `alwaysApply`, `description`, conditions, and scopes. Top-level
`RULES.md` is different: it is a native always-apply sticky rule. Keep it short;
put background and procedures in `AGENTS.md`, a skill, or a normal rule.

Context files are not skills. `AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, and related
files are loaded automatically through their providers. The native
`.omp/AGENTS.md` is the recommended OMP project context form; standalone
`AGENTS.md` can walk repository ancestors. Task subagents do not inherit
`AGENTS.md` context files, while sticky `RULES.md` behavior remains distinct.

## System-prompt customization

Choose deliberately:

| Goal | File/flag |
|---|---|
| Keep default prompt and add instructions | `APPEND_SYSTEM.md` or `--append-system-prompt` |
| Replace default instruction block with plain text | `SYSTEM.md` or `--system-prompt` |
| Replace it with live Handlebars | `SYSTEM_TEMPLATE.md` or `--system-prompt-template <path>` |
| Customize title generation | `TITLE_SYSTEM.md` |
| Replace the personality block | user-level `PERSONALITY.md` |
| Replace every provider-facing system block | programmatic API `systemPrompt` only |

`SYSTEM.md` still keeps OMP-generated skills, rules, and project footer. A
`SYSTEM_TEMPLATE.md` is a raw Handlebars template: it must reference every
live data section it needs and is not a selective inheritance mechanism. Plain
files are inserted as plain text; Handlebars is compiled only on the template
route. A literal `SYSTEM.md` at the same scope wins over a template.

Protect system-prompt files like code: they influence every request. After a
change, start a new session or use the documented reload/reset path and verify
that the generated prompt contains the intended context without duplicating
skills, rules, or append text.

## Themes and keybindings

Custom themes are strict JSON in `themes/<name>.json`, not YAML. They need a
`name`, `colors`, and all required color tokens; optional `vars`, `export`, and
`symbols` sections are version-sensitive. Confirm the current schema before
copying a theme. The theme setting uses dark/light slots; an unknown or invalid
theme falls back according to OMP's runtime behavior and logs the failure.

Keybindings are a separate YAML mapping in `keybindings.yml`, not a nested
`keybindings` object in `config.yml`:

```yaml
app.model.cycleForward: Ctrl+P
app.model.selectTemporary: Alt+P
app.plan.toggle: Alt+Shift+P
app.history.search: []
```

Use `/hotkeys` to see installed action IDs and current remaps. Chords are
case-insensitive. An empty array disables an action. On Windows Terminal,
`Ctrl+Enter` may be swallowed; OMP supplies `Ctrl+Q` alternatives for some
actions, but verify with `/hotkeys`.

## Hooks, extensions, and plugins

Use a hook for an event interceptor, an extension for executable tools/commands,
providers, UI, lifecycle state, or custom APIs, and a plugin when several
resources should ship together. Native extension modules are discovered from
`extensions/`; configured paths can be set in `config.yml`, and `-e/--extension`
loads an explicit module for one run. `--no-extensions` disables ambient
extension discovery but still permits explicit paths.

Extensions run in the OMP process and are not sandboxed. A newly enabled module
that was not imported at startup needs a restart; settings changes can suspend
or resume already-loaded sources. `--trusted-extension <absolute-file>` is an
exact module allowlist, not a whole-process sandbox.

For a distributable bundle, use OMP plugin conventions and pin Git refs or
versions. Useful commands include:

```bash
omp plugin marketplace add owner/repo
omp plugin marketplace list
omp plugin install name@marketplace
omp plugin list
omp plugin upgrade
omp plugin uninstall name@marketplace
```

Review plugin manifests and source before install. Project-scoped plugins can
shadow user-scoped installs of the same ID, and plugin resources may include
skills, commands, rules, hooks, tools, extensions, and MCP servers.

## Authoritative references

- [Skill layout, filters, namespaces and invocation](https://github.com/can1357/oh-my-pi/blob/v18.14.0/docs/skills.md)
- [Commands and argument substitution](https://github.com/can1357/oh-my-pi/blob/v18.14.0/docs/slash-command-internals.md)
- [Context files and sticky rules](https://github.com/can1357/oh-my-pi/blob/v18.14.0/docs/context-files.md)
- [System prompt routes and session-type inheritance](https://github.com/can1357/oh-my-pi/blob/v18.14.0/docs/system-prompt-customization.md)
- [Theme schema and live changes](https://github.com/can1357/oh-my-pi/blob/v18.14.0/docs/theme.md)
- [Keybinding action IDs](https://github.com/can1357/oh-my-pi/blob/v18.14.0/docs/keybindings.md)
- [Extension discovery and restarts](https://github.com/can1357/oh-my-pi/blob/v18.14.0/docs/extension-loading.md)
- [Plugin authoring and install scope](https://github.com/can1357/oh-my-pi/blob/v18.14.0/docs/skills/authoring-marketplaces.md)
