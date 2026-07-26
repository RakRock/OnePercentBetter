"""Full student-facing lesson notes with inline diagram markers."""

from __future__ import annotations

OVERVIEW_NOTES = """
## Course overview — NVIDIA AI Enterprise Reference Architecture

[KEY]
The RA is a **validated stack** from hardware through Kubernetes, NVIDIA operators, model deployment, and AI applications. Each layer has clear **ownership**, **dependencies**, and **failure modes**. Learn the stack **bottom-up** (Lesson 1 → 7) the way platform teams build it.
[/KEY]

### What this course covers

You will learn the **seven layers** of the NVIDIA AI Enterprise Reference Architecture the way a college systems course teaches operating systems or networking: concept first, diagram second, example third, practice last.

| Lesson | Layer | You will understand |
|--------|-------|---------------------|
| **L1** | Hardware | GPUs, NICs, storage, RDMA fabrics |
| **L2** | Platform base | Linux, Kubernetes, containerd |
| **L3** | NVIDIA infra SW | GPU Operator, Network Operator, DCGM |
| **L4** | Kubernetes platform | Quotas, ingress, GPU scheduling |
| **L5** | Model deployment | NIM Operator, KServe, RAG |
| **L6** | Application layer | NIM, NeMo, Triton, frameworks |
| **L7** | Users & teams | RACI, incidents, design reviews |

### The full stack (study this first)

[DIAGRAM:full_stack]

Upper layers **depend on** lower layers. When something breaks, experienced engineers check from the bottom up.

[DIAGRAM:layer_dependencies]

### How to study

1. Read the **Key takeaway** and **Main idea** for each lesson.
2. Study every **diagram** — exam-style questions often ask you to draw or label these.
3. Work through **worked examples** without peeking, then check your reasoning.
4. Complete **practice problems** and **study questions** at the end of each lesson.
5. Use **Context & docs** for official NVIDIA links when writing design documents.
"""

LESSON_NOTES: dict[str, str] = {
    "hardware": """
# Lesson 1: Underlying Infrastructure

[KEY]
Production AI starts with **the right hardware topology**: GPU memory and count, high-bandwidth NICs for multi-node training, and storage that can feed large models. **Software cannot fix** insufficient GPU memory or missing RDMA paths.
[/KEY]

## Learning objectives

- List hardware components validated in the NVIDIA AI Enterprise RA.
- Explain when InfiniBand/RoCE vs standard Ethernet is required.
- Match GPU SKU choice to training, inference, and fine-tuning workloads.
- Identify prerequisites for GPUDirect RDMA and GPUDirect Storage.

## Main idea

The Reference Architecture assumes enterprise servers with NVIDIA GPUs, compatible network adapters, and storage for model artifacts and datasets. This is **Layer 1** — everything above depends on correct hardware. In design reviews, architects map **model size, batch size, and parallelism** to GPU memory, network bandwidth, and storage IOPS **before** discussing Kubernetes or NIM.

### Visual: GPU worker node

Study this diagram until you can redraw it from memory. Label GPU interconnect, NIC path to fabric, and storage paths.

[DIAGRAM:gpu_node_topology]

## 1.1 Why hardware comes first

Students often jump to "install Kubernetes and NIM." The RA teaches **bottom-up capacity planning**:

- A 70B-parameter model may need more VRAM than one GPU provides → you need multi-GPU, tensor parallelism, or a quantized NIM profile.
- That is a **software decision constrained by hardware**.
- Always document GPU SKU, memory, and network on architecture diagrams.

### Visual: Workload → hardware mapping

[DIAGRAM:workload_gpu_selection]

| Workload | Hardware priority |
|----------|-------------------|
| **Training** | High FLOPS, multi-GPU, NVLink within node, RDMA across nodes |
| **Inference** | VRAM fit for NIM profile, memory bandwidth, cost per token |
| **Fine-tuning** | Multi-GPU, fast local NVMe for checkpoints |

## 1.2 Networking for AI clusters

Single-node inference may use standard Ethernet. **Multi-node training**, GPUDirect RDMA, and large east-west traffic require validated NICs and fabrics.

[DIAGRAM:rdma_fabric]

Symptoms of Layer-1 network problems (often misdiagnosed as "Kubernetes issues"):

- Slow NCCL all-reduce
- NCCL timeouts in distributed jobs
- Low GPU utilization despite "busy" training jobs

## 1.3 Storage

- **Local NVMe** — fast NIMCache and pod startup
- **Shared storage** — datasets, multi-node access; must meet throughput targets
- **GPUDirect Storage** — GPU↔storage without CPU copy (when hardware + drivers support it)

## Key vocabulary

| Term | Definition |
|------|------------|
| **GPU / VRAM** | Accelerator and on-device memory; limits model size per GPU |
| **NIC** | Network adapter; ConnectX + RDMA for AI fabrics |
| **InfiniBand / RoCE** | RDMA-capable fabrics for low-latency GPU traffic |
| **DPU** | BlueField SmartNIC offloading network/storage (Lesson 3) |
| **Topology** | Physical layout: GPUs per node, leaf-spine network, storage placement |

## Worked example 1 — Sizing inference hardware

**Scenario:** Team wants an LLM NIM profile requiring **80 GB** GPU memory. Nodes have **L40S (48 GB)** only.

**Solution:**
1. Check NIM profile requirements in NGC.
2. 48 GB < 80 GB → one L40S **cannot** run this profile.
3. Options: smaller/quantized profile, **H100 80GB** nodes, or multi-GPU if profile supports it.

**Answer:** Hardware must match NIM profile **before** any deployment work.

## Worked example 2 — When RDMA matters

**Scenario:** 32-node cluster for distributed fine-tuning on 25 GbE without RDMA.

**Solution:** NCCL collective traffic suffers without RDMA/GPUDirect → use **InfiniBand or RoCE** with ConnectX NICs and Network Operator (Lesson 3).

## Practice

1. **List four hardware attributes** for a new GPU cluster design review.  
   *Answer:* GPU SKU/count, VRAM, NIC/fabric type, storage throughput.

2. **Pod runs but inference is slow** — name two Layer-1 vs two higher-layer causes.  
   *Answer:* L1: VRAM pressure, PCIe/NVLink bottleneck. Higher: wrong NIM profile, CPU preprocessing, ingress latency.

## Common mistakes

- Procuring GPUs without checking **NIM profile compatibility**
- Using general Ethernet for **multi-node training** at scale
- Assuming **more CPU** fixes GPU-bound inference
- Ignoring **storage throughput** for NIMCache cold starts

## Mini summary

- Hardware is the foundation; VRAM, NICs, and storage constrain every upper layer.
- Match GPU SKU to workload type.
- RDMA fabrics matter for multi-node training and GPUDirect.
- Document topology before software design reviews.

## Study questions

1. What is the difference between a capacity problem at Layer 1 vs Layer 4?
2. When would you recommend BlueField DPUs?
3. How does GPU memory affect NIM profile choice?
""",
    "platform_base": """
# Lesson 2: Platform Base

[KEY]
Platform base = **Ubuntu (or supported Linux) + Kubernetes + containerd**. Every NVIDIA operator assumes this trio is correctly installed and version-compatible. Most **"GPU not visible in Kubernetes"** incidents start here — not at NIM.
[/KEY]

## Learning objectives

- Name the three platform base components.
- Explain why containerd is the default CRI (not Docker Engine).
- Trace kubelet → CRI → containerd → running pod.
- Verify OS/K8s versions against the support matrix before GPU Operator.

## Main idea

Before NVIDIA software, you need a **supported Linux host**, a **compatible Kubernetes cluster**, and **containerd** as the CRI. The kubelet creates pod sandboxes via containerd. GPU workloads are regular pods — they request `nvidia.com/gpu` only after Layer 3 is healthy.

### Visual: Platform base stack

[DIAGRAM:platform_base_stack]

## 2.1 The three-legged stool

If any leg fails — wrong kernel, unsupported K8s minor version, broken containerd socket — upper layers fail unpredictably.

**Platform engineer checklist:**
- Pin versions to AI Enterprise lifecycle branch (FB / PB / LTSB)
- Test upgrades in non-production first
- Confirm node `Ready` before GPU Operator

## 2.2 containerd and pod startup

[DIAGRAM:cri_pod_flow]

Modern Kubernetes speaks **CRI**, not Docker directly. Debug with `crictl ps`, containerd logs, and kubelet status **before** GPU Operator.

## 2.3 Kubernetes at this layer

At the base, Kubernetes provides:
- **Node registration** with the control plane
- **Pod scheduling API**
- **CNI hook-in** for pod networking

You are **not** requesting GPUs yet — you are proving a simple pod runs on every worker.

## Key vocabulary

| Term | Definition |
|------|------------|
| **containerd** | CRI runtime: images, containers, pod sandboxes |
| **CRI** | Kubelet interface to container runtimes |
| **kubelet** | Node agent running pods |
| **control plane** | API server, scheduler, etcd |
| **Support matrix** | Validated OS + K8s + AI Enterprise combinations |

## Worked example — Pre-GPU Operator checklist

1. `kubectl get nodes` → all **Ready**
2. Deploy test pod **without GPU** → DNS, CNI, image pull OK
3. containerd socket active, no pull errors
4. OS/K8s versions match support matrix
5. **Then** install or verify GPU Operator

## Practice

1. **Why containerd over Docker?**  
   *Answer:* Native CRI; dockershim removed from Kubernetes.

2. **Three checks on a new worker before GPU labeling?**  
   *Answer:* Node Ready; test pod schedules; containerd healthy; versions match matrix.

## Common mistakes

- GPU Operator on nodes with **unhealthy kubelet/containerd**
- Skipping **version matrix** validation
- Mixing host driver and driver-container strategies without documentation

## Mini summary

- Platform base = OS + Kubernetes + containerd.
- Fix CRI and node Ready before GPU enablement.
- Platform team owns this layer.

## Study questions

1. What is the CRI and who implements it?
2. What symptoms suggest containerd vs GPU driver problems?
""",
    "infra_sw": """
# Lesson 3: NVIDIA Infrastructure Software

[KEY]
**GPU Operator** automates the GPU stack on Kubernetes nodes. **Network Operator** prepares RDMA networking. **DCGM exporter** surfaces GPU telemetry. Together they expose **`nvidia.com/gpu`** so upper layers can schedule AI workloads.
[/KEY]

## Learning objectives

- Trace GPU enablement from driver to schedulable GPU pod.
- Explain ClusterPolicy and NicClusterPolicy CRDs.
- Describe when Network Operator is required.
- Explain MIG vs whole-GPU sharing.

## Main idea

This layer is where **NVIDIA meets Kubernetes**. Operators reconcile CRDs and deploy DaemonSets on labeled nodes — replacing manual per-node driver installs.

### Visual: GPU enablement path (memorize)

[DIAGRAM:gpu_enablement_path]

**Steps:** Driver → Container Toolkit → device plugin → `nvidia.com/gpu` allocatable → pod with GPU.

## 3.1 GPU Operator

[DIAGRAM:gpu_operator_stack]

**ClusterPolicy** is the single configuration object for:
- Driver (containerized or host)
- NVIDIA Container Toolkit
- Device plugin
- DCGM exporter

Operands run on **GPU-labeled nodes** only.

## 3.2 Network Operator

[DIAGRAM:network_rdma]

Required when you need **RDMA**, SR-IOV, or validated high-performance fabrics — not for simple single-node inference.

## 3.3 MIG and time-slicing

- **MIG** — partition one GPU into isolated instances (production inference density)
- **Time-slicing** — share one GPU across pods (dev/test; less isolation)

## Key vocabulary

| Term | Definition |
|------|------------|
| **ClusterPolicy** | GPU Operator cluster-wide config CRD |
| **Device plugin** | Advertises `nvidia.com/gpu` to kubelet |
| **NicClusterPolicy** | Network Operator NIC config CRD |
| **DCGM exporter** | Prometheus-compatible GPU metrics |
| **MIG** | Multi-Instance GPU partitioning |

## Worked example — Pod Pending (0/n nodes)

1. `kubectl describe node` → is `nvidia.com/gpu` **allocatable**?
2. If zero: check GPU Operator pods (driver, plugin) on that node
3. If full: capacity — add nodes or queue jobs
4. If node unlabeled: ClusterPolicy selector mismatch

## Practice

1. **Draw the five-step GPU enablement path.**  
2. **When is Network Operator required for RAG?**  
   *Answer:* Single-node may not need it; multi-node RDMA/GPUDirect paths do.

## Common mistakes

- Manual driver patches causing **cluster drift**
- Ignoring **DCGM alerts** until users complain
- MIG enabled but pods still request whole `nvidia.com/gpu`

## Mini summary

- GPU Operator = automated GPU stack.
- Network Operator = AI-grade networking.
- Device plugin → scheduler sees GPUs.
- DCGM = infrastructure observability.

## Study questions

1. What CRD configures GPU Operator?
2. What breaks GPUDirect RDMA if Network Operator is wrong?
""",
    "k8s_platform": """
# Lesson 4: Kubernetes Platform Layer

[KEY]
Kubernetes turns GPU nodes into a **governed multi-tenant platform**: namespaces, **ResourceQuotas**, ingress, autoscaling, and scheduling. Platform teams translate raw GPU capacity into **services teams can safely consume**.
[/KEY]

## Learning objectives

- Explain GPU ResourceQuotas and namespace isolation.
- Describe taints/tolerations for GPU nodes.
- Map ingress path to NIM endpoints.
- Understand HPA for inference scaling.

## Main idea

GPU nodes are expensive. Platform engineers **taint** GPU nodes, set **quotas** per team, expose APIs via **Ingress**, and scale with **HPA/KEDA**. This is standard Kubernetes applied to scarce accelerators.

### Visual: Multi-tenant GPU platform

[DIAGRAM:multi_tenant_gpu]

## 4.1 Scheduling GPU pods

[DIAGRAM:gpu_scheduling]

Scheduler matches `resources.limits.nvidia.com/gpu` to nodes with free allocatable GPUs and correct tolerations.

## 4.2 Ingress to inference

[DIAGRAM:ingress_path]

Platform team typically owns TLS, WAF, rate limits, and DNS — not the ML model itself.

## Key vocabulary

| Term | Definition |
|------|------------|
| **ResourceQuota** | Caps GPUs (and other resources) per namespace |
| **Taint / toleration** | Keeps non-GPU workloads off GPU nodes |
| **Ingress** | External HTTP(S) routing to services |
| **HPA** | Scales replicas on metrics |

## Worked example — Quota exhaustion

Team applies NIMService needing 4 GPUs; namespace quota allows 2 → **Pending** or admission rejection. Fix: governance process (raise quota, optimize replicas) — not a NIM bug.

## Practice

1. **Design namespace strategy** for dev/staging/prod NIM.  
2. **Why taint GPU nodes?**  
   *Answer:* Preserve expensive GPU node capacity for workloads that request GPUs.

## Common mistakes

- No ResourceQuota — one team consumes entire cluster
- Public NIM ingress **without TLS or auth**
- All replicas in same failure domain

## Mini summary

- Layer 4 = governance + scheduling + exposure.
- Quotas and taints protect GPU capacity.
- Platform/SRE owns this layer.

## Study questions

1. What happens when GPU quota is full?
2. Who configures ingress for NIM?
""",
    "model_deploy": """
# Lesson 5: Model Deployment Layer

[KEY]
The deployment layer turns **model artifacts into running APIs**. **NIMCache → NIMService** is the core NIM pattern; **KServe** adds canary rollouts; **RAG** composes multiple services into one application pattern.
[/KEY]

## Learning objectives

- Explain NIMCache before NIMService ordering.
- List NIM Operator CRDs and their roles.
- Draw an enterprise RAG deployment diagram.
- Compare KServe canary vs direct NIMService rollout.

## Main idea

Teams declare desired state with **CRDs**. NIM Operator reconciles caches, deployments, and services. MLOps engineers live primarily at this layer.

### Visual: NIM deployment lifecycle

[DIAGRAM:nim_deploy_flow]

**Order matters:** NIMCache Ready → NIMService → test API endpoint.

## 5.1 Enterprise RAG pattern

[DIAGRAM:rag_stack]

RAG = **embedding NIM + vector DB + (optional reranker) + LLM NIM**, plus ingress and observability.

## 5.2 KServe canary deployments

[DIAGRAM:kserve_canary]

Shift traffic gradually (e.g., 90/10) to reduce model rollout risk.

## Key vocabulary

| Term | Definition |
|------|------------|
| **NIMCache** | Pre-pulls model artifacts to cluster storage |
| **NIMService** | Declares desired NIM inference deployment |
| **NIMPipeline** | Chains multiple NIM steps |
| **InferenceService** | KServe CRD for predictors and routing |

## Worked example — NIMService pending on cache

1. Check `nimcache` status — Ready?
2. PVC bound? NGC secret valid? Registry reachable?
3. Fix cache first; NIMService reconciles automatically.

## Practice

1. **Order:** NIMCache, NIMService, quota check, API test.  
2. **Name three RAG components at Layer 5.**  
   *Answer:* Embedding NIM, vector DB, LLM NIM.

## Common mistakes

- Skipping NIMCache → slow cold starts
- NGC credentials in ConfigMap instead of **Secret**
- No readiness probes before sending traffic

## Mini summary

- Deployment layer = CRD-driven inference lifecycle.
- Cache before service; KServe for advanced rollouts.
- MLOps owns much of this layer.

## Study questions

1. Which CRD if NIM pods won't start?
2. Why is NIMCache critical in air-gapped sites?
""",
    "app_layer": """
# Lesson 6: AI Application Layer

[KEY]
The application layer is what **teams actually run**: **NIM** microservices, **NeMo** lifecycle tools, **Triton** for custom models, and **PyTorch/TensorFlow** training. Apps consume the platform — they do **not** install GPU drivers.
[/KEY]

## Learning objectives

- Choose NIM vs Triton vs framework jobs for a given use case.
- Map the NeMo Curator → Customizer → Evaluator → Guardrails pipeline.
- Explain NIM profiles and GPU SKU coupling.
- Place Guardrails in the inference path.

## Main idea

NIM standardizes supported models with enterprise APIs. Triton handles custom graphs. NeMo covers the **LLM lifecycle**. All share the same Kubernetes + GPU platform underneath.

### Visual: Application layer options

[DIAGRAM:application_stack]

## 6.1 NeMo LLM lifecycle

[DIAGRAM:nemo_pipeline]

Raw data → curated dataset → fine-tuned model → evaluated quality → governed deployment.

## 6.2 NeMo Guardrails

[DIAGRAM:guardrails]

Guardrails filter **input and output** without retraining the base model — critical for enterprise chatbots.

## Key vocabulary

| Term | Definition |
|------|------------|
| **NIM profile** | Build variant for model size, precision, GPU SKU |
| **Triton** | Multi-model inference server with custom backends |
| **NeMo Curator** | Data preparation for LLM training |
| **Guardrails** | Policy enforcement on LLM I/O |

## Worked example — NIM vs Triton

Proprietary vision model with custom preprocessing → **no NGC NIM** → package in **Triton** with Python backend → deploy via KServe or Deployment.

## Practice

1. **Which layer:** GPU Operator vs NIM LLM vs NeMo Customizer?  
   *Answer:* App layer = NIM and NeMo Customizer only.

2. **What is a NIM profile?**  
   *Answer:* Pre-built container variant matched to model and GPU hardware.

## Common mistakes

- ML team patching **GPU drivers** (wrong layer)
- **CUDA mismatch** after cluster upgrade
- No Guardrails until after a production incident

## Mini summary

- NIM when available; Triton for custom; NeMo for LLM lifecycle.
- Application layer = ML engineer primary domain.
- Version compatibility (CUDA, framework, branch) matters here.

## Study questions

1. NIM vs Triton tradeoffs?
2. Where do Guardrails sit vs NIM?
""",
    "users": """
# Lesson 7: Users and Teams

[KEY]
The top layer is **people and process**: RACI across RA layers, **layer-aware incident response**, design reviews, and **cost governance**. Architecture succeeds when everyone knows **who owns what**.
[/KEY]

## Learning objectives

- Map enterprise roles to RA layers L1–L7.
- Run layer-aware incident triage.
- Conduct an RA design review.
- Onboard a new team across all layers.

## Main idea

The RA is a **communication tool**. Platform owns Layers 1–4; MLOps owns much of Layer 5; ML engineers work in Layer 6; leadership governs Layer 7.

### Visual: Ownership by layer

[DIAGRAM:raci_layers]

## 7.1 Incident triage

[DIAGRAM:incident_flow]

**Example:** Latency spike at 2 AM → SRE checks ingress/pods (L4–5) → DCGM GPU metrics (L3) → recent NIM change (L5–6) → network fabric if timeouts (L1–3).

## 7.2 Onboarding a new team

[DIAGRAM:onboarding_flow]

Every onboarding crosses **all layers** — not just "here is a kubectl command."

## Key vocabulary

| Term | Definition |
|------|------------|
| **RACI** | Responsible, Accountable, Consulted, Informed |
| **Design review** | Architecture walkthrough before production |
| **Runbook** | Layer-tagged incident procedures |
| **Chargeback** | Allocating GPU cost to consuming teams |

## Worked example — Driver crash on half the nodes

**Who is on-call?** Platform engineering / SRE (Layer 3 GPU Operator) — **not** ML engineers.

## Practice

1. **Five design review agenda items.**  
   *Answer:* Workload/SLOs; layer diagram; hardware sizing; quota plan; security/ingress; upgrade path.

2. **Explain RA vs 'K8s on GPU nodes' in two minutes.**  
   *Answer:* RA is validated end-to-end stack with operators, deployment patterns, lifecycle policy, and clear layer ownership — not just Kubernetes with drivers.

## Common mistakes

- Unclear ownership → slow incidents
- No cost guardrails in dev clusters
- "Small pilots" skip review and become production

## Mini summary

- RA requires role clarity across layers.
- Runbooks reference layer numbers.
- Design reviews use the stack as a checklist.
- Governance lives at Layer 7.

## Study questions

1. Platform engineer vs ML engineer ownership?
2. How would you explain the RA to an executive?
""",
}


def get_lesson_notes(layer_id: str) -> str:
    return LESSON_NOTES.get(layer_id, "")
