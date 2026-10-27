#!/usr/bin/env python3
"""Install isolated, pinned poster dependencies; never install image-provider credentials."""
import argparse, json, os, subprocess, sys, venv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
DEPS=ROOT/'.deps'
PYTHON=DEPS/('Scripts/python.exe' if os.name=='nt' else 'bin/python')
PINS=['playwright==1.58.0','Pillow==12.1.0','qrcode==8.2','zxing-cpp==2.3.0']
def env():
    return dict(os.environ,PLAYWRIGHT_BROWSERS_PATH=str(DEPS/'browsers'))
def check():
    if not PYTHON.exists():return False
    code='from PIL import Image; import qrcode,zxingcpp; from playwright.sync_api import sync_playwright; p=sync_playwright().start(); b=p.chromium.launch(); b.close(); p.stop()'
    return subprocess.run([str(PYTHON),'-c',code],env=env(),capture_output=True).returncode==0
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');a=ap.parse_args()
    if check(): print(json.dumps({'ok':True,'missing':[]}));sys.exit(0)
    if a.check:
        print(json.dumps({'ok':False,'missing':['isolated Python packages or Chromium'],'repair':'python3 scripts/setup.py'}));sys.exit(1)
    if not PYTHON.exists():venv.EnvBuilder(with_pip=True).create(DEPS)
    subprocess.run([str(PYTHON),'-m','pip','install','--disable-pip-version-check',*PINS],check=True)
    subprocess.run([str(PYTHON),'-m','playwright','install','chromium'],env=env(),check=True)
    if not check():raise SystemExit('Setup failed; inspect browser system dependencies (Linux may require administrator packages).')
    print(json.dumps({'ok':True,'missing':[]}))
