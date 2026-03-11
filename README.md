# 智潮 / Signal Tide

一个由 **openclaw 驱动** 的 AI 日报静态站。

它不是 RSS 直出站，也不是传统前后端新闻系统。它的工作方式是：

- 由 openclaw 抓取新闻线索
- 由 openclaw 进行筛选、整理、重写
- 由 openclaw 生成多语言正文并写入 `issues.json`
- 页面本身保持纯静态，适合部署到 GitHub Pages 等静态托管平台

## 项目定位

智潮 / Signal Tide 的目标不是做一个“把 RSS 堆上去”的聚合页，而是做一份：

**由 openclaw 驱动的 AI 日报**

重点在于：

- 内容要经过编辑整理
- 版面要像日报，而不是工具后台
- 部署要足够轻，适合低成本长期维护

## 为什么采用纯静态架构

这个项目优先选择纯静态页面，而不是有前后端的服务，主要原因是：

- 成本低
- 运维简单
- 不依赖数据库或常驻后端
- 服务器不稳定时，影响主要是“更新延迟”，而不是整站不可用
- 适合 GitHub Pages / Nginx / 对象存储等任意静态托管方案

换句话说，核心资产是：

- `issues.json`
- `rss.xml`
- 静态页面本身

而不是一个复杂的 Web 应用。

## 当前工作流程

### 1. 抓取候选新闻

openclaw 会抓取多个 RSS 源，覆盖：

- 官方 / 一手发布
- 科技媒体
- 研究与论文
- 开源与开发者生态
- 政策 / 治理 / 安全

候选结果写入：

- `docs/data/raw-feeds.json`

### 2. 编辑与写稿

openclaw 从候选池中选择当天值得写的主题，并直接生成稿件内容：

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

### 4. 静态渲染

前端页面只读取这些静态文件：

- `docs/data/issues.json`
- `docs/rss.xml`
- `docs/locales/*.json`

其中：

- `issues.json` 负责文章内容
- `locales` 负责 UI，例如标题、返回按钮、来源、阅读时间等

## 目录结构

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
│  ├─ build-digest.mjs
│  └─ migrate-article-translations-to-json.mjs
├─ README.md
├─ STATIC_WORKFLOW.md
└─ WORKFLOW.md
```

## 关键文件说明

### `docs/data/issues.json`
这是最核心的文件。

它负责承载：

- 当天版面信息
- 文章列表
- 每篇文章的正文
- 每篇文章的多语言翻译

### `docs/data/raw-feeds.json`
这是当天的原始候选新闻池，用于编辑参考，不直接面向最终用户。

### `docs/rss.xml`
站点自己的 RSS 订阅输出。

用户可以通过页面 footer 的 RSS 图标：

- 复制 RSS 地址
- 跳转到 RSS 文件

## 本地使用

安装依赖：

```bash
npm install
```

抓取候选源：

```bash
npm run fetch:feeds
```

刷新当前归档与 RSS：

```bash
npm run build:static
```

本地预览：

```bash
cd docs
python3 -m http.server 4173
```

打开：

```text
http://localhost:4173
```

## GitHub Pages 部署

推荐做法：

1. 将本项目推送到 GitHub 仓库
2. 在仓库 Settings → Pages 中启用 GitHub Pages
3. 选择：
   - Branch: `main`
   - Folder: `/docs`

之后站点即可通过 GitHub Pages 提供访问。

## 输出结果

每次更新后，项目会输出：

- `docs/data/raw-feeds.json`
- `docs/data/issues.json`
- `docs/data/archive/YYYY-MM-DD.json`
- `docs/rss.xml`

## 说明

本仓库曾包含基于 GitHub Actions / 外部模型接口的早期实验配置，但当前项目的主方向已经调整为：

- 由 openclaw 自己抓取新闻
- 由 openclaw 自己写稿
- 由 openclaw 自己生成翻译
- 最终发布为纯静态日报

因此，理解这个项目时，应以当前 README、WORKFLOW.md 与实际脚本行为为准。
