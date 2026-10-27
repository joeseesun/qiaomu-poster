#!/usr/bin/env python3
import os,subprocess,sys
SCRIPT_INTERFACE = "internal-module"
from pathlib import Path
root=Path(__file__).resolve().parents[1];deps=root/'.deps'
p=deps/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
if not p.exists():raise SystemExit('Missing dependencies. Run: python3 scripts/setup.py')
env=dict(os.environ,PLAYWRIGHT_BROWSERS_PATH=str(deps/'browsers'))
raise SystemExit(subprocess.call([str(p),str(root/'scripts/poster.py'),*sys.argv[1:]],env=env))
