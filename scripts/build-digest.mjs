import fs from 'node:fs/promises';
import path from 'node:path';
import Parser from 'rss-parser';
import { demoEdition } from './demo-fixtures.mjs';
import { FEED_SOURCES } from './feed-sources.mjs';

const root = path.resolve(process.cwd());
const docsDir = path.join(root, 'docs');
const dataDir = path.join(docsDir, 'data');
const parser = new Parser({
  timeout: 20000,
  headers: {
    'user-agent': 'Mozilla/5.0 (compatible; AI Daily Ledger Bot/0.1; +https://github.com/)'
  }
});

const sources = FEED_SOURCES;

const demoMode = process.env.DEMO_MODE === '1';

function isoDate(value = new Date()) {
  return new Date(value).toISOString().slice(0, 10);
}

async function ensureDirs() {
  await fs.mkdir(dataDir, { recursive: true });
}

async function writeJson(file, data) {
  await fs.writeFile(file, JSON.stringify(data, null, 2) + '\n', 'utf8');
}

function stripHtml(input = '') {
  return input
    .replace(/<[^>]*>/g, ' ')
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/\s+/g, ' ')
    .trim();
}

function slugify(input = '') {
  return input
    .toLowerCase()
    .replace(/[^a-z0-9\u4e00-\u9fa5]+/g, '-')
    .replace(/^-+|-+$/g, '')
    .slice(0, 80);
}

function normalizeTitle(title = '') {
  return title.toLowerCase().replace(/[^a-z0-9\u4e00-\u9fa5]+/g, ' ').replace(/\s+/g, ' ').trim();
}

function dedupeItems(items) {
  const seen = new Set();
  return items.filter((item) => {
    if (item.error) return true;
    const key = `${normalizeTitle(item.title)}|${item.link}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

async function fetchFeeds() {
  const results = [];
  for (const source of sources) {
    try {
      const feed = await parser.parseURL(source.url);
      const items = (feed.items || []).slice(0, 10).map((item) => ({
        source: source.name,
        sourceType: source.type || 'general',
        feedTitle: feed.title || source.name,
        title: item.title || '',
        link: item.link || '',
        publishedAt: item.isoDate || item.pubDate || null,
        contentSnippet: stripHtml(item.contentSnippet || item.content || item.summary || item['content:encoded'] || ''),
        categories: item.categories || []
      }));
      results.push(...items);
    } catch (error) {
      results.push({
        source: source.name,
        sourceType: source.type || 'general',
        error: String(error)
      });
    }
  }
  return dedupeItems(results);
}

function buildFallbackEdition(rawItems) {
  return {
    ...demoEdition,
    edition: {
      ...demoEdition.edition,
      id: isoDate(),
      date: isoDate(),
      displayDate: new Intl.DateTimeFormat('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        timeZone: 'UTC'
      }).format(new Date()),
      generatedAt: new Date().toISOString(),
      mode: 'fallback-demo',
      editorNote: '未配置模型密钥，当前自动回退到 demo 版内容；RSS 原始候选已同步输出。'
    }
  };
}

async function maybeGenerateWithModel(rawItems) {
  const apiKey = process.env.OPENAI_API_KEY || process.env.OPENROUTER_API_KEY;
  if (!apiKey) return null;

  const baseUrl = process.env.OPENAI_API_KEY
    ? (process.env.OPENAI_BASE_URL || 'https://api.openai.com/v1')
    : 'https://openrouter.ai/api/v1';
  const model = process.env.LLM_MODEL || (process.env.OPENAI_API_KEY ? 'gpt-4.1-mini' : 'openai/gpt-4.1-mini');

  const system = [
    '你是科技媒体的中文编辑。',
    '你的任务是把给定的 AI 新闻候选整理成一版中文日报。',
    '要求：',
    '1. 只写有事实依据的内容，不编造。',
    '2. 用词克制、准确、像专业记者，不要口号式表述。',
    '3. 删掉废话，不要出现“值得关注的是”“引发广泛关注”等空泛句式。',
    '4. 输出 JSON，不要输出 markdown。',
    '5. 生成 4 到 6 条最重要的新闻。',
    '5.1 尽量保证题材多样，不要让大多数新闻都来自同一家公司或同一类来源。',
    '6. 每条新闻必须包含：id、section、category、headline、deck、kicker、byline、publishedAt、updatedAt、readingTime、tags、summary(长度 2-3 段)、bullets(3 条)、significance、sources。',
    '7. section 只能使用 lead/company/policy/tools/impact 之一。',
    '8. 必须选择一条最适合头版 lead 的新闻，并在 edition.lead 中给出对应 id。'
  ].join('\n');

  const user = JSON.stringify({
    date: isoDate(),
    site: demoEdition.site,
    sections: demoEdition.sections,
    candidates: rawItems.filter((item) => !item.error).slice(0, 20)
  });

  const response = await fetch(`${baseUrl}/chat/completions`, {
    method: 'POST',
    headers: {
      'content-type': 'application/json',
      authorization: `Bearer ${apiKey}`,
      ...(process.env.OPENROUTER_API_KEY
        ? {
            'http-referer': process.env.SITE_BASE_URL || 'https://example.com',
            'x-title': 'AI Daily Ledger'
          }
        : {})
    },
    body: JSON.stringify({
      model,
      response_format: { type: 'json_object' },
      messages: [
        { role: 'system', content: system },
        { role: 'user', content: user }
      ],
      temperature: 0.4
    })
  });

  if (!response.ok) {
    throw new Error(`LLM request failed: ${response.status} ${await response.text()}`);
  }

  const payload = await response.json();
  const text = payload.choices?.[0]?.message?.content;
  if (!text) throw new Error('LLM returned empty content');

  const parsed = JSON.parse(text);
  const articles = (parsed.articles || [])
    .map((article, index) => ({
      id: article.id || slugify(article.headline || `story-${index + 1}`),
      section: article.section || 'company',
      category: article.category || '未分类',
      headline: article.headline || '',
      deck: article.deck || '',
      kicker: article.kicker || '日报',
      byline: article.byline || '编辑部整理',
      publishedAt: article.publishedAt || new Date().toISOString(),
      updatedAt: new Date().toISOString(),
      readingTime: article.readingTime || 3,
      tags: Array.isArray(article.tags) ? article.tags.slice(0, 6) : [],
      summary: Array.isArray(article.summary) ? article.summary.slice(0, 3) : [],
      bullets: Array.isArray(article.bullets) ? article.bullets.slice(0, 3) : [],
      significance: article.significance || '',
      sources: Array.isArray(article.sources) ? article.sources : []
    }))
    .filter((article) => article.headline && article.deck);

  if (articles.length === 0) {
    throw new Error('LLM returned no valid articles');
  }

  const leadFromModel = parsed.edition?.lead;
  const lead = articles.some((item) => item.id === leadFromModel) ? leadFromModel : articles[0].id;

  return {
    site: demoEdition.site,
    sections: demoEdition.sections,
    edition: {
      id: isoDate(),
      issueNumber: 1,
      date: isoDate(),
      displayDate: new Intl.DateTimeFormat('zh-CN', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        timeZone: 'UTC'
      }).format(new Date()),
      generatedAt: new Date().toISOString(),
      mode: 'llm',
      lead,
      editorNote: '本期由脚本抓取候选源后自动整理生成。'
    },
    articles
  };
}

async function main() {
  await ensureDirs();

  if (demoMode) {
    await writeJson(path.join(dataDir, 'issues.json'), demoEdition);
    await writeJson(path.join(dataDir, 'raw-feeds.json'), { generatedAt: new Date().toISOString(), mode: 'demo', items: [] });
    console.log('Wrote demo edition.');
    return;
  }

  const rawItems = await fetchFeeds();
  await writeJson(path.join(dataDir, 'raw-feeds.json'), {
    generatedAt: new Date().toISOString(),
    items: rawItems
  });

  let edition;
  try {
    edition = await maybeGenerateWithModel(rawItems);
  } catch (error) {
    console.warn('Model generation failed, fallback to demo edition:', error.message);
  }

  if (!edition) {
    edition = buildFallbackEdition(rawItems);
  }

  await writeJson(path.join(dataDir, 'issues.json'), edition);
  console.log(`Wrote edition in mode: ${edition.edition.mode}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
