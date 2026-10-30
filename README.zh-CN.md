# customize-omp

[English](README.md)

用于配置、扩展和排查 [oh-my-pi（OMP）](https://github.com/can1357/oh-my-pi) 的 Agent Skill。入口是 [SKILL.md](SKILL.md)，具体配置细节按主题放在 `references/`，由代理按需读取。

这是受 [customize-pi](https://github.com/Ttungx/customize-pi) 启发的社区维护技能。工作方式相同：先选择合适的机制和作用域，核对当前版本的文档与实际配置，再做最小修改，并验证 OMP 是否加载了结果。诊断和审阅保持只读；执行修改时保留无关配置，说明重载方式和撤销方法。

## 覆盖范围与适配版本

- `config.yml`、配置层级、profiles、环境变量和迁移。
- `models.yml`、模型角色、provider、登录和凭据。
- `mcp.json`、MCP 传输、OAuth、工具、eval 和审批。
- skills、commands、prompts、rules、上下文文件和系统提示词。
- themes、`keybindings.yml`、hooks、extensions、plugins 和 Windows 行为。

技能主体及配置参考使用英文。当前适配 **OMP 18.14.0**，已核对本机 CLI 和上游 [v18.14.0](https://github.com/can1357/oh-my-pi/tree/v18.14.0) 文档，来源 commit 为 `31147f9d1a76608549821c3759f8487b4d66c72d`。每份参考都提供固定版本的来源链接；`SKILL.md` 的 `metadata.version` 表示文档对应的 OMP 版本。安装版本不一致时，应重新核对受影响的字段和命令。

## 安装

克隆安装需要 OMP 和 Git。Python 仅用于仓库校验，使用技能本身不依赖 Python。

先确认当前配置目录；命名 profile 使用独立目录：

```bash
omp config path
# 或
omp --profile work config path
```

默认 profile 可使用以下命令。目标目录已存在时，先检查已有安装：

```bash
git clone https://github.com/Ttungx/customize-omp.git ~/.omp/agent/skills/customize-omp
```

使用命名 profile 或自定义 agent 目录时，将 `~/.omp/agent` 替换为上面命令返回的路径。仅供某个项目使用时，从项目根目录执行：

```bash
git clone https://github.com/Ttungx/customize-omp.git .omp/skills/customize-omp
```

也可以将 `SKILL.md`、整个 `references/` 和 `LICENSE` 复制到同一个 `customize-omp` 目录，保留相对布局。需要可复现安装时，在克隆目录中检出已审阅的 commit。

从目标项目启动新 OMP 会话，输入：

```text
/skill:customize-omp
```

检查 OMP 能否读取技能和参考文件：

```bash
omp read skill://customize-omp
omp read skill://customize-omp/references/configuration.md
```

如果未发现技能，检查当前 profile、`skills.enabled`、include/ignore 过滤项、`--no-skills` 和名称冲突。

## 使用示例

```text
/skill:customize-omp 把这个项目的默认模型改成 openai/gpt-5.2，不影响其他项目
/skill:customize-omp 检查为什么 .omp/mcp.json 里的服务没有加载，先不要修改文件
/skill:customize-omp 给 OMP 增加一个按需使用的发布检查 skill
```

模型也可以根据普通配置请求自动选择技能。自动选择取决于模型；显式 `/skill:customize-omp` 可直接调用。安装文件本身不会修改现有 OMP 设置、凭据或启动参数。

## 文件导航

| 文件 | 用途 |
|---|---|
| [SKILL.md](SKILL.md) | 机制选择、诊断路由和修改流程 |
| [configuration.md](references/configuration.md) | 路径、profiles、设置、优先级和重载 |
| [mcp-and-tools.md](references/mcp-and-tools.md) | MCP、工具、eval 和审批 |
| [resources.md](references/resources.md) | 技能、提示词、规则、主题和插件 |
| [runtime.md](references/runtime.md) | 模型、认证、扩展 API 和会话 |
| [security-and-windows.md](references/security-and-windows.md) | 权限边界、凭据和 Windows |
| [evals.json](evals/evals.json) | 测试提示、合成输入和预期结果 |

## 校验与维护

```bash
python -m pip install -r requirements-dev.txt
python scripts/validate.py
python -m unittest discover -s tests -v
```

CI 在 Linux 和 Windows 上执行这些检查，覆盖 frontmatter、参考路径、Markdown 本地链接、夹具语法和测试输入。此前的隔离 OMP 18.14.0 检查确认了配置覆盖关系，以及技能和参考文件 URI 的读取。这些检查不代表已测试真实 MCP 连通性、全部 SDK 兼容性或自动触发准确率。

维护方法见 [CONTRIBUTING.md](CONTRIBUTING.md)。行为测试在隔离目录中执行；会话记录、凭据、本机配置和评测输出保留在仓库外。

## 许可证

[MIT](LICENSE)。变更记录见 [CHANGELOG.md](CHANGELOG.md)。
