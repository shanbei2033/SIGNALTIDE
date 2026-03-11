import {
  formatDateTime,
  formatEditionDate,
  getCurrentLanguage,
  initLanguage,
  initLanguageEvents,
  t,
  updatePageLanguage
} from './i18n.js?v=20260311d';
import { localizeArticle } from './content-i18n.js?v=20260311d';

const dataUrl = './data/issues.json';
const rssUrl = new URL('./rss.xml', window.location.href).href;
let latestData = null;
let currentArticleId = null;

function initRssAction() {
  const button = document.querySelector('#rssAction');
  if (!button) return;
  button.addEventListener('click', async () => {
    try {
      if (navigator.clipboard?.writeText) {
        await navigator.clipboard.writeText(rssUrl);
      }
    } catch (error) {
      console.warn('Failed to copy RSS URL:', error);
    }
    window.location.href = rssUrl;
  });
}

function el(tag, className, text) {
  const node = document.createElement(tag);
  if (className) node.className = className;
  if (text) node.textContent = text;
  return node;
}

function queryId() {
  return new URL(window.location.href).searchParams.get('id');
}

function articleParagraphs(article) {
  return [article.deck, ...(article.summary || []), article.significance].filter(Boolean);
}

function localizedArticle(rawArticle) {
  return localizeArticle(rawArticle, getCurrentLanguage());
}

function renderArticle(root, rawArticle, edition) {
  const article = localizedArticle(rawArticle);
  const template = document.querySelector('#articleTemplate');
  const fragment = template.content.cloneNode(true);

  fragment.querySelector('.article-kicker').textContent = article.kicker || '';
  fragment.querySelector('.article-title').textContent = article.headline;

  const reading = fragment.querySelector('.article-reading');
  reading.dataset.readingMinutes = article.readingTime || 3;
  reading.textContent = t('ui.readingTime', { minutes: article.readingTime || 3 });

  fragment.querySelector('.article-deck').textContent = article.deck || '';

  const summary = fragment.querySelector('.article-summary');
  for (const paragraph of articleParagraphs(article)) {
    summary.append(el('p', null, paragraph));
  }

  const sources = fragment.querySelector('.article-sources');
  for (const source of article.sources || []) {
    const li = document.createElement('li');
    const a = document.createElement('a');
    a.href = source.url;
    a.target = '_blank';
    a.rel = 'noreferrer noopener';
    a.textContent = `${source.publication}｜${source.title}`;
    li.append(a);
    sources.append(li);
  }

  const tags = el('div', 'tags');
  for (const tag of article.tags || []) {
    tags.append(el('span', 'tag', tag));
  }
  fragment.querySelector('.article-main').append(tags);

  const displayDate = formatEditionDate(edition.date, getCurrentLanguage());
  document.querySelector('#articleDate').textContent = `${displayDate} · ${t('ui.date', { date: formatDateTime(article.updatedAt || edition.generatedAt) })}`;
  document.title = `${article.headline} · ${displayDate}`;

  root.replaceChildren(fragment);
  updatePageLanguage();
}

function rerender() {
  if (!latestData || !currentArticleId) return;
  const article = latestData.articles.find((item) => item.id === currentArticleId);
  if (!article) return;
  renderArticle(document.querySelector('#articleRoot'), article, latestData.edition);
}

async function main() {
  await initLanguage();
  initLanguageEvents();
  initRssAction();
  updatePageLanguage();

  currentArticleId = queryId();
  const response = await fetch(dataUrl, { cache: 'no-store' });
  if (!response.ok) {
    throw new Error(t('ui.failed'));
  }

  latestData = await response.json();
  const article = latestData.articles.find((item) => item.id === currentArticleId);

  if (!article) {
    document.querySelector('#articleDate').textContent = formatEditionDate(latestData.edition.date, getCurrentLanguage());
    document.querySelector('#articleRoot').innerHTML = `<div class="block not-found">${t('ui.notFound')}</div>`;
    return;
  }

  rerender();
  window.addEventListener('ai-news-languagechange', rerender);
}

main().catch((error) => {
  console.error(error);
  document.querySelector('#articleRoot').innerHTML = `<div class="block not-found">${t('ui.failed')}：${String(error?.message || error)}</div>`;
});
