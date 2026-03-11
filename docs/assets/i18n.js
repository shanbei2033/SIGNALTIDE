let currentLang = 'zh-CN';
const translations = {};
let languageSwitcherInitialized = false;

const SUPPORTED_LANGS = {
  'zh-CN': '简体中文',
  'zh-TW': '繁體中文',
  en: 'English',
  ja: '日本語',
  ko: '한국어',
  ru: 'Русский',
  fr: 'Français',
  es: 'Español'
};

function closeLanguageMenu() {
  document.querySelectorAll('.language-switcher').forEach((switcher) => {
    switcher.classList.remove('open');
  });
}

function renderLanguageSwitchers() {
  document.querySelectorAll('.language-switcher').forEach((container) => {
    container.innerHTML = `
      <button class="language-toggle" type="button" aria-label="切换语言" title="切换语言" aria-expanded="false">
        <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false" class="language-icon">
          <path d="M12 2a10 10 0 1 0 10 10A10 10 0 0 0 12 2Zm6.92 9h-3.05a15.6 15.6 0 0 0-1.38-5.03A8.03 8.03 0 0 1 18.92 11ZM12 4.04c.83 1.12 1.9 3.34 2.38 6.96H9.62C10.1 7.38 11.17 5.16 12 4.04ZM4.08 13h3.05a15.6 15.6 0 0 0 1.38 5.03A8.03 8.03 0 0 1 4.08 13Zm3.05-2H4.08a8.03 8.03 0 0 1 4.43-5.03A15.6 15.6 0 0 0 7.13 11Zm4.87 8.96c-.83-1.12-1.9-3.34-2.38-6.96h4.76c-.48 3.62-1.55 5.84-2.38 6.96ZM14.87 13h3.05a8.03 8.03 0 0 1-4.43 5.03A15.6 15.6 0 0 0 14.87 13Z" fill="currentColor"></path>
        </svg>
      </button>
      <div class="language-menu" role="menu" aria-label="语言列表">
        ${Object.entries(SUPPORTED_LANGS)
          .map(([lang, label]) => `<button class="lang-btn" type="button" role="menuitem" data-lang="${lang}">${label}</button>`)
          .join('')}
      </div>
    `;
  });
}

async function loadLanguage(lang) {
  if (translations[lang]) return translations[lang];
  const response = await fetch(`./locales/${lang}.json?v=20260311d`);
  if (!response.ok) {
    if (lang !== 'zh-CN') return loadLanguage('zh-CN');
    throw new Error(`Failed to load locale: ${lang}`);
  }
  translations[lang] = await response.json();
  return translations[lang];
}

async function initLanguage() {
  const saved = localStorage.getItem('aiNewsLang');
  if (saved && SUPPORTED_LANGS[saved]) {
    currentLang = saved;
  } else {
    const browserLang = navigator.language || 'zh-CN';
    if (browserLang.startsWith('zh')) {
      currentLang = browserLang.includes('TW') || browserLang.includes('HK') ? 'zh-TW' : 'zh-CN';
    } else if (SUPPORTED_LANGS[browserLang]) {
      currentLang = browserLang;
    } else {
      currentLang = 'zh-CN';
    }
  }

  await loadLanguage(currentLang);
  document.documentElement.lang = currentLang;
  renderLanguageSwitchers();
  updateLanguageButtons();
  return currentLang;
}

function deepGet(obj, path) {
  return path.split('.').reduce((acc, key) => (acc && acc[key] !== undefined ? acc[key] : undefined), obj);
}

function t(key, params = {}) {
  const value = deepGet(translations[currentLang], key) ?? deepGet(translations['zh-CN'], key) ?? key;
  if (typeof value !== 'string') return value;
  return value.replace(/\{(\w+)\}/g, (_, name) => params[name] ?? `{${name}}`);
}

function getCurrentLanguage() {
  return currentLang;
}

async function switchLanguage(lang) {
  if (!SUPPORTED_LANGS[lang] || lang === currentLang) return;
  await loadLanguage(lang);
  currentLang = lang;
  localStorage.setItem('aiNewsLang', lang);
  document.documentElement.lang = lang;
  updateLanguageButtons();
  updatePageLanguage();
  closeLanguageMenu();
  window.dispatchEvent(new CustomEvent('ai-news-languagechange', { detail: { lang } }));
}

function updateLanguageButtons() {
  document.querySelectorAll('.lang-btn').forEach((btn) => {
    btn.classList.toggle('active', btn.dataset.lang === currentLang);
  });
  document.querySelectorAll('.language-toggle').forEach((btn) => {
    btn.setAttribute('title', `切换语言：${SUPPORTED_LANGS[currentLang] || currentLang}`);
    btn.setAttribute('aria-label', `切换语言：${SUPPORTED_LANGS[currentLang] || currentLang}`);
  });
}

function initLanguageEvents() {
  if (languageSwitcherInitialized) {
    updateLanguageButtons();
    return;
  }

  document.addEventListener('click', (event) => {
    const toggle = event.target.closest('.language-toggle');
    const switcher = event.target.closest('.language-switcher');

    if (toggle && switcher) {
      const willOpen = !switcher.classList.contains('open');
      closeLanguageMenu();
      switcher.classList.toggle('open', willOpen);
      const button = switcher.querySelector('.language-toggle');
      if (button) button.setAttribute('aria-expanded', willOpen ? 'true' : 'false');
      return;
    }

    const langBtn = event.target.closest('.lang-btn');
    if (langBtn) {
      switchLanguage(langBtn.dataset.lang);
      return;
    }

    if (!switcher) {
      closeLanguageMenu();
      document.querySelectorAll('.language-toggle').forEach((btn) => btn.setAttribute('aria-expanded', 'false'));
    }
  });

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      closeLanguageMenu();
      document.querySelectorAll('.language-toggle').forEach((btn) => btn.setAttribute('aria-expanded', 'false'));
    }
  });

  languageSwitcherInitialized = true;
  updateLanguageButtons();
}

function updatePageLanguage() {
  document.querySelectorAll('[data-i18n-key]').forEach((node) => {
    const key = node.getAttribute('data-i18n-key');
    const text = t(key);
    if (node.tagName === 'SECTION' || node.tagName === 'ASIDE') {
      node.setAttribute('aria-label', text);
    } else {
      node.textContent = text;
    }
  });
}

function formatEditionDate(dateStr, lang = currentLang) {
  const date = new Date(`${dateStr}T00:00:00Z`);
  if (lang === 'zh-CN') return `${date.getUTCFullYear()}年${date.getUTCMonth() + 1}月${date.getUTCDate()}日`;
  if (lang === 'zh-TW') return `${date.getUTCFullYear()}年${date.getUTCMonth() + 1}月${date.getUTCDate()}日`;
  return new Intl.DateTimeFormat(lang, {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    timeZone: 'UTC'
  }).format(date);
}

function formatDateTime(dateInput, lang = currentLang) {
  const date = new Date(dateInput);
  if (lang === 'zh-CN' || lang === 'zh-TW') {
    return new Intl.DateTimeFormat(lang, {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      timeZone: 'UTC'
    }).format(date);
  }
  return new Intl.DateTimeFormat(lang, {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    timeZone: 'UTC'
  }).format(date);
}

export {
  SUPPORTED_LANGS,
  formatDateTime,
  formatEditionDate,
  getCurrentLanguage,
  initLanguage,
  initLanguageEvents,
  switchLanguage,
  t,
  updateLanguageButtons,
  updatePageLanguage
};
