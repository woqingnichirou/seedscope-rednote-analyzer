"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useMemo, useState } from "react";
import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import { getProject, Note } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Shell } from "@/components/shell";

export default function TagsPage() {
  const params = useParams<{ id: string }>();
  const projectId = Number(params.id);
  const [notes, setNotes] = useState<Note[]>([]);

  useEffect(() => {
    getProject(projectId).then((data) => setNotes(data.notes));
  }, [projectId]);

  const chartData = useMemo(() => {
    const map = new Map<string, { type: string; brand_a: number; brand_b: number }>();
    notes.forEach((note) => {
      const key = note.content_type || "未分类";
      if (!map.has(key)) map.set(key, { type: key, brand_a: 0, brand_b: 0 });
      map.get(key)![note.brand_key] += 1;
    });
    return Array.from(map.values());
  }, [notes]);

  return (
    <Shell>
      <div className="mb-4 flex items-center justify-between">
        <h1 className="text-2xl font-semibold">标签分析</h1>
        <Button asChild><Link href={`/projects/${projectId}/report`}>生成报告</Link></Button>
      </div>
      <Card>
        <CardHeader><CardTitle>内容类型分布</CardTitle></CardHeader>
        <CardContent className="h-80">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="type" />
              <YAxis allowDecimals={false} />
              <Tooltip />
              <Bar dataKey="brand_a" fill="#b42318" name="Brand A" />
              <Bar dataKey="brand_b" fill="#344054" name="Brand B" />
            </BarChart>
          </ResponsiveContainer>
        </CardContent>
      </Card>
      <div className="mt-5 overflow-x-auto rounded-lg border border-border">
        <table className="w-full min-w-[980px] border-collapse text-sm">
          <thead className="bg-muted">
            <tr>
              {["品牌", "标题", "内容类型", "标题类型", "封面类型", "正文结构", "CTA"].map((h) => <th key={h} className="border-b border-border p-2 text-left">{h}</th>)}
            </tr>
          </thead>
          <tbody>
            {notes.map((note) => (
              <tr key={note.id}>
                <td className="border-b border-border p-2">{note.brand_key === "brand_a" ? "Brand A" : "Brand B"}</td>
                <td className="border-b border-border p-2">{note.title}</td>
                <td className="border-b border-border p-2">{note.content_type}</td>
                <td className="border-b border-border p-2">{note.title_type}</td>
                <td className="border-b border-border p-2">{note.cover_type}</td>
                <td className="border-b border-border p-2">{note.body_structure}</td>
                <td className="border-b border-border p-2">{note.cta_type}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Shell>
  );
}
