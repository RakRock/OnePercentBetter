"""Diagram catalog for architecture course lesson notes."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

IMAGES_DIR = Path(__file__).resolve().parent.parent / "images" / "architecture"


def images_dir() -> Path:
    return IMAGES_DIR


@dataclass
class DiagramSpec:
    key: str
    file: str
    caption: str


OVERVIEW_DIAGRAMS: list[DiagramSpec] = [
    DiagramSpec(
        "full_stack",
        "overview_full_stack.png",
        "The seven RA layers taught bottom-up (Lesson 1 → 7). Platform teams build from hardware up; application teams consume services at the top.",
    ),
    DiagramSpec(
        "layer_dependencies",
        "overview_layer_dependencies.png",
        "Each layer depends on the layers below it. Failures often propagate upward — diagnose from the bottom.",
    ),
]

LESSON_DIAGRAMS: dict[str, list[DiagramSpec]] = {
    "hardware": [
        DiagramSpec(
            "gpu_node_topology",
            "lesson_01_gpu_node_topology.png",
            "A GPU worker node: GPUs linked via NVLink/PCIe, CPU, high-speed NIC to the fabric, and local + shared storage paths.",
        ),
        DiagramSpec(
            "workload_gpu_selection",
            "lesson_01_workload_gpu_selection.png",
            "Training, inference, and fine-tuning place different demands on GPU memory, FLOPS, and networking.",
        ),
        DiagramSpec(
            "rdma_fabric",
            "lesson_01_rdma_fabric.png",
            "Multi-node AI clusters use RDMA-capable fabrics (InfiniBand or RoCE) for GPU-to-GPU traffic across nodes.",
        ),
    ],
    "platform_base": [
        DiagramSpec(
            "platform_base_stack",
            "lesson_02_platform_base_stack.png",
            "Platform base = supported Linux OS + Kubernetes control plane + containerd CRI on every worker.",
        ),
        DiagramSpec(
            "cri_pod_flow",
            "lesson_02_cri_pod_flow.png",
            "How kubelet uses containerd to pull images and start pod sandboxes before any GPU software is involved.",
        ),
    ],
    "infra_sw": [
        DiagramSpec(
            "gpu_enablement_path",
            "lesson_03_gpu_enablement_path.png",
            "End-to-end GPU enablement: driver → Container Toolkit → device plugin → nvidia.com/gpu allocatable.",
        ),
        DiagramSpec(
            "gpu_operator_stack",
            "lesson_03_gpu_operator_stack.png",
            "GPU Operator reconciles ClusterPolicy and deploys operands (driver, toolkit, plugin, DCGM) on GPU nodes.",
        ),
        DiagramSpec(
            "network_rdma",
            "lesson_03_network_rdma.png",
            "Network Operator prepares NICs and CNIs for high-performance RDMA east-west traffic.",
        ),
    ],
    "k8s_platform": [
        DiagramSpec(
            "multi_tenant_gpu",
            "lesson_04_multi_tenant_gpu.png",
            "Namespaces and ResourceQuotas isolate teams while sharing expensive GPU node pools.",
        ),
        DiagramSpec(
            "ingress_path",
            "lesson_04_ingress_path.png",
            "External clients reach NIM inference through Ingress/TLS; platform team typically owns this path.",
        ),
        DiagramSpec(
            "gpu_scheduling",
            "lesson_04_gpu_scheduling.png",
            "Scheduler matches pods requesting nvidia.com/gpu to tainted, labeled GPU nodes with free capacity.",
        ),
    ],
    "model_deploy": [
        DiagramSpec(
            "nim_deploy_flow",
            "lesson_05_nim_deploy_flow.png",
            "Production NIM pattern: NIMCache pulls artifacts first, then NIMService deploys GPU inference pods.",
        ),
        DiagramSpec(
            "rag_stack",
            "lesson_05_rag_stack.png",
            "Enterprise RAG composes embedding NIM, vector DB, optional reranker, and LLM NIM at the deployment layer.",
        ),
        DiagramSpec(
            "kserve_canary",
            "lesson_05_kserve_canary.png",
            "KServe supports canary rollouts — shift traffic gradually to a new model version.",
        ),
    ],
    "app_layer": [
        DiagramSpec(
            "application_stack",
            "lesson_06_application_stack.png",
            "Application layer choices: NIM, Triton, NeMo microservices, and framework training jobs on the same platform.",
        ),
        DiagramSpec(
            "nemo_pipeline",
            "lesson_06_nemo_pipeline.png",
            "NeMo LLM lifecycle: Curator → Customizer → Evaluator → Guardrails → production NIM deployment.",
        ),
        DiagramSpec(
            "guardrails",
            "lesson_06_guardrails.png",
            "Guardrails sit around LLM inference to enforce safety policies without retraining the base model.",
        ),
    ],
    "users": [
        DiagramSpec(
            "raci_layers",
            "lesson_07_raci_layers.png",
            "Typical ownership: platform (Layers 1–4), MLOps (Layer 5), ML engineers (Layer 6), leadership (governance).",
        ),
        DiagramSpec(
            "incident_flow",
            "lesson_07_incident_flow.png",
            "Layer-aware incident triage: start at symptoms, map to RA layer, escalate to the owning team.",
        ),
        DiagramSpec(
            "onboarding_flow",
            "lesson_07_onboarding_flow.png",
            "Onboarding a new team touches every layer — namespace quota, deployment templates, and architecture review.",
        ),
    ],
}


def diagram_path(layer_id: str | None, key: str) -> Path | None:
    specs: list[DiagramSpec] = OVERVIEW_DIAGRAMS if layer_id is None else LESSON_DIAGRAMS.get(layer_id, [])
    for spec in specs:
        if spec.key == key:
            return IMAGES_DIR / spec.file
    return None


def diagram_caption(layer_id: str | None, key: str) -> str:
    specs: list[DiagramSpec] = OVERVIEW_DIAGRAMS if layer_id is None else LESSON_DIAGRAMS.get(layer_id, [])
    for spec in specs:
        if spec.key == key:
            return spec.caption
    return ""
