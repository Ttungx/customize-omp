# OMP Runtime Reference

Use this file for models, providers, authentication, role selection, extensions,
custom tools, sessions, and runtime APIs.

## Models and providers

OMP's built-in and configured model catalog is controlled by
`<active-agent-dir>/models.yml` (or `models.yaml`). Legacy `models.json` can be
migrated when YAML is absent. The root key consumed by the model registry is
`providers`:

```yaml
providers:
  my-gateway:
    baseUrl: https://api.example.com/v1
    apiKey: MY_PROVIDER_API_KEY
    api: openai-completions
    models:
      - id: model-id
        name: Model Name
        contextWindow: 128000
        maxTokens: 16384
```

Provider-level fields include `baseUrl`, `apiKey`, `api`, `headers`, `auth`,
`authHeader`, `disableStrictTools`, `discovery`, `modelOverrides`, and provider
compatibility settings. Custom model entries can define their own API, URL,
context, token limits, reasoning, input modalities, cost, headers, and compat
fields. Exact allowed API values and model metadata change; use the installed
`docs/models.md` and the model config schema instead of inventing fields.

Provider keys and headers may use `!command` to resolve a secret from command
stdout. Prefer `/login`, stored auth, environment variables, or the OMP auth
broker. Do not commit `apiKey` values. `omp auth` and `omp login` help inspect
or establish provider credentials without copying them into project files.

Useful inspection commands:

```bash
omp models
omp models --help
omp auth --help
omp login --help
omp config get modelRoles --json
```

The effective model identity is `provider/modelId`. Use the exact provider
prefix when two providers expose the same model ID. Model roles such as
`default`, `smol`, `slow`, `plan`, `judge`, `tiny`, or other version-specific
roles are settings, not universal provider names; confirm the local catalog.
Runtime flags such as `--model`, `--smol`, `--slow`, `--plan`, `--thinking`, and
`--api-key` override persistent choices for one process/session.

## Discovery and reload

Model registry composition generally starts with `models.yml`, merges bundled
models, cached/discovered rows, custom models, extension registrations, and
model overrides, then resolves roles and context policies. An extension's model
registration is executable runtime behavior; inspect it before enabling it.

`/model` or the installed model selector re-reads the catalog where supported.
A setting reload can change later role/fallback decisions but does not
necessarily switch a healthy active session's model. Verify the model shown in
the session after changing a default.

## Extensions and custom tools

Extensions are TypeScript/JavaScript modules that can register tools, commands,
providers, model rows, flags, shortcuts, UI renderers, hooks, lifecycle
handlers, and state. A module's default export is the extension factory. OMP
loads modules in discovery order, catches per-module load failures, and runs
extension code in the same process/runtime as OMP.

A custom tool should declare a name, description, parameters schema, execution
function, and an appropriate approval tier. Extensions may use `pi.registerTool`
and lifecycle APIs documented by the installed SDK. Hook handlers such as
`tool_call` can block a call; fail-safe behavior matters because a hook runs at
the point of execution. Read the OMP extension and hook docs before writing
against event names or TypeScript types.

`--no-extensions` is ambient-discovery control, not a security sandbox. Explicit
`-e`, `--hook`, and trusted paths have separate semantics. New files added to an
already loaded configured directory may require a restart even when settings
watchers are live.

## Eval, task, and sessions

OMP can expose Python and JavaScript eval backends, browser automation,
computer control, LSP, notebooks, web search, and `task` subagents depending on
settings and tool availability. Treat these as runtime capabilities, not mere
text templates. Python may require `omp setup python`; optional local models and
native features have their own setup commands.

`task` launches bounded subagents. Use a complete task description, define the
solution space when automatic effort selection is active, and avoid passing
more tools or permissions than required. Isolated tasks/worktrees are useful
for changes that should not touch the main checkout, but isolation settings and
fields are version-sensitive.

Sessions live below the active profile's agent data. Relevant commands and
flags include:

```bash
omp -c                         # continue
omp -r <session-or-path>       # resume
omp --restore <session-path>   # resume unfinished work
omp --no-session               # ephemeral run
omp --profile <name>           # isolated profile
omp --export <session-path>    # export HTML
omp session --help
```

A profile isolates auth, sessions, configuration, and caches; use it for
experiments or separate accounts, but do not describe it as sandboxing the
process or workspace.

## Authoritative references

- [Model registry and models.yml schema](https://github.com/can1357/oh-my-pi/blob/v18.14.0/docs/models.md)
- [Providers and credential precedence](https://github.com/can1357/oh-my-pi/blob/v18.14.0/docs/providers.md)
- [Auth storage and broker](https://github.com/can1357/oh-my-pi/blob/v18.14.0/docs/secrets.md)
- [Extension API, TypeScript types and events](https://github.com/can1357/oh-my-pi/blob/v18.14.0/docs/extensions.md)
- [Extension authoring patterns](https://github.com/can1357/oh-my-pi/blob/v18.14.0/docs/skills/authoring-extensions.md)
- [Custom tools](https://github.com/can1357/oh-my-pi/blob/v18.14.0/docs/custom-tools.md)
- [Session resume, export and sharing](https://github.com/can1357/oh-my-pi/blob/v18.14.0/docs/session-operations-export-share-fork-resume.md)
