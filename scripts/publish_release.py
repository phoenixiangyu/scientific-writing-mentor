"""Publish assets; preserve the existing version ZIP and any existing installer."""
from pathlib import Path
import hashlib, json, os, shutil, subprocess, uuid
from build_release import ROOT

def gh(*args, check=True):
    result = subprocess.run(['gh', *args], text=True, encoding='utf-8', capture_output=True)
    if check and result.returncode:
        raise RuntimeError(result.stderr.strip())
    return result

if __name__ == '__main__':
    tag = os.environ['RELEASE_TAG']
    package = ROOT / f'dist/scientific-writing-mentor-{tag}.zip'
    installer = ROOT / f'dist/scientific-writing-mentor-{tag}-setup.exe'
    assert package.is_file() and installer.is_file()
    existing = gh('release', 'view', tag, '--json', 'assets,body', check=False)
    if existing.returncode == 0:
        data = json.loads(existing.stdout)
        names = {a['name'] for a in data['assets']}
        published = ROOT / 'dist' / ('published-' + uuid.uuid4().hex)
        published.mkdir()
        gh('release', 'download', tag, '--pattern', package.name, '--dir', str(published))
        if package.read_bytes() != (published / package.name).read_bytes():
            raise RuntimeError('Existing version ZIP differs: bump the version rather than overwrite it')
        if installer.name in names:
            gh('release', 'download', tag, '--pattern', installer.name, '--dir', str(published))
            shutil.copy2(published / installer.name, installer)
        else:
            gh('release', 'upload', tag, str(installer))
        body = data['body']
        if '## Windows EXE 安装程序' not in body:
            body += '\n\n' + (ROOT / 'release-notes/windows-installer.md').read_text(encoding='utf-8')
            notes = ROOT / 'dist/release-body.md'
            notes.write_text(body, encoding='utf-8')
            gh('release', 'edit', tag, '--notes-file', str(notes))
    else:
        notes = ROOT / f'release-notes/{tag}.md'
        gh('release', 'create', tag, '--target', os.environ['GITHUB_SHA'],
           '--title', 'Scientific Writing Mentor ' + tag, '--notes-file', str(notes),
           '--latest', str(package), str(installer))
    checksums = ROOT / 'dist/SHA256SUMS.txt'
    checksums.write_text(''.join(f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n' for p in (package, installer)), encoding='utf-8', newline='\n')
    gh('release', 'upload', tag, str(checksums), '--clobber')
    print(gh('release', 'view', tag, '--json', 'url', '--jq', '.url').stdout.strip())
