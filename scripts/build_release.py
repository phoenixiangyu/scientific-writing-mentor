"""Build the installable skill only; keep private caches and source books out."""
from pathlib import Path
import argparse, hashlib, os, re, zipfile

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skills/scientific-writing-mentor'

def build(output):
    text = (SKILL / 'SKILL.md').read_text(encoding='utf-8')
    match = re.search(r'^  version: "(\d+\.\d+\.\d+)"$', text, re.MULTILINE)
    if not match:
        raise ValueError('Missing stable numeric skill version')
    version = match.group(1)
    assert (ROOT / f'release-notes/v{version}.md').is_file()
    output.mkdir(parents=True, exist_ok=True)
    package = output / f'scientific-writing-mentor-v{version}.zip'
    entries = []
    for path in SKILL.rglob('*'):
        if path.is_file() and '__pycache__' not in path.parts and path.suffix != '.pyc':
            entries.append((path.relative_to(SKILL).as_posix(), path))
    entries += [(name, ROOT / name) for name in ('LICENSE', 'NOTICE.md')]
    with zipfile.ZipFile(package, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for name, path in sorted(entries):
            data = path.read_bytes().replace(b'\r\n', b'\n')
            info = zipfile.ZipInfo('scientific-writing-mentor/' + name, (2026, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            z.writestr(info, data, compresslevel=9)
    with zipfile.ZipFile(package) as z:
        assert z.testzip() is None
        assert 'scientific-writing-mentor/SKILL.md' in z.namelist()
        assert not any('source-materials/' in n or '__pycache__' in n for n in z.namelist())
    digest = hashlib.sha256(package.read_bytes()).hexdigest()
    (output / 'SHA256SUMS.txt').write_text(f'{digest}  {package.name}\n', encoding='utf-8', newline='\n')
    return version, package, digest

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT / 'dist')
    parser.add_argument('--github-output', action='store_true')
    args = parser.parse_args()
    version, package, digest = build(args.output)
    print(f'{package.name}: {digest}')
    if args.github_output:
        with open(os.environ['GITHUB_OUTPUT'], 'a', encoding='utf-8') as stream:
            stream.write(f'tag=v{version}\n')
