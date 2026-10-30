# OMP MCP and Tool Reference

Use this file for MCP servers, tools, approvals, eval backends, browser/LSP
tools, and subagents. MCP configuration is JSON even though OMP settings are
YAML.

## MCP locations and shape

Prefer OMP-native files:

- project: `<cwd>/.omp/mcp.json`
- user: `~/.omp/agent/mcp.json` or the active profile's equivalent

`.omp/.mcp.json`, root `mcp.json`, and root `.mcp.json` are compatibility or
fallback sources. OMP also imports MCP definitions from Claude, Codex, Gemini,
OpenCode, Cursor, Windsurf, VS Code, Agent Plugins, and marketplace plugins.
The native files have the highest discovery priority. Across providers, the
first definition wins; duplicate names are not generally merged.

A portable native file begins like this:

```json
{
  "$schema": "https://raw.githubusercontent.com/can1357/oh-my-pi/main/packages/coding-agent/src/config/mcp-schema.json",
  "mcpServers": {
    "filesystem": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/absolute/path"]
    }
  }
}
```

Supported transports are `stdio`, `http`, and legacy-compatible `sse`:

- `stdio` requires `command`; optional `args`, `env`, and `cwd`.
- `http` and `sse` require `url`; optional `headers`.
- A server must not define both `command` and `url`.
- New hosted servers should normally use Streamable HTTP (`type: "http"`).

Shared fields include `enabled`, `timeout`, `instructions`, `auth`, and `oauth`.
The user file can also define `disabledServers` and `enabledServers`; the
active-profile denylist wins over every source.

## MCP secrets and OAuth

Keep secrets outside committed JSON. OMP-native discovery expands `${VAR}` and
`${VAR:-default}` in MCP string values. Before connecting, an `env` or `headers`
value can be:

- `!command` to run a shell command and use trimmed stdout;
- the exact name of an environment variable, if it is set;
- otherwise a literal value.

Command resolution is cached for the process and has a timeout/backoff. A
failed or empty command result omits that entry. Never paste a bearer token into
`mcp.json`.

Use `/mcp add` for guided setup and `/mcp reauth <name>` for managed OAuth. Inspect the active profile's credential state before assuming a
project definition shares credentials across profiles. A project MCP definition
is trusted input and can execute a local command or use a profile credential.

After editing MCP JSON, verify in the active session:

```text
/mcp reload
/mcp list
/mcp test <name>
/mcp reconnect <name>
/mcp resources
/mcp prompts
/mcp notifications
```

Use `/mcp list` to find the winning source file, enabled state, and connection
error. If a browser MCP is hidden, check whether OMP's native browser
prelude filtered a recognized browser server; set the browser feature according
to the installed docs before disabling the native tool.

## Tool selection

OMP starts with built-in tools unless restricted. The CLI surfaces are:

```bash
omp --tools read,bash,edit,write
omp --no-tools
omp --no-lsp
omp --no-pty
```

Use `omp --help` for the installed tool list. Do not assume Pi's `--tools`
syntax or codemode exposure rules apply to OMP. A subagent may inherit or
restrict tools according to the task agent policy; a task's parent invocation
is the important authorization boundary.

OMP's eval tool can execute Python or JavaScript when enabled. Eval can define
callable tools for `task`, `agent`, or `workpool`; it is executable code and is
not made safe by a bash pattern policy. Treat eval, browser automation,
computer control, task agents, custom tools, and MCP tools as capability-bearing
surfaces.

The `lsp` tool is the preferred path for symbol-aware navigation, rename,
references, code actions, and diagnostics when a language server is available.
Do not use a text replacement for a cross-file rename when OMP LSP can perform
it. `task` spawns subagents; use it only when the user or project instructions
allow delegation and give each child a complete, bounded assignment.

## Approval policy

Tool tiers are `read`, `write`, and `exec`. Configure the global policy in
`config.yml` or override one run:

```yaml
tools:
  approvalMode: always-ask
  approval:
    bash: prompt
    read: allow
  restrictedFolders:
    - /path/that/always-needs-confirmation
```

Modes include `always-ask`, `always-ask-cached`, `write`, and `yolo`; confirm
exact values against the installed version. Runtime flags override persistent
settings:

```bash
omp --approval-mode always-ask
omp --auto-approve
omp --yolo
```

A tool's explicit `deny` or `prompt` policy, restricted folder, provider safety
check, or destructive-command guard can still require confirmation. Approval is
policy, not a filesystem or network sandbox: an approved shell retains the
host's ambient permissions. Report this distinction whenever changing approval
settings, especially for ACP or unattended runs.

## Verification checklist

When a tool or MCP change is complete, verify the effective surface, not only
syntax:

1. `omp config get <relevant-key> --json` or `/settings` for settings.
2. `/mcp list` and `/mcp test <name>` for MCP.
3. `/hotkeys` and a harmless invocation for key-bound tools.
4. A read-only LSP or eval probe before a write-capable operation.
5. A bounded task-agent smoke test only when delegation is part of the change.

Record whether the active session needs `/mcp reload`, a new session, or a full
restart.

## Authoritative references

- [MCP schema, discovery, secrets and OAuth](https://github.com/can1357/oh-my-pi/blob/v18.14.0/docs/mcp-config.md)
- [CLI flags and tool selection](https://github.com/can1357/oh-my-pi/blob/v18.14.0/docs/cli-reference.md)
- [Approval policies](https://github.com/can1357/oh-my-pi/blob/v18.14.0/docs/approval-mode.md)
- [Eval APIs and kernel permissions](https://github.com/can1357/oh-my-pi/blob/v18.14.0/docs/tools/eval.md)
- [LSP configuration](https://github.com/can1357/oh-my-pi/blob/v18.14.0/docs/lsp-config.md)
- [Task-agent discovery and definitions](https://github.com/can1357/oh-my-pi/blob/v18.14.0/docs/task-agent-discovery.md)

OMP uses eval and internal tool surfaces such as `xd://`; verify their API in
these docs when writing scripts. Pi QuickJS codemode and MCP `exposure` values
are separate APIs and should not be copied into OMP configuration.