const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export type User = { id: string; email: string; display_name: string };
export type Project = {
  id: string;
  slug: string;
  title: string;
  summary: string;
  difficulty: string;
  stack: string[];
  checkpoints: {
    id: string;
    title: string;
    description: string;
    tasks: string[];
    order_index: number;
  }[];
};

function headers(): HeadersInit {
  const h: HeadersInit = { "Content-Type": "application/json" };
  if (typeof window !== "undefined") {
    const uid = localStorage.getItem("forge_user_id");
    const email = localStorage.getItem("forge_email") || "rakesh@aiforge.local";
    if (uid) h["X-Forge-User-Id"] = uid;
    h["X-Forge-Email"] = email;
  }
  return h;
}

export async function fetchMe(): Promise<User> {
  const res = await fetch(`${API_URL}/api/v1/auth/me`, { headers: headers() });
  if (!res.ok) throw new Error("Failed to load user");
  const user = await res.json();
  if (typeof window !== "undefined") {
    localStorage.setItem("forge_user_id", user.id);
    localStorage.setItem("forge_email", user.email);
  }
  return user;
}

export async function fetchProjects(): Promise<Project[]> {
  const res = await fetch(`${API_URL}/api/v1/projects`, { headers: headers() });
  if (!res.ok) throw new Error("Failed to load projects");
  return res.json();
}

export async function fetchProject(slug: string): Promise<Project> {
  const res = await fetch(`${API_URL}/api/v1/projects/${slug}`, { headers: headers() });
  if (!res.ok) throw new Error("Project not found");
  return res.json();
}

export async function mentorChatSync(
  message: string,
  opts: { conversationId?: string; projectId?: string; personality?: string } = {}
): Promise<{ conversation_id: string; reply: string }> {
  const res = await fetch(`${API_URL}/api/v1/mentor/chat/sync`, {
    method: "POST",
    headers: headers(),
    body: JSON.stringify({
      message,
      conversation_id: opts.conversationId || null,
      project_id: opts.projectId || null,
      personality: opts.personality || "teacher",
    }),
  });
  if (!res.ok) throw new Error("Mentor request failed");
  return res.json();
}
