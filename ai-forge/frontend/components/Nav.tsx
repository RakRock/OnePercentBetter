import Link from "next/link";

const links = [
  { href: "/dashboard", label: "Dashboard" },
  { href: "/projects", label: "Projects" },
  { href: "/mentor", label: "AI Mentor" },
];

export function Nav() {
  return (
    <header className="border-b border-slate-800 bg-forge-panel/80 backdrop-blur">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-4 py-4">
        <Link href="/" className="font-mono text-lg font-bold text-forge-accent2">
          ⚒ AI Forge
        </Link>
        <nav className="flex gap-4 text-sm text-slate-300">
          {links.map((l) => (
            <Link key={l.href} href={l.href} className="hover:text-white">
              {l.label}
            </Link>
          ))}
        </nav>
      </div>
    </header>
  );
}
