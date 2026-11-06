"""翻译表工具。index.html 里的 window.SQ_I18N 以中文原句为键，值是 [英, 法, 日]。

  python3 tools/i18n.py check          列出代码里有、翻译表里缺的中文句子，以及缺日语的条目
  python3 tools/i18n.py merge-ja F.json  把 {中文: 日语} 写进表里每条的第三格

在别的脚本里也可以 import：load(src) -> (dict, a, b)，dump(d) -> 表的文本。
"""
import json, pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
INDEX = ROOT / 'index.html'
HEAD = '<script>window.SQ_I18N = '
TAIL = '};</script>'
CJK = re.compile(r'[\u3400-\u9fff\uff01-\uff5e\u3000-\u303f]')
# 只在程序内部用、不显示给玩家的中文（道具编号、拼接用的分隔符）
IGNORE = {'靴子', '红鞋', '大手套', '手笼', '鳕鱼干', '\u3000', '\u3000·\u3000', '年', '月', '日'}


def load(src):
    a = src.index(HEAD) + len(HEAD)
    b = src.index(TAIL, a) + 1
    return json.loads(src[a:b]), a, b


def dump(d):
    rows = [json.dumps(k, ensure_ascii=False) + ': ' + json.dumps(v, ensure_ascii=False) for k, v in d.items()]
    return '{\n' + ',\n'.join(rows) + '\n}'


def save(src, d):
    _, a, b = load(src)
    return src[:a] + dump(d) + src[b:]


def code_strings(src):
    """代码里所有带中文的字符串字面量和 data-i18n 属性（改稿台那段只有中文界面，跳过）。"""
    _, a, b = load(src)
    body = src[:a] + src[b:]
    body = re.sub(r'// ---- 改稿台 start ----.*?// ---- 改稿台 end ----', '', body, flags=re.S)
    body = re.sub(r'<style>.*?</style>', '', body, flags=re.S)
    out = []
    for m in re.finditer(r'data-i18n(?:-aria|-title)?="([^"]+)"', body):
        out.append(m.group(1))
    script = '\n'.join(re.findall(r'<script>(.*?)</script>', body, flags=re.S))
    script = re.sub(r'^\s*//.*$', '', script, flags=re.M)
    script = re.sub(r'(?<![:\'"\\])//[^\n\'"]*$', '', script, flags=re.M)
    for m in re.finditer(r"'((?:[^'\\\n]|\\.)*)'", script):
        s = m.group(1).replace("\\'", "'").replace('\\n', '\n')
        if CJK.search(s):
            out.append(s)
    return out


def check():
    src = INDEX.read_text(encoding='utf-8')
    d, _, _ = load(src)
    seen, missing = set(), []
    for s in code_strings(src):
        if s in seen:
            continue
        seen.add(s)
        if s not in d and s not in IGNORE:
            missing.append(s)
    no_ja = [k for k, v in d.items() if len(v) < 3 or not v[2]]
    unused = [k for k in d if k not in seen]
    print(f'{len(d)} entries; {len(missing)} strings missing from the table; {len(no_ja)} without Japanese; {len(unused)} not seen in code')
    for s in missing:
        print('  MISSING', repr(s[:70]))
    return missing, no_ja, unused


def merge_ja(path):
    src = INDEX.read_text(encoding='utf-8')
    d, _, _ = load(src)
    ja = json.loads(pathlib.Path(path).read_text(encoding='utf-8'))
    n = 0
    for k, v in ja.items():
        if k in d:
            row = list(d[k]) + [''] * (3 - len(d[k]))
            row[2] = v
            d[k] = row
            n += 1
    INDEX.write_text(save(src, d), encoding='utf-8')
    print(f'merged {n} Japanese lines ({len(ja) - n} keys not in the table)')


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'check'
    if cmd == 'check':
        check()
    elif cmd == 'merge-ja':
        merge_ja(sys.argv[2])
    else:
        sys.exit(__doc__)
