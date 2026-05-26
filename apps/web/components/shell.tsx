import Link from "next/link";
import { BarChart3, FileText, Settings, UploadCloud } from "lucide-react";

export function Shell({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen">
      <header className="border-b border-border">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
          <Link href="/" className="flex items-center gap-2 text-lg font-semibold">
            <BarChart3 className="h-5 w-5 text-primary" />
            SeedScope
          </Link>
          <nav className="flex items-center gap-5 text-sm text-neutral-600">
            <span className="flex items-center gap-1"><UploadCloud className="h-4 w-4" /> OCR</span>
            <span className="flex items-center gap-1"><FileText className="h-4 w-4" /> Report</span>
            <Link href="/settings" className="flex items-center gap-1 hover:text-neutral-900"><Settings className="h-4 w-4" /> Settings</Link>
          </nav>
        </div>
      </header>
      <main className="mx-auto max-w-7xl px-6 py-8">{children}</main>
    </div>
  );
}
