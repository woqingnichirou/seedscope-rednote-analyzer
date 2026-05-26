from collections import Counter

from jinja2 import Environment, FileSystemLoader, select_autoescape
from sqlmodel import Session, select

from ..config import get_settings
from ..exporters import export_html, export_markdown, export_notes_excel, export_report_ppt, export_report_word
from ..exporters.common import ppt_filename, word_filename
from ..models import Note, Project, Report


def _share(part: int, total: int) -> str:
    if total == 0:
        return "0%"
    return f"{part / total:.0%}"


def build_report_context(project: Project, notes: list[Note]) -> dict:
    brand_a_notes = [n for n in notes if n.brand_key == "brand_a"]
    brand_b_notes = [n for n in notes if n.brand_key == "brand_b"]
    all_notes = notes

    def avg(items: list[Note], field: str) -> float:
        if not items:
            return 0
        return sum(getattr(item, field) for item in items) / len(items)

    title_counter_a = Counter(n.title_type or "未分类" for n in brand_a_notes)
    title_counter_b = Counter(n.title_type or "未分类" for n in brand_b_notes)
    content_counter = Counter(n.content_type or "未分类" for n in all_notes)
    cover_counter = Counter(n.cover_type or "未分类" for n in all_notes)
    cta_counter = Counter(n.cta_type or "未分类" for n in all_notes)

    title_types = sorted(set(title_counter_a) | set(title_counter_b) | {"问题型", "方法型", "对比型", "结果型", "品牌直露型"})
    total_a = len(brand_a_notes)
    total_b = len(brand_b_notes)

    content_items = []
    for name, count in content_counter.most_common():
        content_items.append(
            {
                "name": name,
                "user_question": f"用户在 {name} 场景下如何判断是否值得选择",
                "content_hook": "用具体阶段、选择标准和结果证据降低决策成本",
                "title_direction": f"{name} + 具体问题 + 可验证结果",
                "cover_direction": "大字结论 + 阶段/问题词 + 证据位",
                "creator_fit": "高决策作者或结果陪跑作者",
            }
        )

    return {
        "report_title": f"{project.brand_a} vs {project.brand_b} 小红书种草竞品分析报告",
        "period": {"label": project.period},
        "brand_a": {"name": project.brand_a},
        "brand_b": {"name": project.brand_b},
        "executive_summary": {
            "overall_judgement": f"{project.brand_a} 应优先提升决策型内容比例，把高互动素材沉淀为可复投的标题、封面、正文和 CTA 模板。",
            "insights": [
                {
                    "title": "内容竞争重点不是发布数量，而是决策解释密度",
                    "summary": "高赞内容通常先进入用户问题，再给判断标准和结果证据。",
                    "evidence": f"当前样本共 {len(all_notes)} 条，主要高频内容类型为 {content_counter.most_common(1)[0][0] if content_counter else '未分类'}。",
                    "implication": "把内容从体验反馈升级为选购判断和方法教育。",
                },
                {
                    "title": "标题需要减少品牌前置，增加问题和方法入口",
                    "summary": "问题型、方法型、对比型标题更适合承接搜索和种草。",
                    "evidence": f"{project.brand_a} 当前主要标题类型为 {title_counter_a.most_common(1)[0][0] if title_counter_a else '未分类'}。",
                    "implication": "建立标题公式库，并按标题类型复盘互动表现。",
                },
                {
                    "title": "封面应标准化为高信息密度经验帖",
                    "summary": "阶段、痛点、结果和证据位是提升停留的关键变量。",
                    "evidence": f"样本中封面类型分布：{dict(cover_counter)}。",
                    "implication": "统一封面模板，减少泛化品牌海报式表达。",
                },
            ],
        },
        "overview": {
            "conclusion": "近半年概览应优先判断双方是否形成稳定的高决策内容供给，而不是只比较发布量。",
            "metrics": [
                {"name": "样本笔记数", "brand_a": total_a, "brand_b": total_b, "comment": "用于判断样本规模是否均衡"},
                {"name": "平均点赞", "brand_a": round(avg(brand_a_notes, "likes"), 1), "brand_b": round(avg(brand_b_notes, "likes"), 1), "comment": "衡量内容吸引力"},
                {"name": "平均收藏", "brand_a": round(avg(brand_a_notes, "collects"), 1), "brand_b": round(avg(brand_b_notes, "collects"), 1), "comment": "衡量决策参考价值"},
                {"name": "平均评论", "brand_a": round(avg(brand_a_notes, "comments"), 1), "brand_b": round(avg(brand_b_notes, "comments"), 1), "comment": "衡量咨询和讨论潜力"},
            ],
            "key_observations": [
                "收藏和评论比单纯点赞更能反映种草内容的决策价值。",
                "后续应按内容类型、标题类型、封面类型三维交叉复盘。",
            ],
        },
        "cadence": {
            "conclusion": "发布时间节奏需要识别波段式集中发力与日常维持之间的差异。",
            "timeline": [
                {"window": "分析周期内", "brand_a_action": "按上传样本聚合判断", "brand_b_action": "按上传样本聚合判断", "interpretation": "后续接入发布时间后可识别投放波峰和主题窗口"}
            ],
            "recommendation": "围绕行业关键决策窗口集中投放决策攻略、横向对比和结果证明内容。",
        },
        "spend_and_creators": {
            "conclusion": "第一版未采集真实花费，建议用达人能力分层替代单纯价格分层，避免泄露预算。",
            "creator_tiers": [
                {"name": "高决策作者", "definition": "擅长对比、避坑、方法论和选择标准", "share": "待填充", "performance": "适合建立选购话语权", "action": "优先进入白名单"},
                {"name": "结果陪跑作者", "definition": "擅长记录过程和前后变化", "share": "待填充", "performance": "适合补充真实证据", "action": "绑定阶段窗口选题"},
                {"name": "低成本测试作者", "definition": "适合测试标题、封面、CTA", "share": "待填充", "performance": "适合赛马", "action": "按周淘汰低效题材"},
            ],
            "price_bands": [],
        },
        "title_analysis": {
            "conclusion": "标题优化应从品牌表达转向用户问题、选择方法和结果证据。",
            "types": [
                {
                    "type": title_type,
                    "brand_a_share": _share(title_counter_a[title_type], total_a),
                    "brand_b_share": _share(title_counter_b[title_type], total_b),
                    "finding": "占比差异用于判断双方内容入口是否偏决策型",
                    "formula": "阶段/痛点 + 怎么选/如何避坑 + 结果或证据",
                }
                for title_type in title_types
            ],
            "recommendation": "优先增加问题型、方法型和对比型标题，降低品牌直露型标题占比。",
        },
        "content_strategy": {
            "conclusion": "内容策略应围绕为什么选、怎么选、选后有什么变化展开。",
            "dimensions": [
                {"dimension": "核心主张", "brand_a": "待从样本归纳", "brand_b": "待从样本归纳", "optimization": "把卖点翻译成用户选择理由"},
                {"dimension": "内容起手", "brand_a": "待从样本归纳", "brand_b": "待从样本归纳", "optimization": "先痛点后品牌"},
                {"dimension": "正文结构", "brand_a": "待从样本归纳", "brand_b": "待从样本归纳", "optimization": "补充判断标准和结果证据"},
                {"dimension": "转化方式", "brand_a": "待从样本归纳", "brand_b": "待从样本归纳", "optimization": "把 CTA 放在经验复盘后半段"},
            ],
        },
        "body_structure": {
            "conclusion": "推荐正文结构为立人设、讲痛点、抛认知、引品牌、给结果、接 CTA。",
            "steps": [
                {"name": "立人设", "goal": "建立作者可信度", "guidance": "说明角色、经验或对比基础", "required_data": "账号定位、过往经验"},
                {"name": "讲痛点", "goal": "进入真实需求", "guidance": "描述具体阶段和具体问题", "required_data": "用户阶段、痛点词"},
                {"name": "抛认知", "goal": "教育用户判断", "guidance": "给选择标准、避坑清单或方法框架", "required_data": "判断标准"},
                {"name": "引品牌", "goal": "自然承接产品", "guidance": "解释品牌如何满足标准", "required_data": "品牌卖点"},
                {"name": "给结果", "goal": "提供验证", "guidance": "用互动、反馈或前后变化收束", "required_data": "结果证据"},
                {"name": "接 CTA", "goal": "引导咨询", "guidance": "用评论、私信、试听或资料自然承接", "required_data": "CTA 链路"},
            ],
        },
        "high_like_categories": {
            "conclusion": "高赞内容应沉淀为可复用母题，而不是停留在单篇复盘。",
            "items": content_items
            or [
                {"name": "阶段窗口", "user_question": "当前阶段怎么选", "content_hook": "阶段痛点", "title_direction": "阶段 + 问题", "cover_direction": "年龄/阶段大字", "creator_fit": "结果陪跑作者"}
            ],
        },
        "cover_strategy": {
            "conclusion": "封面需要在首屏同时交代阶段、问题、结果和证据。",
            "templates": [
                {"name": "阶段窗口型", "message": "明确年龄、年级或使用阶段", "evidence_slot": "孩子实拍/学习记录", "content_fit": "阶段窗口内容", "acceptance_criteria": "3 秒内读懂对象和问题"},
                {"name": "结果反差型", "message": "突出前后变化", "evidence_slot": "变化截图/反馈", "content_fit": "结果证明内容", "acceptance_criteria": "结果可感知、不过度承诺"},
                {"name": "选课避坑型", "message": "突出判断标准和试错成本", "evidence_slot": "对比表/清单", "content_fit": "对比和攻略内容", "acceptance_criteria": "包含可执行判断标准"},
                {"name": "证据陪跑型", "message": "突出真实过程", "evidence_slot": "过程记录/作业反馈", "content_fit": "陪跑复盘内容", "acceptance_criteria": "证据位清晰可信"},
            ],
        },
        "cta_analysis": {
            "conclusion": "CTA 应在完成问题教育后自然出现，避免开头强转化破坏信任。",
            "touchpoints": [
                {"position": name, "current_state": f"{count} 条样本", "user_question": "用户是否愿意继续咨询", "action": "沉淀标准话术并追踪转化", "metric": "评论率/私信率/试听率"}
                for name, count in cta_counter.items()
            ],
        },
        "issues": [
            {"layer": "达人层", "problem": "高决策作者识别规则需要补充", "impact": "影响内容决策力", "priority": 1, "action": "建立作者白名单字段"},
            {"layer": "标题层", "problem": "标题类型需要持续复盘", "impact": "影响搜索和点击", "priority": 1, "action": "按类型统计互动表现"},
            {"layer": "封面层", "problem": "封面证据位需要标准化", "impact": "影响停留和信任", "priority": 2, "action": "建立封面模板库"},
            {"layer": "投放层", "problem": "高效素材复投规则未成型", "impact": "影响放大效率", "priority": 2, "action": "建立素材池和入池阈值"},
        ],
        "optimization_initiatives": [
            {
                "name": "内容池重构",
                "objective": "把样本内容沉淀为决策攻略、结果见证和品牌背书三类资产。",
                "actions": [
                    {"name": "建立选题库", "deliverable": "选题标签表", "acceptance_metric": "每个标签有标题公式和封面公式"},
                    {"name": "建立正文 SOP", "deliverable": "正文结构模板", "acceptance_metric": "每篇内容包含痛点、认知、品牌、结果、CTA"},
                ],
            },
            {
                "name": "复投机制重构",
                "objective": "让高赞素材进入二次放大和搜索承接。",
                "actions": [
                    {"name": "定义入池阈值", "deliverable": "素材白名单规则", "acceptance_metric": "按互动率、收藏率、评论率判断"},
                    {"name": "周度复盘", "deliverable": "复盘看板", "acceptance_metric": "按达人、选题、封面、CTA 复盘"},
                ],
            },
        ],
        "next_stage_plan": {
            "phases": [
                {"name": "模板重建", "window": "第 1-2 周", "task": "统一标题、封面、正文、CTA", "deliverable": "模板库", "success_metric": "模板覆盖主要内容类型"},
                {"name": "小规模赛马", "window": "第 3-4 周", "task": "测试题材、封面、CTA", "deliverable": "赛马表", "success_metric": "识别高效组合"},
                {"name": "白名单复投", "window": "第 5-8 周", "task": "放大高效素材", "deliverable": "复投清单", "success_metric": "收藏率和评论率提升"},
                {"name": "品效联动", "window": "第 9-12 周", "task": "同步搜索和投流端", "deliverable": "素材池", "success_metric": "后链路转化提升"},
            ]
        },
        "budget_plan": {
            "conclusion": "预算建议按作者能力和内容目标分配，避免平均铺量；第一版仅输出比例建议，不记录真实预算。",
            "allocation": [
                {"module": "高决策作者", "share": "55%-65%", "goal": "建立选择标准和话语权", "principle": "优先投方法论和对比型作者"},
                {"module": "结果陪跑作者", "share": "20%-25%", "goal": "补充真实变化证据", "principle": "绑定阶段窗口和结果反差"},
                {"module": "低成本测试作者", "share": "10%-15%", "goal": "测试题材和封面", "principle": "快速赛马、及时淘汰"},
                {"module": "品牌背书作者", "share": "5%-10%", "goal": "补充可信度", "principle": "控制硬广比例"},
            ],
        },
        "next_actions": [
            {"name": "补齐达人能力字段", "owner": "内容运营", "due_date": "T+3", "deliverable": "达人分层表", "metric": "覆盖全部候选作者"},
            {"name": "建立标题公式库", "owner": "内容运营", "due_date": "T+5", "deliverable": "标题模板", "metric": "每类不少于 5 条公式"},
            {"name": "建立封面模板库", "owner": "设计", "due_date": "T+7", "deliverable": "封面模板", "metric": "覆盖 4 类封面"},
            {"name": "定义素材入池阈值", "owner": "投放", "due_date": "T+7", "deliverable": "白名单规则", "metric": "可按周自动筛选"},
            {"name": "搭建周复盘看板", "owner": "项目负责人", "due_date": "T+10", "deliverable": "复盘看板", "metric": "按四维度归因"},
        ],
    }


def render_report(session: Session, project: Project, notes: list[Note]) -> Report:
    settings = get_settings()
    env = Environment(
        loader=FileSystemLoader(str(settings.report_template_dir)),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    context = build_report_context(project, notes)
    markdown = env.get_template("report.md.j2").render(**context)
    html = env.get_template("report.html.j2").render(**context)
    report = Report(project_id=project.id or 0, markdown=markdown, html=html)
    session.add(report)
    session.commit()
    session.refresh(report)
    return report


def export_project(session: Session, project: Project) -> dict[str, str]:
    settings = get_settings()
    project_dir = settings.export_dir / f"project_{project.id}"
    project_dir.mkdir(parents=True, exist_ok=True)

    report = session.exec(select(Report).where(Report.project_id == project.id).order_by(Report.created_at.desc())).first()
    notes = session.exec(select(Note).where(Note.project_id == project.id)).all()
    if not report:
        report = render_report(session, project, notes)

    md_path = project_dir / "report.md"
    html_path = project_dir / "report.html"
    xlsx_path = project_dir / "notes.xlsx"
    docx_name = word_filename(project)
    pptx_name = ppt_filename(project)
    docx_path = project_dir / docx_name
    pptx_path = project_dir / pptx_name

    export_markdown(report.markdown, md_path)
    export_html(report.html, html_path)
    export_notes_excel(notes, xlsx_path)
    export_report_word(project, notes, docx_path)
    export_report_ppt(project, notes, pptx_path)

    return {
        "markdown_url": f"/api/exports/project_{project.id}/report.md",
        "html_url": f"/api/exports/project_{project.id}/report.html",
        "excel_url": f"/api/exports/project_{project.id}/notes.xlsx",
        "word_url": f"/api/exports/project_{project.id}/{docx_name}",
        "ppt_url": f"/api/exports/project_{project.id}/{pptx_name}",
    }
