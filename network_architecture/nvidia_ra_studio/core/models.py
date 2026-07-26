"""Data models and constants for the learning studio."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

ROLES = ["platform engineer", "architect", "ML engineer", "SRE", "manager"]
LEVELS = ["beginner", "intermediate", "advanced"]
GOALS = [
    "deploy NIM",
    "understand RA",
    "prepare design review",
    "operate platform",
    "troubleshoot",
]
TIMEFRAMES_WEEKS = [2, 4, 6, 8, 12]
DIFFICULTIES = ["beginner", "intermediate", "advanced"]

ARCHITECTURE_LAYERS = [
    {
        "id": "users",
        "name": "Users / Teams",
        "summary": "Data scientists, ML engineers, platform teams, and application owners consuming AI services.",
        "dependencies": [],
        "failure_modes": ["Unclear ownership of models vs platform", "No quota or cost guardrails"],
        "doc_keys": ["ra_index"],
    },
    {
        "id": "app_layer",
        "name": "AI Application Layer",
        "summary": "NIM, NeMo, Triton, PyTorch, TensorFlow, RAPIDS, and NVIDIA SDKs for building and running AI workloads.",
        "dependencies": ["model_deploy", "k8s_platform"],
        "failure_modes": ["Framework/CUDA mismatch", "Model not cached locally", "Wrong NIM profile for GPU"],
        "doc_keys": ["software_stack", "target_workloads"],
    },
    {
        "id": "model_deploy",
        "name": "Model Deployment Layer",
        "summary": "NIM Operator, KServe, RAG pipelines, fine-tuning jobs, and model APIs.",
        "dependencies": ["k8s_platform", "infra_sw"],
        "failure_modes": ["NIMService pending on NIMCache", "KServe ingress misconfiguration", "RAG latency spikes"],
        "doc_keys": ["nim_operator", "kserve"],
    },
    {
        "id": "k8s_platform",
        "name": "Kubernetes Platform Layer",
        "summary": "Namespaces, scheduling, services, ingress, autoscaling, resource quotas, and multi-tenancy.",
        "dependencies": ["platform_base", "infra_sw"],
        "failure_modes": ["GPU pod pending — no extended resource", "Quota exhaustion", "No topology-aware scheduling"],
        "doc_keys": ["platform_overview"],
    },
    {
        "id": "infra_sw",
        "name": "NVIDIA Infrastructure Software",
        "summary": "GPU Operator, Network Operator, DPU Operator, Container Toolkit, device plugin, driver, DOCA, DCGM.",
        "dependencies": ["platform_base"],
        "failure_modes": ["Driver/container mismatch", "Network Operator not ready for RDMA", "DCGM exporter down"],
        "doc_keys": ["gpu_operator", "network_operator", "dcgm"],
    },
    {
        "id": "platform_base",
        "name": "Platform Base",
        "summary": "Ubuntu (or supported OS), Kubernetes, containerd as the foundation for cloud-native GPU AI.",
        "dependencies": ["hardware"],
        "failure_modes": ["Unsupported K8s version", "containerd CRI misconfiguration", "Kernel not compatible with driver"],
        "doc_keys": ["platform_overview", "software_stack"],
    },
    {
        "id": "hardware",
        "name": "Underlying Infrastructure",
        "summary": "GPUs, NICs, DPUs, storage, and high-performance networking (InfiniBand/RoCE).",
        "dependencies": [],
        "failure_modes": ["Insufficient GPU memory", "No RDMA path for GPUDirect", "Storage bottleneck for model artifacts"],
        "doc_keys": ["ra_index"],
    },
]


@dataclass
class Module:
    id: int
    slug: str
    title: str
    domain: str
    difficulty: str
    minutes: int
    concept: str
    diagram_text: str
    why_it_matters: str
    key_terms: list[str]
    doc_keys: list[str]
    hands_on: str
    interview_questions: list[str]
    lesson_ids: list[int] = field(default_factory=list)


@dataclass
class QuizQuestion:
    id: str
    module_id: int
    domain: str
    qtype: str  # mcq, multi, scenario
    prompt: str
    choices: list[str]
    correct: list[int]
    explanation: str


@dataclass
class DesignDrill:
    id: str
    title: str
    difficulty: str
    requirements: list[str]
    clarifying_questions: list[str]
    architecture_outline: str
    components: list[str]
    tradeoffs: list[str]
    failure_modes: list[str]
    rubric: list[str]
    sample_answer: str


@dataclass
class LearningPlanInput:
    role: str
    level: str
    goal: str
    weeks: int
    hours_per_week: int
    focus_areas: list[str]
    existing_skills: list[str]
    constraints: str


@dataclass
class GeneratedPlan:
    profile: str
    input: LearningPlanInput
    weeks: list[dict[str, Any]]
    markdown: str
