"""Exercise rendered output and adverse cases, not aesthetic self-ratings."""
import json, subprocess, sys, tempfile, unittest, importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('poster',ROOT/'scripts/poster.py')
poster=importlib.util.module_from_spec(spec);spec.loader.exec_module(poster)

def run(*args):
    return subprocess.run([sys.executable,str(ROOT/'scripts/run.py'),*map(str,args)],capture_output=True,text=True)

class RenderAuditTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp=tempfile.TemporaryDirectory();cls.dir=Path(cls.tmp.name)
        r=run('qr','https://example.org/register','--output',cls.dir/'qr.png')
        if r.returncode:raise RuntimeError(r.stderr+r.stdout)
        cls.base={'width':400,'height':600,'scale':1,'thumbnail_width':270,'title':'GEO大会','mixed_title':True,'max_title_gap':24,'qr_url':'https://example.org/register','cta':'马上扫码报名','required_text':['2026.11.21','¥399'],'check_diversity':False}
        cls.items=[]
        for name in ['good','gap','duplicate','missing','outside','ungrouped']:
            title='<div class="event-title"><span class="event-latin">GEO</span><span class="event-han">大会</span></div>'
            if name=='ungrouped':title='<div class="geo">GEO</div><div class="cn">大会</div>'
            gap=100 if name=='gap' else 12
            html="""<!doctype html><meta charset="utf-8"><style>body{margin:24px;font-family:sans-serif}.event-title{display:flex;align-items:baseline;gap:%dpx;font-size:40px;font-weight:700}img{width:180px;height:180px}p{font-size:20px}.geo{position:absolute;left:49px;top:305px;font-size:72px}.cn{position:absolute;right:66px;top:447px;font-size:40px}</style>"""%gap+title+'<p>2026.11.21</p><p>'+('' if name=='missing' else '¥399')+'</p><img src="qr.png"><p>马上扫码报名</p>'
            if name=='duplicate':html+='<p>马上扫码报名</p>'
            if name=='outside':html+='<p style="position:absolute;left:410px">越界文字</p>'
            (cls.dir/(name+'.html')).write_text(html)
            cls.items.append({'id':name,'html':name+'.html','png':name+'.png'})
        (cls.dir/'all.json').write_text(json.dumps(dict(cls.base,posters=cls.items)))
        r=run('render',cls.dir/'all.json')
        if r.returncode:raise RuntimeError(r.stderr+r.stdout)
    @classmethod
    def tearDownClass(cls):cls.tmp.cleanup()
    def audit(self,name,**override):
        item=next(x for x in self.items if x['id']==name)
        (self.dir/'one.json').write_text(json.dumps({**self.base,"posters":[item],**override}))
        r=run('audit',self.dir/'one.json');data=json.loads((self.dir/'audit-report.json').read_text())
        self.assertEqual(r.returncode,0 if data['ok'] else 1)
        return data
    def test_good_render_and_two_size_qr(self):self.assertTrue(self.audit('good')['ok'])
    def test_title_gap(self):self.assertIn('gap: mixed title spacing',self.audit('gap')['issues'])
    def test_real_failure_ungrouped_title(self):self.assertIn('ungrouped: title group missing or text mismatch',self.audit('ungrouped')['issues'])
    def test_duplicate_cta(self):self.assertIn('duplicate: CTA must appear exactly once',self.audit('duplicate')['issues'])
    def test_missing_fact(self):self.assertIn('missing: missing text: ¥399',self.audit('missing')['issues'])
    def test_outside_canvas(self):self.assertIn('outside: text outside canvas',self.audit('outside')['issues'])
    def test_wrong_qr_destination(self):
        data=self.audit('good',qr_url='https://example.org/other')
        self.assertTrue(any('QR destination/count mismatch' in s for s in data['issues']))
    def test_stale_source(self):
        path=self.dir/'good.html';old=path.read_text()
        try:
            path.write_text(old+'<!-- changed -->')
            self.assertIn('good: HTML changed after rendering',self.audit('good')['issues'])
        finally:path.write_text(old)
    def test_path_escape(self):
        with self.assertRaises(ValueError):poster.local(self.dir,'../outside.html')
    def test_repeated_series_layout(self):
        items=[{'id':str(i),'metaphor':'unique claim','topology':'same'} for i in range(6)]
        self.assertTrue(any('fewer than 3' in s for s in poster.diversity(items)))
        self.assertTrue(any('consecutive' in s for s in poster.diversity(items)))

if __name__=='__main__':unittest.main()
