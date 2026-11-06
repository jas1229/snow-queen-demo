# 船尾的冰雪女王

安徒生的《冰雪女王》搬到了一艘世代船上。格尔达从船头走到船尾，一路哈开结霜的舷窗，把看见的回忆收进小册子，最后走进冷舱，把加伊带回家。

在线玩：https://jas1229.github.io/snow-queen-demo/

开始页可以切换中文、English、Français、日本語，还可以选「原版」或「加长版」。右上角的「更新记录」列着每一版改了什么。加长版多几段安徒生原文：加伊看画册时说的话、冰雪女王空荡荡的大殿和“理智之镜”、她临走的话，冷舱里要亲手拼一次“永恒”，回忆里也多了些小毛病。

## 怎么玩

- 电脑：← → 走路，按住空格哈气，E 说话、翻页，B 打开小册子，L 打开对话记录，M 开关音乐
- 手机：屏幕下面有按钮，横过来玩画面更大
- 对话框、章节卡和想起的回忆都会停在那儿，点一下才往下走；错过的话可以点顶上的「记录」翻回去看
- 放到手机桌面：iPhone 用 Safari 打开，点「分享」→「添加到主屏幕」；安卓在浏览器菜单里选「添加到主屏幕」。之后从桌面图标打开是全屏的，没网也能玩
- 进度存在浏览器里，下次打开可以接着玩

从头玩到尾二十分钟左右。

## 说明

七个故事各做了一段，结局后面还有三段回家的路。画面、文字和声音都还是草稿。英文、法文和日文是照中文翻的。

配乐用的是公开授权的真人录音，都来自维基共享资源，剪掉了头尾静音、统一了响度、转成 MP3（在 `docs/audio/`）。文件加载不出来的时候，游戏会退回浏览器里的合成器版本。

| 段落 | 曲子 | 演奏 | 授权 |
|---|---|---|---|
| 船头、尾声 | 莫扎特《小星星变奏曲》K.265（船头用主题和前四段变奏，尾声只用主题） | Stefano Ligoratti，钢琴 | [CC BY 3.0](https://commons.wikimedia.org/wiki/File:Mozart_-_12_Variations_K._265_-_Stefano_Ligoratti.mp3)，有剪辑 |
| 水渠、春天跟着走 | 帕赫贝尔《卡农》 | 美国空军乐团 The Strolling Strings | [公有领域](https://commons.wikimedia.org/wiki/File:Canon_(2004)_-_Strolling_Strings_-_United_States_Air_Force_Band.mp3) |
| 花园 | 格里格《晨景》 | 捷克国家交响乐团（Musopen） | [公有领域](https://commons.wikimedia.org/wiki/File:Musopen_-_Morning.ogg) |
| 舰桥 | 佩措尔德《G 大调小步舞曲》 | Musopen | [公有领域](https://commons.wikimedia.org/wiki/File:Minuet_in_G_major,_Anh._114_-_Notebook_for_Anna_Magdalena_Bach.ogg) |
| 废弃区 | 格里格《山大王的宫殿》 | 捷克国家交响乐团（Musopen） | [公有领域](https://commons.wikimedia.org/wiki/File:Musopen_-_In_the_Hall_Of_The_Mountain_King.ogg) |
| 废弃区的夜里 | 勃拉姆斯《摇篮曲》 | 一只上发条的八音盒（录音：stephan，pdsounds.org） | [公有领域](https://commons.wikimedia.org/wiki/File:Lullaby_wound_up_clock_guten_abend_gute_nacht.ogg) |
| 冰原 | 巴赫《C 大调前奏曲》BWV 846 | 石坂纪美子（Kimiko Ishizaka），Open Well-Tempered Clavier | [CC0](https://commons.wikimedia.org/wiki/File:Kimiko_Ishizaka_-_Bach_-_Well-Tempered_Clavier,_Book_1_-_01_Prelude_No._1_in_C_major,_BWV_846.ogg) |
| 冷舱 | 萨蒂《裸体歌舞》第一首 | Robin Alciatore，钢琴 | [公有领域](https://commons.wikimedia.org/wiki/File:Erik_Satie_-_gymnopedies_-_la_1_ere._lent_et_douloureux.ogg) |
| 归途 | 德沃夏克《念故乡》（《自新大陆》第二乐章） | 美国空军乐团 Concert Band | [公有领域](https://commons.wikimedia.org/wiki/File:Goin%27_Home_-_Concert_Band_-_United_States_Air_Force_Band.mp3) |

改编自安徒生《冰雪女王》（1844）。

## 文件

- `index.html`：游戏源文件，英文、法文、日文的译文表也在里面（按中文原句对应）
- `tools/i18n.py`：检查译文表，`python3 tools/i18n.py check` 列出代码里有、表里还没翻的句子
- 原版和加长版是同一份代码，`index.html` 里的 `LONG` 开关决定走哪条线（开始页选，存档里也记着）
- `docs/`：放在 GitHub Pages 上的那份，运行 `python3 build-local.py` 从源文件生成；里面还有添加到主屏幕用的图标、`manifest.webmanifest` 和离线缓存 `sw.js`
- 一句台词可以分几个对话框：文字里的换行就是翻页。`build-local.py` 还会生成 `play-local-edit.html`（改稿模式：对话框上有「改这句」，能直接改台词、拆框）

---

**The Snow Queen at the Stern** — a short browser game (about 20 minutes) based on Hans Christian Andersen's *The Snow Queen*, set on a generation starship. Walk from the bow to the stern, breathe on frosted portholes to uncover memories, and bring Kay home. Playable in Chinese, English, French and Japanese, as the original cut or an extended one with more of Andersen's own text and a hands-on ice puzzle: https://jas1229.github.io/snow-queen-demo/
