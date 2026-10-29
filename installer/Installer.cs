using System;
using System.IO;
using System.IO.Compression;
using System.Reflection;
using System.Security.Cryptography;
using System.Text;
using System.Windows.Forms;
using System.Drawing;

internal static class Installer
{
    const string SkillName = "scientific-writing-mentor";
    const string Prefix = SkillName + "/";

    static byte[] Payload()
    {
        Assembly assembly = Assembly.GetExecutingAssembly();
        byte[] bytes;
        using (Stream input = assembly.GetManifestResourceStream("SkillPayload"))
        using (MemoryStream output = new MemoryStream())
        {
            if (input == null) throw new InvalidDataException("安装包资源缺失。");
            input.CopyTo(output); bytes = output.ToArray();
        }
        string expected;
        using (StreamReader reader = new StreamReader(assembly.GetManifestResourceStream("PayloadHash")))
            expected = reader.ReadToEnd().Trim();
        using (SHA256 hash = SHA256.Create())
            if (BitConverter.ToString(hash.ComputeHash(bytes)).Replace("-", "").ToLowerInvariant() != expected)
                throw new InvalidDataException("安装包校验失败，请重新下载。");
        return bytes;
    }

    static string Target(string supplied)
    {
        string home = Environment.GetEnvironmentVariable("CODEX_HOME");
        if (String.IsNullOrWhiteSpace(home))
            home = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.UserProfile), ".codex");
        string target = Path.GetFullPath(supplied ?? Path.Combine(home, "skills", SkillName)).TrimEnd(Path.DirectorySeparatorChar);
        if (!String.Equals(Path.GetFileName(target), SkillName, StringComparison.OrdinalIgnoreCase))
            throw new ArgumentException("目标文件夹名称必须为 " + SkillName);
        return target;
    }

    static string EntryPath(string root, string entry)
    {
        if (!entry.StartsWith(Prefix, StringComparison.Ordinal) || entry.Contains("\\"))
            throw new InvalidDataException("安装包包含无效路径。");
        string relative = entry.Substring(Prefix.Length);
        if (relative.Length == 0 || relative.IndexOf(':') >= 0)
            throw new InvalidDataException("安装包路径为空或无效。");
        string path = Path.GetFullPath(Path.Combine(root, relative.Replace('/', Path.DirectorySeparatorChar)));
        if (!path.StartsWith(root + Path.DirectorySeparatorChar, StringComparison.OrdinalIgnoreCase))
            throw new InvalidDataException("安装包路径超出目标目录。");
        return path;
    }

    static void Verify(string target, byte[] payload)
    {
        using (ZipArchive zip = new ZipArchive(new MemoryStream(payload), ZipArchiveMode.Read))
        using (SHA256 hash = SHA256.Create())
        {
            foreach (ZipArchiveEntry entry in zip.Entries)
            {
                if (entry.FullName.EndsWith("/", StringComparison.Ordinal)) continue;
                string path = EntryPath(target, entry.FullName);
                using (Stream input = entry.Open())
                using (FileStream file = File.OpenRead(path))
                    if (BitConverter.ToString(hash.ComputeHash(input)) != BitConverter.ToString(hash.ComputeHash(file)))
                        throw new InvalidDataException("已安装文件校验失败：" + entry.FullName);
            }
        }
    }

    static string Install(string target, byte[] payload)
    {
        string parent = Path.GetDirectoryName(target);
        Directory.CreateDirectory(parent);
        if (File.Exists(target)) throw new IOException("安装目标是文件，未做修改。");
        if (Directory.Exists(target) && (File.GetAttributes(target) & FileAttributes.ReparsePoint) != 0)
            throw new IOException("现有技能目录是链接。请使用压缩包手动安装。");
        string stage = Path.Combine(parent, "." + SkillName + ".install-" + Guid.NewGuid().ToString("N"));
        Directory.CreateDirectory(stage);
        using (ZipArchive zip = new ZipArchive(new MemoryStream(payload), ZipArchiveMode.Read))
        {
            if (zip.Entries.Count > 1000) throw new InvalidDataException("安装包文件数量异常。");
            long total = 0;
            foreach (ZipArchiveEntry entry in zip.Entries)
            {
                if (entry.FullName.EndsWith("/", StringComparison.Ordinal)) continue;
                total += entry.Length;
                if (total > 10 * 1024 * 1024) throw new InvalidDataException("安装包展开大小异常。");
                string path = EntryPath(stage, entry.FullName);
                Directory.CreateDirectory(Path.GetDirectoryName(path));
                using (Stream input = entry.Open())
                using (FileStream output = new FileStream(path, FileMode.CreateNew)) input.CopyTo(output);
            }
        }
        if (!File.Exists(Path.Combine(stage, "SKILL.md"))) throw new InvalidDataException("安装包缺少 SKILL.md。");
        Verify(stage, payload);
        string backup = null;
        if (Directory.Exists(target))
        {
            // Backups live outside skills so Codex does not discover duplicate skills.
            string backupRoot = Path.Combine(Path.GetDirectoryName(parent), "skill-backups");
            Directory.CreateDirectory(backupRoot);
            backup = Path.Combine(backupRoot, SkillName + "-" + DateTime.UtcNow.ToString("yyyyMMdd-HHmmss") + "-" + Guid.NewGuid().ToString("N").Substring(0, 8));
            Directory.Move(target, backup);
        }
        try { Directory.Move(stage, target); }
        catch
        {
            if (backup != null && !Directory.Exists(target)) Directory.Move(backup, target);
            throw;
        }
        Verify(target, payload);
        return backup;
    }

    [STAThread]
    static int Main(string[] args)
    {
        bool silent = Array.IndexOf(args, "--silent") >= 0 || Array.IndexOf(args, "--verify") >= 0;
        try
        {
            string supplied = null;
            for (int i = 0; i < args.Length; i++)
            {
                if (args[i] == "--target" && i + 1 < args.Length) supplied = args[++i];
                else if (args[i] != "--silent" && args[i] != "--verify") throw new ArgumentException("未知或不完整的参数。");
            }
            string target = Target(supplied);
            byte[] payload = Payload();
            if (Array.IndexOf(args, "--verify") >= 0) { Verify(target, payload); return 0; }
            if (silent) { Install(target, payload); return 0; }
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            using (Form form = new Form())
            {
                form.Text = "科技论文写作导师 · 安装程序";
                form.ClientSize = new Size(650, 300);
                form.Font = new Font("Microsoft YaHei UI", 10);
                form.StartPosition = FormStartPosition.CenterScreen;
                form.FormBorderStyle = FormBorderStyle.FixedDialog;
                form.MaximizeBox = false;
                Label intro = new Label { Left = 24, Top = 22, Width = 600, Height = 48, Text = "将 Scientific Writing Mentor 安装到 Codex 的个人 skills 目录。\n无需管理员权限，无需下载教材或安装 Python。" };
                Label location = new Label { Left = 24, Top = 85, Width = 600, Height = 70, Text = "安装位置：\n" + target };
                Label note = new Label { Left = 24, Top = 160, Width = 600, Height = 58, Text = "如已安装，将保留完整备份后更新。其他技能不受影响。\n安装后在下一轮使用；若列表未刷新，请重新打开对话。" };
                Button install = new Button { Left = 410, Top = 240, Width = 100, Height = 36, Text = "安装" };
                Button close = new Button { Left = 525, Top = 240, Width = 100, Height = 36, Text = "关闭", DialogResult = DialogResult.Cancel };
                install.Click += delegate
                {
                    install.Enabled = false;
                    try
                    {
                        string backup = Install(target, payload);
                        MessageBox.Show(form, "安装和文件校验已完成。\n" + target + (backup == null ? "" : "\n\n旧版本备份：\n" + backup), "安装成功", MessageBoxButtons.OK, MessageBoxIcon.Information);
                        form.Close();
                    }
                    catch (Exception error) { MessageBox.Show(form, error.Message, "安装未完成", MessageBoxButtons.OK, MessageBoxIcon.Error); install.Enabled = true; }
                };
                form.Controls.AddRange(new Control[] { intro, location, note, install, close });
                form.AcceptButton = install; form.CancelButton = close;
                Application.Run(form);
            }
            return 0;
        }
        catch (Exception error)
        {
            if (!silent) MessageBox.Show(error.Message, "安装未完成", MessageBoxButtons.OK, MessageBoxIcon.Error);
            return 1;
        }
    }
}
