import fs from 'node:fs/promises';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const root = path.resolve(process.cwd());
const docsDir = path.join(root, 'docs');
const issuesPath = path.join(docsDir, 'data', 'issues.json');
const contentI18nPath = path.join(docsDir, 'assets', 'content-i18n.js');

const issues = JSON.parse(await fs.readFile(issuesPath, 'utf8'));
const mod = await import(pathToFileURL(contentI18nPath).href + `?t=${Date.now()}`);
const translations = mod.CONTENT_TRANSLATIONS || {};

issues.site.i18n ||= {};
issues.edition.i18n ||= {};
for (const section of issues.sections || []) section.i18n ||= {};

for (const [lang, bundle] of Object.entries(translations)) {
  if (bundle.editorNote) {
    issues.edition.i18n[lang] ||= {};
    issues.edition.i18n[lang].editorNote = '';
  }

  for (const article of issues.articles || []) {
    const localized = bundle.articles?.[article.id];
    if (!localized) continue;
    article.i18n ||= {};
    article.i18n[lang] = {
      kicker: localized.kicker ?? article.kicker,
      category: localized.category ?? article.category,
      headline: localized.headline ?? article.headline,
      deck: localized.deck ?? article.deck,
      byline: localized.byline ?? article.byline,
      summary: localized.summary ?? article.summary,
      bullets: localized.bullets ?? article.bullets,
      significance: localized.significance ?? article.significance,
      tags: localized.tags ?? article.tags,
      sources: localized.sources ?? article.sources
    };
  }
}

await fs.writeFile(issuesPath, JSON.stringify(issues, null, 2) + '\n', 'utf8');
console.log(`Migrated article translations into ${issuesPath}`);
