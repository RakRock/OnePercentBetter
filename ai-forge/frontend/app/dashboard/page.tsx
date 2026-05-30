"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { fetchMe, fetchProjects, type User, type Project } from "@/lib/api";

export default function DashboardPage() {
  const [user, setUser] = useState<User | null>(null);
  const [projects, setProjects] = useState<Project[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([fetchMe(), fetchProjects()])
      .then(([u, p]) => {
        setUser(u);
        setProjects(p);
      })
      .catch((e) => setError(e.message));
  }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Dashboard</h1>
      {error && <p className="text-red-400">{error}</p>}
      {user && (
        <p className="text-forge-muted">
          Welcome back, <span className="text-white">{user.display_name}</span>
        </p>
      )}

      <div className="grid gap-4 md:grid-cols-2">
        <Link href="/mentor" className="card hover:border-forge-accent">
          <h2 className="text-xl font-semibold">🧠 AI Mentor</h2>
          <p className="mt-2 text-sm text-forge-muted">
            Claude-powered guidance with teacher, architect, and debugger modes.
          </p>
        </Link>
        <Link href="/projects" className="card hover:border-forge-accent2">
          <h2 className="text-xl font-semibold">🧪 Project Labs</h2>
          <p className="mt-2 text-sm text-forge-muted">
            {projects.length} hands-on labs with milestones and scaffolding.
          </p>
        </Link>
      </div>

      <section className="card">
        <h2 className="font-semibold">Continue learning</h2>
        <ul className="mt-4 space-y-3">
          {projects.map((p) => (
            <li key={p.id} className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div>
                <p className="font-medium">{p.title}</p>
                <p className="text-sm text-forge-muted">{p.difficulty}</p>
              </div>
              <Link href={`/projects/${p.slug}`} className="btn-ghost text-sm">
                Open lab
              </Link>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}
