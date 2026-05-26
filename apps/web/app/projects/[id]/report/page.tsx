"use client";

import { useParams } from "next/navigation";
import { useState } from "react";
import { API_BASE, createExports, generateReport } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Shell } from "@/components/shell";

type ExportLinks = {
  markdown_url: string;
  html_url: string;
  excel_url: string;
  word_url: string;
  ppt_url: string;
};

const exportItems: Array<{ label: string; key: keyof ExportLinks }> = [
  { label: "Export Markdown", key: "markdown_url" },
  { label: "Export HTML", key: "html_url" },
  { label: "Export Excel", key: "excel_url" },
  { label: "Export Word", key: "word_url" },
  { label: "Export PPT", key: "ppt_url" },
];

export default function ReportPage() {
  const params = useParams<{ id: string }>();
  const projectId = Number(params.id);
  const [markdown, setMarkdown] = useState("");
  const [html, setHtml] = useState("");
  const [exports, setExports] = useState<ExportLinks | null>(null);
  const [message, setMessage] = useState("");

  async function runReport() {
    setMessage("Generating report...");
    const report = await generateReport(projectId);
    setMarkdown(report.markdown);
    setHtml(report.html);
    setMessage("Report generated.");
  }

  async function runExport() {
    setMessage("Exporting files...");
    setExports(await createExports(projectId));
    setMessage("Exports are ready.");
  }

  return (
    <Shell>
      <div className="mb-4 flex flex-wrap items-center gap-3">
        <Button onClick={runReport}>Generate Report</Button>
        <Button variant="outline" onClick={runExport}>Create Export Files</Button>
        {message ? <span className="text-sm text-neutral-600">{message}</span> : null}
      </div>
      {exports ? (
        <div className="mb-5 flex flex-wrap gap-3 text-sm">
          {exportItems.map((item) => (
            <a key={item.key} className="rounded-md border border-border px-3 py-2 text-primary hover:bg-muted" href={`${API_BASE}${exports[item.key]}`} target="_blank">
              {item.label}
            </a>
          ))}
        </div>
      ) : null}
      <div className="grid gap-5 xl:grid-cols-2">
        <Card>
          <CardHeader><CardTitle>Markdown</CardTitle></CardHeader>
          <CardContent>
            <pre className="max-h-[720px] overflow-auto whitespace-pre-wrap rounded-md bg-muted p-4 text-xs leading-6">{markdown || "Click Generate Report to preview Markdown."}</pre>
          </CardContent>
        </Card>
        <Card>
          <CardHeader><CardTitle>HTML Preview</CardTitle></CardHeader>
          <CardContent>
            <iframe className="h-[720px] w-full rounded-md border border-border" srcDoc={html || "<p style='font-family:sans-serif;padding:16px'>Click Generate Report to preview HTML.</p>"} />
          </CardContent>
        </Card>
      </div>
    </Shell>
  );
}
