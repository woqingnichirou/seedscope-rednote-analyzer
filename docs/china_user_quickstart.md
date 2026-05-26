# 大陆用户 Windows 本地运行指南

这份指南面向不熟悉代码的品牌方、代理商和内容营销团队用户。目标是在 Windows 电脑上本地运行 SeedScope，上传 demo 数据并导出报告。

## 1. 安装 Node.js

1. 打开 Node.js 官网：https://nodejs.org/
2. 下载 LTS 版本。
3. 按默认选项安装。
4. 安装完成后打开 PowerShell，输入：

```powershell
node -v
npm -v
```

如果能看到版本号，说明安装成功。

## 2. 安装 Python

1. 打开 Python 官网：https://www.python.org/downloads/
2. 下载 Python 3.11 或 3.12。
3. 安装时勾选 `Add python.exe to PATH`。
4. 安装完成后打开 PowerShell，输入：

```powershell
python --version
```

如果能看到版本号，说明安装成功。

## 3. 下载项目

如果已经安装 Git：

```powershell
git clone https://github.com/woqingnichirou/seedscope-rednote-analyzer.git
cd seedscope-rednote-analyzer
```

如果不会使用 Git，可以在 GitHub 页面点击 `Code`，选择 `Download ZIP`，解压后进入项目文件夹。

## 4. 配置 API Key

SeedScope 默认可以不配置 API Key，使用本地规则模式。

复制 `.env.example` 为 `.env`：

```powershell
copy .env.example .env
```

默认配置：

```env
LLM_PROVIDER=rule
OPENAI_API_KEY=
```

如果你需要使用 OpenAI 兼容模型辅助生成洞察，再填写：

```env
LLM_PROVIDER=openai
OPENAI_API_KEY=你的_API_Key
```

请不要把 `.env` 上传到 GitHub 或发给他人。

## 5. 安装依赖

在项目根目录执行：

```powershell
python -m venv .venv
.\.venv\Scripts\activate
pip install -r apps/api/requirements.txt
npm --prefix apps/web install
```

如果下载速度较慢，建议更换网络环境后重试。

## 6. 双击启动脚本

完成依赖安装后，可以双击：

```text
scripts/start_windows.bat
```

脚本会自动打开两个窗口：

- `SeedScope API`：后端服务，地址为 `http://127.0.0.1:8000`
- `SeedScope Web`：前端服务，地址为 `http://127.0.0.1:3000`

如果你希望手动启动，也可以使用以下命令。

后端：

```powershell
.\.venv\Scripts\activate
python -m uvicorn apps.api.app.main:app --host 127.0.0.1 --port 8000
```

前端另开一个 PowerShell：

```powershell
npm --prefix apps/web run dev -- --hostname 127.0.0.1 --port 3000
```

## 7. 打开本地网页

浏览器打开：

```text
http://127.0.0.1:3000
```

如果页面打不开，先确认两个 PowerShell 窗口都没有报错。

## 8. 上传 demo 数据

项目内置 demo 文件：

- `examples/demo_notes.json`
- `examples/demo_ocr_texts/`
- `examples/sample_notes.xlsx`

第一版前端主要支持截图上传。你可以先创建一个项目，再使用自己的测试截图体验 OCR 和校正流程。

如果只是查看报告效果，可以直接打开：

- `examples/sample_report.md`
- `examples/sample_report.html`

## 9. 导出报告

在报告页点击导出后，会生成：

- Markdown 报告
- HTML 报告
- Excel 明细

默认导出目录：

```text
data/exports
```

## 10. 常见问题

### 没有 API Key 能用吗？

能。默认规则模式可以完成基础分析和报告生成。

### OCR 识别不准怎么办？

在校正页手动修改。SeedScope 的正式流程默认包含人工校正。

### 是否会上传数据到云端？

默认不会。SeedScope 是本地优先工具，上传文件、数据库和导出文件都保存在本机。

### 是否能自动抓取平台笔记？

不能。SeedScope 不做爬虫，不绕过平台限制，只处理用户上传截图。

## 11. 安全提醒

- 不要上传真实隐私数据。
- 不要上传未授权截图。
- 不要把 `.env`、API Key 或内部资料提交到 GitHub。
- 示例报告只使用 Brand A / Brand B，不包含真实品牌和真实达人信息。
