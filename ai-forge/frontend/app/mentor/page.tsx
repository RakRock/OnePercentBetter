"use client";

import { useState } from "react";
import { mentorChatSync } from "@/lib/api";

type ChatLine = { role: "user" | "assistant"; content: string };

const PERSONALITIES = ["teacher", "architect", "debugger", "interviewer", "reviewer"];

export default function MentorPage() {
  const [personality, setPersonality] = useState("teacher");
  const [input, setInput] = useState("");
  const [lines, setLines] = useState<ChatLine[]>([]);
  const [conversationId, setConversationId] = useState<string | undefined>();
  const [loading, setLoading] = useState(false);

  async function send() {
    if (!input.trim()) return;
    const text = input.trim();
    setInput("");
    setLines((prev) => [...prev, { role: "user", content: text }]);
    setLoading(true);
    try {
      const res = await mentorChatSync(text, { conversationId, personality });
      setConversationId(res.conversation_id);
      setLines((prev) => [...prev, { role: "assistant", content: res.reply }]);
    } catch {
      setLines((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Could not reach the mentor API. Is the backend running on :8000?",
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">AI Mentor</h1>
      <p className="text-forge-muted">
        Guided help — questions and hints first, not full solutions.
      </p>

      <div className="flex flex-wrap gap-2">
        {PERSONALITIES.map((p) => (
          <button
            key={p}
            type="button"
            onClick={() => setPersonality(p)}
            className={`rounded-full px-3 py-1 text-sm capitalize ${
              personality === p
                ? "bg-forge-accent text-white"
                : "border border-slate-700 text-slate-300"
            }`}
          >
            {p}
          </button>
        ))}
      </div>

      <div className="card min-h-[320px] space-y-4 font-mono text-sm">
        {lines.length === 0 && (
          <p className="text-forge-muted">
            Ask about RAG, agents, deployment, or your current milestone…
          </p>
        )}
        {lines.map((line, i) => (
          <div
            key={i}
            className={
              line.role === "user"
                ? "rounded-lg bg-slate-800/60 p-3 text-cyan-200"
                : "rounded-lg border border-slate-700 p-3"
            }
          >
            <span className="text-xs uppercase text-forge-muted">{line.role}</span>
            <p className="mt-1 whitespace-pre-wrap">{line.content}</p>
          </div>
        ))}
      </div>

      <div className="flex gap-2">
        <input
          className="flex-1 rounded-lg border border-slate-700 bg-slate-900 px-4 py-2"
          placeholder="What are you stuck on?"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && send()}
        />
        <button type="button" className="btn-primary" onClick={send} disabled={loading}>
          {loading ? "Thinking…" : "Send"}
        </button>
      </div>
    </div>
  );
}
