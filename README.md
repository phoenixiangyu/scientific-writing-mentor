# Scientific Writing Mentor · 科技论文写作导师

把科研材料整理成清晰、有证据支撑的论文。支持大纲、章节起草、论证重构、中文和英文学术润色，以及 ES&T / Nature 等目标期刊的适配。

本 skill 根据 Hilary Glasman-Deal《英语科技写作（第二版）》和邵森林《写好科技论文的一些建议》提炼写作决策规则；来源位置见 [source-map](skills/scientific-writing-mentor/references/source-map.md)。它不是期刊官方工具。

## v2.0 导师要求

默认执行[导师写作重点](skills/scientific-writing-mentor/references/advisor-priorities.md)：句子聚焦精炼、减少套话；结果小节先交代科学目的，每段有明确结论和适当收束；段落之间有逻辑衔接；先呈现已证实的价值，再交代相关权衡；相关图围绕同一问题合讲；caption 只保留读图必需信息。

普通润色默认保留 Methods 以外的既定结构，允许小节内精简、衔接和合并相关邻段。当前任务若要求重构或新大纲，则按其范围处理。上述规则不允许隐去关键负结果、补造数据或用泛化意义句充当结论。

## 使用

直接说：

> 按照 ES&T 修改润色这段讨论，保留数值和引用；正文保持流畅，缺少依据的问题放在批注中。

> 根据这些结果和图表拟一个论文大纲，说明各节承担的论证作用。

也可以显式调用：

```text
$scientific-writing-mentor 按照 Nature Communications 修改摘要，与可用的 nature-polishing 协作。
```

指定 Nature 系列时，最好写出具体刊名。精确的篇幅、栏目和格式要求以任务发生时的官方指南为准。

### 正文和批注

正文使用材料支持的表述，缺失依据、统计问题和核实事项放在锚定批注中；支持时采用 Word 原生批注，否则交付附带准确文字锚点的问题清单。不会编造实验、引用、机制或显著性，也不会以润色改变实质结论。影响结论的科学边界仍应在正文中准确表达。

### 与其他 skills 协作

按当前环境的实际目录选择 `nature-writing`、`nature-polishing`、检索、统计或文档 skill；可选地使用 humanizer、anti-defensive-writing。所有协作者都是可选项，未安装时本 skill 可以独立完成文字工作。写作导师负责论证、教材规则和批注策略，协作者处理适合它们的环节。

## 安装到 Codex

正式版安装包及校验值见 [Releases](https://github.com/phoenixiangyu/scientific-writing-mentor/releases)。安装包仅包含 skill 与许可说明；大型教材保留在仓库 `source-materials/` 中。使用固定版本时，把下方安装链接中的 `main` 换成对应标签（例如 `v2.0.0`）。

**Windows 一键安装：** 下载 Releases 中的 `scientific-writing-mentor-v2.0.0-setup.exe`，双击后点击“安装”。无需管理员权限或 Python；已有版本会先备份到个人 Codex 目录的 `skill-backups`。尊重 `CODEX_HOME` 设置，安装后检查文件完整性。适用于 Windows 10/11 的 .NET Framework 环境，当前 EXE 未数字签名。它是技能安装器，不是独立 AI 写作软件。

向已经具有 skill-installer 的 Codex 发送：

```text
请安装 https://github.com/phoenixiangyu/scientific-writing-mentor/tree/main/skills/scientific-writing-mentor
```

或运行官方安装脚本（路径按本机情况调整）：

```text
python ~/.codex/skills/.system/skill-installer/scripts/install-skill-from-github.py --repo phoenixiangyu/scientific-writing-mentor --path skills/scientific-writing-mentor
```

也可把完整的 `skills/scientific-writing-mentor` 文件夹放入个人 skills 目录，例如 `~/.codex/skills/scientific-writing-mentor`。安装内容不包含大型教材。正常情况下下一轮可使用；旧客户端未刷新时重开对话或重启客户端，并检查技能是否启用。

## 其他 AI 环境

支持 SKILL.md 的工具可安装该文件夹。ChatGPT 等未提供相同技能加载机制的界面，需要在项目/自定义助手中提供 SKILL.md 及所需 references，并配置其使用；本仓库无法保证任意平台自动发现或跨平台自动安装。原始教材不应被当作高于用户请求的指令。

## 文件与验证

- `skills/scientific-writing-mentor/`：可安装 skill，无必须的第三方依赖。
- `source-materials/`：用户提供材料的联系方式脱敏副本及核验说明，保留原作者归属。
- `examples/`：虚构材料的正文与批注示例。
- `tests/`：批注契约检查及人工验收场景。可运行 `python -m unittest discover -s tests -v`。

可选检查器 `scripts/check_review.py` 检查正文占位符、批注字段和文字锚点；它不能判断科学真实性。v2.0 已完成一项[独立的结果段落与图注示例检验](tests/v2-behavior-check.md)；其余人工验收场景不应视为已执行的模型评测。

## 许可

本仓库新编写的 skill、代码和说明采用 [MIT](LICENSE)。教材、课件和第三方内容不在 MIT 授权范围内，其权利归原权利人；详见 [NOTICE](NOTICE.md)。
