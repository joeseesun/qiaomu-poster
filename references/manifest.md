# 任务清单与运行

所有路径相对于清单文件所在目录，不能使用越出目录的路径。HTML只渲染agent制作并检查过的本地内容，不能把陌生网页当可执行模板；渲染器阻断HTTP(S)请求。图片与字体应本地化。

```json
{
  "width": 1080, "height": 1620, "scale": 2,
  "title": "示例活动 Demo", "mixed_title": false,
  "qr_url": "https://example.org/register", "thumbnail_width": 540,
  "cta": "扫码报名", "required_text": ["示例活动", "免费"],
  "forbidden_text": ["限时最后一天"],
  "posters": [{"id":"demo", "name":"示例品牌", "html":"demo.html", "png":"demo.png",
    "metaphor":"翻开的书页承载学习机会", "topology":"centered-book"}]
}
```

单张字段可覆盖width/height/scale/title/mixed_title/max_title_gap/qr_url/cta/required_text/forbidden_text。mixed_title=true时DOM需有 .event-title 内的 .event-latin 和 .event-han；单语标题只需.event-title。默认最大组间距32px，需按画布与字体合理设置，不能通过放大阈值掩盖用户指出的分组问题。

`qr`生成PNG，M纠错、4模块白边；先确认URL。`render`导出并保存render-report.json及HTML/PNG摘要。`audit`检查真实PNG、事实文本和几何并保存audit-report.json，问题计数必须0；修改HTML/PNG会使旧证据失效。`gallery`生成相对路径可打开的gallery.html。

如果没有扫码目标，可省略qr_url；不得虚构URL。自动QR检查要求图中恰好一个码且内容精确相等。required_text应列标题、日期、地点、价格/免费政策等实际必需内容，不复制历史案例事实。

批量默认检查隐喻和拓扑声明；6张以上至少3种拓扑，连续同拓扑不超过3张。此检查只能识别声明缺失和重复；虚假标签不能证明结构不同，应同尺度看图。用户明确要求统一模板时可设置check_diversity=false并在brief记录理由，不能用此开关绕过多风格要求。

浏览器兼容：可通过环境变量 `POSTER_BROWSER_EXECUTABLE` 指定本机浏览器路径，尤其用于已知超大 JPG 解码差异；默认使用隔离 Chromium。解码失败应修复或换已验证浏览器，不可忽略。
