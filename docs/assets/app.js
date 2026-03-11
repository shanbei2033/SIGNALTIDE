import {
  formatEditionDate,
  getCurrentLanguage,
  initLanguage,
  initLanguageEvents,
  t,
  updatePageLanguage
} from './i18n.js?v=20260311d';
import { localizeEdition } from './content-i18n.js?v=20260311d';

const dataUrl = './data/issues.json';
const rssUrl = new URL('./rss.xml', window.location.href).href;
let latestData = null;

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

function articleHref(id) {
  return `./article.html?id=${encodeURIComponent(id)}`;
}

function articleParagraphs(article, maxParagraphs = 5) {
  const paragraphs = [article.deck, ...(article.summary || []), article.significance].filter(Boolean);
  return paragraphs.slice(0, maxParagraphs);
}

function impactScore(article, leadId) {
  const sectionWeight = { lead: 100, policy: 85, company: 78, tools: 72, impact: 68 };
  const summaryWeight = Math.min((article.summary || []).length * 4, 12);
  const sourceWeight = Math.min((article.sources || []).length * 3, 9);
  const leadBoost = article.id === leadId ? 1000 : 0;
  return leadBoost + (sectionWeight[article.section] || 50) + summaryWeight + sourceWeight;
}

function localizedData(rawData) {
  const lang = getCurrentLanguage();
  const localized = localizeEdition(rawData, lang);
  return {
    ...localized,
    site: {
      ...localized.site,
      name: t('site.name'),
      tagline: t('site.tagline')
    },
    edition: {
      ...localized.edition,
      displayDate: formatEditionDate(rawData.edition.date, lang),
      editorNote: localized.edition?.editorNote || ''
    }
  };
}

function renderLead(container, article) {
  const link = document.createElement('a');
  link.href = articleHref(article.id);
  link.className = 'lead-link';
  link.setAttribute('aria-labelledby', 'leadTitle');

  const articleEl = el('article', 'lead-article');
  const meta = el('div', 'story-header');
  meta.append(el('p', 'story-kicker', article.kicker || t('ui.lead')));
  meta.append(el('p', 'story-category', article.category || ''));

  const title = el('h2', null, article.headline);
  title.id = 'leadTitle';

  const body = el('div', 'lead-body');
  for (const paragraph of articleParagraphs(article, 5)) {
    body.append(el('p', null, paragraph));
  }

  articleEl.append(meta, title, body);
  link.append(articleEl);
  container.replaceChildren(link);
}

function renderSecondary(container, articles) {
  container.innerHTML = '';
  container.append(el('div', 'section-label', t('ui.secondary')));

  const grid = el('div', 'secondary-grid');
  for (const article of articles.slice(0, 4)) {
    const story = el('article', 'secondary-story');
    const link = document.createElement('a');
    link.className = 'secondary-link';
    link.href = articleHref(article.id);

    link.append(el('p', 'story-kicker', article.kicker || article.category || ''));
    link.append(el('h2', 'story-title', article.headline));

    const body = el('div', 'story-body');
    for (const paragraph of articleParagraphs(article, 2)) {
      body.append(el('p', null, paragraph));
    }
    link.append(body);
    story.append(link);
    grid.append(story);
  }

  container.append(grid);
}

function renderInfoRail(container, articles) {
  container.innerHTML = '';
  container.append(el('div', 'section-label', t('ui.info')));

  const list = el('div', 'info-list');
  for (const article of articles.slice(0, 4)) {
    const item = el('article', 'info-item');
    const title = document.createElement('a');
    title.href = articleHref(article.id);
    title.className = 'info-link';
    title.textContent = article.headline;
    item.append(title);

    const body = el('div', 'info-body');
    for (const paragraph of articleParagraphs(article, 2)) {
      body.append(el('p', null, paragraph));
    }
    item.append(body);
    list.append(item);
  }

  container.append(list);
}

function renderEditorRail(container) {
  container.innerHTML = '';
  container.append(el('div', 'section-label', t('ui.projects')));

  const projects = [
    { key: 'promptfoo', url: 'https://github.com/promptfoo/promptfoo' },
    { key: 'openhands', url: 'https://github.com/All-Hands-AI/OpenHands' },
    { key: 'continue', url: 'https://github.com/continuedev/continue' },
    { key: 'langfuse', url: 'https://github.com/langfuse/langfuse' }
  ];

  for (const project of projects) {
    const item = el('article', 'editor-project');
    const title = document.createElement('a');
    title.href = project.url;
    title.target = '_blank';
    title.rel = 'noreferrer noopener';
    title.className = 'editor-project-link';
    title.textContent = t(`projects.${project.key}.name`);

    const name = el('p', 'editor-project-name');
    name.append(title);
    item.append(name);
    item.append(el('p', 'editor-project-note', t(`projects.${project.key}.note`)));
    container.append(item);
  }
}

function renderPage(rawData) {
  const data = localizedData(rawData);
  const articles = data.articles;
  const lead = articles.find((article) => article.id === data.edition.lead) || articles[0];
  const ranked = [...articles]
    .filter((article) => article.id !== lead.id)
    .sort((a, b) => impactScore(b, lead.id) - impactScore(a, lead.id));

  const secondary = ranked.slice(0, 4);
  const info = [...secondary, ...ranked.slice(4)].slice(0, 4);

  document.title = `${data.site.name} · ${data.edition.displayDate}`;
  document.querySelector('#siteName').textContent = data.site.name;
  document.querySelector('#editionDate').textContent = data.edition.displayDate;
  document.querySelector('#tagline').textContent = data.site.tagline;
  document.querySelector('#editorNote').textContent = data.edition.editorNote;

  renderLead(document.querySelector('#leadStory'), lead);
  renderSecondary(document.querySelector('#secondaryStories'), secondary);
  renderInfoRail(document.querySelector('#infoRail'), info);
  renderEditorRail(document.querySelector('#editorRail'));
  updatePageLanguage();
}

async function main() {
  await initLanguage();
  initLanguageEvents();
  initRssAction();
  updatePageLanguage();

  const response = await fetch(dataUrl, { cache: 'no-store' });
  if (!response.ok) throw new Error(t('ui.failed'));

  const data = await response.json();
  if (!data?.site || !data?.edition || !Array.isArray(data?.articles) || data.articles.length === 0) {
    throw new Error('Invalid edition data');
  }

  latestData = data;
  renderPage(latestData);

  window.addEventListener('ai-news-languagechange', () => {
    if (latestData) renderPage(latestData);
  });
}

main().catch((error) => {
  console.error(error);
  const tagline = document.querySelector('#tagline');
  const editorNote = document.querySelector('#editorNote');
  const leadStory = document.querySelector('#leadStory');
  if (tagline) tagline.textContent = t('ui.failed');
  if (editorNote) editorNote.textContent = String(error?.message || error);
  if (leadStory) leadStory.innerHTML = `<div class="not-found">${t('ui.failed')}</div>`;
});
