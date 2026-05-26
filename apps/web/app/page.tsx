import Link from "next/link";
import { ArrowRight, FileSpreadsheet, ScanText, Tags } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Shell } from "@/components/shell";

export default function HomePage() {
  return (
    <Shell>
      <section className="grid gap-8 lg:grid-cols-[1.1fr_0.9fr] lg:items-center">
        <div>
          <p className="mb-3 text-sm font-medium text-primary">AI-powered Rednote Competitive Content Analyzer</p>
          <h1 className="max-w-3xl text-4xl font-semibold leading-tight tracking-normal">
            用截图生成 Brand A vs Brand B 小红书种草竞品分析报告
          </h1>
          <p className="mt-5 max-w-2xl text-base leading-7 text-neutral-600">
            上传两组高赞笔记截图，SeedScope 通过 OCR 和规则/LLM 分析识别标题、封面文案、互动数据、正文关键词，并生成可导出的 Markdown、HTML 和 Excel。
          </p>
          <div className="mt-7 flex gap-3">
            <Button asChild>
              <Link href="/projects/new">
                创建项目 <ArrowRight className="h-4 w-4" />
              </Link>
            </Button>
            <Button variant="outline" asChild>
              <Link href="https://www.xiaohongshu.com" target="_blank">仅分析用户上传截图</Link>
            </Button>
          </div>
        </div>
        <div className="rounded-lg border border-border bg-muted p-5">
          <div className="grid gap-3">
            {[
              ["1", "创建项目", "填写品牌、行业、周期和分析目标"],
              ["2", "上传截图", "分别上传 Brand A 和 Brand B 的多张笔记截图"],
              ["3", "校正识别", "编辑 OCR 提取出的标题、互动和账号信息"],
              ["4", "生成报告", "自动归因内容策略并导出分析结果"],
            ].map(([step, title, desc]) => (
              <div key={step} className="flex gap-3 rounded-md bg-white p-4">
                <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-md bg-primary text-sm font-semibold text-white">{step}</span>
                <div>
                  <div className="font-medium">{title}</div>
                  <div className="text-sm text-neutral-600">{desc}</div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      <section className="mt-10 grid gap-4 md:grid-cols-3">
        <Card>
          <CardHeader><CardTitle className="flex items-center gap-2"><ScanText className="h-5 w-5" /> OCR 识别</CardTitle></CardHeader>
          <CardContent className="text-sm text-neutral-600">优先 PaddleOCR，安装失败时使用 Tesseract，仍失败时保留文件名和可编辑字段。</CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle className="flex items-center gap-2"><Tags className="h-5 w-5" /> 自动标签</CardTitle></CardHeader>
          <CardContent className="text-sm text-neutral-600">识别内容类型、标题类型、封面类型、正文结构和 CTA 承接方式。</CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle className="flex items-center gap-2"><FileSpreadsheet className="h-5 w-5" /> 多格式导出</CardTitle></CardHeader>
          <CardContent className="text-sm text-neutral-600">基于 Jinja2 生成 Markdown 和 HTML，并用 openpyxl 导出笔记明细。</CardContent>
        </Card>
      </section>
    </Shell>
  );
}
