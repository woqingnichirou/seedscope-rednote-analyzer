import { CheckCircle2, KeyRound, ServerCog, ShieldCheck } from "lucide-react";
import { Shell } from "@/components/shell";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const providers = [
  { name: "DeepSeek", value: "deepseek", note: "推荐大陆用户优先尝试，OpenAI-compatible API。" },
  { name: "Qwen", value: "qwen", note: "适合阿里云 DashScope 兼容模式。" },
  { name: "Kimi", value: "kimi", note: "适合 Moonshot/Kimi API 用户。" },
  { name: "Zhipu GLM", value: "zhipu", note: "适合智谱 GLM API 用户。" },
  { name: "OpenAI", value: "openai", note: "适合可稳定访问 OpenAI API 的用户。" },
  { name: "Mock", value: "mock", note: "无 API Key demo 模式，不调用真实模型。" },
];

export default function SettingsPage() {
  return (
    <Shell>
      <div className="mb-6">
        <p className="text-sm font-medium text-primary">Model Configuration</p>
        <h1 className="mt-2 text-3xl font-semibold tracking-normal">模型配置说明</h1>
        <p className="mt-3 max-w-3xl text-sm leading-6 text-neutral-600">
          SeedScope 通过本地 `.env` 选择模型供应商。大陆用户建议优先使用 DeepSeek、Qwen 或 Kimi。
          API Key 只保存在本机环境文件中，不上传云端，也不应写入 Git。
        </p>
      </div>

      <div className="grid gap-5 lg:grid-cols-[1fr_1fr]">
        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2"><ServerCog className="h-5 w-5" /> Supported Providers</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid gap-3">
              {providers.map((provider) => (
                <div key={provider.value} className="rounded-md border border-border p-4">
                  <div className="flex items-center justify-between gap-3">
                    <span className="font-medium">{provider.name}</span>
                    <code className="rounded bg-muted px-2 py-1 text-xs">LLM_PROVIDER={provider.value}</code>
                  </div>
                  <p className="mt-2 text-sm text-neutral-600">{provider.note}</p>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <CardTitle className="flex items-center gap-2"><KeyRound className="h-5 w-5" /> .env Example</CardTitle>
          </CardHeader>
          <CardContent>
            <pre className="overflow-auto rounded-md bg-muted p-4 text-xs leading-6">{`LLM_PROVIDER=deepseek
LLM_MODEL=
OPENAI_API_KEY=
DEEPSEEK_API_KEY=
QWEN_API_KEY=
KIMI_API_KEY=
ZHIPU_API_KEY=`}</pre>
            <div className="mt-5 grid gap-3 text-sm text-neutral-700">
              <div className="flex gap-2"><CheckCircle2 className="mt-0.5 h-4 w-4 text-primary" /> 推荐大陆用户使用 DeepSeek / Qwen / Kimi。</div>
              <div className="flex gap-2"><CheckCircle2 className="mt-0.5 h-4 w-4 text-primary" /> 首次体验可以使用 `LLM_PROVIDER=mock`，不需要 API Key。</div>
              <div className="flex gap-2"><ShieldCheck className="mt-0.5 h-4 w-4 text-primary" /> API Key 只保存在本地 `.env`，不会上传到 SeedScope 云端。</div>
              <div className="flex gap-2"><ShieldCheck className="mt-0.5 h-4 w-4 text-primary" /> `.env` 已在 `.gitignore` 中，不要提交到 GitHub。</div>
            </div>
          </CardContent>
        </Card>
      </div>
    </Shell>
  );
}
