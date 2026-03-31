from __future__ import annotations
import json
from pathlib import Path
from copy import deepcopy
from datetime import datetime, timezone
from email.utils import format_datetime
from xml.sax.saxutils import escape

ROOT = Path('/root/.openclaw/workspace/ai-news-pages-demo')
DATA = ROOT / 'docs' / 'data'
ARCHIVE = DATA / 'archive'
DOCS = ROOT / 'docs'
DATE = '2026-03-31'
DISPLAY_DATE = '2026年3月31日'
GENERATED_AT = '2026-03-31T02:00:00.000Z'
BASE = 'https://signaltide.ai'
ISSUE_NUMBER = 23

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
    return (text.replace('头版', '頭版')
                .replace('观察', '觀察')
                .replace('影响', '影響')
                .replace('技术人文', '技術人文')
                .replace('公司与产品', '公司與產品')
                .replace('政策与治理', '政策與治理')
                .replace('工具与开源', '工具與開源'))


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
        id='mistral-paris-data-center-debt',
        section='lead',
        category_cn='欧洲算力基础设施',
        category_en='European AI Infrastructure',
        headline_cn='Mistral 为巴黎数据中心举债 8.3 亿美元，欧洲 AI 终于开始为“自己造算力”真掏钱',
        headline_en='Mistral has borrowed $830 million for a Paris data center, showing Europe is finally paying real money for sovereign AI compute',
        deck_cn='这笔融资不是常规产品扩张，而是直接押注欧洲本土算力主权。Mistral 计划在巴黎附近建设由 Nvidia 芯片驱动的数据中心，并把“自主基础设施”从口号拉进资产负债表。',
        deck_en='This is not routine product financing but a direct bet on European compute sovereignty. Mistral plans to build an Nvidia-powered data center near Paris, turning talk of autonomous infrastructure into a balance-sheet commitment.',
        kicker_cn='头版',
        kicker_en='Lead',
        published_at='2026-03-30T12:49:51.000Z',
        reading_time=4,
        tags=['Mistral', 'Europe', 'Data Centers', 'NVIDIA'],
        summary_cn=[
            'TechCrunch 援引 Reuters 与 CNBC 报道称，法国模型公司 Mistral AI 已通过债务融资拿到 8.3 亿美元，用于在巴黎附近的 Bruyères-le-Châtel 建设新数据中心，并计划在 2026 年第二季度投入运行。公司还表示，目标是在 2027 年前于欧洲部署 200 兆瓦算力，并在不依赖第三方云厂商的前提下服务政府、企业和研究机构。',
            '它值得做头版，不只是因为金额大，而是因为这笔钱说明欧洲 AI 竞争开始从“有模型、有政策”走向“有地、有电、有芯片”。过去欧洲最常谈的是监管和价值观，如今 Mistral 直接把债务举到基础设施层，意味着所谓主权 AI 不再只是政治修辞，而是要承担真实资本成本、建设周期和运营风险的重资产生意。'
        ],
        summary_en=[
            'TechCrunch, citing Reuters and CNBC, reports that French lab Mistral AI has secured $830 million in debt financing to build a new data center in Bruyères-le-Châtel near Paris, aiming to have it operational in the second quarter of 2026. The company has also said it wants to deploy 200 megawatts of compute capacity across Europe by 2027 and support governments, enterprises, and research institutions without forcing them onto third-party clouds.',
            'The real significance is not only the financing size. It is that Europe’s AI race is shifting from having models and policy language to having land, power, and chips. Europe has spent years talking about sovereignty in abstract terms; Mistral is now financing that idea as hard infrastructure, with all the capital intensity and execution risk that implies.'
        ],
        bullets_cn=['Mistral 以债务方式筹得 8.3 亿美元建设巴黎附近数据中心。', '项目瞄准欧洲本土政府、企业与研究机构的定制算力需求。', '欧洲 AI 竞争开始真正进入重资产基础设施阶段。'],
        bullets_en=['Mistral has raised $830 million in debt for a data center near Paris.', 'The project targets sovereign compute demand from European governments, enterprises, and researchers.', 'Europe’s AI competition is entering a genuinely capital-intensive infrastructure phase.'],
        significance_cn='当欧洲开始为算力主权承担真金白银的利息，AI 竞争就不再只是模型榜单，而是国家级基础设施竞赛。',
        significance_en='Once Europe is willing to pay real interest costs for compute sovereignty, AI competition stops being only about model rankings and becomes an infrastructure contest.',
        sources=[
            {'title': 'Mistral AI raises $830M in debt to set up a data center near Paris', 'publication': 'TechCrunch', 'url': 'https://techcrunch.com/2026/03/30/mistral-ai-raises-830m-in-debt-to-set-up-a-data-center-near-paris/'},
            {'title': 'France’s Mistral raises debt for AI data centre build-up', 'publication': 'Reuters', 'url': 'https://www.reuters.com/business/finance/frances-mistral-raises-830-million-debt-ai-data-centre-build-up-2026-03-30/'}
        ],
    ),
    article(
        id='rebellions-pre-ipo-inference-push',
        section='company',
        category_cn='AI 芯片',
        category_en='AI Chips',
        headline_cn='韩国芯片公司 Rebellions 再拿 4 亿美元，推理基础设施开始被单独讲成一个故事',
        headline_en='Korean chip startup Rebellions has raised another $400 million, turning inference infrastructure into its own standalone story',
        deck_cn='这家 fabless 芯片公司在 IPO 前继续加速，估值达到约 23 亿美元，并同时推出 RebelRack 与 RebelPOD。重点已不只是“挑战英伟达”，而是把推理部署做成可卖的系统。',
        deck_en='The fabless chip company is accelerating ahead of an IPO at roughly a $2.3 billion valuation while launching RebelRack and RebelPOD. The emphasis is no longer only “challenging Nvidia,” but packaging inference deployment as a sellable system.',
        kicker_cn='公司',
        kicker_en='Company',
        published_at='2026-03-30T13:00:00.000Z',
        reading_time=3,
        tags=['Rebellions', 'Inference', 'Semiconductors', 'Korea'],
        summary_cn=[
            'TechCrunch 报道，韩国 AI 芯片创业公司 Rebellions 在计划年内 IPO 前又完成 4 亿美元融资，最新估值约 23.4 亿美元，过去 6 个月累计融资已达 6.5 亿美元。公司主打推理芯片，并在本轮同时发布 RebelRack 和 RebelPOD 两套基础设施产品，希望把单颗芯片能力打包成企业可直接部署的推理集群。',
            '这条消息重要，是因为“推理”现在越来越像一个独立市场，而不是训练赛道的附属品。模型部署走向大规模商用后，能耗、单位查询成本和系统可集成性，开始比单次峰值算力更值钱。Rebellions 的融资与新品发布，说明越来越多芯片创业公司不再只卖 silicon，而是在卖一整套现实世界里的吞吐与经济性。'
        ],
        summary_en=[
            'TechCrunch reports that South Korean AI chip startup Rebellions has raised another $400 million ahead of a planned IPO, putting its valuation at about $2.34 billion and bringing six-month fundraising to $650 million. The company focuses on inference chips and used the announcement to unveil RebelRack and RebelPOD, infrastructure products designed to package those chips into deployable enterprise-scale systems.',
            'The broader point is that inference is becoming a market in its own right rather than a side effect of training. As models move into commercial deployment, energy use, unit economics, and integration matter more than raw peak compute. Rebellions is therefore selling not just silicon, but an argument about usable throughput in the real world.'
        ],
        bullets_cn=['Rebellions 融资总额已达 8.5 亿美元。', '公司主攻推理芯片，并推出成套部署平台。', 'AI 芯片创业公司正从卖芯片转向卖完整基础设施。'],
        bullets_en=['Rebellions has now raised a total of $850 million.', 'The company is focused on inference chips and packaged deployment systems.', 'AI chip startups are moving from selling chips to selling full infrastructure stacks.'],
        significance_cn='下一代芯片竞争不只是谁最接近英伟达，而是谁最能把推理成本、功耗和集成难度一起打下来。',
        significance_en='The next wave of chip competition will depend not only on who can challenge Nvidia, but on who can lower inference cost, power use, and integration friction at the same time.',
        sources=[
            {'title': 'AI chip startup Rebellions raises $400 million at $2.3B valuation in pre-IPO round', 'publication': 'TechCrunch', 'url': 'https://techcrunch.com/2026/03/30/ai-chip-startup-rebellions-raises-400-million-at-2-3b-valuation-in-pre-ipo-round/'}
        ],
    ),
    article(
        id='openai-disaster-response-asia',
        section='company',
        category_cn='公共应用',
        category_en='Public Sector Applications',
        headline_cn='OpenAI 去曼谷办灾害响应训练营，模型公司开始把“国家项目”做成落地工作坊',
        headline_en='OpenAI has taken disaster-response training to Bangkok, turning “AI for countries” from a slogan into workshops on the ground',
        deck_cn='OpenAI 与盖茨基金会、亚洲防灾中心和 DataKind 在曼谷组织 13 国 50 位灾害管理者共创工作流。重点不是再讲 AI 前景，而是让一线机构直接做 situation reporting、needs assessment 和公共沟通。',
        deck_en='OpenAI, the Gates Foundation, the Asian Disaster Preparedness Center, and DataKind brought 50 disaster managers from 13 countries to Bangkok to co-build workflows. The shift is from talking about AI’s promise to deploying it into situation reports, needs assessment, and public communication.',
        kicker_cn='公司',
        kicker_en='Company',
        published_at='2026-03-29T22:15:00.000Z',
        reading_time=3,
        tags=['OpenAI', 'Disaster Response', 'Public Policy', 'Asia'],
        summary_cn=[
            'OpenAI 官方发文称，其在曼谷与盖茨基金会、亚洲防灾中心和 DataKind 合作举办首场面向灾害管理专业人员的 AI Jam，邀请来自南亚与东南亚 13 个国家的 50 位政府、非营利组织和多边机构代表，围绕定制 GPT、可复用工作流和负责任使用展开实操。文章还提到，在斯里兰卡与泰国的风暴和气旋期间，ChatGPT 内与灾害相关的消息量曾出现数倍到十几倍增长。',
            '这件事值得看，是因为模型公司正在从通用平台提供者转向“特定公共问题的工作流承包商”。过去 AI 公司最爱讲通用能力，现在则开始和灾害管理、教育、医疗等高约束领域的机构一起搭具体流程。真正的门槛不只是模型聪不聪明，而是它能不能嵌进资源紧张、责任明确、信息碎片化的一线治理现场。'
        ],
        summary_en=[
            'In an official post, OpenAI said it partnered with the Gates Foundation, the Asian Disaster Preparedness Center, and DataKind in Bangkok for its first AI Jam aimed at disaster-management professionals. Fifty participants from 13 countries across South and Southeast Asia worked on custom GPTs, reusable workflows, and responsible-use practices. OpenAI also noted sharp spikes in disaster-related ChatGPT usage during cyclone events in Sri Lanka and Thailand.',
            'What matters here is that model companies are shifting from generic platform providers to workflow vendors for specific public problems. AI firms used to talk mostly about broad capability; now they are entering highly constrained domains like disaster response with hands-on process design. The key test is not just whether a model is clever, but whether it can fit into frontline institutions with fragmented data, tight accountability, and limited resources.'
        ],
        bullets_cn=['OpenAI 在曼谷组织了面向灾害管理者的区域性 AI Jam。', '参与者来自 13 个国家，重点做实操工作流而不是概念演示。', '模型公司正更深地进入公共部门场景。'],
        bullets_en=['OpenAI held a regional AI Jam in Bangkok for disaster-management professionals.', 'Participants from 13 countries focused on operational workflows rather than concept demos.', 'Model companies are moving deeper into public-sector deployment.'],
        significance_cn='谁先把模型嵌进真实公共系统，谁就更有机会定义 AI 在国家治理里的默认位置。',
        significance_en='The companies that embed models into real public systems earliest may be the ones that define AI’s default role in state capacity.',
        sources=[
            {'title': 'Helping disaster response teams turn AI into action across Asia', 'publication': 'OpenAI', 'url': 'https://openai.com/index/helping-disaster-response-teams-asia'}
        ],
    ),
    article(
        id='starcloud-space-data-centers',
        section='company',
        category_cn='轨道算力',
        category_en='Orbital Compute',
        headline_cn='Starcloud 融到 1.7 亿美元要把数据中心送上天，地面电网焦虑终于催生了“太空算力”融资叙事',
        headline_en='Starcloud has raised $170 million to put data centers in orbit, showing grid anxiety on Earth is spawning a serious financing story around space compute',
        deck_cn='这家公司已经把搭载 H100 的卫星送上轨道，并瞄准更大的 Starcloud 2 与 Starcloud 3。商业模型仍然极冒险，但市场已经愿意为“把电力和散热问题搬离地球”下注。',
        deck_en='The company has already launched a satellite carrying an H100 and is building toward larger Starcloud 2 and Starcloud 3 systems. The business model remains risky, but investors are now willing to fund the idea of moving power and cooling constraints off Earth.',
        kicker_cn='公司',
        kicker_en='Company',
        published_at='2026-03-30T11:00:00.000Z',
        reading_time=3,
        tags=['Starcloud', 'Space', 'Data Centers', 'Compute'],
        summary_cn=[
            'TechCrunch 报道，Starcloud 完成 1.7 亿美元 A 轮融资，公司估值达到 11 亿美元，距其 YC demo day 仅 17 个月。公司已在 2025 年 11 月发射搭载 Nvidia H100 的卫星，后续还计划推出带 Blackwell 芯片和 AWS server blade 的 Starcloud 2，并为未来由 Starship 发射的大型轨道数据中心 Starcloud 3 铺路。',
            '今天把它放进公司栏目，不是因为“太空数据中心”听起来酷，而是因为它反映出地面算力扩张已经遇到真实摩擦：电力、土地、审批、社区阻力。只要这些问题持续存在，原本像科幻的方案就会被资本市场重新包装成下一层备选基础设施。离落地还很远，但融资叙事已经先成熟了。'
        ],
        summary_en=[
            'TechCrunch reports that Starcloud has raised a $170 million Series A at a $1.1 billion valuation just 17 months after its YC demo day. The company launched a satellite carrying an Nvidia H100 in late 2025 and plans larger follow-on systems, including Starcloud 2 with Blackwell hardware and Starcloud 3, a much bigger orbital data-center craft designed around future Starship launches.',
            'The reason to watch it is not simply the sci-fi angle. It shows that terrestrial compute expansion is hitting real friction in power, land, permitting, and community politics. As long as those constraints intensify, ideas that once sounded absurd can be reframed by investors as plausible second-layer infrastructure—even if the execution timeline remains long and fragile.'
        ],
        bullets_cn=['Starcloud 估值已达 11 亿美元。', '公司已验证把高性能 GPU 带上轨道的早期可行性。', '地面基础设施压力正在抬升“太空算力”想象空间。'],
        bullets_en=['Starcloud is now valued at $1.1 billion.', 'The company has already tested the early feasibility of putting high-performance GPUs in orbit.', 'Pressure on terrestrial infrastructure is expanding the appeal of space-compute narratives.'],
        significance_cn='当电网和土地成为 AI 的瓶颈，最疯狂的方案也会逐渐变成融资市场里的合理选项。',
        significance_en='Once power grids and land become AI bottlenecks, even the wildest compute proposals can start to look financeable.',
        sources=[
            {'title': 'Starcloud raises $170 million Series A to build data centers in space', 'publication': 'TechCrunch', 'url': 'https://techcrunch.com/2026/03/30/starcloud-raises-170-million-series-ato-build-data-centers-in-space/'}
        ],
    ),
    article(
        id='palantir-irs-snap-audits',
        section='policy',
        category_cn='政府审计自动化',
        category_en='Automated Government Audits',
        headline_cn='IRS 想让 Palantir 帮忙挑“最该查”的人，AI 税务执法正在从黑箱分数走向黑箱平台',
        headline_en='The IRS may use Palantir to help pick the “highest-value” audit targets, moving tax enforcement from one black box toward another',
        deck_cn='WIRED 通过公开记录披露，IRS 正测试由 Palantir 参与构建的 SNAP 平台，用于从上百个老旧系统中筛选高价值审计、追缴与刑事调查案件。效率问题正在变成问责问题。',
        deck_en='Through public-record requests, WIRED reveals that the IRS is testing Palantir’s SNAP platform to surface high-value audits, collections, and criminal investigations from more than a hundred legacy systems. An efficiency problem is turning into an accountability problem.',
        kicker_cn='政策',
        kicker_en='Policy',
        published_at='2026-03-30T09:30:00.000Z',
        reading_time=4,
        tags=['IRS', 'Palantir', 'Audits', 'Government AI'],
        summary_cn=[
            'WIRED 报道称，IRS 去年向 Palantir 支付 180 万美元，用于改进一套名为 SNAP（Selection and Analytic Platform）的定制工具，以帮助税务部门在超过 100 个业务系统和 700 种方法之间整合线索，筛出“最高价值”的审计、欠税追缴和潜在刑事调查目标。公开文件显示，平台目前仍处于试点，但已经被设计为从支持材料中的非结构化数据里提取线索。',
            '政策层面真正棘手的地方在于，这类系统会把“谁更值得被国家盯上”从分散规则、人工经验和传统分数模型，转移到更复杂的平台化筛选之中。问题不只是谁被查，更是谁能解释为什么被查。政府部门一旦以效率名义引入更强的分析平台，透明度、偏差纠正和外部监督就会被同时推上台面。'
        ],
        summary_en=[
            'WIRED reports that the IRS paid Palantir $1.8 million last year to improve a custom tool called SNAP, the Selection and Analytic Platform, which is meant to help the agency sift through more than 100 business systems and 700 methods to identify the “highest-value” targets for audits, unpaid-tax collection, and possible criminal investigations. Documents indicate the system is still in pilot mode but is already designed to draw signals from unstructured supporting documents.',
            'The hard policy question is that systems like this shift “who deserves state scrutiny” from scattered rules, human judgment, and older scoring systems into more complex platform logic. The issue is not only who gets flagged, but who can explain why. Once governments import more powerful analytic layers in the name of efficiency, transparency, bias correction, and external oversight all become unavoidable.'
        ],
        bullets_cn=['IRS 正试点由 Palantir 参与构建的 SNAP 审计筛选平台。', '平台目标是整合海量旧系统并从非结构化材料中找线索。', '税务自动化的核心争议将从效率转向可解释性与监督。'],
        bullets_en=['The IRS is piloting SNAP, an audit-selection platform built with Palantir.', 'The system aims to unify legacy data and extract signals from unstructured materials.', 'The key controversy in tax automation is shifting from efficiency to explainability and oversight.'],
        significance_cn='当国家开始用更强平台判断“该查谁”，算法治理就不再是互联网公司的问题，而是公权力的基本问题。',
        significance_en='Once the state starts using stronger platforms to decide who deserves scrutiny, algorithmic governance stops being only a Big Tech issue and becomes a core public-power issue.',
        sources=[
            {'title': 'The IRS Wants Smarter Audits. Palantir Could Help Decide Who Gets Flagged', 'publication': 'WIRED', 'url': 'https://www.wired.com/story/documents-reveal-palantir-irs-contract-fraud-clean-energy-credits/'}
        ],
    ),
    article(
        id='anthropic-pentagon-culture-war-backfire',
        section='policy',
        category_cn='政府采购纠纷',
        category_en='Government Procurement Dispute',
        headline_cn='五角大楼对 Anthropic 的文化战争打过头了：一场合同纠纷被法官看成了公开惩罚',
        headline_en='The Pentagon pushed its culture-war fight with Anthropic too far, and a contract dispute started to look like public punishment',
        deck_cn='MIT Technology Review 梳理法官意见指出，政府一边在社交媒体上高调定性 Anthropic，一边又在法庭上承认不少说法没有法律效力。AI 采购争端正在直接碰到宪法边界。',
        deck_en='MIT Technology Review’s reading of the judge’s opinion shows a government that loudly attacked Anthropic online while admitting in court that several claims had no legal force. AI procurement fights are now running into constitutional limits.',
        kicker_cn='政策',
        kicker_en='Policy',
        published_at='2026-03-30T15:42:50.000Z',
        reading_time=4,
        tags=['Anthropic', 'Pentagon', 'Procurement', 'First Amendment'],
        summary_cn=[
            'MIT Technology Review 根据最新法院文件指出，联邦法官暂时阻止了五角大楼将 Anthropic 认定为供应链风险，并认为政府的公开表态与正式程序之间存在明显错位。报道梳理称，特朗普与国防部长此前在社交媒体上先行对 Anthropic 发难，但政府律师后来又承认部分表述并无法律效力，且对所谓“kill switch”等关键说法缺乏证据支持。',
            '这让事件的意义超过普通采购争议。政府当然可以选择不买谁的产品，但如果它因为企业坚持某些用途红线而公开施压、污名化甚至试图行业封杀，争议就会从商业关系升级为言论、程序与权力边界问题。AI 军采的下一阶段，恐怕会越来越像宪法课，而不只是招投标。'
        ],
        summary_en=[
            'MIT Technology Review, drawing on recent court filings, says the federal judge who temporarily blocked the Pentagon’s supply-chain-risk move against Anthropic saw a major disconnect between the government’s public rhetoric and the formal procedures it was supposed to follow. The reporting emphasizes how Trump and Defense Secretary Pete Hegseth attacked Anthropic on social media first, while government lawyers later conceded that some of those statements had no legal effect and lacked evidence behind claims such as a supposed “kill switch.”',
            'That pushes the case beyond a normal procurement dispute. Governments can choose whom not to buy from, but once officials publicly pressure and stigmatize a company for maintaining certain red lines, the fight turns into one about speech, procedure, and the limits of state power. The next phase of military AI procurement may look as much like constitutional law as contracting.'
        ],
        bullets_cn=['法院认为政府公开表态与正式程序明显脱节。', '关键指控如“kill switch”被指缺乏证据。', 'AI 军采正在进入更强的法律与程序审查。'],
        bullets_en=['The court saw a clear gap between public rhetoric and formal procedure.', 'Key allegations such as a supposed “kill switch” were said to lack evidence.', 'Military AI procurement is entering a deeper era of legal and procedural scrutiny.'],
        significance_cn='如果政府不能随意用意识形态语言打击模型供应商，AI 治理里“谁能说不”这件事就会被重新定义。',
        significance_en='If the government cannot casually use ideological punishment against model suppliers, AI governance will have to rethink who gets to say no and still remain in the market.',
        sources=[
            {'title': 'The Pentagon’s culture war tactic against Anthropic has backfired', 'publication': 'MIT Technology Review', 'url': 'https://www.technologyreview.com/2026/03/30/1134881/the-pentagons-culture-war-tactic-against-anthropic-has-backfired/'},
            {'title': 'Judge sides with Anthropic to temporarily block the Pentagon’s ban', 'publication': 'The Verge', 'url': 'https://www.theverge.com/ai-artificial-intelligence/902149/anthropic-dod-pentagon-lawsuit-supply-chain-risk-injunction'}
        ],
    ),
    article(
        id='qodo-code-verification-series-b',
        section='tools',
        category_cn='代码验证',
        category_en='Code Verification',
        headline_cn='AI 写代码越多，Qodo 就越敢卖“验代码”——验证层开始从配角变主角',
        headline_en='As AI writes more code, Qodo is betting that verification—not generation—becomes the main event',
        deck_cn='Qodo 完成 7000 万美元 B 轮融资，主打代码审查、测试与治理代理。行业开始承认，生成速度上去以后，真正稀缺的是组织上下文里的可信交付。',
        deck_en='Qodo has raised a $70 million Series B for agents focused on review, testing, and governance. The market is starting to admit that once generation gets fast, trusted delivery inside real organizational context becomes scarce.',
        kicker_cn='工具',
        kicker_en='Tools',
        published_at='2026-03-30T12:30:00.000Z',
        reading_time=3,
        tags=['Qodo', 'Code Review', 'AI Coding', 'Verification'],
        summary_cn=[
            'TechCrunch 报道，Qodo 完成由 Qumra Capital 领投的 7000 万美元 B 轮融资，累计融资达到 1.2 亿美元。公司定位不是继续加速代码生成，而是通过多代理系统做代码审查、测试与治理，并强调质量判断必须结合组织标准、历史决策与“部落知识”，单靠 LLM 本身并不够。文章还提到，Qodo 近期在 Martian 的 Code Review Bench 上拿到第一。',
            '这很能代表 AI 编程进入的新阶段：生成正在快速商品化，验证和责任反而变成新瓶颈。企业并不缺一段“看起来能跑”的代码，缺的是知道哪些改动会引入跨文件 bug、哪些风险不符合公司规范、哪些输出能安全进入生产。谁掌握验证层，谁就更接近真正的开发工作流入口。'
        ],
        summary_en=[
            'TechCrunch reports that Qodo has raised a $70 million Series B led by Qumra Capital, bringing total funding to $120 million. Rather than focusing on faster code generation, the company is building multi-agent systems for code review, testing, and governance, arguing that software quality depends on organizational standards, prior decisions, and tribal knowledge that raw LLM capability alone cannot capture. The report also notes Qodo’s recent top ranking on Martian’s Code Review Bench.',
            'This captures the next phase of AI coding. Generation is rapidly commoditizing, while verification and responsibility are becoming the bottleneck. Enterprises do not mainly lack code that “looks runnable”; they lack confidence about cross-file bugs, policy fit, and safe production readiness. Whoever controls the verification layer gets much closer to the real development workflow.'
        ],
        bullets_cn=['Qodo 融资 7000 万美元，累计融资达 1.2 亿美元。', '公司强调生成与验证需要不同系统与思路。', 'AI 编程竞争正在向测试、治理与可信交付迁移。'],
        bullets_en=['Qodo has raised $70 million, bringing total funding to $120 million.', 'The company argues that generation and verification require different systems and mindsets.', 'AI coding competition is shifting toward testing, governance, and trusted delivery.'],
        significance_cn='编程代理真正的护城河，可能不是写得多快，而是错得多慢、审得多准。',
        significance_en='The real moat in coding agents may not be how fast they write, but how slowly they fail and how accurately they review.',
        sources=[
            {'title': 'Qodo raises $70M for code verification as AI coding scales', 'publication': 'TechCrunch', 'url': 'https://techcrunch.com/2026/03/30/qodo-bets-on-code-verification-as-ai-coding-scales-raises-70m/'}
        ],
    ),
    article(
        id='scaleops-autonomous-kubernetes',
        section='tools',
        category_cn='基础设施自动化',
        category_en='Infrastructure Automation',
        headline_cn='ScaleOps 融到 1.3 亿美元，不是因为大家缺 GPU，而是因为大家不会管 GPU',
        headline_en='ScaleOps raised $130 million on the thesis that the problem is not a GPU shortage but GPU mismanagement',
        deck_cn='这家公司要做的是实时重分配计算、内存、存储和网络资源，把 Kubernetes 的静态配置问题交给更自动化的控制层。AI 基础设施越来越像运营问题，而不是采购问题。',
        deck_en='The company wants to reallocate compute, memory, storage, and network resources in real time, adding an autonomous control layer on top of Kubernetes’ static configuration model. AI infrastructure is becoming an operations problem, not just a procurement problem.',
        kicker_cn='工具',
        kicker_en='Tools',
        published_at='2026-03-30T13:52:02.000Z',
        reading_time=3,
        tags=['ScaleOps', 'Kubernetes', 'Cloud', 'GPU'],
        summary_cn=[
            'TechCrunch 报道，ScaleOps 完成 1.3 亿美元 C 轮融资，估值 8 亿美元。公司认为，在 AI 推动下企业并不是单纯缺算力，而是普遍在浪费算力：GPU 闲置、工作负载过度配置、Kubernetes 依赖静态参数难以跟上动态需求。其产品希望自动连接应用上下文与底层资源决策，做出更接近“自治基础设施”的运行方式。',
            '这条新闻的信号很直接：围绕 AI 的下一批大机会，很多并不发生在模型层，而发生在基础设施运维层。谁能把 GPU、内存、网络和存储更细地调度起来，谁就能在同一批硬件上挤出更多生产力。算力时代真正贵的不只是芯片，还有不会用芯片造成的浪费。'
        ],
        summary_en=[
            'TechCrunch reports that ScaleOps has raised a $130 million Series C at an $800 million valuation. The company’s pitch is that AI-era organizations are not simply short on compute; they are wasting it through idle GPUs, overprovisioned workloads, and Kubernetes configurations that remain too static for rapidly changing demand. ScaleOps wants to connect application context to infrastructure decisions and automate the full resource-management loop.',
            'The broader signal is that many of the next big AI opportunities sit below the model layer, in operations. The teams that can schedule GPUs, memory, storage, and networking more intelligently will extract more output from the same hardware base. In the compute era, one of the most expensive things is not chips themselves but the waste created by managing them poorly.'
        ],
        bullets_cn=['ScaleOps C 轮融资 1.3 亿美元，估值 8 亿美元。', '公司主打对 Kubernetes 与 AI 负载的自治化资源管理。', '基础设施调度正在成为 AI 时代的重要软件层。'],
        bullets_en=['ScaleOps raised $130 million in Series C funding at an $800 million valuation.', 'The company focuses on autonomous resource management for Kubernetes and AI workloads.', 'Infrastructure scheduling is becoming a key software layer in the AI era.'],
        significance_cn='算力大战越激烈，越说明会调度的人比会喊缺货的人更值钱。',
        significance_en='The more intense the compute race becomes, the more valuable scheduling intelligence looks compared with simply shouting about shortages.',
        sources=[
            {'title': 'ScaleOps raises $130M to improve computing efficiency amid AI demand', 'publication': 'TechCrunch', 'url': 'https://techcrunch.com/2026/03/30/scaleops-130m-series-c-kubernetes-efficiency-ai-demand-funding/'}
        ],
    ),
    article(
        id='ollama-mlx-apple-preview',
        section='tools',
        category_cn='本地推理',
        category_en='Local Inference',
        headline_cn='Ollama 改用 MLX 跑苹果芯片，本地代理终于开始认真追逐“响应速度”',
        headline_en='Ollama is shifting to MLX on Apple silicon, showing local-agent tooling is finally taking responsiveness seriously',
        deck_cn='Ollama 预览版改由 Apple 的 MLX 框架驱动，配合 NVFP4 与缓存改进，目标很明确：让 OpenClaw、Claude Code 这类本地代理更像“能工作”的系统，而不是玩具。',
        deck_en='Ollama’s preview build is now powered by Apple’s MLX framework, alongside NVFP4 and cache upgrades. The target is clear: make local agents such as OpenClaw and Claude Code feel like working systems rather than toys.',
        kicker_cn='工具',
        kicker_en='Tools',
        published_at='2026-03-30T00:00:00.000Z',
        reading_time=3,
        tags=['Ollama', 'MLX', 'Apple Silicon', 'Local Models'],
        summary_cn=[
            'Ollama 官方宣布其 Apple Silicon 预览版现改由 Apple 的 MLX 框架驱动，并强调在 M5、M5 Pro 与 M5 Max 上能明显改善首 token 延迟与生成速度。文章还介绍了对 NVFP4 格式的支持，以及针对多轮对话与编码代理场景优化的缓存复用、智能 checkpoint 与更聪明的 eviction 机制。',
            '这件事看似是性能更新，实则说明本地模型生态终于开始围绕“代理工作流”做系统优化。过去很多本地部署更像炫技演示；一旦进入编码、工具调用和长 prompt 的真实使用，响应速度和缓存命中才决定体验。谁能把本地推理做得更快、更稳、更接近生产环境，谁就更有机会承接私有化代理的需求。'
        ],
        summary_en=[
            'Ollama says its Apple Silicon preview is now powered by Apple’s MLX framework and promises major gains in time to first token and generation speed on M5-class chips. The post also highlights support for NVFP4 and upgrades to cache reuse, intelligent checkpoints, and eviction policies for coding and agentic workloads.',
            'This may look like a performance note, but it signals something larger: the local-model ecosystem is optimizing around real agent workflows now. Many local deployments used to be impressive demos; once coding, tool use, and long prompts enter the picture, responsiveness and cache behavior determine whether the system feels usable. Faster and more production-like local inference matters because that is what private agent deployment will demand.'
        ],
        bullets_cn=['Ollama 在 Apple Silicon 上切换到 MLX 驱动。', '新版本强调 NVFP4 与缓存优化对代理任务的价值。', '本地模型生态正在转向真实工作流优化。'],
        bullets_en=['Ollama has moved to MLX on Apple silicon.', 'The preview emphasizes NVFP4 and cache optimizations for agent workloads.', 'The local-model ecosystem is shifting toward real workflow optimization.'],
        significance_cn='本地 AI 的下一道门槛不再只是“能跑”，而是“跑起来像不像真的助手”。',
        significance_en='The next threshold for local AI is no longer merely whether it runs, but whether it runs like a real assistant.',
        sources=[
            {'title': 'Ollama is now powered by MLX on Apple Silicon in preview', 'publication': 'Ollama Blog', 'url': 'https://ollama.com/blog/mlx'}
        ],
    ),
    article(
        id='ai-trust-adoption-gap-quinnipiac',
        section='impact',
        category_cn='社会态度',
        category_en='Public Sentiment',
        headline_cn='美国人一边更常用 AI，一边更不信它：采用曲线开始和信任曲线背道而驰',
        headline_en='Americans are using AI more while trusting it less, and the adoption curve is starting to diverge from the trust curve',
        deck_cn='Quinnipiac 民调显示，日常使用 AI 的美国人继续增加，但 76% 的受访者仍表示只会很少或偶尔信任 AI 结果。大规模使用，并没有自动换来社会接受。',
        deck_en='A Quinnipiac poll shows that everyday AI use in the US keeps rising, yet 76 percent of respondents still say they trust AI only rarely or sometimes. Mass usage is not automatically converting into social legitimacy.',
        kicker_cn='影响',
        kicker_en='Impact',
        published_at='2026-03-30T20:24:53.000Z',
        reading_time=4,
        tags=['Polls', 'Trust', 'Jobs', 'Public Opinion'],
        summary_cn=[
            'TechCrunch 报道，Quinnipiac 发布的最新民调显示，只有 27% 的美国受访者从未使用过 AI，较 2025 年下降，但高达 76% 的人表示他们只会很少或偶尔信任 AI 结果，仅 21% 表示大多数时间或几乎总是信任。受访者还普遍担忧 AI 对工作岗位和日常生活的负面影响，并对本地建设 AI 数据中心持明显反对态度。',
            '这组数据值得放在“影响”栏目，因为它提醒人们：AI 的社会扩散并不会自动带来稳定信任。很多人已经把 AI 当作一个不得不用的工具，而不是一个真心认可的系统。也就是说，产品渗透率和政治、文化、就业层面的可接受性，可能会越来越脱钩。'
        ],
        summary_en=[
            'TechCrunch reports that the latest Quinnipiac poll found only 27 percent of Americans say they have never used AI, down from last year, while 76 percent say they trust AI results only rarely or sometimes and just 21 percent say they trust them most or almost all of the time. Respondents also expressed broad concern about jobs, day-to-day harm, and the prospect of AI data centers in their communities.',
            'This belongs in the impact section because it shows that social diffusion does not automatically create trust. Many people are already using AI as a tool they feel compelled to use, not as a system they genuinely endorse. Adoption rates and political, cultural, and labor-market legitimacy may increasingly move on separate tracks.'
        ],
        bullets_cn=['美国 AI 使用率继续上升，但信任度并未同步上升。', '多数受访者担忧 AI 减少工作机会并反对本地数据中心。', '社会接受度与产品渗透率正在明显脱钩。'],
        bullets_en=['AI usage in the US is rising, but trust is not rising with it.', 'Most respondents worry about fewer jobs and oppose local AI data centers.', 'Social acceptance is diverging from product penetration.'],
        significance_cn='当人们带着不信任继续使用 AI，行业面对的就不是教育问题，而是合法性问题。',
        significance_en='When people keep using AI despite distrusting it, the industry is no longer dealing only with education problems but with legitimacy problems.',
        sources=[
            {'title': 'As more Americans adopt AI tools, fewer say they can trust the results', 'publication': 'TechCrunch', 'url': 'https://techcrunch.com/2026/03/30/ai-trust-adoption-poll-more-americans-adopt-tools-fewer-say-they-can-trust-the-results/'},
            {'title': 'Quinnipiac University Poll Release', 'publication': 'Quinnipiac University', 'url': 'https://poll.qu.edu/poll-release?releaseid=3955'}
        ],
    ),
    article(
        id='ai-health-tools-evaluation-gap',
        section='impact',
        category_cn='医疗 AI',
        category_en='Health AI',
        headline_cn='面向大众的 AI 健康助手越来越多，但独立评测还没跟上',
        headline_en='Consumer health AI tools are proliferating faster than independent evaluation can keep up',
        deck_cn='微软、亚马逊、OpenAI 等公司都在把健康问答助手推向大众，MIT Technology Review 则追问：这些系统到底经过了多少第三方、面向真实用户的安全检验？',
        deck_en='Microsoft, Amazon, OpenAI, and others are pushing health assistants to mass users, while MIT Technology Review asks a harder question: how much third-party, real-user safety testing have these systems actually undergone?',
        kicker_cn='影响',
        kicker_en='Impact',
        published_at='2026-03-30T16:00:00.000Z',
        reading_time=4,
        tags=['Health AI', 'Evaluation', 'Microsoft', 'OpenAI'],
        summary_cn=[
            'MIT Technology Review 报道，随着微软 Copilot Health、Amazon Health AI、ChatGPT Health 等面向普通用户的产品密集上线，医学研究者越来越担心这些系统在诊断、分诊和治疗建议等高风险场景中的真实可靠性。文章回顾了 Mount Sinai 团队等外部研究对 ChatGPT Health 的担忧，也指出 OpenAI 的 HealthBench 等内部评测虽然重要，但仍难替代第三方、面向真实用户的实验。',
            '这里最关键的冲突在于：需求是真的，风险也是真的。医疗体系的访问门槛和等待成本，确实让很多人愿意先问 AI；但如果缺少独立验证，所谓“更可及”也可能只是把不确定性更大规模地分发给普通人。健康 AI 的成败，不会只由模型分数决定，而会由谁来审、怎么审、上线前有没有外部证据决定。'
        ],
        summary_en=[
            'MIT Technology Review reports that as products like Microsoft Copilot Health, Amazon Health AI, and ChatGPT Health move into the mainstream, researchers are increasingly worried about how reliable these systems are in high-stakes tasks such as diagnosis, triage, and treatment guidance. The article revisits external research, including concerns raised by Mount Sinai teams, and argues that internal benchmarks like OpenAI’s HealthBench—while useful—cannot replace third-party testing with real users.',
            'The central tension is that the demand is real and the risk is real. Health systems are difficult to access, which pushes people toward AI by necessity. But without independent evaluation, “greater access” may simply mean distributing uncertainty at scale. The fate of health AI will be shaped not just by model scores, but by who evaluates it, how it is evaluated, and whether credible outside evidence exists before release.'
        ],
        bullets_cn=['面向大众的健康 AI 产品正在快速上线。', '外部研究者呼吁更多真实用户、第三方评测。', '健康 AI 的关键门槛正在从能力转向证据。'],
        bullets_en=['Consumer-facing health AI products are launching quickly.', 'External researchers want more real-user and third-party evaluation.', 'The key threshold in health AI is shifting from capability to evidence.'],
        significance_cn='医疗场景里最危险的，不一定是模型不够聪明，而是它足够聪明到让人以为已经可以放心相信。',
        significance_en='In health settings, the most dangerous thing may not be that a model is too weak, but that it is strong enough to invite misplaced confidence.',
        sources=[
            {'title': 'There are more AI health tools than ever—but how well do they work?', 'publication': 'MIT Technology Review', 'url': 'https://www.technologyreview.com/2026/03/30/1134795/there-are-more-ai-health-tools-than-ever-but-how-well-do-they-work/'}
        ],
    ),
    article(
        id='asgardbench-visual-plan-adaptation',
        section='impact',
        category_cn='具身智能评测',
        category_en='Embodied AI Evaluation',
        headline_cn='AsgardBench 专门测机器人会不会“看到变化就改计划”，具身智能终于被拉回现实难题',
        headline_en='AsgardBench measures whether robots revise plans when the world changes, bringing embodied AI back to a more realistic difficulty',
        deck_cn='Microsoft Research 新基准覆盖 12 类任务、108 个实例，刻意压低环境反馈，逼智能体靠图像与最少成败信号持续更新动作计划。问题不再是会不会写计划，而是会不会改计划。',
        deck_en='Microsoft Research’s new benchmark spans 12 task types and 108 instances while minimizing environmental feedback, forcing agents to update plans from images and sparse success signals. The question is no longer whether they can write a plan, but whether they can revise one.',
        kicker_cn='影响',
        kicker_en='Impact',
        published_at='2026-03-26T19:02:53.000Z',
        reading_time=3,
        tags=['Microsoft Research', 'Embodied AI', 'Benchmark', 'Planning'],
        summary_cn=[
            'Microsoft Research 发布 AsgardBench，建立在 AI2-THOR 环境上，专门隔离“视觉驱动的交互式规划”能力。基准让智能体在看到图像并收到简单的成功/失败信号后，每一步都重新提出完整动作序列，但只执行第一步，以此检验它是否真的会根据新观察持续修订计划，而不是预先背好脚本。',
            '这项工作的价值，在于它把机器人评测从“看起来完成任务了”往“到底是不是靠看见变化来做决定”推进了一步。现实世界里最难的，从来不是完美环境中的第一份计划，而是计划在脏乱、意外和状态变化里是否还会更新。具身智能越接近现实，越需要这种专测临场反应的基准。'
        ],
        summary_en=[
            'Microsoft Research has introduced AsgardBench on top of AI2-THOR to isolate visually grounded interactive planning. Agents receive images and minimal success-or-failure signals, must propose a full plan at every step, but can execute only the first action—forcing them to revise continuously rather than rely on a prewritten script.',
            'The value of the benchmark is that it pushes robot evaluation from “the task got done somehow” toward “did the system actually use changing visual evidence to decide what to do next?” In the real world, the hardest part is rarely producing an initial plan in a clean environment; it is updating that plan amid clutter, surprises, and shifting object states. Embodied AI will need benchmarks that stress that reflex directly.'
        ],
        bullets_cn=['AsgardBench 专测视觉驱动的交互式规划。', '基准通过最少反馈逼智能体持续重写计划。', '具身智能评测开始更重视临场适应能力。'],
        bullets_en=['AsgardBench focuses specifically on visually grounded interactive planning.', 'The benchmark uses sparse feedback to force continual replanning.', 'Embodied AI evaluation is placing more weight on adaptation under changing conditions.'],
        significance_cn='机器人真正难学的不是动作列表，而是“看到不对劲时立刻改主意”的能力。',
        significance_en='What robots most need to learn is not a static action list, but the ability to change their minds the moment the world looks different.',
        sources=[
            {'title': 'AsgardBench: A benchmark for visually grounded interactive planning', 'publication': 'Microsoft Research', 'url': 'https://www.microsoft.com/en-us/research/blog/asgardbench-a-benchmark-for-visually-grounded-interactive-planning/'}
        ],
    ),
    article(
        id='litellm-drops-delve-compliance',
        section='insight',
        category_cn='合规信任链',
        category_en='Compliance Trust Chains',
        headline_cn='LiteLLM 火速切割 Delve：AI 创业公司的“合规外包”开始暴露成新的供应链风险',
        headline_en='LiteLLM is cutting ties with Delve, exposing outsourced compliance as a new supply-chain risk for AI startups',
        deck_cn='在开源版本遭遇窃取凭证恶意软件后，LiteLLM 宣布重做安全认证并更换审计路径。合规这件事，正在从销售证明变成反噬点。',
        deck_en='After malware hit its open-source version, LiteLLM said it would redo its security certifications and switch auditors. Compliance is starting to look less like a sales badge and more like a point of failure.',
        kicker_cn='观察',
        kicker_en='Deep Insights',
        published_at='2026-03-30T23:08:12.000Z',
        reading_time=2,
        tags=['LiteLLM', 'Compliance', 'Security', 'Delve'],
        summary_cn=[
            'TechCrunch 报道，AI gateway 创业公司 LiteLLM 已公开宣布放弃与合规创业公司 Delve 的合作，并将改由 Vanta 重新做安全认证，同时寻找独立第三方审计。背景是 LiteLLM 的开源版本此前遭遇凭证窃取恶意软件事件，而 Delve 又被匿名举报存在伪造合规数据、配合宽松审计等问题，尽管其创始人否认了指控。',
            '这条消息之所以值得放进“深度观察”，是因为它揭开了 AI 初创常见却少被正面讨论的一层：很多公司把合规当成增长环节里最快补上的一张证明，但一旦外包链条本身不可靠，所谓“通过认证”反而可能制造更大的虚假安全感。AI 供应链风险并不只在模型和依赖库，也在审计和认证服务本身。'
        ],
        summary_en=[
            'TechCrunch reports that AI gateway startup LiteLLM has publicly cut ties with compliance startup Delve and will redo its security certifications with Vanta while seeking an independent third-party auditor. The move follows a credential-stealing malware incident in LiteLLM’s open-source version and broader allegations that Delve misrepresented compliance work and relied on rubber-stamp auditing, claims its founder denies.',
            'This belongs in deep insights because it highlights a quieter structural issue in the AI startup stack. Many companies treat compliance as a fast-moving growth checkbox, but if the outsourced trust chain itself is weak, passing an audit may create more false confidence than safety. Supply-chain risk in AI does not exist only in models and software dependencies; it also lives inside certification and audit vendors.'
        ],
        bullets_cn=['LiteLLM 将重做安全认证并更换合规供应商。', 'Delve 同时陷入被指“假合规”的争议。', 'AI 公司的信任链风险开始延伸到审计与认证环节。'],
        bullets_en=['LiteLLM will redo its security certifications with a new vendor.', 'Delve is facing allegations around “fake compliance.”', 'Trust-chain risk in AI companies now extends into auditing and certification vendors.'],
        significance_cn='如果合规证明本身都要被审，AI 行业下一轮竞争就会开始重建“谁来担保担保人”的机制。',
        significance_en='If compliance certifications themselves require verification, the next phase of AI trust infrastructure will be about who validates the validators.',
        sources=[
            {'title': 'Popular AI gateway startup LiteLLM ditches controversial startup Delve', 'publication': 'TechCrunch', 'url': 'https://techcrunch.com/2026/03/30/popular-ai-gateway-startup-litellm-ditches-controversial-startup-delve/'}
        ],
    ),
    article(
        id='okta-agent-identity-shift',
        section='insight',
        category_cn='代理身份',
        category_en='Agent Identity',
        headline_cn='Okta 盯上“AI 代理身份”：企业真正害怕的不是代理不聪明，而是代理像员工一样有权限',
        headline_en='Okta is betting on “AI agent identity,” because the real enterprise fear is not that agents are dumb but that they act like employees with privileges',
        deck_cn='The Verge 对 Okta CEO Todd McKinnon 的访谈把问题说得很直白：当代理开始代表人登录、调系统、拿数据时，身份与权限管理就不再只是人和机器账户的问题。',
        deck_en='The Verge’s interview with Okta CEO Todd McKinnon states the problem plainly: once agents log in, call systems, and access data on behalf of humans, identity management stops being only about people and machine accounts.',
        kicker_cn='观察',
        kicker_en='Deep Insights',
        published_at='2026-03-30T15:15:00.000Z',
        reading_time=3,
        tags=['Okta', 'Identity', 'Agents', 'Security'],
        summary_cn=[
            '在 The Verge 的 Decoder 访谈里，Okta CEO Todd McKinnon 将“agent identity”描述成介于人和系统之间的新对象：它会代表员工访问工具、调用服务、接触敏感数据，因此不能继续用传统 SaaS 身份管理思路对待。McKinnon 同时把 AI 时代的软件竞争描述为一种新的“Saaspocalypse”，但认为安全和基础设施软件的护城河会更多来自连接能力、稳定性和责任归属。',
            '这条访谈真正有意思的是，它说明企业 AI 的关键控制面正在迁移。过去大家管理的是员工、设备和服务账号；接下来管理的会是能代替员工行动的代理。只要代理被纳入组织流程，权限边界、追责路径、撤销机制和“kill switch”都会变成核心产品，而不是补丁。'
        ],
        summary_en=[
            'In The Verge’s Decoder interview, Okta CEO Todd McKinnon describes “agent identity” as a new class of entity sitting somewhere between a person and a system account. These agents can log into tools, invoke services, and touch sensitive data on behalf of employees, which means traditional SaaS-era identity models may no longer be enough. McKinnon also framed the AI era as a kind of new SaaSpocalypse, while arguing that security and infrastructure moats still depend on connectivity, reliability, and accountability.',
            'What makes the discussion important is that it identifies a shift in the enterprise control surface. Organizations used to manage employees, devices, and service accounts; soon they will be managing agents that act like delegated coworkers. Once that happens, permission boundaries, revocation, auditability, and kill switches become core product features rather than afterthoughts.'
        ],
        bullets_cn=['Okta 把“代理身份”视为新的企业级安全对象。', 'AI 代理将带来新的权限、撤销与追责问题。', '企业 AI 的控制面正在从人扩展到代表人行动的代理。'],
        bullets_en=['Okta sees “agent identity” as a new enterprise security object.', 'AI agents create new problems around permissions, revocation, and accountability.', 'The enterprise control surface is expanding from humans to delegated agents.'],
        significance_cn='谁定义代理身份，谁就更可能定义下一代企业软件的默认安全边界。',
        significance_en='Whoever defines agent identity may end up defining the default security boundary of next-generation enterprise software.',
        sources=[
            {'title': 'Okta’s CEO is betting big on AI agent identity', 'publication': 'The Verge', 'url': 'https://www.theverge.com/podcast/902264/oktas-ceo-is-betting-big-on-ai-agent-identity'}
        ],
    ),
    article(
        id='mantis-biotech-digital-twins',
        section='insight',
        category_cn='数字孪生人体',
        category_en='Human Digital Twins',
        headline_cn='Mantis 想造“人体数字孪生”，AI 医疗数据稀缺问题开始被重新定义成模拟问题',
        headline_en='Mantis wants to build “digital twins” of the human body, reframing medical data scarcity as a simulation problem',
        deck_cn='这家创业公司把 LLM、物理引擎和多源数据拼在一起，希望生成高保真的人体数字孪生，用于 rare disease、手术机器人和药物试验等难拿数据的场景。',
        deck_en='The startup combines LLM routing, physics engines, and multi-source data to generate high-fidelity human digital twins for rare diseases, surgical robotics, and drug-trial scenarios where real data is hard to obtain.',
        kicker_cn='观察',
        kicker_en='Deep Insights',
        published_at='2026-03-30T14:30:00.000Z',
        reading_time=3,
        tags=['Mantis Biotech', 'Digital Twins', 'Synthetic Data', 'Healthcare'],
        summary_cn=[
            'TechCrunch 报道，Mantis Biotech 正利用教材、动作捕捉、传感器、训练日志和医学影像等多源数据，配合 LLM 做路由和校验，再借助物理引擎生成高保真的“人体数字孪生”，以补足罕见病、边缘病例和伦理限制场景中的数据稀缺问题。公司认为这套系统可用于手术机器人训练、运动员伤病预测、药物试验与更广泛的生物医学研究，并已拿到 740 万美元种子轮融资。',
            '它之所以值得观察，是因为医疗 AI 也许会越来越少地向现实世界“索取更多数据”，而越来越多地转向“能否先模拟出足够可信的身体”。一旦这个方向成立，数据瓶颈会被重写成物理建模、校准质量和合成数据可信度的问题。AI 医疗的竞争，也就会从数据独占逐渐转向世界建模能力。'
        ],
        summary_en=[
            'TechCrunch reports that Mantis Biotech is combining textbooks, motion capture, sensors, training logs, and medical imaging with LLM-based routing and validation plus a physics engine to create high-fidelity “digital twins” of the human body. The company argues that this can fill data gaps in rare diseases, edge cases, and privacy-constrained settings, and support use cases such as surgical-robot training, athlete injury prediction, and pharmaceutical research. It recently raised a $7.4 million seed round.',
            'The reason it belongs in deep insights is that health AI may increasingly stop asking only for more real-world data and start asking whether sufficiently credible bodies can be simulated first. If that works, the bottleneck moves from data ownership to physics modeling, calibration quality, and synthetic-data trustworthiness. Medical AI competition would then become a competition in world modeling.'
        ],
        bullets_cn=['Mantis 用多源数据与物理引擎生成人体数字孪生。', '目标场景包括罕见病、手术机器人和药物试验。', '医疗 AI 的数据问题正被转写为模拟与建模问题。'],
        bullets_en=['Mantis uses multi-source data and physics engines to build human digital twins.', 'Target use cases include rare disease, surgical robotics, and drug testing.', 'Health AI data scarcity is being reframed as a simulation and modeling problem.'],
        significance_cn='如果“先模拟一个人”变成可行路线，医疗 AI 的上游资产就不只是病例，而是对身体的可计算理解。',
        significance_en='If “simulate the person first” becomes viable, the upstream asset in health AI will no longer be only patient records but computable understanding of the body itself.',
        sources=[
            {'title': 'Mantis Biotech is making ‘digital twins’ of humans to help solve medicine’s data availability problem', 'publication': 'TechCrunch', 'url': 'https://techcrunch.com/2026/03/30/mantis-biotech-is-making-digital-twins-of-humans-to-help-solve-medicines-data-availability-problem/'}
        ],
    ),
    article(
        id='ai-boss-poll-americans',
        section='tech-humanities',
        category_cn='劳动关系',
        category_en='Labor Relations',
        headline_cn='已经有 15% 的美国人愿意给 AI 当下属：管理权开始被想象成一种软件接口',
        headline_en='Already 15 percent of Americans say they would work for an AI boss, treating management as something software might do',
        deck_cn='Quinnipiac 调查里，虽然多数人仍不愿意接受 AI 直属上司，但愿意者已达到 15%。AI 不只在替代任务，也在松动“谁有资格管理人”的想象。',
        deck_en='In the Quinnipiac poll, most people still reject the idea of an AI direct supervisor, but 15 percent are open to it. AI is not only replacing tasks; it is loosening assumptions about who gets to manage human workers.',
        kicker_cn='技术人文',
        kicker_en='Tech & Humanities',
        published_at='2026-03-30T23:41:48.000Z',
        reading_time=2,
        tags=['Work', 'Management', 'Polls', 'AI Boss'],
        summary_cn=[
            'TechCrunch 援引 Quinnipiac 民调称，15% 的美国受访者表示愿意接受由 AI 程序担任直属主管，负责分配任务和安排时间。尽管仍是少数，但这一比例已足以说明：把“管理”理解为排班、审批、追踪与反馈的组合功能后，人们并不会天然坚持它必须由真人承担。文章还串联了 Workday、Amazon、Uber 等公司正在把部分中层管理工作自动化的趋势。',
            '这件事最值得写在人文栏目里，因为它动摇的是工作关系的日常感觉。老板过去既是权力角色，也是情绪角色：有人给你定优先级，也有人承担解释、安抚、责备甚至背锅的社会功能。AI 管理一旦真进入组织，员工面对的将不只是效率变化，而是“谁在和我发生劳动关系”这件事被重新软件化。'
        ],
        summary_en=[
            'TechCrunch, citing Quinnipiac polling, says 15 percent of Americans would accept an AI program as a direct supervisor assigning tasks and setting schedules. That remains a minority view, but it is enough to show that once management is reframed as scheduling, approvals, monitoring, and feedback, many people no longer assume it must be done by another human. The story also links the trend to companies such as Workday, Amazon, and Uber automating slices of middle-management work.',
            'This belongs in the tech-and-humanities section because it unsettles the everyday feeling of workplace authority. A boss has traditionally been not just a power role but an emotional role as well: someone who explains, reassures, pressures, and absorbs blame. If AI managers really enter organizations, workers will face not only efficiency changes but a software rewrite of the question of who is actually in the labor relationship with them.'
        ],
        bullets_cn=['15% 的美国受访者愿意接受 AI 当直属上司。', '部分企业已开始自动化中层管理职能。', '管理关系正在被重新理解为可软件化流程。'],
        bullets_en=['Fifteen percent of Americans say they would accept an AI direct supervisor.', 'Some companies are already automating middle-management functions.', 'Managerial authority is being reimagined as software process.'],
        significance_cn='一旦“老板”可以被理解成一个界面，办公室政治和劳动伦理都会跟着重写。',
        significance_en='Once a “boss” can be understood as an interface, office politics and labor ethics both start to get rewritten.',
        sources=[
            {'title': '15% of Americans say they’d be willing to work for an AI boss, according to new poll', 'publication': 'TechCrunch', 'url': 'https://techcrunch.com/2026/03/30/ai-work-boss-supervisor-us-quinnipiac-poll/'},
            {'title': 'Quinnipiac University Poll Release', 'publication': 'Quinnipiac University', 'url': 'https://poll.qu.edu/poll-release?releaseid=3955'}
        ],
    ),
    article(
        id='tech-reporters-using-ai-rewrite-desk',
        section='tech-humanities',
        category_cn='媒体劳动',
        category_en='Media Labor',
        headline_cn='独立记者开始把 Claude 当“重写台”，新闻业最先被改写的可能不是采访而是协作结构',
        headline_en='Independent reporters are turning Claude into a rewrite desk, suggesting journalism may be changed first in its support structure rather than its reporting',
        deck_cn='WIRED 采访了一批把 Claude、Wispr Flow 接进写作流程的记者：有人让 AI 起草，有人只让 AI 做“严厉编辑”。真正被补上的，是独立写作者失去的那层编辑基础设施。',
        deck_en='WIRED spoke with reporters using Claude and Wispr Flow in their writing process: some use AI for first drafts, others only as a severe editor. What is being rebuilt is the editorial infrastructure independent writers no longer have around them.',
        kicker_cn='技术人文',
        kicker_en='Tech & Humanities',
        published_at='2026-03-26T18:00:00.000Z',
        reading_time=3,
        tags=['Journalism', 'Claude', 'Writing', 'Labor'],
        summary_cn=[
            'WIRED 报道，多位独立科技记者正在把 Claude、Wispr Flow 等工具接入报道与写作流程。Alex Heath 让 Claude Cowork 结合邮箱、日历和笔记做首稿与结构整理；Jasmine Sun 则训练 Claude 只做编辑反馈，不允许替她写句子。文章指出，这类工作流尤其吸引失去传统新闻编辑部支持的独立写作者，因为 AI 最先填补的并不是采访，而是重写、校对、结构和反馈这一层协作劳动。',
            '这一变化比“AI 会不会取代记者”更复杂。新闻工作从来就不是单一技能，而是一套多人协作的生产线。AI 进入后，也许不会先把记者这个角色抹掉，而会先把记者周围那套看不见的编辑系统重新软件化。新闻业先被改变的，可能不是人，而是人和人之间原本的工作接口。'
        ],
        summary_en=[
            'WIRED reports that a growing number of independent tech journalists are integrating tools like Claude and Wispr Flow into their reporting and writing process. Alex Heath uses Claude Cowork with email, calendar, and notes to structure first drafts, while Jasmine Sun has trained Claude to behave only as an editor and never write sentences for her. The key point is that these workflows appeal most to writers who no longer have a traditional newsroom’s editorial support around them.',
            'That makes the story more complex than “AI replaces journalists.” Journalism has always been a coordinated production system, not a single skill. AI may not erase the reporter role first; it may first software-ize the invisible editorial scaffolding that used to surround that role. What gets rewritten first may be not the person, but the interface between people.'
        ],
        bullets_cn=['独立记者正把 Claude 接进起草、整理与编辑反馈流程。', 'AI 最先填补的是重写台和编辑支持的空缺。', '媒体行业面临的是协作结构重组，而不只是岗位替代。'],
        bullets_en=['Independent reporters are using Claude for drafting, structuring, and editorial feedback.', 'AI is first filling the gap left by rewrite desks and editorial support.', 'Media faces a reorganization of collaborative structure, not just job replacement.'],
        significance_cn='生成式 AI 改造媒体的第一步，可能不是替代记者，而是把记者身边那层支持系统抽成软件服务。',
        significance_en='The first way generative AI reshapes media may be not by replacing reporters, but by extracting the support system around them into software services.',
        sources=[
            {'title': 'Meet the Tech Reporters Using AI to Help Write and Edit Their Stories', 'publication': 'WIRED', 'url': 'https://www.wired.com/story/tech-reporters-using-ai-write-edit-stories/'}
        ],
    ),
    article(
        id='tiktok-ai-ads-disclosure-gap',
        section='tech-humanities',
        category_cn='平台透明度',
        category_en='Platform Transparency',
        headline_cn='TikTok 连 AI 广告都标不清，透明度问题看起来更像执行懒惰而不是技术难题',
        headline_en='If TikTok cannot clearly label AI ads, transparency is starting to look more like an enforcement failure than a technical one',
        deck_cn='The Verge 追问三星在 TikTok 上投放的疑似 AI 广告为何缺少稳定披露。广告是高度受监管场景，如果连这里都说不清“是不是 AI 做的”，那问题就不只是识别能力。',
        deck_en='The Verge asks why Samsung’s likely AI-generated ads on TikTok lacked consistent disclosure. Advertising is already tightly regulated; if platforms cannot explain whether content is AI-made here, the issue is bigger than detection limits.',
        kicker_cn='技术人文',
        kicker_en='Tech & Humanities',
        published_at='2026-03-28T14:00:00.000Z',
        reading_time=2,
        tags=['TikTok', 'Ads', 'Disclosure', 'Transparency'],
        summary_cn=[
            'The Verge 发现，三星在 TikTok 上投放的若干疑似生成式 AI 广告并未稳定带有平台要求的 AI 披露，而同一批活动在 YouTube 等渠道却能看到更明确的说明。报道指出，TikTok 和三星都属于 Content Authenticity Initiative 成员，因此并不能简单说“没人知道内容是怎么做的”；更像是信息没有被稳定传递给用户。',
            '这件事之所以适合放在人文栏目，是因为它暴露出 AI 透明度的一层真实困境：很多场景的问题不是技术识别做不到，而是平台、品牌和流程没有认真执行。尤其在广告这样本来就承担合规义务的环境中，如果用户仍然被动接收模糊内容，所谓透明度就会从“未来要解决的技术题”变成“现在没人认真负责的治理题”。'
        ],
        summary_en=[
            'The Verge found that several Samsung TikTok ads that appeared likely to be generative-AI creations did not consistently carry the disclosure labels TikTok says advertisers should provide, even though related campaign materials on YouTube were more clearly labeled. The report notes that both Samsung and TikTok are members of the Content Authenticity Initiative, so the problem is less that nobody knows how the content was made than that the information was not reliably passed on to users.',
            'This fits the humanities section because it reveals a more grounded problem with AI transparency. In many settings, the issue is not that technical detection is impossible, but that platforms, brands, and workflows are not enforcing disclosure seriously. In an already regulated ad environment, vague labeling turns transparency from a future technical challenge into a present governance failure.'
        ],
        bullets_cn=['疑似 AI 广告在 TikTok 上缺少稳定披露。', '同一批内容跨平台的标签表现并不一致。', '透明度问题在广告场景里更像执行缺口而非纯技术缺口。'],
        bullets_en=['Likely AI-generated ads lacked consistent disclosure on TikTok.', 'The same campaign was labeled differently across platforms.', 'In advertising, the transparency problem looks more like an enforcement gap than a pure technical limit.'],
        significance_cn='生成式媒体时代最稀缺的不是内容，而是每一次“这是谁做的、怎么做的”都有人真负责。',
        significance_en='In the age of generative media, what is scarcest may not be content but reliable accountability for who made it and how.',
        sources=[
            {'title': 'Why can’t TikTok identify AI generated ads when I can?', 'publication': 'The Verge', 'url': 'https://www.theverge.com/ai-artificial-intelligence/900400/tiktok-ai-ads-labels-samsung-disclosure'}
        ],
    ),
]

edition = {
    'id': DATE,
    'issueNumber': ISSUE_NUMBER,
    'date': DATE,
    'displayDate': DISPLAY_DATE,
    'generatedAt': GENERATED_AT,
    'mode': 'manual-openclaw',
    'lead': 'mistral-paris-data-center-debt',
    'i18n': {}
}

payload = {
    'site': site,
    'edition': edition,
    'sections': sections,
    'articles': articles,
}


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def build_rss(data) -> str:
    updated = datetime.fromisoformat(GENERATED_AT.replace('Z', '+00:00'))
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<rss version="2.0">',
        '  <channel>',
        '    <title>智潮 / Signal Tide</title>',
        f'    <link>{BASE}/</link>',
        '    <description>聚合、重写并归档每日 AI 领域的重要新闻。</description>',
        '    <language>zh-CN</language>',
        f'    <lastBuildDate>{format_datetime(updated)}</lastBuildDate>',
    ]
    for article in data['articles']:
        description = '\n\n'.join([article['deck'], *article['summary'], article['significance']])
        link = f"{BASE}/article.html?id={article['id']}"
        lines.extend([
            '    <item>',
            f'      <title>{escape(article["headline"])}</title>',
            f'      <link>{escape(link)}</link>',
            f'      <guid>{escape(link)}</guid>',
            f'      <pubDate>{format_datetime(updated)}</pubDate>',
            f'      <description>{escape(description)}</description>',
            '    </item>',
        ])
    lines.extend(['  </channel>', '</rss>', ''])
    return '\n'.join(lines)


def update_archive_index():
    index_path = ARCHIVE / 'index.json'
    existing = []
    if index_path.exists():
        existing = json.loads(index_path.read_text(encoding='utf-8')).get('items', [])
    items = [item for item in existing if item.get('date') != DATE]
    items.insert(0, {
        'date': DATE,
        'displayDate': DISPLAY_DATE,
        'articleCount': len(articles),
        'leadId': edition['lead'],
        'leadHeadline': next(a['headline'] for a in articles if a['id'] == edition['lead']),
        'note': '保存当日首页版面与详情内容。'
    })
    write_json(index_path, {'generatedAt': GENERATED_AT, 'items': items})


def main():
    write_json(DATA / 'issues.json', payload)
    write_json(ARCHIVE / f'{DATE}.json', payload)
    update_archive_index()
    (DOCS / 'rss.xml').write_text(build_rss(payload), encoding='utf-8')
    print(f'Wrote {len(articles)} articles for {DATE}.')


if __name__ == '__main__':
    main()
