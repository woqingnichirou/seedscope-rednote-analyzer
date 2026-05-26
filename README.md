# SeedScope

[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Frontend](https://img.shields.io/badge/Frontend-Next.js-black.svg)](apps/web)
[![Backend](https://img.shields.io/badge/Backend-FastAPI-009688.svg)](apps/api)
[![Local First](https://img.shields.io/badge/Local--first-yes-blue.svg)](#privacy--compliance)
[![No Scraping](https://img.shields.io/badge/No%20scraping-enforced-red.svg)](#privacy--compliance)

**SeedScope is a local-first, screenshot-based competitive content analyzer for Rednote/Xiaohongshu seeding strategy.**

[中文 README](README.zh-CN.md) | [Use Cases 中文](docs/use_cases_zh.md) | [China User Quickstart](docs/china_user_quickstart.md) | [Roadmap](docs/roadmap.md)

SeedScope helps brand teams, agencies, growth teams, and content marketing teams compare Brand A vs Brand B using user-provided high-performing note screenshots. It extracts OCR fields, lets users correct the data, classifies content patterns, and generates brand-safe competitive reports.

## Product Preview

> The first open-source release does not include real product screenshots or real platform screenshots. Use the placeholders below when preparing GitHub images or product docs.

| Screen | Placeholder | Description |
|---|---|---|
| Home | `docs/assets/homepage.png` | Product positioning and workflow overview |
| OCR Review | `docs/assets/review-table.png` | Editable OCR correction table |
| Tag Analysis | `docs/assets/tag-analysis.png` | Content type and pattern charts |
| Report | `docs/assets/report-preview.png` | Markdown / HTML competitive report preview |

## Four Principles

- **No scraping**: no crawler, no spider, no automated platform extraction, no login automation.
- **Local-first**: SQLite, local uploads, local exports, and deterministic rule mode by default.
- **Screenshot-based**: users upload screenshots they are allowed to process.
- **Brand-safe**: templates use Brand A / Brand B, anonymized examples, and privacy-first reporting.

## Why This Project

Competitive content analysis is often trapped between two bad options:

- Manual review is slow, subjective, and hard to reproduce.
- Platform scraping is fragile, legally risky, and often violates platform rules.

SeedScope takes a safer workflow: start from user-provided screenshots, extract structured signals, classify marketing patterns, and generate a report that content teams can review and adapt.

The goal is not to replace human strategy work. The goal is to make repeatable Rednote seeding analysis faster, cleaner, and safer.

## Core Features

- Create a Brand A vs Brand B competitive analysis project.
- Upload multiple Rednote/Xiaohongshu note screenshots for each brand.
- OCR extraction for title, cover copy, likes, collects, comments, publish time, and account name.
- Editable correction table for OCR results.
- Rule-based classification for content type, title pattern, cover pattern, body structure, CTA pattern, and risk pattern.
- Competitive report generation in Markdown and HTML.
- Excel export for note-level analysis.
- Optional LLM integration via OpenAI-compatible providers.
- Built-in provider support for OpenAI, DeepSeek, Qwen, Kimi, Zhipu GLM, and mock demo mode.
- Docker Compose setup for one-command local startup.

## Workflow

1. Create a project with Brand A, Brand B, industry, period, and objective.
2. Upload screenshots for Brand A and Brand B separately.
3. Run OCR extraction.
4. Review and correct extracted fields.
5. Generate content tags and risk labels.
6. Generate a competitive seeding report.
7. Export Markdown, HTML, and Excel.

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
- DeepSeek / Qwen / Kimi / Zhipu GLM support for China users
- Rule-based mode available without any API key

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
LLM_PROVIDER=deepseek
LLM_MODEL=
OPENAI_API_KEY=
DEEPSEEK_API_KEY=
QWEN_API_KEY=
KIMI_API_KEY=
ZHIPU_API_KEY=
DATABASE_URL=sqlite:///./data/seedscope.db
UPLOAD_DIR=./data/uploads
EXPORT_DIR=./data/exports
REPORT_TEMPLATE_DIR=./packages/report_templates
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
```

Notes:

- `LLM_PROVIDER=mock` enables a no-key demo mode.
- Mainland China users can use `deepseek`, `qwen`, `kimi`, or `zhipu`.
- Set `LLM_PROVIDER=openai` and `OPENAI_API_KEY` only if you want OpenAI-assisted summaries.
- Uploaded files and exports are stored under `data/` by default.

## Demo Data

SeedScope includes fully anonymized demo data:

- [`examples/demo_notes.json`](examples/demo_notes.json)
- [`examples/demo_ocr_texts/`](examples/demo_ocr_texts/)
- [`examples/sample_notes.xlsx`](examples/sample_notes.xlsx)

The demo data uses only Brand A / Brand B, anonymized account names, synthetic engagement metrics, and generic online education examples.

## Demo Report

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

Each category includes an English key, Chinese label, detection signals, description, and example.

## Roadmap

See [`docs/roadmap.md`](docs/roadmap.md).

## FAQ

### Does SeedScope scrape Rednote/Xiaohongshu?

No. SeedScope does not scrape, crawl, automate login, bypass access controls, or extract platform data directly.

### What data does SeedScope analyze?

Only screenshots and fields uploaded by the user. The user is responsible for ensuring they have the right to process those materials.

### Can I use it without an LLM API key?

Yes. Use `LLM_PROVIDER=mock` for no-key demo mode. If a real provider is not configured, SeedScope falls back to rule-based classification.

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

Do not use SeedScope to collect private data without permission, identify or track private individuals, bypass platform restrictions, scrape any platform, publish misleading competitor claims, or process confidential internal materials without authorization.

## Contributing

Contributions are welcome.

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

MIT License. See [`LICENSE`](LICENSE) for details.
