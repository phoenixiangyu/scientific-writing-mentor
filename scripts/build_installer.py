"""Compile a small offline Windows installer using the installed .NET Framework."""
from pathlib import Path
import hashlib, os, subprocess
from build_release import ROOT, build

if __name__ == '__main__':
    version, payload, digest = build(ROOT / 'dist')
    framework = Path(os.environ['WINDIR']) / 'Microsoft.NET/Framework64/v4.0.30319'
    compiler = framework / 'csc.exe'
    if not compiler.is_file():
        raise SystemExit('Windows .NET Framework C# compiler not found')
    generated = ROOT / 'dist/build'
    generated.mkdir(parents=True, exist_ok=True)
    hash_file = generated / 'payload.sha256'
    hash_file.write_text(digest, encoding='ascii')
    assembly = generated / 'AssemblyInfo.cs'
    assembly.write_text('using System.Reflection;\n'
                        '[assembly: AssemblyTitle("Scientific Writing Mentor Setup")]\n'
                        '[assembly: AssemblyCompany("phoenixiangyu")]\n'
                        f'[assembly: AssemblyVersion("{version}.0")]\n', encoding='utf-8')
    target = ROOT / f'dist/scientific-writing-mentor-v{version}-setup.exe'
    command = [str(compiler), '/nologo', '/optimize+', '/target:winexe', '/platform:anycpu',
               '/codepage:65001', '/out:' + str(target),
               '/win32manifest:' + str(ROOT / 'installer/app.manifest'),
               '/resource:' + str(payload) + ',SkillPayload',
               '/resource:' + str(hash_file) + ',PayloadHash',
               '/reference:System.Windows.Forms.dll', '/reference:System.Drawing.dll',
               '/reference:System.IO.Compression.dll', '/reference:System.IO.Compression.FileSystem.dll',
               str(ROOT / 'installer/Installer.cs'), str(assembly)]
    subprocess.run(command, check=True)
    lines = [f'{hashlib.sha256(p.read_bytes()).hexdigest()}  {p.name}\n' for p in (payload, target)]
    (ROOT / 'dist/SHA256SUMS.txt').write_text(''.join(lines), encoding='utf-8', newline='\n')
    print(f'Built {target.name}: {target.stat().st_size} bytes')
