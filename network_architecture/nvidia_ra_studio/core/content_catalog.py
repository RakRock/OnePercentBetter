"""Seeded learning modules for NVIDIA AI Enterprise RA."""

from __future__ import annotations

from .models import Module

MODULES: list[Module] = [
    Module(
        id=1,
        slug="what-is-nvidia-ai-enterprise-ra",
        title="What is NVIDIA AI Enterprise RA?",
        domain="NVIDIA AI Enterprise overview",
        difficulty="beginner",
        minutes=45,
        concept=(
            "The NVIDIA AI Enterprise Reference Architecture (RA) documents a validated, software-first "
            "blueprint for running production AI on Kubernetes — from GPU infrastructure through NIM "
            "inference and NeMo customization."
        ),
        diagram_text=(
            "Users → Application (NIM/NeMo/Triton) → Deployment (NIM Operator/KServe) → "
            "K8s → NVIDIA infra (GPU/Network Operator) → Ubuntu/K8s/containerd → GPUs/NICs/storage"
        ),
        why_it_matters=(
            "Design reviews, procurement, and operations all reference the same layered model. "
            "The RA separates what app teams own vs what platform teams must harden."
        ),
        key_terms=["Reference Architecture", "NVIDIA AI Enterprise", "validated stack", "software-first"],
        doc_keys=["ra_index", "platform_overview"],
        hands_on="Sketch the RA layers on paper and label which team owns each layer in your org.",
        interview_questions=[
            "How does NVIDIA AI Enterprise RA differ from 'just installing Kubernetes on GPU nodes'?",
            "Which layers would a platform engineer own vs an ML engineer?",
        ],
    ),
    Module(
        id=2,
        slug="application-vs-infrastructure-layer",
        title="Application Layer vs Infrastructure Layer",
        domain="Application layer vs infrastructure layer",
        difficulty="beginner",
        minutes=40,
        concept=(
            "The application layer includes frameworks, NIM, NeMo, and user workloads. "
            "The infrastructure layer includes drivers, operators, networking, and the Kubernetes platform base."
        ),
        diagram_text="Split: TOP = workloads/APIs/models | BOTTOM = operators, drivers, K8s, OS, hardware",
        why_it_matters="Upgrade and support boundaries follow this split — app teams should not patch GPU drivers.",
        key_terms=["application layer", "infrastructure layer", "separation of concerns", "SLA boundary"],
        doc_keys=["platform_overview", "software_stack"],
        hands_on="List three components above and below the line for a RAG service.",
        interview_questions=[
            "Where does NIM Operator sit — application or infrastructure?",
            "Who is on-call when a GPU driver fails vs when NIM inference latency spikes?",
        ],
    ),
    Module(
        id=3,
        slug="platform-base",
        title="Platform Base: OS, Kubernetes, container runtime",
        domain="Platform base: Ubuntu, Kubernetes, containerd",
        difficulty="beginner",
        minutes=50,
        concept=(
            "Supported Ubuntu (or enterprise Linux), a compatible Kubernetes version, and containerd "
            "as the CRI form the foundation. All NVIDIA operators assume this base is correctly configured."
        ),
        diagram_text="Ubuntu → containerd (CRI) → kubelet → Kubernetes control plane → worker nodes",
        why_it_matters="Most 'GPU not available' issues trace back to base OS/K8s/CRI misconfiguration.",
        key_terms=["containerd", "CRI", "kubelet", "supported versions"],
        doc_keys=["platform_overview", "software_stack"],
        hands_on="Verify containerd socket and kubelet status on a lab node checklist.",
        interview_questions=[
            "Why containerd instead of Docker as the runtime in modern RA guidance?",
            "What do you check before installing GPU Operator?",
        ],
    ),
    Module(
        id=4,
        slug="gpu-enablement-path",
        title="GPU Enablement Path",
        domain="NVIDIA GPU enablement",
        difficulty="intermediate",
        minutes=55,
        concept=(
            "GPU enablement flows: compatible driver → container toolkit → device plugin → "
            "GPU Operator automation → `nvidia.com/gpu` extended resource on nodes."
        ),
        diagram_text="Driver → NVIDIA Container Toolkit → device plugin → GPU Operator → allocatable GPU in K8s",
        why_it_matters="Pods request `nvidia.com/gpu`; the enablement path must be healthy end-to-end.",
        key_terms=["device plugin", "extended resource", "Container Toolkit", "MIG", "time-slicing"],
        doc_keys=["gpu_operator", "software_stack"],
        hands_on="Describe the path from bare metal GPU to a pod with `resources.limits.nvidia.com/gpu: 1`.",
        interview_questions=[
            "What is the difference between GPU Operator and manually installing a device plugin?",
            "When would you use MIG vs whole GPUs?",
        ],
    ),
    Module(
        id=5,
        slug="gpu-operator-deep-dive",
        title="GPU Operator Deep Dive",
        domain="GPU Operator",
        difficulty="intermediate",
        minutes=60,
        concept=(
            "GPU Operator deploys and manages driver (optional), container toolkit, device plugin, "
            "DCGM exporter, and related components as DaemonSets/operands on GPU nodes."
        ),
        diagram_text="ClusterPolicy CR → operands on GPU-labeled nodes → Node labels + GPU allocatable",
        why_it_matters="Centralized lifecycle for GPU software stack; required for consistent multi-node clusters.",
        key_terms=["ClusterPolicy", "operand", "DaemonSet", "node selector", "driver container"],
        doc_keys=["gpu_operator"],
        hands_on="Review GPU Operator ClusterPolicy fields: driver, toolkit, devicePlugin, dcgmExporter.",
        interview_questions=[
            "How do you roll out GPU Operator across 20 new GPU nodes safely?",
            "What happens if driver version doesn't match host kernel?",
        ],
    ),
    Module(
        id=6,
        slug="network-operator-deep-dive",
        title="Network Operator Deep Dive",
        domain="Network Operator",
        difficulty="intermediate",
        minutes=55,
        concept=(
            "Network Operator configures high-performance networking (InfiniBand, RoCE), "
            "SR-IOV, and related CNIs for AI workloads needing RDMA and low latency."
        ),
        diagram_text="NicClusterPolicy → MOFED / OFED drivers → CNI plugins → RDMA-ready pods",
        why_it_matters="Multi-node training and GPUDirect RDMA depend on correct network operator configuration.",
        key_terms=["Network Operator", "RoCE", "InfiniBand", "SR-IOV", "NicClusterPolicy"],
        doc_keys=["network_operator"],
        hands_on="Map which workloads in your org require RDMA vs standard overlay networking.",
        interview_questions=[
            "When is Network Operator required vs optional?",
            "How does network misconfiguration affect GPUDirect RDMA?",
        ],
    ),
    Module(
        id=7,
        slug="doca-dpu-operator",
        title="DOCA and DPU Operator",
        domain="DOCA, BlueField DPU, GPUDirect RDMA, GPUDirect Storage",
        difficulty="advanced",
        minutes=50,
        concept=(
            "BlueField DPUs offload networking/storage with DOCA SDK. DPU Operator manages DPU "
            "lifecycle in Kubernetes for accelerated east-west traffic and storage paths."
        ),
        diagram_text="Host GPU ←→ DPU ←→ network/storage | DOCA services on DPU",
        why_it_matters="Large-scale AI fabrics use DPUs to free CPU and enable GPUDirect paths.",
        key_terms=["BlueField", "DOCA", "DPU Operator", "offload", "data path"],
        doc_keys=["ra_index", "software_stack"],
        hands_on="Compare a standard GPU node vs DPU-accelerated node for storage ingress.",
        interview_questions=[
            "What problems do DPUs solve in AI clusters?",
            "Where does DPU Operator sit in the RA stack?",
        ],
    ),
    Module(
        id=8,
        slug="gpudirect-rdma-storage",
        title="GPUDirect RDMA and GPUDirect Storage",
        domain="DOCA, BlueField DPU, GPUDirect RDMA, GPUDirect Storage",
        difficulty="advanced",
        minutes=45,
        concept=(
            "GPUDirect RDMA enables direct GPU-to-NIC memory transfers. GPUDirect Storage "
            "accelerates GPU access to storage, reducing CPU copies for I/O heavy inference/training."
        ),
        diagram_text="GPU memory ←direct→ NIC or storage adapter (bypass CPU for data path)",
        why_it_matters="Latency and throughput for distributed training and large model loading.",
        key_terms=["GPUDirect RDMA", "GPUDirect Storage", "NIC compatibility", "CUDA", "peer memory"],
        doc_keys=["software_stack", "network_operator"],
        hands_on="List prerequisites: compatible GPU, driver, NIC, network operator, peer mapping.",
        interview_questions=[
            "When would you invest in GPUDirect vs standard TCP/NFS?",
            "What breaks GPUDirect RDMA in practice?",
        ],
    ),
    Module(
        id=9,
        slug="nim-fundamentals",
        title="NIM Fundamentals",
        domain="NIM and NIM Operator",
        difficulty="intermediate",
        minutes=50,
        concept=(
            "NVIDIA NIM provides optimized inference microservices for LLMs, embeddings, and more — "
            "packaged for enterprise deployment with consistent APIs."
        ),
        diagram_text="Model artifact → NIM container → OpenAI-compatible or custom API → clients",
        why_it_matters="Standardizes inference deployment without every team rebuilding Triton/TensorRT pipelines.",
        key_terms=["NIM", "inference microservice", "model profile", "NGC", "API contract"],
        doc_keys=["nim_operator", "target_workloads"],
        hands_on="Identify which NIM profiles match your GPU SKU and model size.",
        interview_questions=[
            "NIM vs self-managed Triton — tradeoffs?",
            "What is a NIM 'profile'?",
        ],
    ),
    Module(
        id=10,
        slug="nim-operator-crds",
        title="NIM Operator and CRDs",
        domain="NIM Operator",
        difficulty="intermediate",
        minutes=55,
        concept=(
            "NIM Operator manages NIM lifecycle via Kubernetes CRDs — coordinating caches, services, "
            "pipelines, and builds on the cluster."
        ),
        diagram_text="NIM Operator watches CRDs → reconciles Deployments/Services/PVCs for NIM workloads",
        why_it_matters="GitOps-friendly, Kubernetes-native NIM operations at scale.",
        key_terms=["NIM Operator", "CRD", "reconciliation", "operand", "namespace scope"],
        doc_keys=["nim_operator"],
        hands_on="List the main NIM CRDs and what each controls.",
        interview_questions=[
            "Which CRD would you inspect if NIM pods aren't starting?",
            "How does NIM Operator interact with GPU Operator?",
        ],
    ),
    Module(
        id=11,
        slug="nimcache-model-lifecycle",
        title="NIMCache and Model Lifecycle",
        domain="NIMCache, NIMService, NIMPipeline, NIMBuild",
        difficulty="intermediate",
        minutes=50,
        concept=(
            "NIMCache pre-pulls and stores model artifacts on cluster storage so NIMService "
            "startups are fast and repeatable."
        ),
        diagram_text="NGC/registry → NIMCache (PVC/local) → NIMService mounts cache → ready endpoint",
        why_it_matters="Cold-start latency and air-gapped deployments depend on cache strategy.",
        key_terms=["NIMCache", "model artifact", "PVC", "prefetch", "NGC API key"],
        doc_keys=["nim_operator"],
        hands_on="Design cache storage sizing for three LLM models on one cluster.",
        interview_questions=[
            "Why would NIMService fail if NIMCache is unavailable?",
            "How do you refresh models safely?",
        ],
    ),
    Module(
        id=12,
        slug="nimservice-deployment",
        title="NIMService Deployment Lifecycle",
        domain="NIMCache, NIMService, NIMPipeline, NIMBuild",
        difficulty="intermediate",
        minutes=55,
        concept=(
            "NIMService declares desired NIM inference — replicas, resources, ingress, and model reference. "
            "NIMPipeline chains multiple NIM steps; NIMBuild customizes builds."
        ),
        diagram_text="NIMCache ready → NIMService CR → Deployment + Service + HPA → ingress/route",
        why_it_matters="Production inference SLAs are defined at the NIMService layer.",
        key_terms=["NIMService", "NIMPipeline", "NIMBuild", "replicas", "resource limits"],
        doc_keys=["nim_operator", "target_workloads"],
        hands_on="Write a checklist for promoting NIMService from dev namespace to prod.",
        interview_questions=[
            "How do you scale NIMService under load?",
            "What resources must be requested besides GPU?",
        ],
    ),
    Module(
        id=13,
        slug="triton-framework-workloads",
        title="Triton and Framework Workloads",
        domain="Triton, PyTorch, TensorFlow, RAPIDS",
        difficulty="intermediate",
        minutes=50,
        concept=(
            "Not every workload uses NIM — Triton Inference Server, PyTorch, TensorFlow, and RAPIDS "
            "remain first-class for custom training and bespoke inference graphs."
        ),
        diagram_text="Custom models → Triton / framework containers → same K8s + GPU stack underneath",
        why_it_matters="Hybrid platforms serve both standardized NIM and custom model pipelines.",
        key_terms=["Triton", "TensorRT", "PyTorch", "TensorFlow", "RAPIDS", "multi-framework"],
        doc_keys=["software_stack", "target_workloads"],
        hands_on="Place Triton and NIM on the same architecture diagram — shared vs unique components.",
        interview_questions=[
            "When keep Triton instead of migrating to NIM?",
            "How does GPU sharing differ for training vs inference jobs?",
        ],
    ),
    Module(
        id=14,
        slug="nemo-microservices",
        title="NeMo Microservices",
        domain="NeMo: Curator, Customizer, Evaluator, Guardrails",
        difficulty="advanced",
        minutes=60,
        concept=(
            "NeMo microservices cover data curation, fine-tuning (Customizer), evaluation, and "
            "Guardrails for safe LLM deployment — composable on the same platform."
        ),
        diagram_text="Curator → Customizer → Evaluator → Guardrails → NIM deployment",
        why_it_matters="Enterprise LLM lifecycle from raw data to governed production inference.",
        key_terms=["NeMo Curator", "Customizer", "Evaluator", "Guardrails", "fine-tuning"],
        doc_keys=["target_workloads", "software_stack"],
        hands_on="Map one fine-tuning workflow to NeMo components and required GPU pools.",
        interview_questions=[
            "Where do Guardrails sit relative to NIM inference?",
            "How would you isolate fine-tuning jobs from production inference?",
        ],
    ),
    Module(
        id=15,
        slug="rag-on-nvidia-ai-enterprise",
        title="RAG on NVIDIA AI Enterprise",
        domain="RAG architecture on NVIDIA AI Enterprise",
        difficulty="advanced",
        minutes=65,
        concept=(
            "RAG combines embedding NIM, vector DB, optional reranker NIM, and LLM NIM — "
            "orchestrated via pipelines, ingress, and observability on Kubernetes."
        ),
        diagram_text="Query → embed NIM → vector DB → rerank → LLM NIM → response | audit/logs",
        why_it_matters="Most enterprise GenAI apps are RAG — platform must standardize the pattern.",
        key_terms=["RAG", "embedding", "vector database", "reranking", "retrieval latency"],
        doc_keys=["target_workloads", "nim_operator"],
        hands_on="Design a RAG reference diagram with namespaces for dev/staging/prod.",
        interview_questions=[
            "Which components are stateful vs stateless in RAG?",
            "How do you debug retrieval quality vs inference quality?",
        ],
    ),
    Module(
        id=16,
        slug="kserve-model-serving",
        title="KServe and Model-Serving Patterns",
        domain="KServe and model serving",
        difficulty="intermediate",
        minutes=50,
        concept=(
            "KServe provides Kubernetes-native model serving with canary rollouts, "
            "scale-to-zero, and standardized InferenceService CRDs — often alongside NIM."
        ),
        diagram_text="InferenceService → predictor pod (Triton/NIM) → Knative/Istio routing → metrics",
        why_it_matters="Unified serving abstraction for mixed model types and progressive delivery.",
        key_terms=["KServe", "InferenceService", "canary", "scale-to-zero", "predictor"],
        doc_keys=["kserve", "target_workloads"],
        hands_on="Compare KServe InferenceService vs raw NIMService for one use case.",
        interview_questions=[
            "When use KServe vs NIM Operator alone?",
            "How do canary deployments reduce inference risk?",
        ],
    ),
    Module(
        id=17,
        slug="lifecycle-release-branches",
        title="Lifecycle Policy and Release Branches",
        domain="Lifecycle policy: FB, PB, LTSB",
        difficulty="intermediate",
        minutes=45,
        concept=(
            "NVIDIA AI Enterprise uses Feature Branch (FB), Production Branch (PB), and "
            "Long-Term Support Branch (LTSB) with defined support windows and compatibility rules."
        ),
        diagram_text="FB (newest) → PB (stabilized) → LTSB (extended support) | upgrade paths validated",
        why_it_matters="Upgrade planning and security patching depend on branch policy.",
        key_terms=["Feature Branch", "Production Branch", "LTSB", "support matrix", "compatibility"],
        doc_keys=["lifecycle", "ra_index"],
        hands_on="Draft an upgrade plan from current PB to next PB using lifecycle docs.",
        interview_questions=[
            "What is the difference between FB and PB?",
            "Why must GPU Operator versions align with AI Enterprise branch?",
        ],
    ),
    Module(
        id=18,
        slug="production-ops-security",
        title="Production Operations, Monitoring, Security",
        domain="Observability, security, troubleshooting",
        difficulty="advanced",
        minutes=70,
        concept=(
            "Production RA operations include DCGM/GPU metrics, capacity planning, RBAC, "
            "namespaces, secrets, image governance, and runbooks for common failures."
        ),
        diagram_text="DCGM exporter → Prometheus/Grafana → alerts | RBAC + quotas + network policies",
        why_it_matters="Platform engineering value is proven in uptime, security, and cost control.",
        key_terms=["DCGM", "capacity planning", "RBAC", "NetworkPolicy", "image signing", "runbook"],
        doc_keys=["dcgm", "lifecycle", "gpu_operator"],
        hands_on="Build a troubleshooting flowchart: pod pending → GPU → driver → operator → quota.",
        interview_questions=[
            "What metrics do you alert on for GPU clusters?",
            "How do you implement multi-tenancy safely?",
        ],
    ),
]


def get_module(module_id: int) -> Module | None:
    return next((m for m in MODULES if m.id == module_id), None)


def get_module_by_slug(slug: str) -> Module | None:
    return next((m for m in MODULES if m.slug == slug), None)


def all_domains() -> list[str]:
    seen: list[str] = []
    for m in MODULES:
        if m.domain not in seen:
            seen.append(m.domain)
    return seen
