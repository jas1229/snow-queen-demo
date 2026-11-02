# 把 index.html（artifact 的写法，没有 <head>）包成完整网页：
#   play-local.html  本地双击就能玩
#   docs/index.html  放在 GitHub Pages 上给别人玩的那份
# 谷歌字体改成不挡渲染的加载方式：连不上谷歌的时候页面照样马上出来，先用系统字体。
import pathlib, re, urllib.parse
here = pathlib.Path(__file__).parent
src = (here / 'index.html').read_text(encoding='utf-8')
m = re.match(r'\s*<title>(.*?)</title>\s*', src)
title = m.group(1) if m else '船尾的冰雪女王'
body = src[m.end():] if m else src
font = re.search(r'<link rel="stylesheet" href="(https://fonts\.googleapis\.com/[^"]+)">', body)
if font:
    body = body.replace(font.group(0), '<link rel="stylesheet" href="%s" media="print" onload="this.media=\'all\'">' % font.group(1))
desc = '世代船上的《冰雪女王》：格尔达从船头走到船尾，哈开结霜的舷窗找回忆，去冷舱把加伊带回家。一个能玩的小 demo。'
icon = 'data:image/svg+xml,' + urllib.parse.quote("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>❄</text></svg>")
head = ('<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">'
        '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
        f'<title>{title}</title><meta name="description" content="{desc}">'
        f'<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">'
        f'<link rel="icon" href="{icon}">'
        '<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
        'body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style></head><body>')
page = head + body + '</body></html>'
(here / 'play-local.html').write_text(page, encoding='utf-8')
(here / 'docs').mkdir(exist_ok=True)
(here / 'docs' / 'index.html').write_text(page, encoding='utf-8')
(here / 'docs' / '.nojekyll').write_text('', encoding='utf-8')
print('ok')
