# 智潮 / Signal Tide 工作流程

这是一份 **执行用工作流**，不是对外宣传文档。

目标：

- 每天由 openclaw 抓取 AI 新闻线索
- 由 openclaw 自行筛选、重写、翻译
- 更新静态页面所需的 `issues.json` 与 `rss.xml`
- 推送到 GitHub 仓库 `shanbei2033/SIGNALTIDE`
- 由 GitHub Pages 自动发布最新页面

---

## 一、总原则

1. **新闻由 openclaw 抓取**，不是 RSS 直接展示。
2. **稿件由 openclaw 编写**，不是外部模型代写。
3. **文章多语言内容直接写入 `issues.json`**。
4. **UI 文案与文章正文分离**：
   - UI 在 `docs/locales/*.json`
   - 文章正文在 `docs/data/issues.json`
5. 页面是纯静态页面，核心产物是：
   - `docs/data/raw-feeds.json`
   - `docs/data/issues.json`
   - `docs/data/archive/YYYY-MM-DD.json`
   - `docs/rss.xml`
6. 如果当天候选源质量很差，也不要硬凑大新闻；可以更克制，但不能空白。
7. 所有改动都以 **页面完整、可读、能发布** 为优先目标。

---

## 二、仓库与发布目标

- 本地项目目录：`/root/.openclaw/workspace/ai-news-pages-demo`
- GitHub 仓库：`https://github.com/shanbei2033/SIGNALTIDE`
- GitHub Pages：使用仓库 `main` 分支的 `/docs` 目录发布
- 当前预览目录：
  - `/var/www/ai-news/`
  - `/var/www/ai-news-ai1/`

发布逻辑：

1. 本地生成并更新 `docs/` 内文件
2. `git add / commit / push`
3. GitHub Pages 自动刷新

---

## 三、每日执行流程

### 第 1 步：抓取候选新闻

进入项目目录：

```bash
cd /root/.openclaw/workspace/ai-news-pages-demo
```

抓取候选源：

```bash
npm run fetch:feeds
```

执行后会更新：

- `docs/data/raw-feeds.json`

要求：

- 先看候选池，不要盲写
- 候选尽量覆盖：
  - 官方 / 一手发布
  - 科技媒体
  - 研究
  - 开源与开发者生态
  - 政策 / 治理 / 安全

---

### 第 2 步：筛选当天版面主题

目标是做出一版 **像日报** 的内容，而不是简单聚合。

筛选时遵循：

1. 头版必须选当天最有代表性的 1 条
2. 其余条目尽量多样化
3. 不要让同一家公司占据大多数版面
4. 优先覆盖这些面向：
   - 公司与产品
   - 模型 / 安全
   - 政策治理
   - 开源工具 / 开发者生态
   - 研究与产业影响
5. 总量应足够填满当前首页布局，不留大块空白

当前首页至少要照顾这些区块：

- 头版
- 今日要闻
- 趋势
- 观察
- 开源项目推荐

如果内容不足：

- 趋势和观察优先补足
- 必要时增加更偏研究 / 产业影响的条目
- 不要为了凑数重复同一主题

---

### 第 3 步：编写中文主稿

每篇文章至少要写这些字段：

- `id`
- `section`
- `category`
- `headline`
- `deck`
- `kicker`
- `byline`
- `publishedAt`
- `updatedAt`
- `readingTime`
- `tags`
- `summary`
- `bullets`
- `significance`
- `sources`

写作要求：

1. 标题不要过长，优先像报纸标题
2. `deck` 要解释这条新闻为什么重要
3. `summary` 用 2 段为主，必要时 3 段
4. 不要写空话、套话、过度夸张的话
5. 不要直接照搬原标题
6. 保留来源，不编造事实
7. 语气像日报编辑，不像营销文案

---

### 第 4 步：生成所有语言版本

必须写入这些语言：

- `zh-CN`
- `zh-TW`
- `en`
- `ja`
- `ko`
- `ru`
- `fr`
- `es`

写入位置：

- `articles[].i18n.<lang>`

要求：

1. 所有语言都要完整，不允许缺项
2. 至少包含：
   - `headline`
   - `deck`
   - `kicker`
   - `category`
   - `summary`
   - `significance`
3. 翻译可以自然表达，不追求逐字直译
4. 同一篇文章的语气在不同语言里尽量一致

---

### 第 5 步：写入 `issues.json`

最终产物写入：

- `docs/data/issues.json`

同时要求：

- `edition.date` 更新为当天
- `edition.generatedAt` 更新为当前时间
- `edition.lead` 指向头版文章 id
- 页面分区需要被当前文章数量撑起来

---

### 第 6 步：刷新 RSS 与归档

执行：

```bash
node scripts/daily-static-update.mjs
```

这一步会：

- 根据当前 `issues.json` 刷新 `docs/rss.xml`
- 刷新 `docs/data/archive/YYYY-MM-DD.json`

---

### 第 7 步：同步到本地预览目录

执行：

```bash
cp -R docs/. /var/www/ai-news/
cp -R docs/. /var/www/ai-news-ai1/
```

目的：

- 线上预览地址立即可看
- 便于人工检查版面是否留白、标题是否过长、语言切换是否正常

---

### 第 8 步：发布到 GitHub

在项目目录执行：

```bash
git add docs README.md WORKFLOW.md .github/workflows/nightly.yml scripts package.json package-lock.json
```

如果只是数据更新，至少保证：

```bash
git add docs
```

然后提交并推送：

```bash
git commit -m "Update daily edition"
git push origin main
```

要求：

- 推送前确认没有把无关临时文件带上
- 推送后 GitHub Pages 会自动刷新

---

## 四、版面要求

当前页面编辑要求：

1. 头版标题不要太长
2. 今日要闻、趋势、观察不能明显留空
3. 观察区如果偏空：
   - 优先补新文章
   - 再考虑增加单条显示密度
4. 趋势区要更紧凑，像短栏
5. 开源项目推荐保持紧凑，不要抢版面
6. 中文站名显示“智潮”，其他语言站名显示“Signal Tide”
7. 页面要保持“日报感”，不要做成资讯流或 SaaS 面板

---

## 五、每日完成后的检查清单

在推送前，至少检查：

- [ ] 首页能正常打开
- [ ] 详情页能正常打开
- [ ] RSS 能打开
- [ ] 头版标题不过长
- [ ] 今日要闻不空
- [ ] 趋势不空
- [ ] 观察不空
- [ ] 各语言切换后文章内容存在
- [ ] `issues.json` 日期正确
- [ ] `rss.xml` 已刷新
- [ ] GitHub push 成功

---

## 六、自动任务要求

每天早上自动执行时，必须做的事：

1. 先读本文件 `WORKFLOW.md`
2. 严格按本文件执行，不要依赖旧印象
3. 抓取新候选源
4. 生成当天新版 `issues.json`
5. 刷新 `rss.xml`
6. 推送到 GitHub Pages 仓库
7. 给用户发一条简短 Telegram 通知，说明今天版面已更新

通知风格要求：

- 简短
- 自然
- 不发内部执行细节
- 只说明版面已更新、可查看即可

---

## 七、失败时的处理

如果自动执行失败：

1. 不要清空现有 `issues.json`
2. 不要发布空版面
3. 保留昨天仍可访问的页面
4. 如果能恢复就恢复
5. 如果不能恢复，至少发一条简短 Telegram 说明：
   - 今天更新失败
   - 稍后补上

---

## 八、一句话定位

智潮 / Signal Tide 是：

**由 openclaw 抓取、编辑、翻译并发布的 AI 日报。**
