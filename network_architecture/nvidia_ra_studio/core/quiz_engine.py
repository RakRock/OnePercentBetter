"""Quiz bank and scoring for NVIDIA AI Enterprise RA."""

from __future__ import annotations

import random
from typing import Any

from .content_catalog import MODULES
from .models import QuizQuestion

# Hand-crafted questions (2 per module) + templates fill to 5+ each
_EXTRA: list[dict[str, Any]] = [
    {
        "module_id": 1,
        "prompt": "What is the primary purpose of the NVIDIA AI Enterprise Reference Architecture?",
        "choices": [
            "Sell GPU hardware only",
            "Document a validated software-first blueprint for production AI on Kubernetes",
            "Replace Kubernetes with a proprietary orchestrator",
            "Provide gaming driver downloads",
        ],
        "correct": [1],
        "explanation": "The RA is a validated, software-first blueprint for enterprise AI on K8s.",
    },
    {
        "module_id": 1,
        "prompt": "Who is the primary audience for mastering the RA software/platform view?",
        "choices": ["Game developers only", "Enterprise platform and cloud architects", "Mobile app designers", "CAD users"],
        "correct": [1],
        "explanation": "Platform engineers, cloud architects, and AI infra engineers are the target learners.",
    },
    {
        "module_id": 5,
        "prompt": "GPU Operator primarily automates deployment of which stack components?",
        "choices": [
            "Only LLM weights",
            "Driver, container toolkit, device plugin, and related GPU operands",
            "Only ingress controllers",
            "Only vector databases",
        ],
        "correct": [1],
        "explanation": "GPU Operator manages the NVIDIA GPU software stack on Kubernetes nodes.",
    },
    {
        "module_id": 5,
        "qtype": "scenario",
        "prompt": "A new GPU node shows zero nvidia.com/gpu allocatable. First check?",
        "choices": [
            "Delete all pods cluster-wide",
            "GPU Operator pods and device plugin on that node",
            "Change DNS settings",
            "Upgrade the ingress controller",
        ],
        "correct": [1],
        "explanation": "Verify GPU Operator operands and device plugin registration on the node.",
    },
    {
        "module_id": 10,
        "prompt": "NIM Operator manages NIM workloads using:",
        "choices": ["Excel spreadsheets", "Kubernetes Custom Resource Definitions (CRDs)", "SSH only", "Manual systemd units"],
        "correct": [1],
        "explanation": "NIM Operator is Kubernetes-native and driven by NIM CRDs.",
    },
    {
        "module_id": 11,
        "prompt": "NIMCache exists primarily to:",
        "choices": [
            "Replace GPUs",
            "Pre-pull and store model artifacts for faster NIMService startup",
            "Run CI pipelines",
            "Manage user passwords",
        ],
        "correct": [1],
        "explanation": "NIMCache localizes model artifacts on cluster storage.",
    },
    {
        "module_id": 15,
        "qtype": "multi",
        "prompt": "Select all typical components in a RAG architecture on NVIDIA AI Enterprise:",
        "choices": ["Embedding NIM", "Vector database", "LLM NIM", "Game engine renderer"],
        "correct": [0, 1, 2],
        "explanation": "RAG uses embedding, retrieval store, and LLM inference — not game engines.",
    },
    {
        "module_id": 17,
        "prompt": "Production Branch (PB) in NVIDIA AI Enterprise lifecycle typically means:",
        "choices": [
            "Unsupported experimental code",
            "Stabilized release branch with defined support for production",
            "End of all updates",
            "Consumer GPU drivers only",
        ],
        "correct": [1],
        "explanation": "PB is the stabilized branch intended for production deployments.",
    },
    {
        "module_id": 18,
        "prompt": "DCGM is primarily used for:",
        "choices": [
            "GPU metrics and health monitoring",
            "Word processing",
            "DNS load balancing",
            "Image editing",
        ],
        "correct": [0],
        "explanation": "DCGM provides GPU telemetry for observability and troubleshooting.",
    },
]


def _template_questions(module_id: int, domain: str, title: str) -> list[QuizQuestion]:
    """Generate template MCQs so each module has at least 5 questions."""
    templates = [
        (
            f"Which layer of the RA most directly relates to '{title}'?",
            ["Application layer only", "Infrastructure / platform software layer", "Physical desk furniture", "None — unrelated"],
            [1],
            f"'{title}' maps to the RA software stack documented for enterprise AI platforms.",
        ),
        (
            f"For {domain}, official guidance should be verified in:",
            ["Random forums only", "NVIDIA AI Enterprise RA and operator documentation", "Deprecated README files", "Unverified blogs"],
            [1],
            "Always ground decisions in official NVIDIA docs and support matrices.",
        ),
        (
            f"A platform engineer implementing '{title}' should coordinate with:",
            ["Only graphic designers", "Cluster admins, security, networking, and ML app teams", "Nobody", "HR payroll"],
            [1],
            "RA implementations are cross-functional platform efforts.",
        ),
        (
            f"Before production rollout of {domain}, you must verify:",
            ["Random blog posts", "NVIDIA AI Enterprise support matrix and lifecycle docs", "Nothing", "Social media trends"],
            [1],
            "Version compatibility must come from official NVIDIA lifecycle documentation.",
        ),
        (
            f"Troubleshooting '{title}' typically starts at which RA layer?",
            ["Application or infrastructure layer depending on symptom", "Only physical furniture", "DNS only", "Email server"],
            [0],
            "Triage whether the issue is app workload vs platform operator/infrastructure.",
        ),
    ]
    out: list[QuizQuestion] = []
    for i, (prompt, choices, correct, explanation) in enumerate(templates):
        out.append(
            QuizQuestion(
                id=f"m{module_id}-tpl-{i}",
                module_id=module_id,
                domain=domain,
                qtype="mcq",
                prompt=prompt,
                choices=choices,
                correct=correct,
                explanation=explanation,
            )
        )
    return out


def build_quiz_bank() -> list[QuizQuestion]:
    bank: list[QuizQuestion] = []
    extra_by_mod: dict[int, list] = {}
    for e in _EXTRA:
        extra_by_mod.setdefault(e["module_id"], []).append(e)

    for mod in MODULES:
        count = 0
        for e in extra_by_mod.get(mod.id, []):
            bank.append(
                QuizQuestion(
                    id=f"m{mod.id}-ex-{count}",
                    module_id=mod.id,
                    domain=mod.domain,
                    qtype=e.get("qtype", "mcq"),
                    prompt=e["prompt"],
                    choices=e["choices"],
                    correct=e["correct"],
                    explanation=e["explanation"],
                )
            )
            count += 1
        bank.extend(_template_questions(mod.id, mod.domain, mod.title))

    return bank


QUIZ_BANK: list[QuizQuestion] = build_quiz_bank()


def questions_for_module(module_id: int) -> list[QuizQuestion]:
    return [q for q in QUIZ_BANK if q.module_id == module_id]


def questions_for_domain(domain: str) -> list[QuizQuestion]:
    return [q for q in QUIZ_BANK if q.domain == domain]


def final_assessment_questions(n: int = 50, seed: int = 42) -> list[QuizQuestion]:
    rng = random.Random(seed)
    pool = QUIZ_BANK.copy()
    rng.shuffle(pool)
    # Ensure spread across modules
    chosen: list[QuizQuestion] = []
    seen_mod: set[int] = set()
    for q in pool:
        if len(chosen) >= n:
            break
        if q.module_id not in seen_mod or len(seen_mod) >= len(MODULES):
            chosen.append(q)
            seen_mod.add(q.module_id)
    for q in pool:
        if len(chosen) >= n:
            break
        if q not in chosen:
            chosen.append(q)
    return chosen[:n]


def grade_answer(question: QuizQuestion, selected: list[int]) -> bool:
    return sorted(selected) == sorted(question.correct)


def score_quiz(questions: list[QuizQuestion], answers: dict[str, list[int]]) -> tuple[int, int]:
    correct = sum(1 for q in questions if grade_answer(q, answers.get(q.id, [])))
    return correct, len(questions)
