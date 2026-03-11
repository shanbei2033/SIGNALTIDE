# AI Daily Pages Demo

一个可直接部署到 GitHub Pages 的静态站点 demo。

目标：
- 像日报一样，清晰列出当天 AI 领域的重要新闻
- 每条新闻都经过重新整理，不直接照搬原标题或原文
- 点击列表项可进入详情页
- 页面尽量接近专业媒体的版式，避免夸张视觉和“AI 味”设计
- 支持每天 00:05 UTC 自动抓取并生成数据，然后提交回仓库并部署到 GitHub Pages

## 目录结构

- `docs/`：静态页面与生成后的数据
- `scripts/build-digest.mjs`：生成日报数据
- `.github/workflows/nightly.yml`：定时抓取、提交、部署

## 本地预览

```bash
npm install
npm run build:demo
cd docs
python3 -m http.server 4173
```

打开：`http://localhost:4173`

## 运行模式

### 1. Demo 模式

直接写入当前这版人工整理的示例内容：

```bash
npm run build:demo
```

### 2. 自动抓取模式

```bash
npm run build
```

默认会抓取这些 RSS：
- Google AI Blog
- TechCrunch AI
- The Verge AI

如果仓库配置了以下任一 Secret，脚本可以进入“模型整理”模式，把候选新闻重写成中文条目：
- `OPENAI_API_KEY`
- `OPENROUTER_API_KEY`

可选环境变量：
- `LLM_MODEL`：指定模型名
- `OPENAI_BASE_URL`：自定义 OpenAI 兼容接口地址
- `SITE_BASE_URL`：站点根地址，用于 SEO 元信息

如果没有配置模型密钥，脚本仍会成功执行，但会回退到 demo 内容，避免页面空白。

## GitHub Pages 部署

### 最简单的做法

1. 新建 GitHub 仓库
2. 把这个目录内容推上去
3. 在仓库设置里启用 GitHub Pages
4. 使用 Actions 部署（本项目已附带 workflow）

### 工作流行为

- 每天 `00:05 UTC` 运行
- 抓取新闻源并生成 `docs/data/issues.json`
- 如果文件有变化，则自动提交回仓库
- 将 `docs/` 作为 Pages 内容部署

## 建议的下一步

如果这版排版和语气方向对了，我可以继续做两件事：

1. 把自动抓取扩展成更多信源，并做更稳的去重与分栏
2. 按你的要求，把“夜里 12 点后自动整理并同步到 GitHub”做成可直接上线的一版，包括仓库初始化说明
