"use client";

import { useRouter } from "next/navigation";
import { FormEvent, useState } from "react";
import { createProject } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Input, Textarea } from "@/components/ui/input";
import { Shell } from "@/components/shell";

export default function NewProjectPage() {
  const router = useRouter();
  const [form, setForm] = useState({
    brand_a: "Brand A",
    brand_b: "Brand B",
    industry: "在线教育",
    period: "近半年",
    objective: "分析两组高赞笔记的内容策略差异，并输出 Brand A 的优化动作。",
  });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      const project = await createProject(form);
      router.push(`/projects/${project.id}/upload`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "创建失败");
    } finally {
      setLoading(false);
    }
  }

  return (
    <Shell>
      <Card className="max-w-3xl">
        <CardHeader>
          <CardTitle>创建竞品分析项目</CardTitle>
        </CardHeader>
        <CardContent>
          <form onSubmit={onSubmit} className="grid gap-4">
            <div className="grid gap-4 md:grid-cols-2">
              <label className="grid gap-2 text-sm font-medium">优化对象<Input value={form.brand_a} onChange={(e) => setForm({ ...form, brand_a: e.target.value })} required /></label>
              <label className="grid gap-2 text-sm font-medium">对标对象<Input value={form.brand_b} onChange={(e) => setForm({ ...form, brand_b: e.target.value })} required /></label>
            </div>
            <div className="grid gap-4 md:grid-cols-2">
              <label className="grid gap-2 text-sm font-medium">行业<Input value={form.industry} onChange={(e) => setForm({ ...form, industry: e.target.value })} required /></label>
              <label className="grid gap-2 text-sm font-medium">周期<Input value={form.period} onChange={(e) => setForm({ ...form, period: e.target.value })} required /></label>
            </div>
            <label className="grid gap-2 text-sm font-medium">分析目标<Textarea value={form.objective} onChange={(e) => setForm({ ...form, objective: e.target.value })} required /></label>
            {error ? <p className="text-sm text-primary">{error}</p> : null}
            <Button className="w-fit" disabled={loading}>{loading ? "创建中..." : "创建并上传截图"}</Button>
          </form>
        </CardContent>
      </Card>
    </Shell>
  );
}
