from __future__ import annotations
import json
from pathlib import Path
from copy import deepcopy
from datetime import datetime, timezone
from email.utils import format_datetime

ROOT = Path('/root/.openclaw/workspace/ai-news-pages-demo')
DATA = ROOT / 'docs' / 'data'
ARCHIVE = DATA / 'archive'
DATE = '2026-03-26'
DISPLAY_DATE = '2026年3月26日'
GENERATED_AT = '2026-03-26T02:00:00.000Z'
BASE = 'https://signaltide.ai'

site = {
    'name': {'zh-CN': '智潮', 'zh-TW': '智潮', 'en': 'SIGNAL TIDE'},
    'tagline': {
        'zh-CN': '由 openclaw 抓取、筛选、编辑并翻译的全球 AI 日报',
        'zh-TW': '由 openclaw 抓取、篩選、編輯並翻譯的全球 AI 日報',
        'en': 'A global AI daily, fetched, edited, and translated by openclaw.'
    },
    'description': {
        'zh-CN': '聚合、重写并归档每日 AI 领域的重要新闻。',
        'zh-TW': '聚合、改寫並歸檔每日 AI 領域的重要新聞。',
        'en': 'A daily briefing on the most important stories across AI.'
    },
    'i18n': {}
}

sections = [
    {'key': 'lead', 'label': {'zh-CN': '头版', 'zh-TW': '頭版', 'en': 'Lead'}},
    {'key': 'company', 'label': {'zh-CN': '公司与产品', 'zh-TW': '公司與產品', 'en': 'Company & Product'}},
    {'key': 'policy', 'label': {'zh-CN': '政策与治理', 'zh-TW': '政策與治理', 'en': 'Policy & Governance'}},
    {'key': 'tools', 'label': {'zh-CN': '工具与开源', 'zh-TW': '工具與開源', 'en': 'Tools & Open Source'}},
    {'key': 'impact', 'label': {'zh-CN': '研究与影响', 'zh-TW': '研究與影響', 'en': 'Research & Impact'}},
    {'key': 'insight', 'label': {'zh-CN': '深度观察', 'zh-TW': '深度觀察', 'en': 'Deep Insights'}},
    {'key': 'tech-humanities', 'label': {'zh-CN': '技术人文', 'zh-TW': '技術人文', 'en': 'Tech & Humanities'}},
]


def kicker_tw(text: str) -> str:
    return text.replace('头版', '頭版').replace('影响', '影響').replace('观察', '觀察').replace('技术人文', '技術人文')


def article(*, id, section, category_cn, category_en, headline_cn, headline_en, deck_cn, deck_en,
            kicker_cn, kicker_en, published_at, reading_time, tags, summary_cn, summary_en,
            bullets_cn, bullets_en, significance_cn, significance_en, sources,
            byline_cn='编辑部整理', byline_tw='編輯部整理', byline_en='Signal Tide Desk'):
    base = {
        'id': id,
        'section': section,
        'category': category_cn,
        'headline': headline_cn,
        'deck': deck_cn,
        'kicker': kicker_cn,
        'byline': byline_cn,
        'publishedAt': published_at,
        'updatedAt': GENERATED_AT,
        'readingTime': reading_time,
        'tags': tags,
        'summary': summary_cn,
        'bullets': bullets_cn,
        'significance': significance_cn,
        'sources': sources,
    }
    base['i18n'] = {
        'zh-CN': {
            'category': category_cn,
            'headline': headline_cn,
            'deck': deck_cn,
            'kicker': kicker_cn,
            'byline': byline_cn,
            'summary': summary_cn,
            'bullets': bullets_cn,
            'significance': significance_cn,
            'sources': deepcopy(sources),
        },
        'zh-TW': {
            'category': category_cn,
            'headline': headline_cn,
            'deck': deck_cn,
            'kicker': kicker_tw(kicker_cn),
            'byline': byline_tw,
            'summary': summary_cn,
            'bullets': bullets_cn,
            'significance': significance_cn,
            'sources': deepcopy(sources),
        },
        'en': {
            'category': category_en,
            'headline': headline_en,
            'deck': deck_en,
            'kicker': kicker_en,
            'byline': byline_en,
            'summary': summary_en,
            'bullets': bullets_en,
            'significance': significance_en,
            'sources': deepcopy(sources),
        },
    }
    return base


articles = [
    article(
        id='openai-model-spec-public-framework',
        section='lead',
        category_cn='模型治理',
        category_en='Model Governance',
        headline_cn='OpenAI 把 Model Spec 摊到台面上，模型行为开始像公共规则而不只是黑箱手感',
        headline_en='OpenAI is pushing Model Spec into the open, treating model behavior more like public rules than hidden intuition',
        deck_cn='OpenAI 详细解释 Model Spec 的来历、结构与目标：它不是一纸公关声明，而是把模型该如何服从指令、处理冲突、兼顾安全与用户自由，尽量写成可被外界审视的框架。',
        deck_en='OpenAI published a detailed explanation of how its Model Spec is designed and why it exists. The company is trying to turn instruction-following, conflict resolution, safety, and user freedom into an inspectable framework rather than a vague internal instinct.',
        kicker_cn='头版',
        kicker_en='Lead',
        published_at='2026-03-25T10:00:00.000Z',
        reading_time=4,
        tags=['OpenAI', 'Model Spec', 'Governance', 'Safety'],
        summary_cn=[
            'OpenAI 在新文章中把 Model Spec 解释得比以往更完整：这套规范用于说明模型应当如何遵循指令、在冲突目标之间作取舍，并在安全与用户自由之间维持一致的行为边界。公司强调，Model Spec 既描述当前训练方向，也是一份面向未来的目标文档，供外部用户、研究者和政策制定者讨论。',
            '这件事值得放头版，不是因为它立刻带来一个新模型，而是因为主流模型公司开始承认：真正影响用户体验与社会接受度的，不只有参数和基准分数，还有“模型到底被允许怎么做”的公开可辩论规则。AI 产品往后走，行为规范本身会越来越像基础设施。'
        ],
        summary_en=[
            'In a new post, OpenAI laid out the philosophy and mechanics behind its Model Spec: a framework for how models should follow instructions, resolve conflicts, respect user freedom, and behave safely. The company frames it not as a statement of perfection today, but as a target that can be inspected, debated, and improved over time.',
            'That matters because the next stage of AI competition will not be defined only by model size or benchmark wins. It will also depend on whether companies can make behavioral expectations legible enough for users, developers, researchers, and governments to scrutinize.'
        ],
        bullets_cn=['Model Spec 被定位为可被公众阅读和讨论的行为框架。', '它试图把服从指令、冲突处理和安全边界写得更明确。', '主流模型公司的治理竞争正在从“内部规则”走向“公开规则”。'],
        bullets_en=['Model Spec is being framed as a public-facing framework for model behavior.', 'It tries to formalize instruction-following, conflict resolution, and safety boundaries.', 'AI governance competition is shifting from private rules to publicly legible ones.'],
        significance_cn='一旦模型行为规范变成公开对象，AI 公司的竞争就不只是训练得更强，还包括谁能把价值取舍解释得更清楚、修订得更快。',
        significance_en='Once model behavior becomes a public object, AI companies compete not only on capability, but on who can explain and revise their tradeoffs more credibly.',
        sources=[{'title': 'Inside our approach to the Model Spec', 'publication': 'OpenAI', 'url': 'https://openai.com/index/our-approach-to-the-model-spec'}],
    ),
    article(
        id='google-lyria-3-api-rollout',
        section='company',
        category_cn='音乐生成',
        category_en='Music Generation',
        headline_cn='Google 把 Lyria 3 推进 Gemini API，AI 音乐开始从玩具变成开发平台',
        headline_en='Google is pushing Lyria 3 into the Gemini API, turning AI music from a toy into a developer platform',
        deck_cn='Google 宣布 Lyria 3 与 Lyria 3 Pro 通过 Gemini API、Google AI Studio 等渠道开放给开发者，主打更长的歌曲结构、真实人声与更细的节奏控制。AI 音乐这条线，正从单次生成走向可嵌入产品。',
        deck_en='Google is rolling out Lyria 3 and Lyria 3 Pro through the Gemini API, Google AI Studio, and other surfaces, with longer song structure, more realistic vocals, and finer control. AI music is moving from one-off demos toward product infrastructure.',
        kicker_cn='公司',
        kicker_en='Company',
        published_at='2026-03-25T16:00:00.000Z',
        reading_time=3,
        tags=['Google', 'Lyria 3', 'Gemini API', 'Music AI'],
        summary_cn=[
            'Google 表示，Lyria 3 和 Lyria 3 Pro 已开始通过 Gemini API 与 Google AI Studio 向开发者提供预览。官方给出的重点包括最长约三分钟的完整歌曲生成、30 秒高速片段模式、多语言人声、节奏设定、歌词时间轴以及图像到音乐的多模态输入。',
            '更值得注意的是发布位置。Google 没有把它只留在单一应用里，而是把音乐生成能力接进开发者工具、企业产品和多种工作流。这意味着 AI 音乐的竞争已经不只是“谁能生成更像”，而是“谁先成为别家产品里的默认音频引擎”。'
        ],
        summary_en=[
            'Google says Lyria 3 and Lyria 3 Pro are entering preview through the Gemini API and Google AI Studio. The release emphasizes up to roughly three-minute tracks, a fast 30-second clip mode, multilingual vocals, tempo control, time-aligned lyrics, and image-to-music prompting.',
            'What matters is not just quality but placement. Google is treating music generation as a developer capability that can live inside many tools and workflows, which suggests the AI music race is shifting from novelty to infrastructure.'
        ],
        bullets_cn=['Lyria 3 Pro 支持更长的完整歌曲结构。', '控制项延伸到节奏、歌词时间轴和图像输入。', 'Google 正把音乐生成做成可嵌入的开发能力。'],
        bullets_en=['Lyria 3 Pro supports longer, more structured song generation.', 'Controls now extend to tempo, lyric timing, and image input.', 'Google is packaging music generation as an embeddable developer capability.'],
        significance_cn='一旦音乐生成被接进 API 和办公流，AI 音频就更像云服务能力，而不只是创作演示。',
        significance_en='Once music generation is wired into APIs and work tools, AI audio starts to look less like a demo and more like a cloud capability.',
        sources=[
            {'title': 'Build with Lyria 3, our newest music generation model', 'publication': 'Google', 'url': 'https://blog.google/innovation-and-ai/technology/developers-tools/lyria-3-developers/'},
            {'title': 'Google Lyria 3 Pro makes longer AI songs', 'publication': 'The Verge', 'url': 'https://www.theverge.com/ai-artificial-intelligence/900425/google-lyria-3-pro-ai-music'}
        ],
    ),
    article(
        id='granola-enterprise-spaces-api',
        section='company',
        category_cn='会议与知识流',
        category_en='Meeting Intelligence',
        headline_cn='Granola 融资 1.25 亿美元，想把会议纪要产品抬成企业知识入口',
        headline_en='Granola raised $125 million to turn meeting notes into an enterprise knowledge entry point',
        deck_cn='Granola 新一轮融资后估值来到 15 亿美元，并上线团队 Spaces、个人与企业 API。会议纪要赛道开始证明，真正值钱的不是“会转写”，而是能否把零散对话变成企业上下文。',
        deck_en='Granola’s new round values it at $1.5 billion, and the company is launching team Spaces plus personal and enterprise APIs. The meeting-notes market is showing that the real prize is not transcription alone, but turning conversation into reusable organizational context.',
        kicker_cn='公司',
        kicker_en='Company',
        published_at='2026-03-25T14:48:40.000Z',
        reading_time=3,
        tags=['Granola', 'Enterprise AI', 'Meetings', 'Context'],
        summary_cn=[
            'TechCrunch 报道称，Granola 完成 1.25 亿美元 C 轮融资，估值达到 15 亿美元。公司同时推出团队级 Spaces 与 Folders，以及个人 API、企业 API，试图把会议记录、共享笔记和组织上下文连接进更大的 AI 工作流。',
            '这说明会议纪要产品正在进入第二阶段：转写与总结越来越像标配，壁垒开始转向权限体系、上下文共享、API 接入以及是否能进入企业知识栈。AI 办公产品最终抢的不是“某一场会”，而是会后能被不断复用的信息层。'
        ],
        summary_en=[
            'TechCrunch reports that Granola has raised a $125 million Series C at a $1.5 billion valuation. Alongside the round, it introduced team Spaces and Folders, plus personal and enterprise APIs to bring meeting context into broader AI workflows.',
            'That suggests meeting-note products are entering a second phase. Transcription is becoming table stakes; the defensible layer is shifting toward permissions, context sharing, and whether those notes can function as reusable enterprise memory.'
        ],
        bullets_cn=['Granola 估值升至 15 亿美元。', '新功能核心是团队空间与上下文 API。', '会议纪要产品正在向企业知识层进化。'],
        bullets_en=['Granola is now valued at $1.5 billion.', 'The new products center on team spaces and context APIs.', 'Meeting-note tools are evolving into enterprise knowledge layers.'],
        significance_cn='未来办公 AI 的价值，很可能由“谁拥有组织上下文”决定，而不只是“谁写摘要写得快”。',
        significance_en='The future value of workplace AI may depend less on who writes the fastest summary and more on who controls organizational context.',
        sources=[{'title': 'Granola raises $125M, hits $1.5B valuation as it expands from meeting notetaker to enterprise AI app', 'publication': 'TechCrunch', 'url': 'https://techcrunch.com/2026/03/25/granola-raises-125m-hits-1-5b-valuation-as-it-expands-from-meeting-notetaker-to-enterprise-ai-app/'}],
    ),
    article(
        id='meta-shopping-ai-instagram-facebook',
        section='company',
        category_cn='社交电商',
        category_en='Social Commerce',
        headline_cn='Meta 也把 AI 塞进购物流，Instagram 和 Facebook 想把导购和结账都留在站内',
        headline_en='Meta is putting AI into social shopping, trying to keep product discovery and checkout inside Instagram and Facebook',
        deck_cn='Meta 在 Shoptalk 上公布新的 AI 购物体验：广告或链接点开后可直接看到品牌信息、评论摘要、推荐商品与站内结账。它争的不是聊天入口，而是社交流量里的购买闭环。',
        deck_en='At Shoptalk, Meta unveiled a new AI shopping flow that summarizes products, reviews, and brand details while keeping checkout inside its apps. The company is fighting not for chatbot primacy, but for a tighter commerce loop inside social feeds.',
        kicker_cn='公司',
        kicker_en='Company',
        published_at='2026-03-25T14:16:17.000Z',
        reading_time=3,
        tags=['Meta', 'Instagram', 'Facebook', 'Commerce'],
        summary_cn=[
            'Meta 表示，将测试一套新的购物体验：用户点击 Facebook 或 Instagram 上的广告或外链后，可以直接看到 AI 整理的商品信息、评论摘要、品牌介绍、优惠信息与推荐商品，并通过与 Stripe、PayPal 等伙伴合作的流程在应用内完成购买。',
            '这表明 AI 电商的路径并不只有聊天机器人一种。Meta 选择把 AI 作为社交流量里的“决策辅助层”和“转化加速层”，让用户少跳页、少离站，把原本分散在商家页面、评论区和支付链路里的信息重新打包。'
        ],
        summary_en=[
            'Meta says it will test a new shopping experience in which users clicking ads or links from Facebook and Instagram can see AI-generated summaries of product information, reviews, brand details, offers, and recommendations before buying inside the app.',
            'That shows AI commerce is not only a chatbot story. Meta is using AI as a decision-support and conversion layer embedded in social traffic, tightening the path from browsing to payment without sending users elsewhere.'
        ],
        bullets_cn=['Meta 用 AI 总结商品和评论信息。', '新的站内流程试图缩短从种草到付款的路径。', '社交平台正在把 AI 当成转化工具而非纯聊天功能。'],
        bullets_en=['Meta is using AI to summarize products and reviews.', 'The new flow tries to shorten the path from discovery to payment.', 'Social platforms are treating AI as a conversion layer, not just a chat feature.'],
        significance_cn='如果社交平台把商品理解、推荐和支付都吞进站内，品牌未来会更难把用户带回自己的独立站。',
        significance_en='If social platforms absorb product understanding, recommendation, and payment into one surface, brands may find it even harder to pull users back to their own sites.',
        sources=[{'title': 'Meta turns to AI to make shopping easier on Instagram and Facebook', 'publication': 'TechCrunch', 'url': 'https://techcrunch.com/2026/03/25/meta-turns-to-ai-to-make-shopping-easier-on-instagram-and-facebook/'}],
    ),
    article(
        id='data-center-ban-opening-bid',
        section='policy',
        category_cn='算力监管',
        category_en='Compute Regulation',
        headline_cn='Sanders 和 AOC 提议暂停新数据中心，AI 监管第一次直接冲着机房开刀',
        headline_en='Sanders and AOC want to pause new data centers, taking AI regulation straight to the physical layer',
        deck_cn='两位美国议员提出法案，拟暂停峰值负载超过 20 兆瓦的新数据中心建设，直到国会通过更完整的 AI 监管框架。关于 AI 的争论，开始从模型输出一路压到土地、电力与施工许可。',
        deck_en='Two US lawmakers proposed a bill to halt new data centers above 20 megawatts of peak load until Congress passes broader AI rules. The AI debate is moving from model outputs down to land use, power demand, and construction permits.',
        kicker_cn='政策',
        kicker_en='Policy',
        published_at='2026-03-25T17:15:50.000Z',
        reading_time=3,
        tags=['Data Centers', 'Regulation', 'Energy', 'Congress'],
        summary_cn=[
            'TechCrunch 报道称，伯尼·桑德斯与亚历山大·奥卡西奥-科尔特斯提出配套法案，拟暂停所有峰值功率超过 20 兆瓦的新数据中心项目，直到国会通过更全面的 AI 监管。法案还提到模型预发布审查、就业保护、环境影响和建设中的工会劳工要求。',
            '这条消息的关键不只是“禁建”两个字，而是它把 AI 监管从模型层面拖回了物理世界。算力扩张越重资产化，争议就越难停留在抽象伦理层，而会变成电网、土地、碳排、劳工和地方许可的现实政治问题。'
        ],
        summary_en=[
            'TechCrunch reports that Bernie Sanders and Alexandria Ocasio-Cortez have introduced companion legislation to halt new data centers with peak loads above 20 megawatts until Congress enacts broader AI regulation. The proposal also points toward pre-release model review, labor protections, and environmental limits.',
            'The bigger shift is that AI regulation is being aimed at infrastructure, not just outputs. As compute becomes more capital-intensive, policy fights increasingly move into power grids, land use, emissions, and construction politics.'
        ],
        bullets_cn=['法案针对的是高负载新数据中心。', '监管诉求同时覆盖模型、就业、环境与劳工。', 'AI 政策战正在从代码层下沉到基础设施层。'],
        bullets_en=['The bill targets high-load new data centers.', 'Its demands span models, jobs, the environment, and labor.', 'AI policy battles are moving from code to infrastructure.'],
        significance_cn='一旦监管开始卡数据中心门槛，算力就不再只是科技公司的内部成本，而会成为公开政治资源。',
        significance_en='Once regulation starts targeting data-center thresholds, compute stops being a private internal cost and becomes a public political resource.',
        sources=[{'title': 'Bernie Sanders and AOC propose a ban on data center construction', 'publication': 'TechCrunch', 'url': 'https://techcrunch.com/2026/03/25/bernie-sanders-and-aoc-propose-a-ban-on-data-center-construction/'}],
    ),
    article(
        id='medicare-ai-foia-lawsuit',
        section='policy',
        category_cn='公共服务透明度',
        category_en='Public-Service Transparency',
        headline_cn='EFF 起诉追问 Medicare 的 AI 审批试点，算法进医保之前先撞上透明度问题',
        headline_en='EFF is suing over Medicare’s AI pilot, showing that public-sector AI hits a transparency wall before anything else',
        deck_cn='EFF 就 CMS 的 WISeR 试点提起 FOIA 诉讼，要求公开用于医保事前审批的 AI 系统细节、测试与审计记录。AI 一旦进入公共福利系统，“先公开怎么运作”会比“先吹效率提升”更难回避。',
        deck_en='EFF filed a FOIA lawsuit over CMS’s WISeR pilot, seeking details, tests, and audits for an AI system used in Medicare prior authorization. Once AI enters public-benefit systems, transparency becomes harder to dodge than efficiency talking points.',
        kicker_cn='政策',
        kicker_en='Policy',
        published_at='2026-03-25T17:20:02.000Z',
        reading_time=3,
        tags=['EFF', 'Medicare', 'CMS', 'AI Oversight'],
        summary_cn=[
            'EFF 表示，已就 CMS 的 WISeR 试点项目提起 FOIA 诉讼。该项目使用 AI 评估 Medicare 的事前授权申请，但外界仍不清楚其训练数据、偏见测试、审计机制与防止错误拒赔的保障措施。EFF 指出，项目已在六个州落地，可能影响数百万 Medicare 受益人。',
            '这件事的敏感处在于，公共部门部署 AI 与互联网产品不同。它面对的不是“推荐是否更准”，而是治疗是否被拖延、患者是否被错拒以及公众是否有权知道系统是怎么做判断的。医疗场景中的算法，天然要先过问责门槛。'
        ],
        summary_en=[
            'EFF says it has filed a FOIA lawsuit over CMS’s WISeR pilot, which uses AI to evaluate Medicare prior authorization requests. The group says key details remain unclear, including the system’s training data, bias testing, safeguards, and audit mechanisms, even though the pilot is already active in six states.',
            'That is what makes the case bigger than one program. In public benefits, AI does not merely shape convenience; it can shape treatment delays, denials, and accountability. Transparency becomes part of the product, not an optional afterthought.'
        ],
        bullets_cn=['WISeR 已在多个州落地，却缺乏充分公开信息。', 'EFF 追问训练数据、偏差测试与审计记录。', '公共福利领域的 AI 更难绕开问责要求。'],
        bullets_en=['WISeR is active in multiple states despite limited disclosure.', 'EFF is seeking training, bias-testing, and audit records.', 'AI in public benefits faces stricter accountability expectations.'],
        significance_cn='谁先把算法带进公共服务，谁也必须先承担解释义务；没有这一步，所谓“智能治理”只会更像黑箱治理。',
        significance_en='Anyone bringing algorithms into public services must also carry the burden of explanation; without that, “smart governance” starts to look like black-box governance.',
        sources=[{'title': 'EFF Sues for Answers About Medicare\'s AI Experiment', 'publication': 'EFF', 'url': 'https://www.eff.org/press/releases/eff-sues-answers-about-medicares-ai-experiment'}],
    ),
    article(
        id='openai-safety-bug-bounty',
        section='tools',
        category_cn='安全研究',
        category_en='Safety Research',
        headline_cn='OpenAI 开安全漏洞赏金，但这次找的不是传统漏洞而是 AI 滥用路径',
        headline_en='OpenAI launched a bug bounty for AI safety abuse paths, not just conventional vulnerabilities',
        deck_cn='OpenAI 新的 Safety Bug Bounty 计划接受代理劫持、提示注入导致的数据外泄、账户完整性绕过等 AI 特有风险报告。安全研究的重心，正在从“服务器有没有洞”转向“模型会不会被人带偏”。',
        deck_en='OpenAI’s new Safety Bug Bounty accepts reports on agent hijacking, prompt-injection-driven data exfiltration, account-integrity bypasses, and other AI-specific risks. Security research is shifting from server flaws toward whether models can be steered into harmful behavior.',
        kicker_cn='工具',
        kicker_en='Tools',
        published_at='2026-03-25T00:00:00.000Z',
        reading_time=3,
        tags=['OpenAI', 'Bug Bounty', 'Safety', 'Agents'],
        summary_cn=[
            'OpenAI 宣布推出面向 AI 安全与滥用风险的公开赏金计划，覆盖的重点包括第三方提示注入导致的代理劫持与数据外泄、OpenAI 网站上的不当自动化动作、模型生成专有推理信息，以及账户与平台完整性相关的绕过问题。',
            '这说明主流厂商已经开始把“AI 滥用路径”当成一种独立于传统网络安全的漏洞类型。未来的赏金项目不只是查 XSS、提权和权限错配，也要查代理是否会被诱导做不该做的事。模型时代的安全边界，越来越像行为边界。'
        ],
        summary_en=[
            'OpenAI has launched a public bounty program focused on AI-specific safety and abuse risks, including third-party prompt injection that hijacks agents, large-scale harmful actions by agentic products, exposure of proprietary reasoning information, and account-integrity manipulation.',
            'The bigger message is that major labs are starting to treat AI abuse paths as a distinct vulnerability class. Security in the model era is no longer only about infrastructure weaknesses, but about behavioral pathways that can be exploited.'
        ],
        bullets_cn=['赏金范围涵盖代理劫持、数据外泄与完整性绕过。', 'AI 安全问题被单独从传统漏洞分类中拎出来。', '安全研究正在更靠近模型行为本身。'],
        bullets_en=['The bounty covers agent hijacking, data exfiltration, and integrity bypasses.', 'AI safety issues are being separated from classic vulnerability categories.', 'Security research is moving closer to model behavior itself.'],
        significance_cn='当主流实验室开始为“行为级漏洞”付钱，说明 AI 安全已经正式进入工程化、外部审计和持续对抗的新阶段。',
        significance_en='When major labs start paying for behavioral vulnerabilities, AI safety enters a more operational era of external auditing and continuous adversarial testing.',
        sources=[{'title': 'Introducing the OpenAI Safety Bug Bounty program', 'publication': 'OpenAI', 'url': 'https://openai.com/index/safety-bug-bounty'}],
    ),
    article(
        id='eva-voice-agent-evaluation',
        section='tools',
        category_cn='评测框架',
        category_en='Evaluation Framework',
        headline_cn='Hugging Face 上线 EVA，语音代理终于不只比“答对没”还开始比“说得像不像人”',
        headline_en='EVA gives voice agents a benchmark that scores not only correctness but whether they actually sound usable',
        deck_cn='ServiceNow AI 团队在 Hugging Face 发布 EVA，试图同时评估语音代理的任务完成度与对话体验，并给出 Accuracy 与 Experience 两条分数。语音代理的真正难点，越来越像系统工程而不是单点模型能力。',
        deck_en='ServiceNow AI released EVA on Hugging Face to jointly score voice agents on task completion and conversational experience. Voice agents increasingly look like a systems problem, not just a single-model problem.',
        kicker_cn='工具',
        kicker_en='Tools',
        published_at='2026-03-24T02:01:52.000Z',
        reading_time=3,
        tags=['Hugging Face', 'Voice Agents', 'Benchmark', 'Evaluation'],
        summary_cn=[
            'EVA 把语音代理的评测拆成 EVA-A（准确性）与 EVA-X（体验）两条主分数，并采用多轮、完整、bot-to-bot 的真实对话场景来测试系统。项目还给出首批航空场景数据集，覆盖改签、取消、代金券等任务。',
            '有意思的是，作者强调目前系统普遍存在“完成任务”和“对话自然”之间的权衡。也就是说，语音代理真正难的地方，不是单次语音转文字或单次回复，而是整段通话里能否既不出错、又不让人烦。'
        ],
        summary_en=[
            'EVA introduces two headline scores for voice agents—EVA-A for accuracy and EVA-X for experience—using complete, multi-turn spoken conversations in a bot-to-bot setup. The initial dataset focuses on airline scenarios such as rebooking, cancellations, and vouchers.',
            'Its most interesting claim is that strong task success often comes with a weaker user experience, and vice versa. That turns voice-agent quality into a systems tradeoff across speech recognition, timing, dialogue structure, and tool use.'
        ],
        bullets_cn=['EVA 同时衡量准确性与体验。', '首批数据集围绕航空客服多轮场景。', '语音代理的瓶颈被重新定义成整体交互质量。'],
        bullets_en=['EVA jointly measures accuracy and user experience.', 'Its first dataset centers on multi-turn airline support scenarios.', 'The bottleneck for voice agents is being reframed as total interaction quality.'],
        significance_cn='谁先把语音代理的体验问题量化清楚，谁就更接近真正可商用的电话与语音助手。',
        significance_en='Whoever quantifies the experience problem of voice agents most effectively gets closer to commercially viable phone and voice assistants.',
        sources=[{'title': 'A New Framework for Evaluating Voice Agents (EVA)', 'publication': 'Hugging Face', 'url': 'https://huggingface.co/blog/ServiceNow-AI/eva'}],
    ),
    article(
        id='axplorer-math-tool',
        section='tools',
        category_cn='科研工具',
        category_en='Research Tools',
        headline_cn='Axiom Math 把 PatternBoost 缩进 Mac Pro，想让数学家的 AI 工具不再只活在超算上',
        headline_en='Axiom Math shrank PatternBoost onto a Mac Pro, trying to make AI tools for mathematicians more accessible',
        deck_cn='MIT Technology Review 报道称，Axiom Math 发布免费工具 Axplorer，用于帮助数学家发现模式并探索难题。它的意义不只是又多一个 AI 助手，而是把原本依赖重型算力的研究工具变成个人可用的软件。',
        deck_en='MIT Technology Review reports that Axiom Math released a free tool, Axplorer, to help mathematicians discover patterns and explore hard problems. The bigger story is not another assistant, but moving a previously heavyweight research system onto a personal machine.',
        kicker_cn='工具',
        kicker_en='Tools',
        published_at='2026-03-25T13:59:17.000Z',
        reading_time=3,
        tags=['Axiom Math', 'Mathematics', 'Research Tools', 'Axplorer'],
        summary_cn=[
            'MIT Technology Review 报道称，Axiom Math 推出免费工具 Axplorer，它基于 François Charton 先前参与开发的 PatternBoost 思路，目标是帮助数学家发现模式、提出猜想并探索长期难题。文章提到，旧系统曾运行在超级计算机上，而新版可在 Mac Pro 上运行。',
            '真正值得看的是这种工具化方向。AI 在科研里的价值不一定先体现在“自动证明”，也可能先体现在加快探索、筛选和提出线索的过程。对于很多学科来说，缩短试错时间本身就是生产力革命。'
        ],
        summary_en=[
            'MIT Technology Review reports that Axiom Math has released Axplorer, a free tool designed to help mathematicians spot patterns and explore difficult problems. It builds on earlier work around PatternBoost, but now runs on a Mac Pro instead of requiring supercomputing resources.',
            'That matters because AI in research may scale first through exploration tools rather than fully automated breakthroughs. In many fields, reducing the cost of experimentation and pattern discovery is already a meaningful productivity shift.'
        ],
        bullets_cn=['Axplorer 试图把数学探索工具下放到个人机器。', '它聚焦模式发现与猜想生成，而不是直接替代数学家。', '科研 AI 的第一波落地可能是“更快探索”而非“自动证明”。'],
        bullets_en=['Axplorer tries to bring mathematical exploration tools onto personal hardware.', 'It focuses on pattern discovery rather than replacing mathematicians outright.', 'The first wave of research AI may be about faster exploration, not full automation.'],
        significance_cn='如果高门槛科研工具能被压缩到个人设备上，学术生产力的分配方式也会跟着改变。',
        significance_en='If high-end research tools can be compressed onto personal machines, the distribution of academic productivity could change with them.',
        sources=[{'title': 'This startup wants to change how mathematicians do math', 'publication': 'MIT Technology Review', 'url': 'https://www.technologyreview.com/2026/03/25/1134642/this-startup-wants-to-change-how-mathematicians-do-math/'}],
    ),
    article(
        id='turboquant-kv-cache-cost',
        section='impact',
        category_cn='模型效率',
        category_en='Model Efficiency',
        headline_cn='TurboQuant 再次提醒行业：AI 最贵的部分，很多时候不是聪明而是记忆',
        headline_en='TurboQuant is another reminder that the most expensive part of AI is often not intelligence but memory',
        deck_cn='Google 的 TurboQuant 围绕 KV cache 压缩与向量量化效率展开，目标是在不明显掉精度的情况下把运行时“工作记忆”压得更小。推理成本战，继续往底层内存结构里钻。',
        deck_en='Google’s TurboQuant targets KV-cache compression and vector-quantization efficiency, aiming to shrink runtime working memory without obvious quality loss. The cost war in inference keeps moving deeper into memory architecture.',
        kicker_cn='影响',
        kicker_en='Impact',
        published_at='2026-03-25T20:38:45.000Z',
        reading_time=3,
        tags=['Google', 'TurboQuant', 'KV Cache', 'Inference'],
        summary_cn=[
            'TechCrunch 对 Google Research 的 TurboQuant 做了通俗介绍：这套方法围绕向量量化、PolarQuant 和 QJL 等技术，目标是减少 KV cache 等“工作记忆”占用，让模型在推理时用更少内存保留更多上下文，并有望把相关成本压低至少数倍。',
            '这类新闻反复出现，说明行业的真正痛点已经越来越明确。模型越大，训练之外的瓶颈越集中在内存、带宽和运行成本上。未来决定产品规模化能力的，也许不是谁再多做一点参数，而是谁先把“记住这么多信息”的代价打下来。'
        ],
        summary_en=[
            'TechCrunch summarized Google Research’s TurboQuant work as a way to compress AI working memory—especially KV cache—through techniques such as PolarQuant and QJL, potentially reducing runtime memory costs by several multiples without major quality loss.',
            'The larger signal is that AI bottlenecks are increasingly concrete. As models get larger, the most painful constraints shift away from training alone and toward memory, bandwidth, and deployment cost at inference time.'
        ],
        bullets_cn=['TurboQuant 盯上的是推理时的内存瓶颈。', '核心目标是更少内存、更多上下文、尽量不掉精度。', '效率竞争正在深入到模型运行的底层结构。'],
        bullets_en=['TurboQuant targets memory bottlenecks at inference time.', 'The goal is more context with less memory and minimal quality loss.', 'Efficiency competition is moving into the deepest layers of model runtime.'],
        significance_cn='推理成本一旦继续下降，真正被重写的不只是云账单，还包括长上下文、代理执行与检索增强的可行边界。',
        significance_en='If inference memory costs keep falling, what changes is not just cloud spending but the practical limits of long context, agents, and retrieval-heavy systems.',
        sources=[
            {'title': 'Google unveils TurboQuant, a new AI memory compression algorithm', 'publication': 'TechCrunch', 'url': 'https://techcrunch.com/2026/03/25/google-turboquant-ai-memory-compression-silicon-valley-pied-piper/'},
            {'title': 'TurboQuant: Redefining AI efficiency with extreme compression', 'publication': 'Google Research', 'url': 'https://research.google/blog/turboquant-redefining-ai-efficiency-with-extreme-compression/'}
        ],
    ),
    article(
        id='anthropic-ai-skills-gap',
        section='impact',
        category_cn='劳动分化',
        category_en='Labor Stratification',
        headline_cn='Anthropic 说还没大规模裁员，但“会用 AI 的人”和“不会用的人”已经开始拉开',
        headline_en='Anthropic says mass layoffs are not here yet, but the gap between AI power users and everyone else is already widening',
        deck_cn='Anthropic 最新研究称，当前尚无明显证据表明 AI 已大规模替代工作，但熟练用户正在更快放大优势，尤其对刚进入职场的人而言。AI 对劳动市场的第一击，可能不是失业潮，而是能力分层。',
        deck_en='Anthropic’s latest economic readout says there is little evidence of broad AI-driven job loss yet, but skilled users are pulling away faster, especially relative to new entrants. The first labor-market effect of AI may be stratification before outright displacement.',
        kicker_cn='影响',
        kicker_en='Impact',
        published_at='2026-03-25T21:44:13.000Z',
        reading_time=3,
        tags=['Anthropic', 'Labor Market', 'Skills', 'Work'],
        summary_cn=[
            'TechCrunch 援引 Anthropic 经济研究负责人 Peter McCrory 的说法称，目前还看不到 AI 已经大规模消灭岗位的证据，至少失业率层面没有显著分化。但公司观察到，能把 Claude 用在核心任务上的“重度用户”正在更快拉开效率差距，而年轻、刚入场的白领更容易被这轮变化挤压。',
            '这类信号值得警惕，因为它意味着 AI 对职场的早期冲击不一定表现为公司今天裁掉多少人，而可能先表现为谁更快成为超级个体、谁更快掉出竞争轨道。失业也许还没来，但不平等已经开始有轮廓。'
        ],
        summary_en=[
            'TechCrunch reports that Anthropic’s latest economic analysis finds little evidence of broad AI-driven job destruction so far, at least in unemployment data. But the company says users who apply Claude to central job tasks are already pulling ahead, while younger and newer workers may be more exposed.',
            'That makes the near-term story less about an immediate jobs apocalypse and more about capability divergence. AI may reshape labor markets first by amplifying some workers faster than others before it clearly eliminates roles.'
        ],
        bullets_cn=['Anthropic 暂未看到明确的大规模岗位消失。', '重度 AI 用户正在形成效率优势。', '职场分层可能先于失业潮出现。'],
        bullets_en=['Anthropic does not yet see clear evidence of mass job loss.', 'Heavy AI users are building a productivity edge.', 'Labor stratification may arrive before layoffs do.'],
        significance_cn='如果 AI 先制造的是能力鸿沟，那么教育、培训和岗位设计会比裁员数字更早成为政策焦点。',
        significance_en='If AI first creates capability gaps, then education, training, and job design may become policy flashpoints before layoff statistics do.',
        sources=[{'title': 'The AI skills gap is here, says AI company, and power users are pulling ahead', 'publication': 'TechCrunch', 'url': 'https://techcrunch.com/2026/03/25/the-ai-skills-gap-is-here-says-ai-company-and-power-users-are-pulling-ahead/'}],
    ),
    article(
        id='deccan-ai-india-posttraining',
        section='impact',
        category_cn='数据劳工',
        category_en='Data Labor',
        headline_cn='Deccan AI 融资 2500 万美元，后训练繁荣继续把大量高技能数据劳动吸进印度',
        headline_en='Deccan AI raised $25 million as the post-training boom pulls more high-skill data labor into India',
        deck_cn='Deccan AI 主打后训练数据、评测与强化学习环境，运营重心放在海得拉巴并依赖大规模专家网络。大模型热潮的另一面，仍是全球化的人力供应链。',
        deck_en='Deccan AI focuses on post-training data, evaluations, and reinforcement-learning environments, with major operations in Hyderabad and a large expert network. The other side of the model boom remains a globalized labor supply chain.',
        kicker_cn='影响',
        kicker_en='Impact',
        published_at='2026-03-26T00:30:00.000Z',
        reading_time=3,
        tags=['Deccan AI', 'India', 'Post-Training', 'Data Work'],
        summary_cn=[
            'TechCrunch 报道称，Deccan AI 完成 2500 万美元 A 轮融资，业务覆盖后训练数据生成、评测、强化学习环境和工具调用相关工作。公司总部在湾区，但在海得拉巴有大型运营团队，并依赖超过百万贡献者网络，其中包括学生、领域专家和博士。',
            '这条消息提醒人们，大模型产业链的扩张并不只发生在实验室和数据中心里。模型越来越强的背后，仍然需要大规模、分层次、跨地域的人类标注、反馈、评估和流程化知识劳动。所谓“自动化”，往往是建立在更复杂的人力编排上。'
        ],
        summary_en=[
            'TechCrunch reports that Deccan AI has raised a $25 million Series A to provide post-training data generation, evaluation, reinforcement-learning environments, and tool-use support. The company is Bay Area-based but runs major operations in Hyderabad and depends on a contributor network of more than one million people.',
            'The broader point is that the model economy still rests on globally distributed human labor. Behind more capable systems lies an expanding market for expert feedback, evaluation, and structured data work that is increasingly industrialized.'
        ],
        bullets_cn=['Deccan 服务的是后训练与评测环节。', '公司依赖大规模印度专家与贡献者网络。', 'AI 自动化背后依旧站着密集的人类数据劳动。'],
        bullets_en=['Deccan is focused on post-training and evaluation work.', 'It relies on a large India-based contributor and expert network.', 'Human data labor remains central to AI automation.'],
        significance_cn='如果后训练继续外包化、规模化，AI 产业的劳工政治与利润分配问题只会越来越难被忽略。',
        significance_en='If post-training keeps scaling through outsourcing, the labor politics and value distribution of AI will become harder to ignore.',
        sources=[{'title': 'Mercor competitor Deccan AI raises $25M, sources experts from India', 'publication': 'TechCrunch', 'url': 'https://techcrunch.com/2026/03/25/deccan-ai-raises-25m-as-ai-training-push-relies-on-india-based-workforce/'}],
    ),
    article(
        id='reddit-human-verification-bots',
        section='insight',
        category_cn='平台治理',
        category_en='Platform Governance',
        headline_cn='Reddit 要求“像机器人”的账号证明自己是人，开放社区开始补身份门槛',
        headline_en='Reddit wants suspicious accounts to prove they are human, adding identity friction to the open web',
        deck_cn='Reddit 将对可疑账号启用“证明自己是人类”的机制，同时标注提供服务的自动化账号。机器人洪水正在迫使开放社区重新发明身份防线。',
        deck_en='Reddit will require suspicious accounts to verify they are human while labeling service bots. Bot pressure is forcing open communities to rebuild identity defenses.',
        kicker_cn='观察',
        kicker_en='Insight',
        published_at='2026-03-25T16:10:00.000Z',
        reading_time=2,
        tags=['Reddit', 'Bots', 'Verification', 'Identity'],
        summary_cn=[
            'TechCrunch 报道称，Reddit 将标记提供服务的自动化账号，并对被判定为“行为可疑”的账号要求进行人类验证。公司称不会全站统一验证，而会依赖账户行为与技术信号判断是否需要触发验证，手段可能包括 passkeys、生物识别或在特定地区使用政府证件。',
            '这类动作暴露出开放平台的尴尬：为了保住匿名与低门槛，它们过去尽量少做身份验证；但一旦机器人和自动化内容过量，平台又不得不重新引入摩擦。互联网的下一轮治理，很可能就是在“匿名”“便利”和“真人证明”之间反复拉扯。'
        ],
        summary_en=[
            'TechCrunch reports that Reddit will label service bots and ask suspicious accounts to verify that they are human, based on behavioral and technical signals rather than a blanket sitewide mandate. Verification may involve passkeys, biometrics, or, in some regions, government IDs.',
            'The tension is structural. Open communities have long tried to preserve anonymity and low friction, but bot saturation pushes them back toward stronger identity checks. The next governance fight online may revolve around how much humanity needs to be proven.'
        ],
        bullets_cn=['Reddit 将区分“服务型机器人”和可疑未标注账号。', '验证不是全站强制，而是风险触发。', '开放社区正在用身份摩擦对抗自动化洪水。'],
        bullets_en=['Reddit will distinguish service bots from suspicious unlabeled accounts.', 'Verification is meant to be risk-triggered, not universal.', 'Open communities are using identity friction to fight automation floods.'],
        significance_cn='如果真人证明变成大型平台默认配置，匿名互联网的旧想象会继续退场。',
        significance_en='If proving one’s humanity becomes a default feature on major platforms, the older vision of an anonymous internet will keep receding.',
        sources=[
            {'title': 'Reddit takes on the bots with new human verification requirements for fishy behavior', 'publication': 'TechCrunch', 'url': 'https://techcrunch.com/2026/03/25/reddit-bots-new-human-verification-requirements/'},
            {'title': 'Reddit accounts with fishy bot-like behavior will soon need to prove they’re human', 'publication': 'The Verge', 'url': 'https://www.theverge.com/tech/900363/reddit-human-verification-bots-crackdown'}
        ],
    ),
    article(
        id='meta-layoffs-ai-capex',
        section='insight',
        category_cn='资本重排',
        category_en='Capital Reallocation',
        headline_cn='Meta 一边裁员一边猛砸 AI，说明大厂内部的资源迁移已经不打算装得温和了',
        headline_en='Meta is cutting jobs while spending heavily on AI, showing that big-tech resource shifts are no longer pretending to be gentle',
        deck_cn='Meta 被曝裁撤数百个岗位，同时仍准备把更多预算砸向 AI 数据中心与相关基础设施。所谓“AI 优先”在大公司里，越来越像一场赤裸的内部再分配。',
        deck_en='Meta is reportedly cutting hundreds of roles even as it prepares to spend aggressively on AI data centers and related infrastructure. Inside big companies, “AI first” is increasingly a blunt resource reallocation story.',
        kicker_cn='观察',
        kicker_en='Insight',
        published_at='2026-03-25T21:10:32.000Z',
        reading_time=2,
        tags=['Meta', 'Layoffs', 'AI Infrastructure', 'Big Tech'],
        summary_cn=[
            'The Verge 报道称，Meta 正在多个团队进行裁员，波及招聘、社交媒体、销售以及 Reality Labs 等部门。与此同时，公司仍计划大举投入 AI 数据中心，并继续推进相关芯片与基础设施布局。',
            '这类组合动作越来越典型：大公司嘴上说“重组优化”，本质上是在把资金、人力和战略注意力从旧愿景抽走，集中押到 AI 上。AI 投资并不是在原有预算之外自然长出来的，它往往伴随着别的业务被压缩、边缘化甚至切断。'
        ],
        summary_en=[
            'The Verge reports that Meta is cutting hundreds of jobs across recruiting, sales, social-media teams, and Reality Labs while still planning large spending on AI data centers and related infrastructure.',
            'That combination is becoming emblematic of the AI era in big tech. “Restructuring” often means redirecting money, people, and executive attention away from older bets and into AI. AI investment is not additive forever; it usually comes out of something else.'
        ],
        bullets_cn=['Meta 裁员与 AI 扩建在同一时间发生。', '受影响团队包括 Reality Labs 等旧战略重点。', 'AI 预算扩张正伴随大厂内部的资源再分配。'],
        bullets_en=['Meta’s layoffs and AI expansion are happening simultaneously.', 'The affected teams include former strategic priorities like Reality Labs.', 'AI budget growth is being matched by internal resource reallocation.'],
        significance_cn='大厂的 AI 转向越明确，市场就越该把“增长故事”拆开看：有人会被新资本推高，也一定有人被旧资本放弃。',
        significance_en='The clearer big tech’s AI pivot becomes, the more markets should read the growth story as a redistribution story: some areas are being elevated because others are being abandoned.',
        sources=[{'title': 'Meta is laying off hundreds of employees as it pours money into AI', 'publication': 'The Verge', 'url': 'https://www.theverge.com/tech/900946/meta-layoffs-hundreds-employees'}],
    ),
    article(
        id='harvey-11b-legal-ai',
        section='insight',
        category_cn='垂直软件',
        category_en='Vertical Software',
        headline_cn='Harvey 估值冲到 110 亿美元，法律 AI 继续证明垂直场景最容易吞下高估值',
        headline_en='Harvey’s $11 billion valuation shows vertical AI still has the easiest path to giant valuations',
        deck_cn='Harvey 新一轮融资后估值来到 110 亿美元，且一年内连续数次跳升。AI 创业里最被资本追捧的，仍然是能够明确嵌进高价值专业流程的垂直软件。',
        deck_en='Harvey’s latest funding gives it an $11 billion valuation after repeated jumps over the past year. In AI startups, the clearest path to huge pricing is still vertical software tied to expensive professional workflows.',
        kicker_cn='观察',
        kicker_en='Insight',
        published_at='2026-03-25T15:27:15.000Z',
        reading_time=2,
        tags=['Harvey', 'Legal Tech', 'Venture Capital', 'Vertical AI'],
        summary_cn=[
            'TechCrunch 报道称，法律 AI 公司 Harvey 确认以 110 亿美元估值完成 2 亿美元新融资，GIC 与 Sequoia 共同领投，多家老股东继续跟进。公司总融资已超过 10 亿美元，过去一年估值也连续数次上跳。',
            '这说明资本对“垂直 AI”这件事依然非常买账，前提是它足够贴近真实付费场景。法律服务并不性感，但单价高、流程重、知识密度高，恰好符合生成式 AI 最容易先吃进去的部分。与其说 Harvey 是个例，不如说它像一种估值模板。'
        ],
        summary_en=[
            'TechCrunch reports that legal AI startup Harvey has confirmed a new $200 million raise at an $11 billion valuation, with GIC and Sequoia co-leading and multiple existing investors returning. The company has now raised more than $1 billion in total.',
            'The signal is that vertical AI remains highly legible to capital when it plugs into expensive, repeatable workflows. Legal work is information-dense, process-heavy, and monetizable, making it one of the cleanest categories for investors to underwrite.'
        ],
        bullets_cn=['Harvey 估值一年内多次上跳。', 'Sequoia 等老股东持续加码。', '高价值专业流程仍是 AI 创业估值高地。'],
        bullets_en=['Harvey’s valuation has jumped repeatedly within a year.', 'Existing investors like Sequoia are still increasing exposure.', 'High-value professional workflows remain the valuation sweet spot for AI startups.'],
        significance_cn='只要资本继续奖励垂直场景里的高客单价软件，下一波 AI 创业也会更像行业化渗透，而不是通用助手复制。',
        significance_en='As long as investors keep rewarding high-ticket vertical software, the next startup wave in AI will look more like industry-by-industry penetration than generic assistant cloning.',
        sources=[{'title': 'Harvey confirms $11B valuation: Sequoia triples down', 'publication': 'TechCrunch', 'url': 'https://techcrunch.com/2026/03/25/harvey-confirms-11b-valuation-sequoia-triples-down/'}],
    ),
    article(
        id='openai-sora-focus-era',
        section='tech-humanities',
        category_cn='平台文化',
        category_en='Platform Culture',
        headline_cn='OpenAI 砍掉 Sora，不只是收缩产品线，也是承认“惊艳内容”不等于成立的平台文化',
        headline_en='OpenAI killing Sora is not just product focus, but an admission that dazzling output is not the same as platform culture',
        deck_cn='Wired 将此解读为 OpenAI 为 IPO 做准备的“聚焦期”。更深一层看，Sora 的收缩也在提醒行业：一个会生成内容的模型，不会自动长出一个有人愿意停留的社区。',
        deck_en='Wired frames the Sora shutdown as part of OpenAI’s pre-IPO focus era. At a deeper level, it shows that a model capable of generating media does not automatically turn into a community people want to inhabit.',
        kicker_cn='技术人文',
        kicker_en='Tech & Humanities',
        published_at='2026-03-25T14:57:45.000Z',
        reading_time=3,
        tags=['OpenAI', 'Sora', 'Social Apps', 'Platform Strategy'],
        summary_cn=[
            'Wired 报道称，OpenAI 将关闭 Sora 应用与相关 API，把资源进一步收回到统一助手与企业编码工具等更核心的方向。报道还提到，Sora 的下载量在最近几个月明显下滑，公司内部也在为“更聚焦”的路线让路。',
            '如果只把这件事理解成“产品聚焦”，就看轻了问题。真正的教训是：生成模型可以提供源源不断的内容供给，但社交产品需要的是关系、习惯、文化和留下来的理由。AI 让内容更容易出现，却没有让社区更容易成立。'
        ],
        summary_en=[
            'Wired reports that OpenAI is shutting down the Sora app and API as it narrows focus toward a more unified assistant and enterprise coding push. The report also notes slowing download momentum and internal pressure to concentrate resources.',
            'The deeper lesson is cultural rather than merely financial. Generative models can flood the world with media, but they do not automatically create community, habit, or a durable place where people want to spend time.'
        ],
        bullets_cn=['OpenAI 将资源从 Sora 回收到更核心业务。', 'Sora 的问题不只是增长放缓，也是社区没有成立。', 'AI 内容供给能力并不自动等于平台生命力。'],
        bullets_en=['OpenAI is pulling resources back from Sora into core bets.', 'Sora’s problem was not only slowing growth but weak community formation.', 'AI content supply does not automatically produce platform vitality.'],
        significance_cn='未来很多 AI 平台会反复撞上同一个现实：内容生成很便宜，但人类停留、认同和社交归属依旧很贵。',
        significance_en='Many AI platforms will keep relearning the same reality: generated content is cheap, but human attention, identity, and belonging remain expensive.',
        sources=[{'title': 'OpenAI Enters Its Focus Era by Killing Sora', 'publication': 'Wired', 'url': 'https://www.wired.com/story/openai-shuts-down-sora-ipo-ai-superapp/'}],
    ),
    article(
        id='robot-homeschool-vision',
        section='tech-humanities',
        category_cn='教育想象',
        category_en='Educational Imagination',
        headline_cn='“机器人老师”又被搬上白宫讲台，AI 教育叙事越来越像把耐心误认成教学',
        headline_en='The White House staged another robot-teacher fantasy, mistaking infinite patience for actual education',
        deck_cn='TechCrunch 报道称，梅拉尼娅·特朗普在白宫活动中描绘了由类人机器人担当家庭教师的未来图景。问题不在它离现实有多远，而在这种叙事总把教育理解成信息输送而不是人与人的关系。',
        deck_en='TechCrunch reports that Melania Trump used a White House event to imagine humanoid robots as ideal home tutors. The issue is not just how unrealistic that is, but how often this vision reduces education to information delivery rather than human relationships.',
        kicker_cn='技术人文',
        kicker_en='Tech & Humanities',
        published_at='2026-03-25T18:55:41.000Z',
        reading_time=3,
        tags=['Education', 'Robotics', 'Figure AI', 'Politics'],
        summary_cn=[
            'TechCrunch 报道称，梅拉尼娅·特朗普在白宫一场关于儿童教育科技的活动中，与 Figure AI 的人形机器人一同亮相，并设想未来会有名为“Plato”的机器人教师在家中为孩子提供个性化、永远耐心、随时在线的教育体验。',
            '这种画面之所以值得写，不是因为它明天就会成真，而是因为它暴露了科技圈与政治圈常见的一种误判：把教育抽象成内容访问、答疑速度和个性化反馈，却忽略了教师的判断、陪伴、权威与伦理责任。教育从来不只是把知识塞得更顺。'
        ],
        summary_en=[
            'TechCrunch reports that Melania Trump appeared at a White House event with a humanoid robot from Figure AI and described a future in which a robot tutor named “Plato” provides personalized, always-available teaching from home.',
            'What matters is the educational philosophy embedded in that image. It treats teaching as endless access to information and patient responses, while downplaying the roles of judgment, authority, care, and human responsibility that actual education depends on.'
        ],
        bullets_cn=['白宫活动把类人机器人包装成教育愿景。', '叙事重点是“永远在线、永远耐心”的个性化教学。', '它再次暴露了技术想象中对教育关系的简化。'],
        bullets_en=['A White House event packaged humanoid robots as an educational vision.', 'The pitch centered on always-available, infinitely patient personalization.', 'It exposes how tech narratives often flatten the relational nature of education.'],
        significance_cn='AI 进入教育最需要警惕的，也许不是技术不够好，而是我们太快把“教书”误写成“分发内容”。',
        significance_en='The greatest risk in AI education may not be weak technology, but our willingness to redefine teaching as content delivery too quickly.',
        sources=[{'title': 'Melania Trump wants a robot to homeschool your child', 'publication': 'TechCrunch', 'url': 'https://techcrunch.com/2026/03/25/melania-trump-wants-a-robot-to-homeschool-your-child/'}],
    ),
    article(
        id='disney-ai-slop-metaverse',
        section='tech-humanities',
        category_cn='娱乐工业',
        category_en='Entertainment Industry',
        headline_cn='Disney 的 AI 和元宇宙押注一起失速，内容工业发现“跟风未来感”远不如想象中便宜',
        headline_en='Disney’s AI and metaverse bets are stalling together, showing that trend-chasing futurism is not as cheap as it looks',
        deck_cn='The Verge 认为，Disney 新管理层上任就撞上两场尴尬：OpenAI 关停 Sora，Epic 也在裁员，连带让 Disney 的 AI 与元宇宙合作显得更悬。娱乐工业对“下一代内容形态”的焦虑，正在被现实挤压。',
        deck_en='The Verge argues that Disney’s new leadership is immediately confronting two awkward setbacks: OpenAI is winding down Sora and Epic is cutting staff, leaving Disney’s AI and metaverse bets looking shakier. The entertainment industry’s fear of missing the next format is running into reality.',
        kicker_cn='技术人文',
        kicker_en='Tech & Humanities',
        published_at='2026-03-25T20:02:48.000Z',
        reading_time=2,
        tags=['Disney', 'Sora', 'Metaverse', 'Media'],
        summary_cn=[
            'The Verge 指出，Disney 新 CEO Josh D\'Amaro 上任之初，就撞上 OpenAI 关停 Sora 以及 Epic 相关业务收缩的连锁影响。这让 Disney 先前围绕 AI 视频与元宇宙内容的几笔大赌注显得更加不稳。',
            '对内容行业来说，这不是八卦，而是一种症状。传统媒体公司既怕错过技术浪潮，又怕被技术公司拖进并不真正适合自己的叙事里。结果往往是：最贵的不是试验本身，而是把平台焦虑包装成战略眼光后留下的一地半成品。'
        ],
        summary_en=[
            'The Verge argues that Disney’s new CEO is immediately facing the fallout of OpenAI winding down Sora and broader uncertainty around Epic-related metaverse plans, leaving several of Disney’s recent “future media” bets looking weaker.',
            'For the entertainment industry, that is more than corporate gossip. It reflects a recurring anxiety: legacy media fears missing tech waves, but also risks getting trapped inside narratives that flatter innovation optics more than actual audience demand.'
        ],
        bullets_cn=['Disney 的 AI 与元宇宙合作同时承压。', '技术公司路线变化让内容公司的战略外包更显脆弱。', '娱乐工业的“未来焦虑”往往比技术本身更昂贵。'],
        bullets_en=['Disney’s AI and metaverse bets are under pressure at the same time.', 'Shifts inside tech partners make outsourced strategy look fragile.', 'The entertainment industry’s fear of the future can be costlier than the tech itself.'],
        significance_cn='媒体公司越想通过外部技术快速买到未来，越可能在未来真正到来前就先为幻觉埋单。',
        significance_en='The more media companies try to buy the future through outside tech partnerships, the more likely they are to pay for illusions before the future actually arrives.',
        sources=[{'title': 'Disney’s big bets on the metaverse and AI slop aren’t going so well', 'publication': 'The Verge', 'url': 'https://www.theverge.com/streaming/900837/disney-open-ai-sora-epic-fortnite-metaverse'}],
    ),
]

issue = {
    'site': site,
    'edition': {
        'id': DATE,
        'issueNumber': 19,
        'date': DATE,
        'displayDate': DISPLAY_DATE,
        'generatedAt': GENERATED_AT,
        'mode': 'manual-openclaw',
        'lead': 'openai-model-spec-public-framework',
        'i18n': {}
    },
    'sections': sections,
    'articles': articles,
}


def write_json(path: Path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def escape_xml(value: str) -> str:
    return (str(value)
            .replace('&', '&amp;')
            .replace('<', '&lt;')
            .replace('>', '&gt;')
            .replace('"', '&quot;')
            .replace("'", '&apos;'))


def render_rss(edition) -> str:
    items = []
    for art in edition['articles']:
        link = f"{BASE}/article.html?id={art['id']}"
        title = art['i18n']['zh-CN']['headline']
        description = '\n\n'.join([
            art['i18n']['zh-CN']['deck'],
            *art['i18n']['zh-CN']['summary'],
            art['i18n']['zh-CN']['significance'],
        ])
        pub_date = format_datetime(datetime.fromisoformat((art['updatedAt'] or art['publishedAt']).replace('Z', '+00:00')))
        items.append(
            f"    <item>\n"
            f"      <title>{escape_xml(title)}</title>\n"
            f"      <link>{escape_xml(link)}</link>\n"
            f"      <guid>{escape_xml(link)}</guid>\n"
            f"      <pubDate>{escape_xml(pub_date)}</pubDate>\n"
            f"      <description>{escape_xml(description)}</description>\n"
            f"    </item>"
        )
    build_date = format_datetime(datetime.fromisoformat(GENERATED_AT.replace('Z', '+00:00')))
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<rss version="2.0">\n'
        '  <channel>\n'
        '    <title>智潮 / Signal Tide</title>\n'
        f'    <link>{escape_xml(BASE + "/")}</link>\n'
        f'    <description>{escape_xml(site["description"]["zh-CN"])}</description>\n'
        '    <language>zh-CN</language>\n'
        f'    <lastBuildDate>{escape_xml(build_date)}</lastBuildDate>\n'
        + '\n'.join(items) + '\n'
        '  </channel>\n'
        '</rss>\n'
    )


write_json(DATA / 'issues.json', issue)
write_json(ARCHIVE / f'{DATE}.json', issue)

index_path = ARCHIVE / 'index.json'
index = json.loads(index_path.read_text(encoding='utf-8'))
items = [item for item in index['items'] if item['date'] != DATE]
items.insert(0, {
    'date': DATE,
    'displayDate': DISPLAY_DATE,
    'articleCount': len(articles),
    'leadId': issue['edition']['lead'],
    'leadHeadline': next(a['headline'] for a in articles if a['id'] == issue['edition']['lead']),
    'note': '保存当日首页版面与详情内容。'
})
index['generatedAt'] = GENERATED_AT
index['items'] = items
write_json(index_path, index)

(ROOT / 'docs' / 'rss.xml').write_text(render_rss(issue), encoding='utf-8')
print(f'Wrote {len(articles)} articles for {DATE}')
