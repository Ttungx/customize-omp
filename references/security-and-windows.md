# OMP Security and Windows Reference

Use this file when a customization changes execution, approvals, credentials,
profiles, project discovery, terminal behavior, unattended operation, or
installed code.

## Trust boundaries

OMP project files, context files, skills, prompts, rules, MCP definitions,
hooks, extensions, plugins, and model descriptions can all influence execution
or model behavior. Extensions run in-process and are not sandboxed. MCP stdio
servers launch local commands; remote servers receive configured requests and
may supply instructions. Skills and system-prompt files are prompt input, not a
security boundary.

Approval modes constrain the user interaction policy, not the underlying OS:

- `always-ask` and `always-ask-cached` add confirmation gates;
- `write` approves read/write tiers and prompts for exec;
- `yolo` removes ordinary tier prompts, but explicit deny/prompt policies,
  restricted folders, provider safety checks, and critical command guards can
  still apply.

An approved `bash` or `eval` command retains ambient filesystem, network, and
subprocess access. `bash.patterns` is an approval policy, not process
containment, and does not automatically govern shell commands launched by eval.
For untrusted or unattended work, use a container, VM, dedicated low-privilege
account, or a separately isolated machine profile and credentials.

## Credential hygiene

Use `/login`, `omp login`, the auth broker, provider environment variables,
MCP OAuth storage, or command-resolved `!` values. Local credentials normally
live in the active auth store (`agent.db`), with broker mode using the shared
broker instead. Keep the auth store, broker state, session files, logs, exports,
and debug artifacts private. Review
sessions and exported HTML before sharing: prompts, file contents, command
output, URLs, and secrets can appear in them.

A project MCP file can run a command and a project model file can configure a
provider. Review both before launching an existing checkout with a profile that
holds credentials. Use a dedicated `--profile` for repositories you do not
trust; remember that this isolates OMP state, not OS permissions.

## Windows and shell behavior

Start with the installed CLI rather than assuming Pi's shell defaults:

```bash
omp --help
omp config list --json
omp --no-pty -p "..."
```

OMP's non-PTY shell path applies non-interactive environment hardening and
Windows UTF-8 defaults; PTY mode is a different path intended for interactive
programs. `PI_NO_PTY=1` and `--no-pty` disable PTY use for the process. Native
Windows process cancellation does not provide the same catchable TERM behavior
as POSIX.

On Windows, terminal key chords may be intercepted before OMP receives them.
`Ctrl+Enter` can be swallowed by Windows Terminal, and OMP commonly supplies a
`Ctrl+Q` alternative for follow-up/approval flows. Verify effective bindings
with `/hotkeys`; do not assume a remap was loaded from the wrong profile.

When a command depends on PowerShell, cmd, Git Bash, WSL, a PTY, or a native
Windows path, make that shell choice explicit and test it in the same launch
mode the user will use. A command that works in an interactive PTY is not proof
that it works in print mode, RPC, ACP, or a non-PTY tool call.

## Review checklist

Before enabling executable customization, answer:

1. Which file or package will load it, at what scope, and at what precedence?
2. Does it execute code, spawn a process, access the network, or receive
   credentials?
3. What user confirmation or restricted-folder policy applies?
4. Does the change affect the current session, later sessions, or only a new
   process/profile?
5. How can the user undo it, and what evidence confirms it is no longer active?

After editing, report the exact path, whether the file is committed/project
shared or private/user-local, the validation and smoke test, and any residual
risk from executable code or credentials.

## Authoritative references

- [Approvals are policy, not containment](https://github.com/can1357/oh-my-pi/blob/v18.14.0/docs/approval-mode.md)
- [Credential storage](https://github.com/can1357/oh-my-pi/blob/v18.14.0/docs/secrets.md)
- [Bash, embedded shell, PTY and Windows behavior](https://github.com/can1357/oh-my-pi/blob/v18.14.0/docs/bash-tool-runtime.md)
- [Keybindings and Windows Terminal](https://github.com/can1357/oh-my-pi/blob/v18.14.0/docs/keybindings.md)
- [Extension execution boundaries](https://github.com/can1357/oh-my-pi/blob/v18.14.0/docs/extension-loading.md)
