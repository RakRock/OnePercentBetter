import Link from "next/link";

export default function LandingPage() {
  return (
    <div className="space-y-10">
      <section className="card border-forge-accent/30">
        <p className="font-mono text-sm text-forge-accent2">PHASE 1 — SHIP REAL AI SYSTEMS</p>
        <h1 className="mt-3 text-4xl font-bold tracking-tight md:text-5xl">
          Learn AI engineering by building production projects.
        </h1>
        <p className="mt-4 max-w-2xl text-lg text-forge-muted">
          AI Forge combines guided labs, a Claude-powered mentor, checkpoints, and
          evaluation — like ByteByteGo meets Replit meets GitHub Classroom.
        </p>
        <div className="mt-8 flex flex-wrap gap-4">
          <Link href="/dashboard" className="btn-primary">
            Enter the forge
          </Link>
          <Link href="/projects" className="btn-ghost">
            Browse projects
          </Link>
        </div>
      </section>

      <section className="grid gap-4 md:grid-cols-3">
        {[
          ["🧠", "AI Mentor", "Socratic hints — not answer dumps"],
          ["🧪", "Project Labs", "RAG, agents, inference APIs"],
          ["📊", "Evaluation", "Rubrics + improvement plans"],
        ].map(([icon, title, desc]) => (
          <div key={title} className="card">
            <div className="text-3xl">{icon}</div>
            <h3 className="mt-2 font-semibold">{title}</h3>
            <p className="mt-1 text-sm text-forge-muted">{desc}</p>
          </div>
        ))}
      </section>
    </div>
  );
}
