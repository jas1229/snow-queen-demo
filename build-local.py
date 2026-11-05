# 把 index.html（artifact 的写法，没有 <head>）包成完整网页：
#   play-local.html            本地双击就能玩
#   docs/index.html            放在 GitHub Pages 上的那份，能「添加到主屏幕」，离线也能打开
#   itch/snow-queen-itch.zip   传到 itch.io 的包（itch 文件夹存在时才生成）
#   play-local-edit.html / artifact-edit.html   改稿台（游戏里直接改台词），后者发成单独的 artifact
# 配乐录音在 docs/audio/，页面默认从 audio/ 找；本地双击的那两份改成从 docs/audio/ 找。
# 谷歌字体改成不挡渲染的加载方式：连不上谷歌的时候页面照样马上出来，先用系统字体。
import hashlib, json, pathlib, re, urllib.parse, zipfile
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
base_head = ('<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">'
             '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">'
             f'<title>{title}</title><meta name="description" content="{desc}">'
             f'<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">'
             '<style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}'
             'body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>')
LOCAL_AUDIO = "<script>window.SQ_AUDIO_BASE='docs/audio/';</script>"
EDIT_FLAG = '<script>window.SQ_EDIT=true;</script>'
plain_head = base_head + f'<link rel="icon" href="{icon}"></head><body>'
pwa_head = (base_head +
            '<link rel="manifest" href="manifest.webmanifest">'
            '<link rel="icon" href="icon-192.png"><link rel="apple-touch-icon" href="icon-180.png">'
            '<meta name="theme-color" content="#0a0f1c">'
            '<meta name="mobile-web-app-capable" content="yes"><meta name="apple-mobile-web-app-capable" content="yes">'
            '<meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">'
            '<meta name="apple-mobile-web-app-title" content="冰雪女王">'
            "<script>window.SQ_PWA=true;if('serviceWorker'in navigator&&location.protocol.indexOf('http')===0)"
            "addEventListener('load',function(){navigator.serviceWorker.register('sw.js').catch(function(){})});</script>"
            '</head><body>')
plain = plain_head + body + '</body></html>'
pwa = pwa_head + body + '</body></html>'

(here / 'play-local.html').write_text(plain.replace('</head>', LOCAL_AUDIO + '</head>', 1), encoding='utf-8')
(here / 'play-local-edit.html').write_text(plain.replace('</head>', LOCAL_AUDIO + EDIT_FLAG + '</head>', 1).replace(f'<title>{title}</title>', '<title>冰雪女王改稿台</title>', 1), encoding='utf-8')
(here / 'artifact-edit.html').write_text('<title>冰雪女王改稿台</title>\n' + EDIT_FLAG + '\n' + src[m.end():] if m else EDIT_FLAG + src, encoding='utf-8')

docs = here / 'docs'
docs.mkdir(exist_ok=True)
(docs / 'index.html').write_text(pwa, encoding='utf-8')
(docs / '.nojekyll').write_text('', encoding='utf-8')
manifest = {
    'name': title, 'short_name': '冰雪女王', 'description': desc, 'lang': 'zh-CN',
    'start_url': './', 'scope': './', 'display': 'fullscreen', 'orientation': 'any',
    'background_color': '#0a0f1c', 'theme_color': '#0a0f1c',
    'icons': [
        {'src': 'icon-192.png', 'sizes': '192x192', 'type': 'image/png'},
        {'src': 'icon-512.png', 'sizes': '512x512', 'type': 'image/png'},
        {'src': 'icon-512-maskable.png', 'sizes': '512x512', 'type': 'image/png', 'purpose': 'maskable'},
    ],
}
(docs / 'manifest.webmanifest').write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
# 离线缓存：有网先拿新的，没网用存下的；版本号跟着页面内容变，旧缓存会被清掉
ver = hashlib.sha1(pwa.encode('utf-8')).hexdigest()[:10]
sw = """const CACHE = 'snowqueen-%s';
const FILES = ['./', './index.html', './manifest.webmanifest', './icon-180.png', './icon-192.png', './icon-512.png', './icon-512-maskable.png'];
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => {
  const req = e.request;
  if (req.method !== 'GET' || new URL(req.url).origin !== location.origin) return;
  if (new URL(req.url).pathname.indexOf('/audio/') >= 0) return;  // 配乐文件按段请求，交给浏览器自己处理
  e.respondWith(fetch(req).then(res => { if (res.ok) { const copy = res.clone(); caches.open(CACHE).then(c => c.put(req, copy)); } return res; })
    .catch(() => caches.match(req, { ignoreSearch: true }).then(r => r || caches.match('./index.html'))));
});
""" % ver
(docs / 'sw.js').write_text(sw, encoding='utf-8')

itch = here / 'itch'
if itch.is_dir():
    with zipfile.ZipFile(itch / 'snow-queen-itch.zip', 'w', zipfile.ZIP_DEFLATED) as z:
        z.writestr('index.html', plain)
        for f in sorted((docs / 'audio').glob('*.mp3')):
            z.write(f, 'audio/' + f.name)
print('ok', ver)
