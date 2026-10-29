"""Exercise the real EXE in an isolated user home, including repeat-install backup."""
from pathlib import Path
import os, re, subprocess, tempfile, zipfile
from build_release import ROOT

if __name__ == '__main__':
    version = re.search(r'^  version: "(\d+\.\d+\.\d+)"$', (ROOT / 'skills/scientific-writing-mentor/SKILL.md').read_text(encoding='utf-8'), re.MULTILINE).group(1)
    payload = ROOT / f'dist/scientific-writing-mentor-v{version}.zip'
    exe = ROOT / f'dist/scientific-writing-mentor-v{version}-setup.exe'
    sandbox = Path(tempfile.mkdtemp(prefix='mentor-installer-test-')).resolve()
    home = sandbox / '中文 空格 home'
    env = dict(os.environ, CODEX_HOME=str(home))
    target = home / 'skills/scientific-writing-mentor'
    def run(*args, expected=0):
        p = subprocess.run([str(exe), *args], env=env, timeout=30)
        assert p.returncode == expected, (args, p.returncode)
    run('--silent')
    with zipfile.ZipFile(payload) as z:
        for entry in z.namelist():
            relative = entry.split('/', 1)[1]
            assert (target / relative).read_bytes() == z.read(entry), relative
    run('--verify')
    (target / 'local-customization.txt').write_text('preserve me', encoding='utf-8')
    (target / 'SKILL.md').write_text('customized previous skill', encoding='utf-8')
    run('--verify', expected=1)
    run('--silent')
    backups = list((home / 'skill-backups').iterdir())
    assert len(backups) == 1
    assert (backups[0] / 'local-customization.txt').read_text() == 'preserve me'
    assert (backups[0] / 'SKILL.md').read_text() == 'customized previous skill'
    assert not (target / 'local-customization.txt').exists()
    run('--verify')
    assert len(list((home / 'skills').iterdir())) == 1
    run('--silent', '--target', str(sandbox / 'wrong-name'), expected=1)
    blocked = sandbox / 'blocked/scientific-writing-mentor'
    blocked.parent.mkdir(); blocked.write_text('keep', encoding='utf-8')
    run('--silent', '--target', str(blocked), expected=1)
    assert blocked.read_text() == 'keep'
    print('EXE tests passed: fresh install, Chinese path, exact file verification, tamper detection, backup, safe rejection.')
    print('Isolated test folder:', sandbox)
