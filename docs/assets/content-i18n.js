function pickLocalizedValue(value, lang) {
  if (value == null) return value;
  if (Array.isArray(value)) return value;
  if (typeof value !== 'object') return value;
  return value[lang] ?? value['zh-CN'] ?? Object.values(value)[0] ?? '';
}

function localizeSource(source, lang) {
  if (!source) return source;
  return {
    ...source,
    title: pickLocalizedValue(source.title, lang) ?? source.title,
    publication: pickLocalizedValue(source.publication, lang) ?? source.publication
  };
}

function localizeArray(values, lang) {
  if (!Array.isArray(values)) return values;
  return values.map((value) => pickLocalizedValue(value, lang) ?? value).filter(Boolean);
}

export function localizeArticle(article, lang) {
  if (!article || !lang) return article;
  const localized = article.i18n?.[lang] || {};

  return {
    ...article,
    kicker: localized.kicker ?? pickLocalizedValue(article.kicker, lang) ?? article.kicker,
    category: localized.category ?? pickLocalizedValue(article.category, lang) ?? article.category,
    headline: localized.headline ?? pickLocalizedValue(article.headline, lang) ?? article.headline,
    deck: localized.deck ?? pickLocalizedValue(article.deck, lang) ?? article.deck,
    byline: localized.byline ?? pickLocalizedValue(article.byline, lang) ?? article.byline,
    significance: localized.significance ?? pickLocalizedValue(article.significance, lang) ?? article.significance,
    tags: Array.isArray(localized.tags) ? localized.tags : localizeArray(article.tags, lang),
    summary: Array.isArray(localized.summary) ? localized.summary : localizeArray(article.summary, lang),
    bullets: Array.isArray(localized.bullets) ? localized.bullets : localizeArray(article.bullets, lang),
    sources: (Array.isArray(localized.sources) ? localized.sources : article.sources || []).map((source) => localizeSource(source, lang))
  };
}

export function localizeEdition(rawData, lang) {
  const siteI18n = rawData?.site?.i18n?.[lang] || {};
  const editionI18n = rawData?.edition?.i18n?.[lang] || {};

  return {
    ...rawData,
    site: {
      ...rawData.site,
      name: siteI18n.name ?? pickLocalizedValue(rawData.site?.name, lang) ?? rawData.site?.name,
      tagline: siteI18n.tagline ?? pickLocalizedValue(rawData.site?.tagline, lang) ?? rawData.site?.tagline,
      description: siteI18n.description ?? pickLocalizedValue(rawData.site?.description, lang) ?? rawData.site?.description
    },
    edition: {
      ...rawData.edition,
      editorNote: editionI18n.editorNote ?? pickLocalizedValue(rawData.edition?.editorNote, lang) ?? rawData.edition?.editorNote ?? ''
    },
    sections: (rawData.sections || []).map((section) => {
      const sectionI18n = section?.i18n?.[lang] || {};
      return {
        ...section,
        label: sectionI18n.label ?? pickLocalizedValue(section.label, lang) ?? section.label
      };
    }),
    articles: (rawData.articles || []).map((article) => localizeArticle(article, lang))
  };
}
