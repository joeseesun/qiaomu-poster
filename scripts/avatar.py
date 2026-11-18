"""Avatar-only project bootstrap. Local inputs; no image edits or provider calls.

Produces a reviewable draft, never an automatic aesthetic acceptance claim.
"""
import argparse
from datetime import date, datetime
import hashlib
import html
import json
from pathlib import Path
import shutil
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[1]
STYLES = ('spotlight', 'editorial', 'signature')


def read_event(path=None, *, archive=False, today=None):
    event = json.loads(Path(path or ROOT/'presets/geo-2026.json').read_text())
    fields = ['title', 'edition', 'start_date', 'end_date', 'timezone', 'date_label',
              'city', 'hotel', 'hotel_branch', 'price', 'ticket', 'registration_url', 'cta']
    if any(not isinstance(event.get(k), str) or not event[k].strip() for k in fields):
        raise ValueError('Event requires nonempty string fields: '+', '.join(fields))
    from urllib.parse import urlparse
    url = urlparse(event['registration_url'])
    if url.scheme not in ('https', 'http') or not url.netloc or url.username or url.password:
        raise ValueError('Registration URL must be a public http(s) URL without credentials')
    if event['title'] != 'GEO大会':
        raise ValueError('Avatar quick entry is for GEO大会; use the general workflow for other events')
    start, end = date.fromisoformat(event['start_date']), date.fromisoformat(event['end_date'])
    if start > end:
        raise ValueError('Event start must precede end')
    local_today = today or datetime.now(ZoneInfo(event['timezone'])).date()
    if local_today > end and not archive:
        raise ValueError('Event has ended. Obtain updated facts or use --archive only for an explicitly requested historical reproduction.')
    return event


def inspect_avatar(path):
    from PIL import Image
    with Image.open(path) as im:
        if im.format not in ('PNG', 'JPEG', 'WEBP'):
            raise ValueError('Use a PNG, JPEG or WebP avatar; no executable SVG/HTML')
        if getattr(im, 'n_frames', 1) != 1:
            raise ValueError('Use a still image, not an animation')
        im.load()
        w, h = im.size
        if min(w, h) < 48:
            raise ValueError('Avatar is too small; minimum side is 48 pixels')
        # Read corner pixels only: do not alter or export a transformed source image.
        rgb = im.convert('RGBA')
        corners = [rgb.getpixel(xy) for xy in [(0, 0), (w-1, 0), (0, h-1), (w-1, h-1)]]
        flat = all(c[3] == 255 and max(abs(c[i]-corners[0][i]) for i in range(3)) < 12 for c in corners)
        color = '#%02x%02x%02x' % corners[0][:3] if flat else '#f4f2e9'
        lum = sum(a*b for a, b in zip(corners[0][:3], (.2126, .7152, .0722))) if flat else 240
        return {'width': w, 'height': h, 'background': color, 'ink': '#f8f8ee' if lum < 115 else '#17251d',
                'format': im.format, 'style': 'signature' if w/h >= 1.8 else 'editorial' if h/w >= 1.25 else 'spotlight',
                'background_is_corner_estimate': True}


def document(e, info, avatar_name, style, archive):
    esc = lambda k: html.escape(e[k], quote=True)
    title = '<div class="event-title"><span class="event-latin">GEO</span><span class="event-han">大会</span></div>'
    geometry = {
        'spotlight': '.event-title{left:62px;top:176px}.hero{left:278px;top:436px;width:524px;height:524px}.slogan{left:68px;top:985px;font-size:38px}.sub{left:68px;top:1038px}',
        'editorial': '.event-title{left:62px;top:176px}.hero{left:533px;top:445px;width:480px;height:600px}.slogan{left:68px;top:590px;width:400px;font-size:57px;line-height:1.5}.sub{left:68px;top:902px;width:350px;line-height:1.8}',
        'signature': '.event-title{left:62px;top:700px}.hero{left:98px;top:230px;width:884px;height:300px}.slogan{left:68px;top:570px;font-size:43px}.sub{left:68px;top:970px}'
    }[style]
    headline = '让你的品牌，成为 AI 的推荐答案。' if style != 'editorial' else '让品牌<br>被 AI 看见。'
    archive_notice = '<div class="archive">历史活动 · 资料留存</div>' if archive else ''
    cta = '扫码查看活动资料' if archive else esc('cta')
    return f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><title>GEO大会 · 个性邀请</title><style>
@font-face{{font-family:PosterSans;src:url('assets/poster-sans.woff2');font-weight:100 900;font-display:block}}
*{{box-sizing:border-box}}html,body{{margin:0;width:1080px;height:1620px}}body{{font-family:PosterSans,sans-serif;background:{info['background']};color:{info['ink']}}}
.poster{{position:relative;width:1080px;height:1620px;overflow:hidden}}.p,.hero,.event-title,.slogan,.sub{{position:absolute}}.hero{{object-fit:contain}}.event-title{{display:inline-flex;align-items:baseline;gap:18px;white-space:nowrap;line-height:1}}
.event-latin{{font-family:Arial,sans-serif;font-size:222px;font-weight:800;letter-spacing:-12px}}.event-han{{font-size:164px;font-weight:800;letter-spacing:-4px;position:relative;top:-6px}}.slogan{{font-weight:650}}.sub{{font-size:23px;opacity:.8}}.footer{{position:absolute;left:0;top:1110px;width:1080px;height:510px;background:#e9f2df;color:#17251d}}.archive{{position:absolute;left:68px;top:124px;font-size:20px;font-weight:650}}{geometry}
</style></head><body><main class="poster">
<div class="p" style="left:68px;top:56px;font-size:22px;letter-spacing:2px">{esc('edition')}</div><div class="p" style="right:68px;top:56px;font-size:22px">{esc('city')} · {'历史回顾' if archive else '邀你参加'}</div>
<div class="p" style="left:68px;top:110px;width:944px;height:1px;background:currentColor;opacity:.25"></div>{archive_notice}{title}
<img class="hero" src="assets/{avatar_name}" alt="用户提供的原始头像或品牌标识"><div class="slogan">{headline}</div><div class="sub">生成式引擎优化 · 品牌增长实战</div>
<section class="footer"><div class="p" style="left:64px;top:35px;font-family:Arial,sans-serif;font-size:61px;font-weight:600;letter-spacing:-2px">{esc('date_label')}</div><div class="p" style="right:66px;top:57px;font-size:23px">{esc('city')} · 两天大会</div>
<div class="p" style="left:66px;top:135px;width:948px;height:1px;background:#b6c9af"></div>
<div class="p" style="left:66px;top:177px;display:flex;gap:14px"><svg width="30" height="35" viewBox="0 0 24 24" fill="none" stroke="#397044" stroke-width="1.6"><path d="M20 10c0 6-8 11-8 11S4 16 4 10a8 8 0 1 1 16 0Z"/><circle cx="12" cy="10" r="2.5"/></svg><div><div style="font-size:30px;font-weight:650">{esc('hotel')}</div><div style="font-size:22px;margin-top:8px">{esc('hotel_branch')}</div></div></div>
<div class="p" style="left:66px;top:309px;font-size:21px">{esc('ticket')}</div><div class="p" style="left:66px;top:346px;color:#326740;font-family:Arial,sans-serif;font-size:91px;font-weight:700;letter-spacing:-4px"><span style="font-size:35px">¥</span>{esc('price')}<span style="font-family:PosterSans;font-size:21px;letter-spacing:0;margin-left:14px">/人</span></div>
<div class="p" style="left:66px;top:462px;font-size:18px">品牌增长 · 海外获客 · Agent 实操</div><div class="p" style="left:786px;top:180px;width:228px;text-align:center"><img src="assets/registration-qr.png" width="228" height="228" alt="活动网址二维码" style="display:block;image-rendering:pixelated"><div style="margin-top:14px;font-size:24px;font-weight:650;white-space:nowrap">{cta}</div></div></section></main></body></html>'''


def prepare(avatar, output, *, event_path=None, style='auto', archive=False, today=None):
    event = read_event(event_path, archive=archive, today=today)
    source, out = Path(avatar).resolve(), Path(output).resolve()
    info = inspect_avatar(source)
    style = info['style'] if style == 'auto' else style
    if style not in STYLES:
        raise ValueError('Unsupported style')
    if out == ROOT or ROOT in out.parents:
        raise ValueError('Write user projects outside the installed skill')
    if out.exists():
        raise ValueError('Output already exists; choose a new directory. Existing files are never overwritten.')
    font = ROOT/'assets/avatar/poster-sans.woff2'
    if not font.is_file():
        raise ValueError('Missing bundled font')
    out.mkdir(parents=True)
    assets = out/'assets'; assets.mkdir()
    name = 'avatar-original'+{'PNG':'.png','JPEG':'.jpg','WEBP':'.webp'}[info['format']]
    shutil.copy2(source, assets/name)
    shutil.copy2(font, assets/'poster-sans.woff2')
    shutil.copy2(ROOT/'assets/avatar/OFL.txt', assets/'OFL.txt')
    from poster import qr
    qr(event['registration_url'], assets/'registration-qr.png')
    (out/'poster.html').write_text(document(event, info, name, style, archive))
    cta = '扫码查看活动资料' if archive else event['cta']
    manifest = {'width':1080, 'height':1620, 'scale':2, 'title':'GEO大会', 'mixed_title':True, 'max_title_gap':32,
                'qr_url':event['registration_url'], 'cta':cta,
                'required_text':[event[k] for k in ('date_label','hotel','hotel_branch','price','ticket')]+(['历史活动'] if archive else []),
                'forbidden_text':['中国GEO大会']+(['马上扫码报名', '邀你参加'] if archive else []),
                'posters':[{'id':'avatar','name':'GEO大会 · 个性海报','html':'poster.html','png':'poster.png',
                            'topology':style,'metaphor':'Draft: agent must replace with an avatar-specific visual concept before final delivery'}]}
    (out/'posters.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
    (out/'event.json').write_text(json.dumps(event, ensure_ascii=False, indent=2))
    record = {'status':'draft-needs-source-and-visual-review', 'style':style, 'input_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),
              'avatar_analysis':info, 'archive':archive, 'source_check':'Agent must reread the official source for each new live task',
              'no_identity_inference':True, 'original_preserved':True}
    (out/'job.json').write_text(json.dumps(record, ensure_ascii=False, indent=2))
    (out/'brief.md').write_text(f'''# GEO大会头像快速入口\n\n布局：{style}。原图保持不变。只从画面识别形状、颜色与风格，不猜姓名、机构、嘉宾或主办关系。\n\n这是可编辑初稿。Agent 仍须读取官网核对 event.json，写头像专属隐喻、调整图文关系；需要去底/衍生图时使用宿主 image_gen。然后 render → audit → gallery，看全图、手机缩图和边缘，问题清零后交付。\n\n禁止中国 GEO 大会、嘉宾名单、箭头、虚构身份/余票/优惠。源图与衍生图分开，二维码只由脚本编码。默认本地交付，未经要求不上传头像。\n''')
    return out


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('avatar', help='Local PNG/JPEG/WebP file')
    parser.add_argument('--output', required=True, help='New project directory outside the skill')
    parser.add_argument('--event', help='Complete reviewed event JSON; defaults to GEO 2026 snapshot')
    parser.add_argument('--style', choices=('auto',)+STYLES, default='auto')
    parser.add_argument('--archive', action='store_true', help='Explicitly requested historical poster only; marks output and changes CTA')
    args = parser.parse_args(argv)
    try:
        out = prepare(args.avatar, args.output, event_path=args.event, style=args.style, archive=args.archive)
    except (ValueError, OSError) as exc:
        parser.exit(2, str(exc)+'\n')
    print(json.dumps({'ok':True, 'project':str(out), 'status':'draft-needs-source-and-visual-review'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
