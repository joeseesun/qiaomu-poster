"""Real input preservation, expiry, escaping and output safety regressions."""
from datetime import date
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
import avatar


class AvatarTests(unittest.TestCase):
    def test_expired_event_is_not_a_new_invitation(self):
        with self.assertRaisesRegex(ValueError, 'ended'):
            avatar.read_event(today=date(2026, 11, 23))

    def test_final_day_and_archive(self):
        self.assertEqual(avatar.read_event(today=date(2026,11,22))['price'], '399')
        event=avatar.read_event(archive=True, today=date(2027,1,1))
        info={'background':'#fff','ink':'#111'}
        doc=avatar.document(event, info, 'avatar.png', 'editorial', True)
        self.assertIn('历史活动',doc)
        self.assertIn('扫码查看活动资料',doc)
        self.assertNotIn('马上扫码报名',doc)
        self.assertNotIn('邀你参加',doc)

    def test_source_text_is_not_html(self):
        event=avatar.read_event(today=date(2026,11,18))
        event['hotel']='<script>alert(1)</script>'
        doc=avatar.document(event, {'background':'#fff','ink':'#111'}, 'avatar.png','spotlight',False)
        self.assertNotIn('<script>',doc)
        self.assertIn('&lt;script&gt;',doc)

    def test_avatar_cli_preserves_bytes_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            out=Path(tmp)/'draft'
            source=ROOT/'examples/geo-three-brands/assets/01-original.jpg'
            args=[sys.executable,str(ROOT/'scripts/run.py'),'avatar',str(source),'--output',str(out),'--archive']
            first=subprocess.run(args,capture_output=True,text=True)
            self.assertEqual(first.returncode,0,first.stderr)
            saved=out/'assets/avatar-original.jpg'
            self.assertEqual(hashlib.sha256(source.read_bytes()).hexdigest(),hashlib.sha256(saved.read_bytes()).hexdigest())
            self.assertEqual(json.loads((out/'job.json').read_text())['style'],'spotlight')
            second=subprocess.run(args,capture_output=True,text=True)
            self.assertNotEqual(second.returncode,0)
            self.assertIn('already exists',second.stderr)

    def test_bad_url_and_date_are_rejected(self):
        event=avatar.read_event(today=date(2026,11,18))
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'event.json'
            for k,v in [('registration_url','javascript:alert(1)'),('end_date','2026-11-01')]:
                p.write_text(json.dumps({**event,k:v}))
                with self.assertRaises(ValueError):avatar.read_event(p,today=date(2026,11,18))

    def test_broken_image_leaves_no_output(self):
        with tempfile.TemporaryDirectory() as tmp:
            image=Path(tmp)/'bad.png';image.write_text('not an image')
            out=Path(tmp)/'output'
            run=subprocess.run([sys.executable,str(ROOT/'scripts/run.py'),'avatar',str(image),'--output',str(out),'--archive'],capture_output=True,text=True)
            self.assertNotEqual(run.returncode,0)
            self.assertFalse(out.exists())


if __name__ == '__main__':unittest.main()
