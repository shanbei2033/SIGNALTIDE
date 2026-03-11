import fs from 'node:fs/promises';
import path from 'node:path';
import Parser from 'rss-parser';
import { FEED_SOURCES } from './feed-sources.mjs';

const root = path.resolve(process.cwd());
const docsDir = path.join(root, 'docs');
const dataDir = path.join(docsDir, 'data');
const archiveDir = path.join(dataDir, 'archive');

const parser = new Parser({
  timeout: 20000,
  headers: {
    'user-agent': 'Mozilla/5.0 (compatible; Signal Tide Editor/1.0; +https://github.com/)'
  }
});

const SOURCES = FEED_SOURCES;

const LANGS = ['zh-CN', 'zh-TW', 'en', 'ja', 'ko', 'ru', 'fr', 'es'];

function isoDate(value = new Date()) {
  return new Date(value).toISOString().slice(0, 10);
}

function stripHtml(input = '') {
  return input
    .replace(/<[^>]*>/g, ' ')
    .replace(/&nbsp;/g, ' ')
    .replace(/&amp;/g, '&')
    .replace(/\s+/g, ' ')
    .trim();
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

async function ensureDirs() {
  await fs.mkdir(dataDir, { recursive: true });
  await fs.mkdir(archiveDir, { recursive: true });
}

async function writeJson(file, data) {
  await fs.writeFile(file, JSON.stringify(data, null, 2) + '\n', 'utf8');
}

async function writeText(file, text) {
  await fs.writeFile(file, text, 'utf8');
}

function escapeXml(value = '') {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

function articleUrl(article) {
  const base = (process.env.SITE_BASE_URL || 'https://example.com').replace(/\/$/, '');
  return `${base}/article.html?id=${encodeURIComponent(article.id)}`;
}

function renderRss(edition) {
  const base = (process.env.SITE_BASE_URL || 'https://example.com').replace(/\/$/, '');
  const siteTitle = '智潮 / Signal Tide';
  const siteDescription = edition?.site?.description || 'AI daily edition';
  const buildDate = new Date(edition?.edition?.generatedAt || Date.now()).toUTCString();
  const items = (edition.articles || []).map((article) => {
    const title = article.i18n?.['zh-TW']?.headline || article.headline || '';
    const description = [article.deck, ...(article.summary || []), article.significance].filter(Boolean).join('\n\n');
    const pubDate = new Date(article.updatedAt || article.publishedAt || edition?.edition?.generatedAt || Date.now()).toUTCString();
    const link = articleUrl(article);
    return `    <item>\n      <title>${escapeXml(title)}</title>\n      <link>${escapeXml(link)}</link>\n      <guid>${escapeXml(link)}</guid>\n      <pubDate>${escapeXml(pubDate)}</pubDate>\n      <description>${escapeXml(description)}</description>\n    </item>`;
  }).join('\n');

  return `<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0">\n  <channel>\n    <title>${escapeXml(siteTitle)}</title>\n    <link>${escapeXml(base + '/')}</link>\n    <description>${escapeXml(siteDescription)}</description>\n    <language>zh-CN</language>\n    <lastBuildDate>${escapeXml(buildDate)}</lastBuildDate>\n${items}\n  </channel>\n</rss>\n`;
}

async function fetchFeeds() {
  const items = [];
  for (const source of SOURCES) {
    try {
      const feed = await parser.parseURL(source.url);
      for (const item of (feed.items || []).slice(0, 12)) {
        items.push({
          source: source.name,
          sourceType: source.type || 'general',
          feedTitle: feed.title || source.name,
          title: item.title || '',
          link: item.link || '',
          publishedAt: item.isoDate || item.pubDate || null,
          contentSnippet: stripHtml(item.contentSnippet || item.content || item.summary || item['content:encoded'] || ''),
          categories: item.categories || []
        });
      }
    } catch (error) {
      items.push({ source: source.name, sourceType: source.type || 'general', error: String(error) });
    }
  }
  return dedupeItems(items);
}

function buildPrompt(rawItems) {
  return [
    '你是“Signal Tide / 智潮”的主编。',
    '目标：根据给定 AI 新闻候选，手工编辑式地筛选、重写、翻译，生成一个适用于纯静态新闻网站的 issues.json。',
    '严格要求：',
    '1. 只使用候选里有依据的信息，不编造事实。',
    '2. 你不是摘要器，而是编辑：要挑选最重要的 4-6 条，按轻重排序。',
    '2.1 尽量保证题材多样，不要让 4-6 条里大部分都来自同一家公司或同一类型来源。优先覆盖公司产品、研究、开源工具、政策治理、产业影响等不同面向。',
    '3. 用自己的语言重写，语气克制、像科技媒体，不要空话套话。',
    '4. 每篇新闻正文 summary 必须是 2-3 段自然段，不要列表腔。',
    '5. 输出必须是 JSON 对象，不要 markdown。',
    '6. issues.json 必须是纯静态站可直接消费的数据：文章多语言内容写进 JSON 本身。',
    '7. 顶层结构必须包含 site、edition、sections、articles。',
    '8. article 基础字段至少包含 id、section、headline、deck、kicker、category、byline、publishedAt、updatedAt、readingTime、tags、summary、significance、sources。',
    `9. 每篇 article 必须包含 i18n，至少覆盖这些语言：${LANGS.join(', ')}。`,
    '10. i18n 里的每个语言对象必须包含 headline、deck、kicker、category、summary、significance；可选 byline、tags、sources。',
    '11. UI 文案（站点名、tagline、栏目标签、按钮文案）可以放在 site/edition/sections 的 i18n 或 locales 文件里；文章正文翻译必须写在 article.i18n 里。',
    '12. edition.lead 必须指向最重要的一条。',
    '13. sections 使用 lead/company/policy/tools/impact。',
    '14. 所有 sources 必须保留 publication、title、url。',
    '',
    JSON.stringify({
      date: isoDate(),
      site: {
        name: 'Signal Tide',
        tagline: '由 openclaw 驱动的 AI 日报',
        description: '聚合、重写并归档每日 AI 领域的重要新闻。'
      },
      sections: [
        { key: 'lead', label: '头版' },
        { key: 'company', label: '公司与产品' },
        { key: 'policy', label: '政策与治理' },
        { key: 'tools', label: '开发工具' },
        { key: 'impact', label: '应用与影响' }
      ],
      candidates: rawItems.filter((item) => !item.error).slice(0, 60)
    })
  ].join('\n');
}

function currentEditionPath() {
  return path.join(dataDir, 'issues.json');
}

async function loadCurrentEdition() {
  try {
    const text = await fs.readFile(currentEditionPath(), 'utf8');
    return JSON.parse(text);
  } catch {
    return null;
  }
}

async function main() {
  await ensureDirs();
  const rawItems = await fetchFeeds();

  await writeJson(path.join(dataDir, 'raw-feeds.json'), {
    generatedAt: new Date().toISOString(),
    items: rawItems
  });

  if (process.argv.includes('--fetch-only')) {
    console.log(`Fetched ${rawItems.filter((item) => !item.error).length} candidate items.`);
    return;
  }

  const edition = await loadCurrentEdition();
  if (edition) {
    await writeJson(path.join(archiveDir, `${edition.edition?.date || isoDate()}.json`), edition);
    await writeText(path.join(docsDir, 'rss.xml'), renderRss(edition));
    console.log('Refreshed archive and rss.xml from current issues.json');
    console.log('Next step: let openclaw write a new issues.json from raw-feeds.json');
    return;
  }

  throw new Error('No existing issues.json found. Fetch completed, but a new edition must be written by openclaw into docs/data/issues.json.');
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
