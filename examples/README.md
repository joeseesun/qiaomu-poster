# 分级案例

首批18张来自同一真实活动批次。时间、票价、酒店与二维码均为历史案例，不是新任务默认值。源图和品牌标识由用户提供并明确授权将本批次作为GitHub案例展示；第三方标识、头像、角色及商标权益不随本仓库MIT代码许可转授。

| 级别 | 案例 | 可学习的机制 |
|---|---|---|
| 小：单张精排 | [04 蓝色连接](geo-2026/04.png) / [HTML](geo-2026/04.html) | 组内字距、曲线品牌语言、信息分栏 |
| 中：人物融合 | [11 斜面人物](geo-2026/11.png) / [HTML](geo-2026/11.html) | 原头像透明化、跨色面、合理前景遮挡 |
| 中：衍生主视觉 | [14 书页狐狸](geo-2026/14.png) / [HTML](geo-2026/14.html) | 原Logo署名与品牌衍生物分离 |
| 大：18媒体系列 | [总览](geo-2026/overview.png) / [画廊](geo-2026/index.html) / [清单](geo-2026/posters.json) | 读取全量记录、独立拓扑、统一事实与逐图二维码验证 |

技术评级：18/18 原批次全尺寸及540px缩图二维码解码通过，图片加载/文本边界/标题组通过。审美评级：agent多轮目视修订，未取得用户对最终18张的逐张评价；不能称作客户认可、盲评胜出或转化效果证明。

本技能新运行时已独立重渲染这18张，输出[render-report.json](geo-2026/render-report.json)、[audit-report.json](geo-2026/audit-report.json)，18张均通过。系统字体可能造成跨平台字形差异；本地Noto子集随案例打包。需要复现指定系统字体时应合法安装，或选择可再分发字体并重新目视验收。

## 新增三品牌案例

同一大会新增三个品牌设计，原始标志由用户提供，用户明确要求推送GitHub。第一标志未提供品牌名，保持中性称呼。

| 案例 | 高清图 | 源文件 | 构图方法 |
| --- | --- | --- | --- |
| 黑白汇聚 | [PNG](geo-three-brands/01.png) | [HTML](geo-three-brands/01.html) | 四向标志的中央留白与交汇线 |
| WaytoAGI | [PNG](geo-three-brands/02.png) | [HTML](geo-three-brands/02.html) | 彩虹延伸至画布边缘，中段紧密标题 |
| YouMind | [PNG](geo-three-brands/03.png) | [HTML](geo-three-brands/03.html) | 原标志署名，纸带衍生视觉与衬线字体 |

[全部打包下载](geo-three-brands/three-brand-posters-and-source.zip) · [三张技术验收](geo-three-brands/audit-report.json)。第三方素材权利边界与原案例相同。
