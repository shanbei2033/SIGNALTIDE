function normalizeHeadline(value) {
  if (!value) return '未命名期刊';
  if (typeof value === 'string') return value;
  return value['zh-CN'] || value['zh-TW'] || value.en || Object.values(value)[0] || '未命名期刊';
}

async function main() {
  const list = document.querySelector('#archiveList');
  const template = document.querySelector('#archiveCardTemplate');

  try {
    const response = await fetch('./data/archive/index.json', { cache: 'no-store' });
    if (!response.ok) throw new Error('无法读取归档索引');
    const data = await response.json();

    if (!Array.isArray(data.items) || data.items.length === 0) {
      list.innerHTML = '<div class="panel-card block archive-empty">当前还没有可显示的归档。</div>';
      return;
    }

    list.innerHTML = '';
    for (const item of data.items) {
      const fragment = template.content.cloneNode(true);
      fragment.querySelector('.archive-date').textContent = item.displayDate || item.date;
      fragment.querySelector('.archive-count').textContent = `${item.articleCount || 0} 篇`;
      fragment.querySelector('.archive-title').textContent = normalizeHeadline(item.leadHeadline);
      fragment.querySelector('.archive-note').textContent = item.note || '查看这一天的完整版面和归档数据。';
      fragment.querySelector('.archive-open').href = `./edition.html?date=${encodeURIComponent(item.date)}`;
      fragment.querySelector('.archive-json').href = `./data/archive/${encodeURIComponent(item.date)}.json`;
      list.append(fragment);
    }
  } catch (error) {
    console.error(error);
    list.innerHTML = `<div class="panel-card block archive-empty">归档列表加载失败：${String(error.message || error)}</div>`;
  }
}

main();
