#!/usr/bin/env python3
"""Deterministic QR/render/audit/gallery helpers. No aesthetic score or provider calls."""
from pathlib import Path
import argparse, hashlib, html, json, re, sys, os
from urllib.parse import urlparse,unquote

def digest(path):return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def norm(s):return re.sub(r'\s+','',s)
def local(root,name):
    path=(root/name).resolve()
    if not path.is_relative_to(root.resolve()):raise ValueError('Path must remain inside the project: '+name)
    return path
def load(path):
    path=Path(path).resolve();m=json.loads(path.read_text());ids=[p['id'] for p in m['posters']]
    if not ids or len(set(ids))!=len(ids):raise ValueError('Poster IDs must be nonempty and unique')
    for p in m['posters']:
        for field in ['html','png']:local(path.parent,p[field])
    return path.parent,m

def diversity(items):
    issues=[]
    for p in items:
        if not p.get('metaphor','').strip():issues.append(p['id']+': missing visual metaphor')
        if not p.get('topology'):issues.append(p['id']+': missing topology')
    if len(items)>=6:
        if len({p.get('topology') for p in items})<3:issues.append('series: fewer than 3 declared layout topologies')
        for i in range(3,len(items)):
            if len({p.get('topology') for p in items[i-3:i+1]})==1:issues.append('series: more than 3 consecutive same topologies at '+items[i]['id'])
    return issues

JS=r'''async()=>{await document.fonts.ready;await Promise.all([...document.images].map(i=>i.decode()));await new Promise(r=>requestAnimationFrame(()=>requestAnimationFrame(r)));const outside=[];const w=document.createTreeWalker(document.body,NodeFilter.SHOW_TEXT);while(w.nextNode()){const n=w.currentNode;if(!n.textContent.trim()||n.parentElement.closest('style,script'))continue;const range=document.createRange();range.selectNodeContents(n);for(const b of range.getClientRects())if(b.width&&b.height&&(b.left< -1||b.top< -1||b.right>innerWidth+1||b.bottom>innerHeight+1))outside.push(n.textContent.trim())}const rect=e=>{if(!e)return null;const b=e.getBoundingClientRect();return {x:b.x,y:b.y,w:b.width,h:b.height,right:b.right,bottom:b.bottom}};const t=document.querySelector('.event-title'),l=document.querySelector('.event-latin'),h=document.querySelector('.event-han');return {text:document.body.innerText,outside,images:[...document.images].map(i=>({src:i.getAttribute('src'),loaded:i.complete&&i.naturalWidth>0})),title:{text:t?.innerText,group:rect(t),latin:rect(l),han:rect(h),gap:l&&h?h.getBoundingClientRect().left-l.getBoundingClientRect().right:null}}}'''

def qr(url,output):
    import qrcode
    if urlparse(url).scheme not in ('https','http'):raise ValueError('QR target must be an http(s) URL')
    q=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M,box_size=12,border=4);q.add_data(url);q.make(fit=True)
    out=Path(output);out.parent.mkdir(parents=True,exist_ok=True);q.make_image(fill_color='black',back_color='white').save(out)
    print(out)

def render(path):
    from playwright.sync_api import sync_playwright
    root,m=load(path);records=[]
    with sync_playwright() as p:
        browser=p.chromium.launch(**({'executable_path':os.environ['POSTER_BROWSER_EXECUTABLE']} if os.environ.get('POSTER_BROWSER_EXECUTABLE') else {}))
        for item in m['posters']:
            width=item.get('width',m.get('width',1080));height=item.get('height',m.get('height',1620));scale=item.get('scale',m.get('scale',2))
            page=browser.new_page(viewport={'width':width,'height':height},device_scale_factor=scale)
            # Render only trusted agent-authored local HTML. External network is disabled.
            page.route('http://**/*',lambda route:route.abort());page.route('https://**/*',lambda route:route.abort())
            src=local(root,item['html']);out=local(root,item['png']);out.parent.mkdir(parents=True,exist_ok=True)
            page.goto(src.as_uri(),wait_until='load');r=page.evaluate(JS)
            page.screenshot(path=str(out),full_page=False);page.close()
            r.update(id=item['id'],html_sha256=digest(src),png_sha256=digest(out),width=width,height=height,scale=scale)
            records.append(r);print(item['id'],'rendered')
        browser.close()
    (root/'render-report.json').write_text(json.dumps(records,ensure_ascii=False,indent=2))

def audit(path):
    from PIL import Image
    import zxingcpp
    root,m=load(path);rp=root/'render-report.json';records={x['id']:x for x in json.loads(rp.read_text())} if rp.exists() else {}
    issues=diversity(m['posters']) if m.get('check_diversity',True) else [];results=[]
    for item in m['posters']:
        bad=[];r=records.get(item['id']);png=local(root,item['png']);src=local(root,item['html'])
        if not r:bad.append('missing render evidence')
        if not png.exists():bad.append('missing PNG')
        if r:
            if not src.exists() or digest(src)!=r['html_sha256']:bad.append('HTML changed after rendering')
            if png.exists() and digest(png)!=r['png_sha256']:bad.append('PNG changed after rendering')
            if r['outside']:bad.append('text outside canvas')
            if not all(i['loaded'] for i in r['images']):bad.append('unloaded image')
            txt=norm(r['text'])
            for text in item.get('required_text',m.get('required_text',[])):
                if norm(text) not in txt:bad.append('missing text: '+text)
            for text in item.get('forbidden_text',m.get('forbidden_text',[])):
                if norm(text) in txt:bad.append('forbidden text: '+text)
            cta=item.get('cta',m.get('cta'))
            if cta and txt.count(norm(cta))!=1:bad.append('CTA must appear exactly once')
            title=r['title'];expected=item.get('title',m.get('title'))
            if expected and norm(title.get('text') or '')!=norm(expected):bad.append('title group missing or text mismatch')
            if item.get('mixed_title',m.get('mixed_title',False)):
                gap=title.get('gap')
                if gap is None or not 0<=gap<=item.get('max_title_gap',m.get('max_title_gap',32)):bad.append('mixed title spacing')
        decodes=[]
        if png.exists():
            im=Image.open(png);w=item.get('width',m.get('width',1080));h=item.get('height',m.get('height',1620));scale=item.get('scale',m.get('scale',2))
            if im.size!=(round(w*scale),round(h*scale)):bad.append('wrong exported dimensions')
            url=item.get('qr_url',m.get('qr_url'))
            if url:
                tw=m.get('thumbnail_width',540)
                for label,img in [('full',im),('phone',im.resize((tw,round(im.height*tw/im.width)),Image.Resampling.LANCZOS))]:
                    found=zxingcpp.read_barcodes(img);values=[x.text for x in found];decodes.append({'size':label,'values':values})
                    if values!=[url]:bad.append(label+' QR destination/count mismatch')
        issues.extend(item['id']+': '+b for b in bad);results.append({'id':item['id'],'issue_count':len(bad),'issues':bad,'qr':decodes})
    report={'ok':not issues,'issue_count':len(issues),'issues':issues,'posters':results,'limits':'Geometry and decoding checks do not establish visual quality, source truth, conversion lift, or print certification.'}
    (root/'audit-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2));return 0 if not issues else 1

def gallery(path):
    root,m=load(path);cards=[]
    for p in m['posters']:
        url=html.escape(p['png'],quote=True);name=html.escape(p.get('name',p['id']))
        cards.append(f'<figure><a href="{url}"><img src="{url}" alt="{name}"></a><figcaption>{name}</figcaption></figure>')
    content='<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Poster gallery</title><style>body{margin:0;padding:32px;background:#eee;font-family:system-ui}main{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:28px}figure{margin:0}img{width:100%;display:block}figcaption{padding:10px 0}@media(max-width:700px){main{grid-template-columns:1fr}}</style><main>'+''.join(cards)+'</main></html>'
    (root/'gallery.html').write_text(content);print(root/'gallery.html')

def main():
    ap=argparse.ArgumentParser();s=ap.add_subparsers(dest='cmd',required=True)
    q=s.add_parser('qr');q.add_argument('url');q.add_argument('--output',required=True)
    for name in ['render','audit','gallery']:s.add_parser(name).add_argument('manifest')
    a=ap.parse_args()
    if a.cmd=='qr':qr(a.url,a.output)
    elif a.cmd=='render':render(a.manifest)
    elif a.cmd=='audit':return audit(a.manifest)
    else:gallery(a.manifest)
    return 0
if __name__=='__main__':sys.exit(main())
