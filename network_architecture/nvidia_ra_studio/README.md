# NVIDIA AI Enterprise RA Learning Studio

AlgoExpert / SystemsExpert–style learning platform for **NVIDIA AI Enterprise Reference Architecture** (software & platform view).

## Quick start

```bash
cd network_architecture/nvidia_ra_studio
pip install -r requirements.txt
streamlit run app.py
```

Open http://localhost:8501

### Optional: Claude (Anthropic) features

Your key in `~/.zshrc` works when you launch Streamlit from a terminal that loaded it:

```bash
export ANTHROPIC_API_KEY=sk-ant-...
```

Or add to `.streamlit/secrets.toml` on Streamlit Cloud:

```toml
ANTHROPIC_API_KEY = "sk-ant-..."
```

Without a key: **template learning plans** and **offline coach** still work.

## OnePercent integration (Rakesh)

In the family app: **Rakesh → Network Architecture → NVDA Reference Architecture**.

## Features

| Feature | Description |
|---------|-------------|
| Dashboard | Progress, quiz average, continue learning |
| Learning path | Role/goal-based week plan (LLM or template) |
| Architecture map | Clickable layered RA diagram |
| Modules | 18 seeded modules with notes & completion |
| Quizzes | Module quizzes + 50-question final |
| Design drills | 8 system-design prompts with rubrics |
| Agent coach | Q&A grounded in catalog + NVIDIA doc links |
| Export | Markdown plan/progress, JSON progress |

## Project layout

```
nvidia_ra_studio/
├── app.py                 # Standalone Streamlit entry
├── core/
│   ├── content_catalog.py # 18 modules
│   ├── quiz_engine.py       # Quiz bank (5+ per domain)
│   ├── design_drills.py
│   ├── planner_agent.py
│   ├── progress_store.py    # SQLite
│   ├── exporter.py
│   └── rag_sources.py       # Official doc URLs
├── pages/                   # UI pages (dashboard, quizzes, …)
├── ui/session.py
├── data/studio.db           # Created at runtime
└── samples/
```

## Persistence

SQLite database at `data/studio.db`:

- users (local profiles)
- user_progress, quiz_attempts, drill_completions
- generated_plans, notes, bookmarks

## Extension guide

1. **Add a module** — edit `core/content_catalog.py` and add quiz entries in `quiz_engine.py`.
2. **Add a design drill** — append to `core/design_drills.py`.
3. **Add architecture layer** — edit `ARCHITECTURE_LAYERS` in `core/models.py`.
4. **Wire a new reference architecture** — add a card in `nvidia_ra_ui.render_network_arch_home()`.

## Official NVIDIA docs

- [Reference Architecture](https://docs.nvidia.com/ai-enterprise/reference-architecture/latest/index.html)
- [GPU Operator](https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/index.html)
- [NIM Operator](https://docs.nvidia.com/nim-operator/latest/index.html)
- [Lifecycle](https://docs.nvidia.com/ai-enterprise/lifecycle/latest/index.html)

## Acceptance checklist

- [x] `streamlit run app.py` works
- [x] No OpenAI key → template planner + offline coach
- [x] SQLite persistence
- [x] Plans, lessons, quizzes, map, drills, export
- [x] Modular Python packages, no hardcoded secrets
