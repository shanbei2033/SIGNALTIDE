export const FEED_SOURCES = [
  // Official / labs
  { name: 'OpenAI', type: 'official', url: 'https://openai.com/news/rss.xml' },
  { name: 'Anthropic', type: 'official', url: 'https://www.anthropic.com/news/rss.xml' },
  { name: 'Google AI Blog', type: 'official', url: 'https://blog.google/technology/ai/rss/' },
  { name: 'Google DeepMind', type: 'official', url: 'https://deepmind.google/blog/rss.xml' },
  { name: 'Meta AI', type: 'official', url: 'https://ai.meta.com/blog/rss/' },
  { name: 'Hugging Face Blog', type: 'official', url: 'https://huggingface.co/blog/feed.xml' },
  { name: 'Mistral AI', type: 'official', url: 'https://mistral.ai/news/rss.xml' },
  { name: 'Cohere', type: 'official', url: 'https://cohere.com/blog/rss.xml' },
  { name: 'NVIDIA Blog', type: 'official', url: 'https://blogs.nvidia.com/blog/category/ai/feed/' },
  { name: 'Microsoft Research', type: 'official', url: 'https://www.microsoft.com/en-us/research/feed/' },

  // Media
  { name: 'TechCrunch AI', type: 'media', url: 'https://techcrunch.com/category/artificial-intelligence/feed/' },
  { name: 'The Verge AI', type: 'media', url: 'https://www.theverge.com/rss/ai-artificial-intelligence/index.xml' },
  { name: 'Ars Technica AI', type: 'media', url: 'https://feeds.arstechnica.com/arstechnica/technology-lab' },
  { name: 'VentureBeat AI', type: 'media', url: 'https://venturebeat.com/ai/feed/' },
  { name: 'MIT Technology Review AI', type: 'media', url: 'https://www.technologyreview.com/topic/artificial-intelligence/feed/' },
  { name: 'Wired Business', type: 'media', url: 'https://www.wired.com/feed/category/business/latest/rss' },

  // Research / papers
  { name: 'arXiv AI', type: 'research', url: 'https://rss.arxiv.org/rss/cs.AI' },
  { name: 'arXiv CL', type: 'research', url: 'https://rss.arxiv.org/rss/cs.CL' },
  { name: 'arXiv ML', type: 'research', url: 'https://rss.arxiv.org/rss/cs.LG' },
  { name: 'Google Research', type: 'research', url: 'https://research.google/blog/rss/' },

  // Open-source / developer ecosystem
  { name: 'Ollama Blog', type: 'opensource', url: 'https://ollama.com/blog/rss.xml' },
  { name: 'LangChain Blog', type: 'opensource', url: 'https://blog.langchain.dev/rss/' },
  { name: 'LlamaIndex Blog', type: 'opensource', url: 'https://www.llamaindex.ai/blog/rss.xml' },
  { name: 'Replicate Blog', type: 'opensource', url: 'https://replicate.com/blog/rss.xml' },
  { name: 'Modal Blog', type: 'opensource', url: 'https://modal.com/blog/rss.xml' },
  { name: 'Vercel Blog AI', type: 'opensource', url: 'https://vercel.com/blog/rss.xml' },

  // Policy / governance / security
  { name: 'NIST News', type: 'policy', url: 'https://www.nist.gov/news-events/news/rss.xml' },
  { name: 'UK AISI', type: 'policy', url: 'https://www.aisi.gov.uk/feed' },
  { name: 'OECD AI', type: 'policy', url: 'https://oecd.ai/en/rss' },
  { name: 'EFF Deeplinks', type: 'policy', url: 'https://www.eff.org/rss/updates.xml' }
];
