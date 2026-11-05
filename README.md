# 船尾的冰雪女王

安徒生的《冰雪女王》搬到了一艘世代船上。格尔达从船头走到船尾，一路哈开结霜的舷窗，把看见的回忆收进小册子，最后走进冷舱，把加伊带回家。

在线玩：https://jas1229.github.io/snow-queen-demo/

开始页可以切换中文、English、Français，还可以选「原版」或「加长版」。加长版多几段安徒生原文：加伊看画册时说的话、冰雪女王空荡荡的大殿和“理智之镜”、她临走的话，冷舱里要亲手拼一次“永恒”，回忆里也多了些小毛病。

## 怎么玩

- 电脑：← → 走路，按住空格哈气，E 说话、翻页，B 打开小册子，M 开关音乐
- 手机：屏幕下面有按钮，横过来玩画面更大
- 放到手机桌面：iPhone 用 Safari 打开，点「分享」→「添加到主屏幕」；安卓在浏览器菜单里选「添加到主屏幕」。之后从桌面图标打开是全屏的，没网也能玩
- 进度存在浏览器里，下次打开可以接着玩

从头玩到尾二十分钟左右。

## 说明

七个故事各做了一段，结局后面还有三段回家的路。画面、文字和声音都还是草稿。英文和法文是照中文翻的。

配乐是莫扎特、帕赫贝尔、格里格、佩措尔德、勃拉姆斯、巴赫、萨蒂、德沃夏克的曲子，都已经过了版权期，在浏览器里用合成器现场弹。

改编自安徒生《冰雪女王》（1844）。

## 文件

- `index.html`：游戏源文件，英文和法文的译文表也在里面（按中文原句对应）
- 原版和加长版是同一份代码，`index.html` 里的 `LONG` 开关决定走哪条线（开始页选，存档里也记着）
- `docs/`：放在 GitHub Pages 上的那份，运行 `python3 build-local.py` 从源文件生成；里面还有添加到主屏幕用的图标、`manifest.webmanifest` 和离线缓存 `sw.js`

---

**The Snow Queen at the Stern** — a short browser game (about 20 minutes) based on Hans Christian Andersen's *The Snow Queen*, set on a generation starship. Walk from the bow to the stern, breathe on frosted portholes to uncover memories, and bring Kay home. Playable in Chinese, English and French, as the original cut or an extended one with more of Andersen's own text and a hands-on ice puzzle: https://jas1229.github.io/snow-queen-demo/
