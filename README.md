# 智潮 / Signal Tide

一个由 **openclaw 驱动** 的 AI 日报。

它不是 RSS 直出站，也不是简单的新闻聚合页。它的工作方式是：

- 由 openclaw 抓取新闻线索
- 由 openclaw 筛选当天值得写的主题
- 由 openclaw 重写稿件与生成多语言内容
- 由 openclaw 将结果写入 `issues.json`
- 由静态页面负责展示当天版面

## 项目定位

智潮 / Signal Tide 想做的不是“把 RSS 堆上去”，而是一份：

**由 openclaw 驱动的 AI 日报**

它强调的是：

- 内容经过整理与重写
- 版面更接近日报而不是工具页
- 每天生成一版新的 AI 新闻页面

## 当前工作流程

### 1. 抓取候选新闻

openclaw 会抓取多个 RSS 源，候选结果写入：

- `docs/data/raw-feeds.json`

这一步是线索收集，不直接面向最终读者。

### 2. 编辑与写稿

openclaw 从候选池中选择当天值得写的主题，并直接生成稿件内容，包括：

- headline
- deck
- kicker
- category
- summary
- significance
- tags
- sources

这些内容由 openclaw 自己写入，不依赖额外外部 AI 接口代写。

### 3. 多语言内容

文章翻译直接写入：

- `docs/data/issues.json`

结构为：

- `articles[].i18n.<lang>`

也就是说：

- **文章正文多语言在 JSON 里**
- **前端翻译表只负责 UI 文案**

### 4. 页面展示

前端页面读取：

- `docs/data/issues.json`
- `docs/rss.xml`
- `docs/locales/*.json`

其中：

- `issues.json` 负责文章内容
- `locales` 负责 UI，例如标题、返回按钮、来源、阅读时间等

## 关键文件

### `docs/data/issues.json`
这是最核心的文件，负责承载：

- 当天版面信息
- 文章列表
- 每篇文章正文
- 每篇文章的多语言翻译

### `docs/data/raw-feeds.json`
当天的原始候选新闻池，用于编辑参考。

### `docs/rss.xml`
站点自己的 RSS 订阅输出。

用户可以通过页面 footer 的 RSS 图标：

- 复制 RSS 地址
- 跳转到 RSS 文件

## 输出结果

每次更新后，项目会产出：

- `docs/data/raw-feeds.json`
- `docs/data/issues.json`
- `docs/data/archive/YYYY-MM-DD.json`
- `docs/rss.xml`
