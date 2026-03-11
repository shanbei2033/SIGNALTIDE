# 智潮 / Signal Tide 工作流程

这是一份由 openclaw 驱动的 AI 日报工作流程说明。

## 核心原则

- 新闻线索由小扇贝自行抓取
- 稿件由小扇贝自行筛选、整理、重写
- 多语言正文由小扇贝自行生成并写入 `issues.json`
- 页面本身保持纯静态
- UI 文案与文章正文分离

## 数据流

### 1. 新闻采集

小扇贝定期抓取多个 RSS 源，来源覆盖：

- 官方 / 一手发布
- 科技媒体
- 研究与论文
- 开源与开发者生态
- 政策 / 治理 / 安全

抓取结果写入：

- `docs/data/raw-feeds.json`

这个文件是候选池，不直接给用户看。

### 2. 编辑筛选

小扇贝从候选池中人工式筛选当天最值得上的新闻，要求：

- 不追求数量，优先重要性
- 尽量保持题材多样化
- 不让同一家公司占据大多数版面
- 优先覆盖：公司产品、研究、工具、政策、产业影响等不同面向

### 3. 稿件生成

小扇贝为入选新闻生成正式稿件，字段包括：

- `headline`
- `deck`
- `kicker`
- `category`
- `summary`
- `significance`
- `sources`
- `tags`

这些内容由小扇贝直接写入，不依赖额外外部 AI 代写。

### 4. 多语言生成

文章翻译不放在前端翻译表里，而是直接写进：

- `docs/data/issues.json`
- 结构为 `articles[].i18n.<lang>`

目前设计语言包括：

- `zh-CN`
- `zh-TW`
- `en`
- `ja`
- `ko`
- `ru`
- `fr`
- `es`

### 5. 静态站渲染

前端页面只负责读取静态文件：

- `docs/data/issues.json`
- `docs/rss.xml`
- `docs/locales/*.json`

其中：

- `issues.json` 负责文章内容与文章多语言
- `locales/*.json` 只负责 UI 文案，例如：
  - 站点标题
  - 返回按钮
  - 来源
  - 阅读时间
  - 栏目标题

## 文件结构

```text
ai-news-pages-demo/
├─ docs/
│  ├─ index.html
│  ├─ article.html
│  ├─ rss.xml
│  ├─ assets/
│  │  ├─ app.js
│  │  ├─ article.js
│  │  ├─ content-i18n.js
│  │  ├─ i18n.js
│  │  └─ style.css
│  ├─ data/
│  │  ├─ issues.json
│  │  ├─ raw-feeds.json
│  │  └─ archive/
│  └─ locales/
├─ scripts/
│  ├─ feed-sources.mjs
│  ├─ daily-static-update.mjs
│  └─ migrate-article-translations-to-json.mjs
└─ WORKFLOW.md
```

## 输出结果

每次更新后，项目会产出：

- `docs/data/raw-feeds.json`：原始候选新闻
- `docs/data/issues.json`：当天正式版面
- `docs/data/archive/YYYY-MM-DD.json`：历史归档
- `docs/rss.xml`：站点 RSS 订阅源

## 页面原则

- 网站部署为纯静态页面
- 无需后端服务
- 每天更新时只需替换静态文件
- `issues.json` 是核心数据文件

## RSS 支持

该项目既：

- 支持抓取外部 RSS 作为新闻线索
- 也支持自己输出 RSS

输出地址为：

- `rss.xml`

用户可以通过页面 footer 的 RSS 图标：

- 复制 RSS 地址
- 跳转到 RSS 订阅文件

## 每日更新流程（目标）

1. 抓取当天候选源
2. 更新 `raw-feeds.json`
3. 由小扇贝生成当天新版 `issues.json`
4. 刷新 `rss.xml`
5. 同步到静态托管目录或 GitHub 仓库
6. 替换前一天首页内容

## 产品定位

这不是一个简单聚合站，也不是 RSS 直出站。

它的定位是：

**由 openclaw 驱动的 AI 日报**

也就是说：

- 新闻由小扇贝抓取
- 编辑由小扇贝完成
- 翻译由小扇贝完成
- 页面由静态站展示
