"use client";

import Link from "next/link";
import { useParams } from "next/navigation";
import { useEffect, useState } from "react";
import { getProject, Note, tagProject, updateNote } from "@/lib/api";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Shell } from "@/components/shell";

const fields: Array<keyof Note> = ["account_name", "title", "cover_text", "likes", "collects", "comments", "published_at"];

export default function ReviewPage() {
  const params = useParams<{ id: string }>();
  const projectId = Number(params.id);
  const [notes, setNotes] = useState<Note[]>([]);
  const [message, setMessage] = useState("");

  useEffect(() => {
    getProject(projectId).then((data) => setNotes(data.notes));
  }, [projectId]);

  function updateLocal(id: number, key: keyof Note, value: string) {
    setNotes((items) => items.map((note) => (note.id === id ? { ...note, [key]: ["likes", "collects", "comments"].includes(key) ? Number(value) : value } : note)));
  }

  async function saveAll() {
    setMessage("保存中...");
    await Promise.all(notes.map((note) => updateNote(note)));
    setMessage("已保存");
  }

  async function classify() {
    setMessage("标签生成中...");
    const tagged = await tagProject(projectId);
    setNotes(tagged);
    setMessage("标签已生成");
  }

  return (
    <Shell>
      <div className="mb-4 flex flex-wrap items-center gap-3">
        <Button onClick={saveAll}>保存校正</Button>
        <Button variant="outline" onClick={classify}>生成标签</Button>
        <Button variant="outline" asChild><Link href={`/projects/${projectId}/tags`}>查看标签分析</Link></Button>
        {message ? <span className="text-sm text-neutral-600">{message}</span> : null}
      </div>
      <div className="overflow-x-auto rounded-lg border border-border">
        <table className="w-full min-w-[1180px] border-collapse text-sm">
          <thead className="bg-muted">
            <tr>
              <th className="border-b border-border p-2 text-left">品牌</th>
              {fields.map((field) => <th key={field} className="border-b border-border p-2 text-left">{field}</th>)}
            </tr>
          </thead>
          <tbody>
            {notes.map((note) => (
              <tr key={note.id}>
                <td className="border-b border-border p-2">{note.brand_key === "brand_a" ? "Brand A" : "Brand B"}</td>
                {fields.map((field) => (
                  <td key={field} className="border-b border-border p-2">
                    <Input value={String(note[field] ?? "")} onChange={(event) => updateLocal(note.id, field, event.target.value)} />
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </Shell>
  );
}
