"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { FormEvent, useState } from "react";
import { UploadCloud } from "lucide-react";
import { uploadNotes } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Shell } from "@/components/shell";

export default function UploadPage() {
  const params = useParams<{ id: string }>();
  const projectId = Number(params.id);
  const [brandAFiles, setBrandAFiles] = useState<FileList | null>(null);
  const [brandBFiles, setBrandBFiles] = useState<FileList | null>(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    setLoading(true);
    setMessage("");
    try {
      if (brandAFiles?.length) await uploadNotes(projectId, "brand_a", brandAFiles);
      if (brandBFiles?.length) await uploadNotes(projectId, "brand_b", brandBFiles);
      setMessage("上传和 OCR 已完成，可以进入校正页。");
    } catch (err) {
      setMessage(err instanceof Error ? err.message : "上传失败");
    } finally {
      setLoading(false);
    }
  }

  return (
    <Shell>
      <form onSubmit={onSubmit} className="grid gap-5 lg:grid-cols-2">
        <Uploader title="Brand A 截图" onChange={setBrandAFiles} />
        <Uploader title="Brand B 截图" onChange={setBrandBFiles} />
        <div className="lg:col-span-2 flex items-center gap-3">
          <Button disabled={loading}>{loading ? "识别中..." : "上传并 OCR 识别"}</Button>
          <Button variant="outline" asChild><Link href={`/projects/${projectId}/review`}>进入校正页</Link></Button>
          {message ? <span className="text-sm text-neutral-600">{message}</span> : null}
        </div>
      </form>
    </Shell>
  );
}

function Uploader({ title, onChange }: { title: string; onChange: (files: FileList | null) => void }) {
  return (
    <Card>
      <CardHeader><CardTitle>{title}</CardTitle></CardHeader>
      <CardContent>
        <label className="flex min-h-52 cursor-pointer flex-col items-center justify-center rounded-md border border-dashed border-border bg-muted p-6 text-center">
          <UploadCloud className="mb-3 h-8 w-8 text-primary" />
          <span className="font-medium">选择多张截图</span>
          <span className="mt-1 text-sm text-neutral-600">支持 PNG/JPG/WebP，本地存储，不包含爬虫能力</span>
          <input className="hidden" type="file" multiple accept="image/*" onChange={(event) => onChange(event.target.files)} />
        </label>
      </CardContent>
    </Card>
  );
}
