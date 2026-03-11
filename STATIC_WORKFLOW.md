# Signal Tide 静态发布流程

目标：站点本身保持纯静态，前端只读取 `docs/data/issues.json`。

## 当前前端原则

- `index.html` / `article.html` 是纯静态页面
- 页面运行时只 fetch 本地 JSON 数据
- 新闻正文与文章多语言内容必须写入 `issues.json`
- 不依赖后端 API、数据库或服务器渲染

## 每日更新流程

1. 抓取 RSS 候选源
2. 由编辑脚本筛选并重写当天新闻
3. 将多语言内容写入 `docs/data/issues.json`
4. 可选写入 `docs/data/archive/YYYY-MM-DD.json`
5. git commit
6. git push 到 GitHub 仓库
7. 静态托管（例如 GitHub Pages）自动刷新

## 新脚本

```bash
npm run build:static
```

对应脚本：

- `scripts/daily-static-update.mjs`

它会：

- 抓取 RSS 源
- 生成 `docs/data/raw-feeds.json`
- 由 openclaw 编辑生成静态站可消费的 `docs/data/issues.json`
- 同时归档到 `docs/data/archive/`

## 建议的 issues.json 结构

- `site`
- `edition`
- `sections`
- `articles`
- `articles[].i18n.<lang>`

这样前端切换语言时，文章正文完全来自 `issues.json`；JS 里的翻译只负责 UI 文案，不负责新闻正文。

## 后续你需要提供的外部配置

- GitHub 仓库地址
- GitHub token（用于 push）
- （可选）额外外部服务配置
- 定时运行方式（例如服务器 cron，每天 09:00）
