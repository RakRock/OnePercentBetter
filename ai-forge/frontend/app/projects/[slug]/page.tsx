"use client";

import { useEffect, useState } from "react";
import { useParams } from "next/navigation";
import Link from "next/link";
import { fetchProject, type Project } from "@/lib/api";

export default function ProjectDetailPage() {
  const params = useParams();
  const slug = params.slug as string;
  const [project, setProject] = useState<Project | null>(null);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!slug) return;
    fetchProject(slug)
      .then(setProject)
      .catch((e) => setError(e.message));
  }, [slug]);

  if (error) return <p className="text-red-400">{error}</p>;
  if (!project) return <p className="text-forge-muted">Loading project…</p>;

  return (
    <div className="space-y-6">
      <Link href="/projects" className="text-sm text-forge-accent2 hover:underline">
        ← All projects
      </Link>
      <h1 className="text-3xl font-bold">{project.title}</h1>
      <p className="text-forge-muted">{project.summary}</p>

      <div className="card">
        <h2 className="font-semibold">Milestones</h2>
        <ol className="mt-4 space-y-4">
          {project.checkpoints
            .sort((a, b) => a.order_index - b.order_index)
            .map((cp, idx) => (
              <li key={cp.id} className="border-l-2 border-forge-accent pl-4">
                <p className="font-medium">
                  {idx + 1}. {cp.title}
                </p>
                <p className="text-sm text-forge-muted">{cp.description}</p>
                <ul className="mt-2 list-disc pl-5 text-sm text-slate-300">
                  {cp.tasks.map((t) => (
                    <li key={t}>{t}</li>
                  ))}
                </ul>
              </li>
            ))}
        </ol>
      </div>

      <div className="flex gap-3">
        <Link href="/mentor" className="btn-primary">
          Ask the mentor
        </Link>
        <Link href="/dashboard" className="btn-ghost">
          Dashboard
        </Link>
      </div>
    </div>
  );
}
