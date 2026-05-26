# SeedScope

**SeedScope is a local-first, screenshot-based competitive content analyzer for Rednote/Xiaohongshu seeding strategy.**

It helps marketing, growth, and content teams compare Brand A vs Brand B using user-provided high-performing note screenshots. SeedScope extracts OCR fields, lets users correct the data, classifies content patterns, and generates brand-safe competitive reports.

> 中文补充：SeedScope 用于分析用户自行上传的小红书/Rednote 笔记截图，不包含爬虫能力，不绕过平台限制，不处理未授权隐私数据。

## Product Screenshot

Screenshots are intentionally not committed in the first open-source version.

Suggested placeholders:

- `docs/assets/homepage.png` — project landing page and workflow overview.
- `docs/assets/review-table.png` — OCR correction table.
- `docs/assets/report-preview.png` — generated Markdown/HTML report preview.

## Why This Project

Competitive content analysis is often trapped between two bad options:

- Manual review is slow, subjective, and hard to reproduce.
- Platform scraping is fragile, legally risky, and often violates platform rules.

SeedScope takes a different path:

- **No scraping**: users upload screenshots they are allowed to process.
- **Screenshot-based**: OCR converts visual note screenshots into structured fields.
- **Local-first**: SQLite, local uploads, local exports, and deterministic rule-based analysis by default.
- **Brand-safe**: templates use Brand A / Brand B, anonymized examples, and privacy-first reporting.

The goal is not to replace human strategy work. The goal is to make repeatable analysis faster, cleaner, and safer.

## Core Features

- Create a Brand A vs Brand B competitive analysis project.
- Upload multiple Rednote/Xiaohongshu note screenshots for each brand.
- OCR extraction for:
  - title
  - cover copy
  - likes
  - collects
  - comments
  - publish time
  - account name
- Editable correction table for OCR results.
- Rule-based classification for:
  - content type
  - title pattern
  - cover pattern
  - body structure
  - CTA pattern
  - risk pattern
- Competitive report generation in Markdown and HTML.
- Excel export for note-level analysis.
- Optional LLM integration via `OPENAI_API_KEY`.
- Extension points for DeepSeek and Claude-compatible providers.
- Docker Compose setup for one-command local startup.

## Workflow

1. **Create project**
   - Enter Brand A, Brand B, industry, analysis period, and objective.

2. **Upload screenshots**
   - Upload Brand A and Brand B note screenshots separately.

3. **Run OCR**
   - SeedScope attempts PaddleOCR first.
   - If PaddleOCR is unavailable, it falls back to Tesseract.
   - If OCR fails, fields remain editable.

4. **Review and correct**
   - Edit extracted title, cover text, account, engagement metrics, and publish time.

5. **Classify content**
   - Apply rules for content type, title structure, cover style, body structure, CTA, and risk.

6. **Generate report**
   - Produce a structured competitive seeding analysis report.

7. **Export**
   - Export Markdown, HTML, and Excel files.

## Tech Stack

### Frontend

- Next.js
- React
- Tailwind CSS
- shadcn/ui-style local components
- Recharts

### Backend

- FastAPI
- SQLite
- SQLModel
- Jinja2
- openpyxl

### OCR

- PaddleOCR preferred
- Tesseract fallback

### LLM

- OpenAI-compatible integration via `OPENAI_API_KEY`
- DeepSeek / Claude extension interfaces reserved
- Rule-based mode available without any API key

### Deployment

- Docker Compose
- Local-first filesystem storage

## Quick Start

### Option 1: Docker Compose

```bash
cp .env.example .env
docker compose up --build
```

Open:

- Web app: http://localhost:3000
- API docs: http://localhost:8000/docs

### Option 2: Local Development

Backend:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r apps/api/requirements.txt
uvicorn apps.api.app.main:app --reload --port 8000
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

Frontend:

```bash
cd apps/web
npm install
npm run dev
```

Open:

```text
http://localhost:3000
```

## Environment Variables

Create a `.env` file from `.env.example`:

```env
OPENAI_API_KEY=
LLM_PROVIDER=rule
DATABASE_URL=sqlite:///./data/seedscope.db
UPLOAD_DIR=./data/uploads
EXPORT_DIR=./data/exports
REPORT_TEMPLATE_DIR=./packages/report_templates
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

Notes:

- `LLM_PROVIDER=rule` keeps the app deterministic and local-first.
- Set `LLM_PROVIDER=openai` and `OPENAI_API_KEY` only if you want to add LLM-assisted summaries.
- Uploaded files and exports are stored under `data/` by default.

## Demo Data

SeedScope includes fully anonymized demo data:

- [`examples/demo_notes.json`](examples/demo_notes.json)
- [`examples/demo_ocr_texts/`](examples/demo_ocr_texts/)
- [`examples/sample_notes.xlsx`](examples/sample_notes.xlsx)

The demo data uses only:

- Brand A
- Brand B
- anonymized account names
- synthetic engagement metrics
- generic online education examples

No real brand names, creators, screenshots, internal budgets, or private business data are included.

## Sample Report

You can review the generated demo report here:

- Markdown: [`examples/sample_report.md`](examples/sample_report.md)
- HTML: [`examples/sample_report.html`](examples/sample_report.html)
- Excel notes: [`examples/sample_notes.xlsx`](examples/sample_notes.xlsx)

These files are suitable for README demos, product walkthroughs, and local testing.

## Rule Libraries

SeedScope ships with first-version marketing analysis rules under [`packages/rules`](packages/rules):

- `content_types.json`
- `title_patterns.json`
- `cover_patterns.json`
- `body_structure.json`
- `cta_patterns.json`
- `risk_patterns.json`
- `report_sections.json`

Each category includes:

- English key
- Chinese label
- detection signals
- description
- example

## Roadmap

- Import demo data directly from `examples/demo_notes.json`.
- Add OCR health checks in the UI.
- Add optional PaddleOCR dependency profile.
- Add LLM-assisted report insights with strict JSON schema validation.
- Add creator-level scoring and whitelist recommendations.
- Add thumbnail preview during OCR correction.
- Add richer charts for cadence, title structure, cover strategy, and CTA performance.
- Add report history and project comparison.
- Add automated tests for API, templates, and rules.
- Add Playwright smoke tests for the full workflow.

## FAQ

### Does SeedScope scrape Rednote/Xiaohongshu?

No. SeedScope does not scrape, crawl, automate login, bypass access controls, or extract platform data directly.

### What data does SeedScope analyze?

Only screenshots and fields uploaded by the user. The user is responsible for ensuring they have the right to process those materials.

### Can I use it without an LLM API key?

Yes. The default mode is rule-based and works without `OPENAI_API_KEY`.

### Why screenshot-based instead of crawler-based?

Screenshots are easier to review, safer to handle, and better aligned with brand-safe internal analysis workflows.

### Is this only for online education?

No. The demo uses online education because it has clear decision-making patterns, but the framework can be adapted to consumer brands, local services, SaaS, and other content-driven categories.

### Does the project include real brand data?

No. Demo files are anonymized and use Brand A / Brand B only.

## Privacy & Compliance

SeedScope is designed for privacy-first competitive content analysis.

Principles:

- **No scraping**: no crawler, spider, browser automation, or platform bypass.
- **Screenshot-based**: analysis starts from user-provided screenshots.
- **Local-first**: uploaded files, SQLite database, and exports stay local by default.
- **Brand-safe**: examples and templates avoid real brand names, real creators, real budgets, and identifiable screenshots.
- **Human review required**: generated reports are drafts and should be reviewed before business use.

Do not use SeedScope to:

- collect private data without permission
- identify or track private individuals
- bypass platform restrictions
- scrape Rednote/Xiaohongshu or any other platform
- publish misleading or defamatory competitor claims
- process confidential internal materials without authorization

## Contributing

Contributions are welcome.

Good first contribution areas:

- Improve rule libraries in `packages/rules`.
- Add tests for the FastAPI endpoints.
- Add sample screenshot placeholders using synthetic assets.
- Improve OCR parsing heuristics.
- Add more export formats.
- Improve report templates.

Before submitting a pull request:

1. Keep examples anonymized.
2. Do not add real brand names or private datasets.
3. Do not add scraping functionality.
4. Run frontend checks:

```bash
npm --prefix apps/web run lint
npm --prefix apps/web run build
```

5. If you change backend code, run the API locally and verify `/api/health`.

## License

MIT License.

See [`LICENSE`](LICENSE) for details.
