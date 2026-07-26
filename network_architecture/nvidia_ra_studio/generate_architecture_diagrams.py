"""
Generate matplotlib diagrams for NVIDIA RA Architecture course lesson notes.

Usage:
    python generate_architecture_diagrams.py
    python generate_architecture_diagrams.py --force
"""

from __future__ import annotations

import argparse
import os
import sys

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, ROOT)

from core.architecture_diagrams import IMAGES_DIR, LESSON_DIAGRAMS, OVERVIEW_DIAGRAMS  # noqa: E402

DPI = 150
BG = "#ffffff"
NV_GREEN = "#76b900"
DARK = "#0f172a"
BLUE = "#1e3a5f"
TEAL = "#0d9488"
ORANGE = "#f97316"
PURPLE = "#8b5cf6"
RED = "#ef4444"
GRID = "#e5e7eb"
TEXT = "#1f2937"
MUTED = "#6b7280"

LAYER_COLORS = [
    "#fef3c7",
    "#dbeafe",
    "#d1fae5",
    "#ede9fe",
    "#fce7f3",
    "#e0e7ff",
    "#ecfccb",
]


def _save(fig, name: str) -> None:
    os.makedirs(IMAGES_DIR, exist_ok=True)
    path = os.path.join(IMAGES_DIR, name)
    fig.savefig(path, dpi=DPI, bbox_inches="tight", facecolor=BG, edgecolor="none")
    plt.close(fig)
    print(f"  saved {path}")


def _off(ax):
    ax.set_facecolor(BG)
    ax.axis("off")


def _box(ax, x, y, w, h, label, color, sub="", fs=10, sub_fs=8):
    ax.add_patch(
        FancyBboxPatch(
            (x, y),
            w,
            h,
            boxstyle="round,pad=0.03",
            facecolor=color,
            alpha=0.35,
            edgecolor=color,
            lw=2,
        )
    )
    ax.text(x + w / 2, y + h / 2 + (0.12 if sub else 0), label, ha="center", va="center", fontsize=fs, fontweight="bold", color=TEXT)
    if sub:
        ax.text(x + w / 2, y + h / 2 - 0.22, sub, ha="center", va="center", fontsize=sub_fs, color=MUTED)


def _arrow(ax, x1, y1, x2, y2, color=MUTED):
    ax.add_patch(FancyArrowPatch((x1, y1), (x2, y2), arrowstyle="->", color=color, lw=1.8, mutation_scale=12))


# ── Overview ─────────────────────────────────────────────────────────────────


def overview_full_stack():
    fig, ax = plt.subplots(figsize=(9, 7))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    layers = [
        ("L7 · Users / Teams", "Data scientists · Platform · App owners", LAYER_COLORS[6]),
        ("L6 · AI Application Layer", "NIM · NeMo · Triton · PyTorch", LAYER_COLORS[5]),
        ("L5 · Model Deployment", "NIM Operator · KServe · RAG pipelines", LAYER_COLORS[4]),
        ("L4 · Kubernetes Platform", "Quotas · Ingress · Scheduling · HPA", LAYER_COLORS[3]),
        ("L3 · NVIDIA Infra Software", "GPU Op · Network Op · DCGM", LAYER_COLORS[2]),
        ("L2 · Platform Base", "Ubuntu · Kubernetes · containerd", LAYER_COLORS[1]),
        ("L1 · Hardware", "GPUs · NICs · Storage · IB/RoCE", LAYER_COLORS[0]),
    ]
    y = 8.8
    for title, sub, color in layers:
        _box(ax, 1.2, y, 7.6, 0.95, title, color, sub=sub, fs=11)
        y -= 1.15
    ax.text(5, 9.55, "NVIDIA AI Enterprise Reference Architecture", ha="center", fontsize=13, fontweight="bold", color=DARK)
    ax.annotate("", xy=(9.2, 1.5), xytext=(9.2, 9.2), arrowprops=dict(arrowstyle="->", color=NV_GREEN, lw=2.5))
    ax.text(9.45, 5.3, "Build\nbottom-up", ha="left", fontsize=9, color=NV_GREEN, fontweight="bold", rotation=90, va="center")
    _save(fig, "overview_full_stack.png")


def overview_layer_dependencies():
    fig, ax = plt.subplots(figsize=(9, 5.5))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ids = ["hardware", "platform_base", "infra_sw", "k8s_platform", "model_deploy", "app_layer", "users"]
    labels = ["L1 Hardware", "L2 Base", "L3 NVIDIA SW", "L4 K8s", "L5 Deploy", "L6 Apps", "L7 Users"]
    xs = [1.0, 2.3, 3.6, 4.9, 6.2, 7.5, 8.8]
    for x, lab in zip(xs, labels):
        _box(ax, x - 0.45, 2.5, 0.9, 1.0, lab.split()[0], NV_GREEN, sub=lab.split()[1] if " " in lab else "", fs=9, sub_fs=7)
    for i in range(len(xs) - 1):
        _arrow(ax, xs[i] + 0.48, 3.0, xs[i + 1] - 0.48, 3.0, color=BLUE)
    ax.text(5, 5.2, "Each upper layer depends on healthy layers below", ha="center", fontsize=12, fontweight="bold", color=DARK)
    ax.text(5, 0.8, "Troubleshoot: verify Layer 1 → 2 → 3 before blaming NIM or apps", ha="center", fontsize=10, color=TEAL)
    _save(fig, "overview_layer_dependencies.png")


# ── Lesson 1 ─────────────────────────────────────────────────────────────────


def lesson_01_gpu_node_topology():
    fig, ax = plt.subplots(figsize=(9, 5))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    for i, x in enumerate([1.5, 3.0, 4.5, 6.0]):
        _box(ax, x, 3.8, 1.2, 0.9, f"GPU {i}", ORANGE, sub="VRAM", fs=10)
    ax.plot([2.1, 6.6], [4.25, 4.25], color=ORANGE, lw=2, linestyle="--")
    ax.text(4.35, 4.55, "NVLink / PCIe", ha="center", fontsize=9, color=MUTED)
    _box(ax, 3.5, 2.3, 3.0, 0.8, "CPU + System RAM", GRID, fs=10)
    _box(ax, 1.0, 1.0, 2.2, 0.8, "Local NVMe", TEAL, sub="fast cache", fs=9)
    _box(ax, 3.8, 1.0, 2.4, 0.8, "NIC (ConnectX)", BLUE, sub="to fabric", fs=9)
    _box(ax, 6.8, 1.0, 2.2, 0.8, "Shared Storage", PURPLE, sub="models/data", fs=9)
    for gx in [2.1, 3.6, 5.1, 6.6]:
        _arrow(ax, gx, 3.8, 5.0, 3.1, color=MUTED)
    _arrow(ax, 5.0, 2.3, 2.1, 1.8)
    _arrow(ax, 5.0, 2.3, 5.0, 1.8)
    _arrow(ax, 5.0, 2.3, 7.9, 1.8)
    fig.suptitle("Lesson 1 · GPU worker node topology", fontsize=13, fontweight="bold", color=DARK)
    _save(fig, "lesson_01_gpu_node_topology.png")


def lesson_01_workload_gpu_selection():
    fig, ax = plt.subplots(figsize=(9, 3.8))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    cols = [
        ("Training", "High FLOPS\nMulti-GPU\nRDMA fabric", ORANGE),
        ("Inference", "VRAM fit\nNIM profile\nCost/token", NV_GREEN),
        ("Fine-tuning", "Multi-GPU\nFast NVMe\nCheckpoint I/O", TEAL),
    ]
    for i, (title, body, color) in enumerate(cols):
        x = 0.8 + i * 3.1
        _box(ax, x, 0.8, 2.6, 2.4, title, color, fs=11)
        ax.text(x + 1.3, 1.55, body, ha="center", va="center", fontsize=9, color=TEXT)
    fig.suptitle("Match GPU hardware to workload type", fontsize=13, fontweight="bold", color=DARK)
    _save(fig, "lesson_01_workload_gpu_selection.png")


def lesson_01_rdma_fabric():
    fig, ax = plt.subplots(figsize=(9, 4.5))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    for i, x in enumerate([1.0, 4.0, 7.0]):
        _box(ax, x, 2.0, 2.0, 1.6, f"Node {i+1}", BLUE, sub="GPUs + NIC", fs=10)
    ax.plot([3.0, 4.0], [2.8, 2.8], color=NV_GREEN, lw=3)
    ax.plot([6.0, 7.0], [2.8, 2.8], color=NV_GREEN, lw=3)
    _box(ax, 3.5, 3.5, 3.0, 0.7, "InfiniBand / RoCE fabric", NV_GREEN, fs=10)
    _arrow(ax, 5.0, 3.5, 5.0, 3.15, color=NV_GREEN)
    ax.text(5.0, 0.8, "NCCL / GPUDirect RDMA for multi-node training", ha="center", fontsize=10, color=TEAL)
    fig.suptitle("Lesson 1 · High-performance AI network fabric", fontsize=13, fontweight="bold", color=DARK)
    _save(fig, "lesson_01_rdma_fabric.png")


# ── Lesson 2 ─────────────────────────────────────────────────────────────────


def lesson_02_platform_base_stack():
    fig, ax = plt.subplots(figsize=(8, 5))
    _off(ax)
    ax.set_xlim(0, 8)
    ax.set_ylim(0, 6)
    stack = [
        ("Worker pods (CPU only at first)", LAYER_COLORS[3]),
        ("kubelet on each node", LAYER_COLORS[2]),
        ("containerd (CRI)", LAYER_COLORS[1]),
        ("Ubuntu / supported Linux", LAYER_COLORS[0]),
    ]
    y = 4.5
    for label, color in stack:
        _box(ax, 1.5, y, 5.0, 0.85, label, color, fs=10)
        y -= 1.05
    _box(ax, 1.5, 0.6, 5.0, 0.85, "Kubernetes control plane (API · scheduler · etcd)", DARK, fs=10)
    _arrow(ax, 4.0, 1.45, 4.0, 2.35, color=BLUE)
    fig.suptitle("Lesson 2 · Platform base stack", fontsize=13, fontweight="bold", color=DARK)
    _save(fig, "lesson_02_platform_base_stack.png")


def lesson_02_cri_pod_flow():
    fig, ax = plt.subplots(figsize=(9, 3.2))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 3.5)
    steps = ["API Server\nschedules pod", "kubelet\non node", "containerd\npulls image", "Pod sandbox\nrunning"]
    for i, label in enumerate(steps):
        x = 0.6 + i * 2.3
        _box(ax, x, 1.0, 1.9, 1.4, label.split("\n")[0], TEAL if i % 2 else BLUE, sub=label.split("\n")[1] if "\n" in label else "", fs=9)
        if i < len(steps) - 1:
            _arrow(ax, x + 1.95, 1.7, x + 2.35, 1.7)
    fig.suptitle("Pod startup before GPU enablement", fontsize=13, fontweight="bold", color=DARK)
    _save(fig, "lesson_02_cri_pod_flow.png")


# ── Lesson 3 ─────────────────────────────────────────────────────────────────


def lesson_03_gpu_enablement_path():
    fig, ax = plt.subplots(figsize=(10, 3.2))
    _off(ax)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 3.5)
    steps = ["Driver", "Container\nToolkit", "Device\nPlugin", "nvidia.com/gpu\nallocatable", "GPU pod\nrunning"]
    colors = [ORANGE, TEAL, BLUE, NV_GREEN, PURPLE]
    for i, (lab, col) in enumerate(zip(steps, colors)):
        x = 0.4 + i * 2.05
        lines = lab.split("\n")
        _box(ax, x, 1.0, 1.75, 1.35, lines[0], col, sub=lines[1] if len(lines) > 1 else "", fs=9)
        if i < len(steps) - 1:
            _arrow(ax, x + 1.78, 1.65, x + 2.02, 1.65, color=NV_GREEN)
    fig.suptitle("Lesson 3 · GPU enablement path (memorize)", fontsize=13, fontweight="bold", color=DARK)
    _save(fig, "lesson_03_gpu_enablement_path.png")


def lesson_03_gpu_operator_stack():
    fig, ax = plt.subplots(figsize=(9, 5))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    _box(ax, 3.0, 4.5, 4.0, 0.9, "ClusterPolicy (CRD)", NV_GREEN, fs=11)
    _box(ax, 3.5, 3.3, 3.0, 0.7, "GPU Operator", DARK, fs=10)
    _arrow(ax, 5.0, 4.5, 5.0, 4.0)
    operands = ["Driver DS", "Toolkit", "Device Plugin", "DCGM Exporter"]
    for i, op in enumerate(operands):
        x = 0.8 + i * 2.2
        _box(ax, x, 1.5, 1.8, 1.0, op, ORANGE, fs=9)
        _arrow(ax, 5.0, 3.3, x + 0.9, 2.5, color=MUTED)
    _box(ax, 2.5, 0.3, 5.0, 0.7, "GPU-labeled worker nodes", GRID, fs=10)
    fig.suptitle("GPU Operator reconciliation", fontsize=13, fontweight="bold", color=DARK)
    _save(fig, "lesson_03_gpu_operator_stack.png")


def lesson_03_network_rdma():
    fig, ax = plt.subplots(figsize=(9, 4))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    _box(ax, 3.2, 3.5, 3.6, 0.8, "NicClusterPolicy", NV_GREEN, fs=10)
    _box(ax, 3.5, 2.4, 3.0, 0.7, "Network Operator", DARK, fs=10)
    _arrow(ax, 5.0, 3.5, 5.0, 3.1)
    for i, (lab, x) in enumerate([("MOFED/OFD", 1.0), ("SR-IOV CNI", 4.0), ("RDMA-ready pod", 7.0)]):
        _box(ax, x, 0.9, 2.2, 1.0, lab, TEAL, fs=9)
        _arrow(ax, 5.0, 2.4, x + 1.1, 1.9, color=MUTED)
    fig.suptitle("Network Operator for AI-grade east-west traffic", fontsize=13, fontweight="bold", color=DARK)
    _save(fig, "lesson_03_network_rdma.png")


# ── Lesson 4 ─────────────────────────────────────────────────────────────────


def lesson_04_multi_tenant_gpu():
    fig, ax = plt.subplots(figsize=(9, 5))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    _box(ax, 0.8, 3.5, 3.5, 1.8, "ns: team-a", BLUE, sub="Quota: 4 GPUs", fs=10)
    _box(ax, 5.7, 3.5, 3.5, 1.8, "ns: team-b", PURPLE, sub="Quota: 8 GPUs", fs=10)
    ax.text(2.55, 3.9, "NIM · Jobs", ha="center", fontsize=9, color=MUTED)
    ax.text(7.45, 3.9, "RAG · NIM", ha="center", fontsize=9, color=MUTED)
    _box(ax, 2.0, 1.0, 6.0, 1.2, "Shared GPU node pool (tainted)", NV_GREEN, sub="Scheduler + nvidia.com/gpu", fs=10)
    _arrow(ax, 2.55, 3.5, 3.5, 2.2)
    _arrow(ax, 7.45, 3.5, 6.5, 2.2)
    fig.suptitle("Lesson 4 · Multi-tenant GPU platform", fontsize=13, fontweight="bold", color=DARK)
    _save(fig, "lesson_04_multi_tenant_gpu.png")


def lesson_04_ingress_path():
    fig, ax = plt.subplots(figsize=(9, 3.5))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    chain = ["External\nclient", "Ingress\n+ TLS", "NIM\nService", "NIM\npod (GPU)"]
    for i, lab in enumerate(chain):
        x = 0.5 + i * 2.3
        _box(ax, x, 1.2, 1.9, 1.5, lab.split("\n")[0], NV_GREEN if i == 3 else BLUE, sub=lab.split("\n")[1] if "\n" in lab else "", fs=9)
        if i < len(chain) - 1:
            _arrow(ax, x + 1.95, 1.95, x + 2.35, 1.95)
    fig.suptitle("Exposing inference APIs securely", fontsize=13, fontweight="bold", color=DARK)
    _save(fig, "lesson_04_ingress_path.png")


def lesson_04_gpu_scheduling():
    fig, ax = plt.subplots(figsize=(9, 4))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    _box(ax, 0.8, 2.5, 2.2, 1.4, "Pending pod\nrequests 1 GPU", ORANGE, fs=9)
    _box(ax, 3.8, 3.2, 2.4, 1.0, "Scheduler", DARK, fs=10)
    _box(ax, 7.0, 2.5, 2.2, 1.4, "GPU node\nallocatable: 2", NV_GREEN, fs=9)
    _arrow(ax, 3.0, 3.2, 3.8, 3.5)
    _arrow(ax, 6.2, 3.5, 7.0, 3.2)
    ax.text(5.0, 1.0, "Taints/tolerations keep non-GPU workloads off GPU nodes", ha="center", fontsize=9, color=TEAL)
    fig.suptitle("GPU scheduling in Kubernetes", fontsize=13, fontweight="bold", color=DARK)
    _save(fig, "lesson_04_gpu_scheduling.png")


# ── Lesson 5 ─────────────────────────────────────────────────────────────────


def lesson_05_nim_deploy_flow():
    fig, ax = plt.subplots(figsize=(9, 3.5))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    steps = ["NGC /\nregistry", "NIMCache\n(PVC)", "NIMService\n(CR)", "Deployment\n+ Service"]
    for i, lab in enumerate(steps):
        x = 0.5 + i * 2.3
        _box(ax, x, 1.2, 1.9, 1.5, lab.split("\n")[0], NV_GREEN if i >= 2 else TEAL, sub=lab.split("\n")[1] if "\n" in lab else "", fs=9)
        if i < len(steps) - 1:
            _arrow(ax, x + 1.95, 1.95, x + 2.35, 1.95, color=NV_GREEN)
    fig.suptitle("Lesson 5 · NIM deployment lifecycle", fontsize=13, fontweight="bold", color=DARK)
    _save(fig, "lesson_05_nim_deploy_flow.png")


def lesson_05_rag_stack():
    fig, ax = plt.subplots(figsize=(9, 5))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    _box(ax, 0.8, 4.0, 2.0, 1.0, "User query", GRID, fs=10)
    _box(ax, 3.2, 4.0, 2.0, 1.0, "Embed NIM", TEAL, fs=10)
    _box(ax, 5.6, 4.0, 2.0, 1.0, "Vector DB", PURPLE, fs=10)
    _box(ax, 3.2, 2.2, 2.0, 1.0, "Rerank NIM", ORANGE, fs=10)
    _box(ax, 5.6, 2.2, 2.0, 1.0, "LLM NIM", NV_GREEN, fs=10)
    _box(ax, 8.0, 3.1, 1.5, 1.0, "Response", BLUE, fs=10)
    _arrow(ax, 2.8, 4.5, 3.2, 4.5)
    _arrow(ax, 5.2, 4.5, 5.6, 4.5)
    _arrow(ax, 6.6, 4.0, 4.2, 3.2)
    _arrow(ax, 5.2, 2.7, 5.6, 2.7)
    _arrow(ax, 7.6, 2.7, 8.0, 3.4)
    fig.suptitle("Enterprise RAG on NVIDIA AI Enterprise", fontsize=13, fontweight="bold", color=DARK)
    _save(fig, "lesson_05_rag_stack.png")


def lesson_05_kserve_canary():
    fig, ax = plt.subplots(figsize=(9, 3.5))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    _box(ax, 0.8, 1.5, 2.0, 1.2, "Traffic", GRID, fs=10)
    _box(ax, 3.5, 2.5, 2.2, 1.0, "Stable v1\n90%", BLUE, fs=10)
    _box(ax, 3.5, 0.8, 2.2, 1.0, "Canary v2\n10%", NV_GREEN, fs=10)
    _box(ax, 6.5, 1.5, 2.5, 1.2, "InferenceService", DARK, fs=10)
    _arrow(ax, 2.8, 2.0, 3.5, 2.2)
    _arrow(ax, 2.8, 1.8, 3.5, 1.3)
    _arrow(ax, 5.7, 2.0, 6.5, 2.0)
    fig.suptitle("KServe canary rollout", fontsize=13, fontweight="bold", color=DARK)
    _save(fig, "lesson_05_kserve_canary.png")


# ── Lesson 6 ─────────────────────────────────────────────────────────────────


def lesson_06_application_stack():
    fig, ax = plt.subplots(figsize=(9, 4.5))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5)
    apps = [("NIM", NV_GREEN), ("Triton", ORANGE), ("NeMo", TEAL), ("PyTorch Job", PURPLE)]
    for i, (name, col) in enumerate(apps):
        _box(ax, 0.6 + i * 2.3, 2.8, 2.0, 1.2, name, col, fs=11)
        _arrow(ax, 1.6 + i * 2.3, 2.8, 5.0, 1.8, color=MUTED)
    _box(ax, 2.5, 0.8, 5.0, 1.0, "Model Deployment Layer (Lesson 5)", DARK, fs=10)
    fig.suptitle("Lesson 6 · Application layer options", fontsize=13, fontweight="bold", color=DARK)
    _save(fig, "lesson_06_application_stack.png")


def lesson_06_nemo_pipeline():
    fig, ax = plt.subplots(figsize=(10, 3.2))
    _off(ax)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 3.5)
    steps = ["Curator", "Customizer", "Evaluator", "Guardrails", "NIM deploy"]
    for i, lab in enumerate(steps):
        x = 0.3 + i * 2.05
        _box(ax, x, 1.0, 1.75, 1.35, lab, TEAL if i < 4 else NV_GREEN, fs=9)
        if i < len(steps) - 1:
            _arrow(ax, x + 1.78, 1.65, x + 2.02, 1.65, color=NV_GREEN)
    fig.suptitle("NeMo enterprise LLM lifecycle", fontsize=13, fontweight="bold", color=DARK)
    _save(fig, "lesson_06_nemo_pipeline.png")


def lesson_06_guardrails():
    fig, ax = plt.subplots(figsize=(9, 3.5))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    _box(ax, 0.8, 1.5, 1.8, 1.2, "User", GRID, fs=10)
    _box(ax, 3.0, 1.5, 2.0, 1.2, "Guardrails\n(input)", TEAL, fs=9)
    _box(ax, 5.4, 1.5, 2.0, 1.2, "LLM NIM", NV_GREEN, fs=10)
    _box(ax, 7.8, 1.5, 2.0, 1.2, "Guardrails\n(output)", TEAL, fs=9)
    for x1, x2 in [(2.6, 3.0), (5.0, 5.4), (7.4, 7.8)]:
        _arrow(ax, x1, 2.1, x2, 2.1)
    fig.suptitle("Policy enforcement with NeMo Guardrails", fontsize=13, fontweight="bold", color=DARK)
    _save(fig, "lesson_06_guardrails.png")


# ── Lesson 7 ─────────────────────────────────────────────────────────────────


def lesson_07_raci_layers():
    fig, ax = plt.subplots(figsize=(9, 5.5))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 7)
    rows = [
        ("L1–2 Hardware & base", "Platform / Infra", ORANGE),
        ("L3 NVIDIA operators", "Platform + SRE", TEAL),
        ("L4 K8s platform", "Platform / SRE", BLUE),
        ("L5 Model deploy", "MLOps", NV_GREEN),
        ("L6 Applications", "ML Engineering", PURPLE),
        ("L7 Governance", "Leadership", DARK),
    ]
    y = 5.8
    for layer, owner, color in rows:
        _box(ax, 0.8, y, 4.5, 0.75, layer, color, fs=9)
        _box(ax, 5.5, y, 3.5, 0.75, owner, GRID, fs=9)
        y -= 0.95
    fig.suptitle("Lesson 7 · Who owns each RA layer", fontsize=13, fontweight="bold", color=DARK)
    _save(fig, "lesson_07_raci_layers.png")


def lesson_07_incident_flow():
    fig, ax = plt.subplots(figsize=(9, 3.5))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    steps = ["Alert /\nticket", "Map to\nRA layer", "Owner\nteam", "Fix +\nrunbook"]
    for i, lab in enumerate(steps):
        x = 0.5 + i * 2.3
        _box(ax, x, 1.2, 1.9, 1.5, lab.split("\n")[0], RED if i == 0 else NV_GREEN, sub=lab.split("\n")[1] if "\n" in lab else "", fs=9)
        if i < len(steps) - 1:
            _arrow(ax, x + 1.95, 1.95, x + 2.35, 1.95)
    fig.suptitle("Layer-aware incident triage", fontsize=13, fontweight="bold", color=DARK)
    _save(fig, "lesson_07_incident_flow.png")


def lesson_07_onboarding_flow():
    fig, ax = plt.subplots(figsize=(9, 4.5))
    _off(ax)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 5.5)
    steps = [
        (1, "Namespace + GPU quota", "L4"),
        (2, "NIM templates / cache", "L5"),
        (3, "Build RAG or app", "L6"),
        (4, "Architecture review", "L7"),
    ]
    y = 4.2
    for num, action, layer in steps:
        ax.add_patch(mpatches.Circle((1.2, y + 0.35), 0.25, facecolor=NV_GREEN, edgecolor=DARK))
        ax.text(1.2, y + 0.35, str(num), ha="center", va="center", fontsize=10, fontweight="bold", color=BG)
        _box(ax, 2.0, y, 5.5, 0.7, action, TEAL, fs=10)
        _box(ax, 7.8, y, 1.5, 0.7, layer, GRID, fs=10)
        y -= 1.1
    fig.suptitle("Onboarding a new team to the RA platform", fontsize=13, fontweight="bold", color=DARK)
    _save(fig, "lesson_07_onboarding_flow.png")


GENERATORS = {
    "overview_full_stack.png": overview_full_stack,
    "overview_layer_dependencies.png": overview_layer_dependencies,
    "lesson_01_gpu_node_topology.png": lesson_01_gpu_node_topology,
    "lesson_01_workload_gpu_selection.png": lesson_01_workload_gpu_selection,
    "lesson_01_rdma_fabric.png": lesson_01_rdma_fabric,
    "lesson_02_platform_base_stack.png": lesson_02_platform_base_stack,
    "lesson_02_cri_pod_flow.png": lesson_02_cri_pod_flow,
    "lesson_03_gpu_enablement_path.png": lesson_03_gpu_enablement_path,
    "lesson_03_gpu_operator_stack.png": lesson_03_gpu_operator_stack,
    "lesson_03_network_rdma.png": lesson_03_network_rdma,
    "lesson_04_multi_tenant_gpu.png": lesson_04_multi_tenant_gpu,
    "lesson_04_ingress_path.png": lesson_04_ingress_path,
    "lesson_04_gpu_scheduling.png": lesson_04_gpu_scheduling,
    "lesson_05_nim_deploy_flow.png": lesson_05_nim_deploy_flow,
    "lesson_05_rag_stack.png": lesson_05_rag_stack,
    "lesson_05_kserve_canary.png": lesson_05_kserve_canary,
    "lesson_06_application_stack.png": lesson_06_application_stack,
    "lesson_06_nemo_pipeline.png": lesson_06_nemo_pipeline,
    "lesson_06_guardrails.png": lesson_06_guardrails,
    "lesson_07_raci_layers.png": lesson_07_raci_layers,
    "lesson_07_incident_flow.png": lesson_07_incident_flow,
    "lesson_07_onboarding_flow.png": lesson_07_onboarding_flow,
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true")
    args = parser.parse_args()
    print(f"Generating architecture diagrams → {IMAGES_DIR}")
    for name, fn in GENERATORS.items():
        path = os.path.join(IMAGES_DIR, name)
        if os.path.isfile(path) and not args.force:
            print(f"  skip {name} (exists)")
            continue
        fn()
    print("Done.")


if __name__ == "__main__":
    main()
