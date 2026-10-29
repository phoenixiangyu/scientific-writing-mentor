## Windows EXE 安装程序

下载 `scientific-writing-mentor-{{TAG}}-setup.exe` 并双击，点击“安装”。支持 Windows 10/11 的 .NET Framework 环境，无需管理员权限、Python 或联网下载依赖。

- 默认安装到 `%USERPROFILE%\.codex\skills\scientific-writing-mentor`；如果设置了 `CODEX_HOME`，则使用该目录下的 `skills`。
- 现有版本会先完整备份到个人 Codex 目录的 `skill-backups` 中；备份不放入 skills，避免重复发现。
- 安装后逐个校验文件；下一轮即可使用，列表未刷新时重新打开对话。
- EXE 是技能安装器，不是独立的 AI 写作软件，也不会自动安装到其他 AI 产品。
- 当前 EXE 未进行数字签名。可用 `SHA256SUMS.txt` 核对下载完整性；不包含大型教材。

安装器源码和构建脚本位于仓库 `installer/` 与 `scripts/`，通过 Windows 发布流程构建并测试。补充附件不会覆盖已经发布的同版本 skill ZIP。
