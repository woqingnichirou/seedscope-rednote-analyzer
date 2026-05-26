# SeedScope 中文说明

SeedScope 是一个面向品牌方、代理商和内容营销团队的本地优先小红书/Rednote 种草竞品内容分析工具。用户上传 Brand A 与 Brand B 的高赞笔记截图后，系统通过 OCR、规则标签和报告模板，生成可校正、可导出、可复盘的竞品种草分析报告。

> SeedScope 不做爬虫，不绕过平台限制，不采集未授权数据。所有示例均为脱敏 demo data。

## 项目定位

SeedScope 关注“内容如何影响用户决策”。它不是舆情监控工具，也不是投放后台，而是帮助团队把截图、标题、封面、互动数据、正文关键词和 CTA 承接方式结构化，形成可复用的内容策略资产。

## 适合谁使用

- 品牌市场团队：做竞品种草月报、季度复盘和大促前策略。
- 内容运营团队：复盘高赞笔记，沉淀标题、封面和正文 SOP。
- 代理商团队：做投前竞品拆解、提案分析和内容方向建议。
- 投放团队：筛选可复投素材，建立高效内容白名单。
- 创始团队或增长团队：快速判断品牌在内容种草链路中的短板。

## 解决什么问题

- 手工看截图效率低，结论难复用。
- 竞品内容分析容易停留在“谁发得多、谁点赞高”。
- 标题、封面、正文、CTA 没有统一标签体系。
- 高赞内容没有沉淀成可投放、可复盘、可复制的素材池。
- 直接抓取平台数据存在合规和稳定性风险。

## 核心功能

- 创建 Brand A vs Brand B 分析项目。
- 分别上传两组截图。
- OCR 识别标题、封面文案、点赞、收藏、评论、发布时间、账号名称。
- 用可编辑表格校正 OCR 结果。
- 自动判断内容类型、标题套路、封面表达、正文结构、CTA 承接和风险类型。
- 基于 Jinja2 模板生成 Markdown 和 HTML 报告。
- 导出 Excel 明细表。
- 默认本地规则模式，可选配置 OpenAI API Key。

## 使用流程

1. 创建项目：填写品牌代号、行业、周期和分析目标。
2. 上传截图：分别上传 Brand A 和 Brand B 的多张笔记截图。
3. OCR 识别：系统自动提取基础字段。
4. 人工校正：修正标题、互动数据、发布时间和账号信息。
5. 自动打标：生成内容类型、标题类型、封面类型、正文结构、CTA 和风险标签。
6. 生成报告：输出竞品种草分析报告。
7. 导出结果：下载 Markdown、HTML 和 Excel。

## 本地启动方式

### Windows 一键启动

适合不熟悉命令行的品牌方、代理商和内容团队用户。

1. 下载或 clone 项目到本地。
2. 双击运行：

```text
scripts/windows/setup_windows.bat
```

该脚本会检查 Node.js、Python、pip，安装前端和后端依赖，并在缺少 `.env` 时自动从 `.env.example` 复制一份。

3. 可选：双击检查模型配置：

```text
scripts/windows/check_env.bat
```

如果 `LLM_PROVIDER=mock`，不需要 API Key，也可以直接体验 demo。

4. 双击启动 SeedScope：

```text
scripts/windows/start_windows.bat
```

脚本会启动 FastAPI 后端、Next.js 前端，自动打开浏览器访问：

```text
http://127.0.0.1:3000
```

5. 如需停止服务，双击：

```text
scripts/windows/stop_windows.bat
```

日志会写入 `logs/`，该目录不会提交到 Git。

### Docker 启动

```bash
cp .env.example .env
docker compose up --build
```

访问：

- 前端：http://localhost:3000
- API 文档：http://localhost:8000/docs

### 本地开发启动

后端：

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r apps/api/requirements.txt
uvicorn apps.api.app.main:app --reload --port 8000
```

前端：

```bash
cd apps/web
npm install
npm run dev
```

访问：

```text
http://localhost:3000
```

## 模型配置方式

SeedScope 支持 OpenAI、DeepSeek、Qwen、Kimi、Zhipu GLM 和 mock provider。大陆用户建议优先尝试 DeepSeek / Qwen / Kimi。

### 无 API Key demo 模式

首次体验可以使用 mock provider，不调用真实模型：

```env
LLM_PROVIDER=mock
LLM_MODEL=
OPENAI_API_KEY=
DEEPSEEK_API_KEY=
QWEN_API_KEY=
KIMI_API_KEY=
ZHIPU_API_KEY=
```

### DeepSeek

```env
LLM_PROVIDER=deepseek
LLM_MODEL=deepseek-chat
DEEPSEEK_API_KEY=your_deepseek_api_key
```

### Qwen 通义千问

Qwen 使用 DashScope OpenAI-compatible 模式：

```env
LLM_PROVIDER=qwen
LLM_MODEL=qwen-plus
QWEN_API_KEY=your_qwen_api_key
```

### Kimi

```env
LLM_PROVIDER=kimi
LLM_MODEL=moonshot-v1-8k
KIMI_API_KEY=your_kimi_api_key
```

### Zhipu GLM 智谱

```env
LLM_PROVIDER=zhipu
LLM_MODEL=glm-4-flash
ZHIPU_API_KEY=your_zhipu_api_key
```

### OpenAI

```env
LLM_PROVIDER=openai
LLM_MODEL=gpt-4o-mini
OPENAI_API_KEY=your_openai_api_key
```

安全说明：

- API Key 只保存在本地 `.env`。
- `.env` 已写入 `.gitignore`，不要提交到 GitHub。
- SeedScope 默认本地运行，不会把 API Key 上传到云端。
- 如果 provider 接口细节变化，SeedScope 会回退到规则模式，不影响项目启动。

## 示例数据说明

示例数据位于：

- `examples/demo_notes.json`
- `examples/demo_ocr_texts/`
- `examples/sample_notes.xlsx`

示例数据只使用 Brand A / Brand B、脱敏账号、模拟互动数据和通用行业场景，不包含真实品牌、真实截图、真实预算或真实达人信息。

## 示例报告说明

示例报告位于：

- `examples/sample_report.md`
- `examples/sample_report.html`
- `examples/sample_report.docx`
- `examples/sample_report.pptx`

报告结构覆盖核心结论、近半年概览、发布时间节奏、达人与预算结构、标题策略、内容策略、正文结构、封面策略、CTA 承接、问题总结、优化措施、下阶段打法、预算建议和下一步行动。

## 导出格式说明

SeedScope 支持面向不同工作流的多格式导出：

| 格式 | 文件 | 适用场景 |
|---|---|---|
| Markdown | `report.md` | 放入知识库、GitHub、飞书文档二次整理 |
| HTML | `report.html` | 浏览器预览、轻量分享、内部页面归档 |
| Excel | `notes.xlsx` | 明细复盘、筛选高赞内容、透视标题/封面/CTA 标签 |
| Word | `SeedScope_竞品分析报告_项目名_日期.docx` | 品牌方内部汇报、代理商交付文档、可二次修改报告 |
| PPT | `SeedScope_竞品分析报告_项目名_日期.pptx` | 月报会、策略会、投前提案和管理层简报 |

Word 报告使用清晰标题层级，并对关键结论加粗。PPT 采用 16:9 简洁蓝灰色样式，每页聚焦一个核心结论，不使用任何真实品牌色或真实品牌素材。

## 常见问题

### SeedScope 会自动抓取小红书数据吗？

不会。SeedScope 只分析用户上传的截图，不包含爬虫、自动登录、批量抓取或绕过平台限制的能力。

### 没有 API Key 可以用吗？

可以。默认规则模式可以完成 OCR 校正、内容打标和报告生成。

### 可以用于消费品牌吗？

可以。当前 demo 使用在线教育场景，但规则库适合迁移到消费品牌、本地生活、SaaS 和服务类品牌。

### OCR 识别不准怎么办？

进入校正页手动修改识别结果。SeedScope 的设计假设 OCR 不是最终答案，人工校正是正式分析前的必要步骤。

### 可以上传真实项目数据吗？

建议仅在本地环境处理，并确保你拥有处理这些截图和数据的授权。不要上传个人隐私、内部敏感材料或未授权信息。

## 隐私与合规声明

SeedScope 坚持以下原则：

- No scraping：不做爬虫，不绕过平台限制。
- Screenshot-based：只处理用户上传截图。
- Local-first：数据库、上传文件和导出文件默认保存在本地。
- Brand-safe：示例和模板默认使用 Brand A / Brand B。
- Human review：所有报告都是分析草稿，正式使用前需要人工复核。

请勿将 SeedScope 用于侵犯隐私、未经授权的数据处理、恶意竞品攻击、虚假宣传或任何违反平台规则的行为。

## Roadmap

详见 [`docs/roadmap.md`](docs/roadmap.md)。

核心方向：

- v0.1：本地 MVP、截图上传、OCR 校正、规则打标、报告导出。
- v0.2：中文产品体验增强、规则库扩展、示例数据导入。
- v0.3：LLM 洞察生成、素材白名单、投放复盘。
- v1.0：团队协作、项目历史、可配置报告体系和更完整的品牌安全检查。
