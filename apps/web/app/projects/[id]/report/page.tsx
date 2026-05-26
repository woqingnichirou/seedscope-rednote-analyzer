"use client";

import { useParams } from "next/navigation";
import { useState } from "react";
import { API_BASE, createExports, generateReport } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Shell } from "@/components/shell";

export default function ReportPage() {
  const params = useParams<{ id: string }>();
  const projectId = Number(params.id);
  const [markdown, setMarkdown] = useState("");
  const [html, setHtml] = useState("");
  const [exports, setExports] = useState<{ markdown_url: string; html_url: string; excel_url: string } | null>(null);
  const [message, setMessage] = useState("");

  async function runReport() {
    setMessage("报告生成中...");
    const report = await generateReport(projectId);
    setMarkdown(report.markdown);
    setHtml(report.html);
    setMessage("报告已生成");
  }

  async function runExport() {
    setMessage("导出中...");
    setExports(await createExports(projectId));
    setMessage("导出已完成");
  }

  return (
    <Shell>
      <div className="mb-4 flex flex-wrap items-center gap-3">
        <Button onClick={runReport}>生成报告</Button>
        <Button variant="outline" onClick={runExport}>导出 Markdown / HTML / Excel</Button>
        {message ? <span className="text-sm text-neutral-600">{message}</span> : null}
      </div>
      {exports ? (
        <div className="mb-5 flex flex-wrap gap-3 text-sm">
          <a className="text-primary underline" href={`${API_BASE}${exports.markdown_url}`} target="_blank">Markdown</a>
          <a className="text-primary underline" href={`${API_BASE}${exports.html_url}`} target="_blank">HTML</a>
          <a className="text-primary underline" href={`${API_BASE}${exports.excel_url}`} target="_blank">Excel</a>
        </div>
      ) : null}
      <div className="grid gap-5 xl:grid-cols-2">
        <Card>
          <CardHeader><CardTitle>Markdown</CardTitle></CardHeader>
          <CardContent>
            <pre className="max-h-[720px] overflow-auto whitespace-pre-wrap rounded-md bg-muted p-4 text-xs leading-6">{markdown || "点击生成报告后显示 Markdown。"}</pre>
          </CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle>HTML 预览</CardTitle></CardHeader>
          <CardContent>
            <iframe className="h-[720px] w-full rounded-md border border-border" srcDoc={html || "<p style='font-family:sans-serif;padding:16px'>点击生成报告后显示 HTML。</p>"} />
          </CardContent>
        </Card>
      </div>
    </Shell>
  );
}
