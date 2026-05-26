export const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export type Project = {
  id: number;
  brand_a: string;
  brand_b: string;
  industry: string;
  period: string;
  objective: string;
  created_at: string;
};

export type Note = {
  id: number;
  project_id: number;
  brand_key: "brand_a" | "brand_b";
  image_path: string;
  account_name: string;
  title: string;
  cover_text: string;
  body_keywords: string;
  likes: number;
  collects: number;
  comments: number;
  published_at: string;
  content_type: string;
  title_type: string;
  cover_type: string;
  body_structure: string;
  cta_type: string;
  raw_ocr_text: string;
  created_at: string;
};

export async function api<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers: init?.body instanceof FormData ? init.headers : { "Content-Type": "application/json", ...(init?.headers || {}) },
  });
  if (!response.ok) {
    const text = await response.text();
    throw new Error(text || `HTTP ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export async function createProject(payload: Omit<Project, "id" | "created_at">) {
  return api<Project>("/api/projects", { method: "POST", body: JSON.stringify(payload) });
}

export async function getProject(id: number) {
  return api<{ project: Project; notes: Note[] }>(`/api/projects/${id}`);
}

export async function uploadNotes(projectId: number, brandKey: "brand_a" | "brand_b", files: FileList) {
  const form = new FormData();
  Array.from(files).forEach((file) => form.append("files", file));
  return api<{ notes: Note[] }>(`/api/projects/${projectId}/uploads/${brandKey}`, { method: "POST", body: form });
}

export async function updateNote(note: Note) {
  return api<Note>(`/api/notes/${note.id}`, { method: "PUT", body: JSON.stringify(note) });
}

export async function tagProject(projectId: number) {
  return api<Note[]>(`/api/projects/${projectId}/tag`, { method: "POST" });
}

export async function generateReport(projectId: number) {
  return api<{ report_id: number; markdown: string; html: string }>(`/api/projects/${projectId}/report`, { method: "POST" });
}

export async function createExports(projectId: number) {
  return api<{ markdown_url: string; html_url: string; excel_url: string; word_url: string; ppt_url: string }>(`/api/projects/${projectId}/exports`, { method: "POST" });
}
