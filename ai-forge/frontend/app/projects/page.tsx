"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { fetchProjects, type Project } from "@/lib/api";

export default function ProjectsPage() {
  const [projects, setProjects] = useState<Project[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchProjects()
      .then(setProjects)
      .catch((e) => setError(e.message));
  }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Project Labs</h1>
      {error && <p className="text-red-400">{error}</p>}
      <div className="grid gap-4 md:grid-cols-2">
        {projects.map((p) => (
          <Link key={p.id} href={`/projects/${p.slug}`} className="card block hover:border-forge-accent">
            <p className="text-xs uppercase text-forge-accent2">{p.difficulty}</p>
            <h2 className="mt-1 text-xl font-semibold">{p.title}</h2>
            <p className="mt-2 text-sm text-forge-muted">{p.summary}</p>
            <p className="mt-3 text-xs text-slate-400">
              {p.checkpoints.length} milestones · {p.stack.join(", ")}
            </p>
          </Link>
        ))}
      </div>
    </div>
  );
}
