"""College-style lecture notes for the NVIDIA AI Enterprise Reference Architecture."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class WorkedExample:
    title: str
    scenario: str
    solution: str
    takeaway: str


@dataclass
class PracticeProblem:
    prompt: str
    hint: str
    answer: str


@dataclass
class ArchitectureLesson:
    layer_id: str
    lesson_number: int
    title: str
    subtitle: str
    key_takeaway: str
    learning_objectives: list[str]
    main_idea: str
    vocabulary: list[tuple[str, str]]
    lecture_sections: list[tuple[str, str]]
    diagram: str
    worked_examples: list[WorkedExample]
    practice: list[PracticeProblem]
    common_mistakes: list[str]
    mini_summary: list[str]
    study_questions: list[str]
    related_modules: list[int] = field(default_factory=list)


COURSE_OVERVIEW = {
    "title": "NVIDIA AI Enterprise Reference Architecture — Architecture Course",
    "subtitle": "A layered, software-first blueprint for production AI on Kubernetes",
    "key_takeaway": (
        "The RA is a **validated stack** from hardware through Kubernetes, NVIDIA operators, "
        "model deployment, and AI applications. Each layer has clear **ownership**, "
        "**dependencies**, and **failure modes**. Platform teams harden the bottom; "
        "application teams consume services at the top."
    ),
    "learning_objectives": [
        "Explain why NVIDIA publishes a Reference Architecture instead of only product docs.",
        "Draw the seven RA layers bottom-up and label dependencies between them.",
        "Identify which team owns each layer in a typical enterprise.",
        "Diagnose common failures by knowing which layer they originate in.",
        "Connect RA layers to NIM, NeMo, GPU Operator, and KServe components.",
    ],
    "how_to_use": (
        "Work through **Lessons 1–7** in order (hardware → users). Each lesson follows the "
        "same structure: key idea, vocabulary, lecture notes, worked examples, practice, "
        "and study questions. Use the **Architecture Map** sidebar to jump to a layer when "
        "reviewing or troubleshooting."
    ),
    "full_stack_diagram": """
┌─────────────────────────────────────────────────────────────┐
│  Lesson 7 · Users / Teams                                   │
│  Data scientists, ML engineers, platform SRE, app owners    │
├─────────────────────────────────────────────────────────────┤
│  Lesson 6 · AI Application Layer                            │
│  NIM · NeMo · Triton · PyTorch · TensorFlow · RAPIDS        │
├─────────────────────────────────────────────────────────────┤
│  Lesson 5 · Model Deployment Layer                          │
│  NIM Operator · KServe · RAG pipelines · fine-tuning jobs   │
├─────────────────────────────────────────────────────────────┤
│  Lesson 4 · Kubernetes Platform Layer                       │
│  Scheduling · Services · Ingress · Quotas · Autoscaling     │
├─────────────────────────────────────────────────────────────┤
│  Lesson 3 · NVIDIA Infrastructure Software                  │
│  GPU Operator · Network Operator · DPU Operator · DCGM      │
├─────────────────────────────────────────────────────────────┤
│  Lesson 2 · Platform Base                                   │
│  Ubuntu · Kubernetes · containerd (CRI)                       │
├─────────────────────────────────────────────────────────────┤
│  Lesson 1 · Underlying Infrastructure                       │
│  GPUs · NICs · DPUs · Storage · InfiniBand / RoCE           │
└─────────────────────────────────────────────────────────────┘
""",
}


LESSONS: list[ArchitectureLesson] = [
    ArchitectureLesson(
        layer_id="hardware",
        lesson_number=1,
        title="Lesson 1: Underlying Infrastructure",
        subtitle="GPUs, networking, storage, and the physical foundation of AI",
        key_takeaway=(
            "Production AI starts with **the right hardware topology**: GPU memory and count, "
            "high-bandwidth NICs for multi-node training, and storage that can feed large "
            "models without choking the data path. Software cannot fix insufficient GPU "
            "memory or missing RDMA paths."
        ),
        learning_objectives=[
            "List the hardware components validated in the NVIDIA AI Enterprise RA.",
            "Explain when InfiniBand/RoCE vs standard Ethernet is required.",
            "Describe how GPU SKU choice affects inference vs training workloads.",
            "Identify hardware prerequisites for GPUDirect RDMA and GPUDirect Storage.",
        ],
        main_idea=(
            "The Reference Architecture assumes enterprise-grade servers with NVIDIA GPUs, "
            "compatible network adapters, and shared or local storage suitable for model "
            "artifacts and datasets. This is the **lowest layer** — everything above depends "
            "on correct hardware selection and cabling. In design reviews, architects map "
            "workload requirements (model size, batch size, parallelism) to GPU memory, "
            "interconnect bandwidth, and storage IOPS **before** discussing Kubernetes or NIM."
        ),
        vocabulary=[
            ("GPU (Graphics Processing Unit)", "Accelerators (e.g., H100, L40S, A100) that run CUDA workloads; primary compute for AI."),
            ("GPU memory (VRAM)", "On-device memory limiting model size per GPU; critical for LLM inference and training."),
            ("NIC (Network Interface Card)", "Connects nodes; high-performance AI uses ConnectX adapters with RDMA support."),
            ("InfiniBand / RoCE", "Low-latency RDMA-capable fabrics; required for large-scale distributed training and GPUDirect RDMA."),
            ("DPU (Data Processing Unit)", "BlueField SmartNIC that offloads networking/storage (see Lesson 3)."),
            ("Shared storage", "NFS, parallel filesystems, or object storage holding datasets and model weights."),
            ("Topology", "Physical layout: GPU count per node, leaf-spine network, storage proximity to compute."),
        ],
        lecture_sections=[
            (
                "1.1 Why hardware comes first",
                "Students often jump to 'install Kubernetes and NIM.' The RA teaches **capacity "
                "planning bottom-up**: if a 70B-parameter model needs more VRAM than one GPU "
                "provides, you need multi-GPU, tensor parallelism, or a smaller quantized profile — "
                "a software decision **constrained** by hardware. Document GPU SKU, memory, and "
                "network in every architecture diagram.",
            ),
            (
                "1.2 GPU selection for workloads",
                "**Training** favors high-FLOPS GPUs with NVLink/NVSwitch within nodes and RDMA "
                "across nodes. **Inference** favors memory bandwidth and cost-per-token; NIM "
                "profiles map to specific GPU SKUs. **Fine-tuning** sits between — often "
                "multi-GPU nodes with fast local NVMe for checkpoint I/O.",
            ),
            (
                "1.3 Networking for AI clusters",
                "Single-node inference may use standard networking. **Multi-node training**, "
                "GPUDirect RDMA, and east-west traffic at scale require validated NICs and "
                "fabrics (InfiniBand or RoCE). Misconfigured or under-provisioned networks "
                "show up as slow all-reduce, NCCL timeouts, and poor GPU utilization — "
                "symptoms often blamed on 'Kubernetes' when the root cause is Layer 1.",
            ),
            (
                "1.4 Storage considerations",
                "Model artifacts (NIM caches, checkpoints), datasets (NeMo Curator), and "
                "vector DBs for RAG all stress storage. **Local NVMe** speeds pod startup; "
                "**shared storage** enables multi-node access but must meet throughput targets. "
                "GPUDirect Storage bypasses CPU for GPU↔storage paths when hardware and drivers support it.",
            ),
        ],
        diagram="""
Node (simplified)
┌──────────────────────────────────────────┐
│  GPU 0   GPU 1   GPU 2   GPU 3           │
│    │       │       │       │             │
│    └───────┴───────┴───────┘             │
│              NVLink / PCIe               │
│  CPU ── NIC (ConnectX) ── To fabric      │
│  Local NVMe          Shared storage path │
└──────────────────────────────────────────┘
""",
        worked_examples=[
            WorkedExample(
                title="Example 1 — Sizing inference hardware",
                scenario=(
                    "A team wants to serve an LLM NIM with a profile requiring 80 GB GPU memory. "
                    "They have L40S (48 GB) nodes only."
                ),
                solution=(
                    "1. Check NIM profile GPU requirements in NGC documentation.\n"
                    "2. 48 GB < 80 GB → single L40S **cannot** run this profile.\n"
                    "3. Options: use a **different NIM profile** (quantized/smaller), "
                    "deploy on **H100 80GB**, or use **multi-GPU** if the profile supports it."
                ),
                takeaway="Always validate NIM/model profiles against **available GPU SKUs** at Layer 1.",
            ),
            WorkedExample(
                title="Example 2 — When RDMA matters",
                scenario=(
                    "Platform team builds a 32-node GPU cluster for distributed fine-tuning. "
                    "They use 25 GbE without RDMA."
                ),
                solution=(
                    "1. Distributed training uses NCCL for collective communication.\n"
                    "2. Without RDMA/GPUDirect, GPU↔GPU traffic may traverse CPU and slow training.\n"
                    "3. RA guidance for this scale: **InfiniBand or RoCE** with ConnectX NICs "
                    "and Network Operator configuration (Lesson 3)."
                ),
                takeaway="Multi-node training at scale is a **hardware + network** requirement, not optional.",
            ),
        ],
        practice=[
            PracticeProblem(
                prompt="List four hardware attributes you would document in a design review for a new GPU cluster.",
                hint="Think compute, memory, network, storage.",
                answer="GPU SKU and count per node; VRAM per GPU; NIC type and fabric (IB/RoCE/Ethernet); storage type and throughput for models/datasets.",
            ),
            PracticeProblem(
                prompt="A pod runs but inference is slow on a single GPU. Name two Layer-1 causes vs two higher-layer causes.",
                hint="Separate hardware from software stack issues.",
                answer="Layer 1: insufficient VRAM causing swapping/thrashing; PCIe/NVLink bottleneck. Higher layers: wrong NIM profile; CPU-bound preprocessing; network ingress latency.",
            ),
        ],
        common_mistakes=[
            "Procuring GPUs without checking **NIM profile compatibility** for intended models.",
            "Using general-purpose networking for **multi-node training** and expecting RA-level performance.",
            "Assuming **more CPU** fixes GPU-bound inference latency.",
            "Ignoring **storage throughput** for large model cache pulls (NIMCache cold start).",
        ],
        mini_summary=[
            "Hardware is the foundation; VRAM, NICs, and storage constrain every upper layer.",
            "Match GPU SKU to workload (training vs inference vs fine-tuning).",
            "RDMA-capable fabrics matter for multi-node and GPUDirect paths.",
            "Document topology before software design reviews.",
        ],
        study_questions=[
            "What is the difference between a capacity problem at Layer 1 vs Layer 4 (Kubernetes)?",
            "When would you recommend BlueField DPUs in addition to GPUs?",
            "How does GPU memory affect your choice of NIM profile?",
        ],
        related_modules=[1, 2, 7, 8],
    ),
    ArchitectureLesson(
        layer_id="platform_base",
        lesson_number=2,
        title="Lesson 2: Platform Base",
        subtitle="Operating system, Kubernetes, and container runtime",
        key_takeaway=(
            "The platform base is **Ubuntu (or supported enterprise Linux) + Kubernetes + containerd**. "
            "Every NVIDIA operator assumes this trio is correctly installed and version-compatible. "
            "Most 'GPU not visible in Kubernetes' incidents trace to problems here — not to NIM."
        ),
        learning_objectives=[
            "State the three components of the RA platform base.",
            "Explain why containerd replaced Docker as the default CRI.",
            "Describe the kubelet → CRI → containerd → pod sandbox path.",
            "Verify supported Kubernetes and OS versions before installing GPU Operator.",
        ],
        main_idea=(
            "Before any NVIDIA software, you need a **supported, hardened Linux host**, a "
            "**Kubernetes cluster** at a RA-compatible version, and **containerd** as the "
            "Container Runtime Interface (CRI). The kubelet on each worker talks to containerd "
            "to create pod sandboxes and pull images. GPU workloads are still regular pods — "
            "they just request `nvidia.com/gpu` extended resources once Layer 3 is configured."
        ),
        vocabulary=[
            ("Platform base", "OS + Kubernetes + container runtime — the non-NVIDIA foundation."),
            ("containerd", "Industry-standard CRI implementation; pulls images and runs containers."),
            ("CRI (Container Runtime Interface)", "Kubelet API for talking to container runtimes."),
            ("kubelet", "Node agent that registers the node and runs pods."),
            ("control plane", "API server, scheduler, etcd — cluster brain."),
            ("worker node", "Runs user pods; where GPU Operator operands execute."),
            ("Supported versions matrix", "NVIDIA-validated combinations of OS, K8s, and AI Enterprise branch."),
        ],
        lecture_sections=[
            (
                "2.1 The three-legged stool",
                "If any leg wobbles — wrong kernel for drivers, unsupported K8s minor version, "
                "broken containerd socket — upper layers fail unpredictably. Platform engineers "
                "**pin versions** to the lifecycle branch (FB/PB/LTSB) and test upgrades in "
                "non-production first.",
            ),
            (
                "2.2 containerd and the CRI",
                "Modern Kubernetes uses CRI, not Docker directly. containerd manages image pulls, "
                "snapshots, and container lifecycle. When debugging: `crictl ps`, containerd logs, "
                "and kubelet status are first checks before GPU Operator.",
            ),
            (
                "2.3 Kubernetes responsibilities at this layer",
                "At the base, K8s provides **node registration**, **pod scheduling API**, and "
                "**network plugin hook-in** (CNI). You are not yet requesting GPUs — you are "
                "ensuring nodes are Ready and can run a simple `pause` pod.",
            ),
            (
                "2.4 Hardening checklist",
                "NTP/time sync, disk layout for `/var/lib/containerd`, swap disabled (typical for "
                "K8s), kernel headers if using host drivers, and **taints/labels** plan for "
                "GPU vs non-GPU nodes.",
            ),
        ],
        diagram="""
Worker node boot flow
  Ubuntu host
       │
  kubelet ──CRI──► containerd ──► pull image ──► run pod sandbox
       │
  register with API server → Node condition: Ready
""",
        worked_examples=[
            WorkedExample(
                title="Example 1 — Pre-GPU Operator checklist",
                scenario="New GPU worker nodes join the cluster but no GPU workloads yet.",
                solution=(
                    "1. Confirm node `Ready`: `kubectl get nodes`.\n"
                    "2. Run a test pod without GPU: verify DNS, CNI, image pull.\n"
                    "3. Check containerd: socket active, no pull errors.\n"
                    "4. Compare OS/K8s versions to NVIDIA AI Enterprise support matrix.\n"
                    "5. **Only then** install or verify GPU Operator."
                ),
                takeaway="**Platform base health** is a gate before NVIDIA infrastructure software.",
            ),
            WorkedExample(
                title="Example 2 — Unsupported Kubernetes version",
                scenario="Cluster runs Kubernetes 1.29; new GPU Operator release supports up to 1.28 on current branch.",
                solution=(
                    "1. Check lifecycle/support matrix for your AI Enterprise branch.\n"
                    "2. Upgrade Kubernetes **or** select operator version validated for 1.29.\n"
                    "3. Do not force-install — subtle CRI/API breaks cause production incidents."
                ),
                takeaway="Version compatibility is a **platform base** concern, not negotiable at install time.",
            ),
        ],
        practice=[
            PracticeProblem(
                prompt="Why does the RA prefer containerd over Docker Engine as the runtime?",
                hint="Think about Kubernetes architecture since 1.24+.",
                answer="Kubernetes uses CRI; containerd implements CRI natively. Docker required an extra shim; dockershim removal makes containerd the standard supported path.",
            ),
            PracticeProblem(
                prompt="Name three checks you run on a new worker node before labeling it for GPU workloads.",
                hint="Node status, runtime, versions.",
                answer="Node Ready; test non-GPU pod schedules; containerd healthy; OS/K8s versions match support matrix; kernel compatible with planned driver strategy.",
            ),
        ],
        common_mistakes=[
            "Installing GPU Operator on nodes where **kubelet or containerd is unhealthy**.",
            "Skipping **version matrix** validation for OS + K8s + operator.",
            "Mixing **host driver** and **driver container** strategies without documentation.",
            "Treating all nodes as GPU nodes instead of **labeling and tainting**.",
        ],
        mini_summary=[
            "Platform base = OS + Kubernetes + containerd.",
            "Fix CRI and node Ready before GPU enablement.",
            "Pin versions to NVIDIA AI Enterprise lifecycle branch.",
            "Platform team owns this layer.",
        ],
        study_questions=[
            "What is the CRI and which component implements it on RA nodes?",
            "Who owns platform base vs GPU Operator in a typical enterprise?",
            "What symptoms suggest a containerd problem vs a GPU driver problem?",
        ],
        related_modules=[3, 17],
    ),
    ArchitectureLesson(
        layer_id="infra_sw",
        lesson_number=3,
        title="Lesson 3: NVIDIA Infrastructure Software",
        subtitle="GPU Operator, Network Operator, DPU Operator, and observability",
        key_takeaway=(
            "**GPU Operator** automates the GPU software stack on Kubernetes nodes. "
            "**Network Operator** prepares RDMA-capable networking. **DPU Operator** manages "
            "BlueField DPUs. Together they expose `nvidia.com/gpu`, healthy NICs, and metrics "
            "so upper layers can schedule AI workloads reliably."
        ),
        learning_objectives=[
            "Trace the GPU enablement path from driver to device plugin to allocatable GPU.",
            "Explain ClusterPolicy vs NicClusterPolicy CRDs.",
            "Describe DCGM exporter role in production monitoring.",
            "List when Network Operator is required vs optional.",
        ],
        main_idea=(
            "This layer is where **NVIDIA meets Kubernetes**. Instead of manually SSH-ing to "
            "each node to install drivers and device plugins, operators reconcile custom resources "
            "and deploy DaemonSets (operands) to labeled nodes. GPU Operator manages driver "
            "(containerized or host), NVIDIA Container Toolkit, device plugin, DCGM exporter, "
            "and related components. Network Operator configures MOFED/OFD, SR-IOV, and CNIs "
            "for high-performance fabrics."
        ),
        vocabulary=[
            ("GPU Operator", "Kubernetes operator deploying and managing GPU stack components."),
            ("ClusterPolicy", "GPU Operator CRD defining driver, toolkit, plugin, DCGM settings."),
            ("Device plugin", "Advertises `nvidia.com/gpu` extended resource to kubelet."),
            ("NVIDIA Container Toolkit", "Configures container runtime to inject GPU devices into containers."),
            ("Network Operator", "Manages NIC drivers, SR-IOV, RDMA-related CNIs."),
            ("NicClusterPolicy", "Network Operator CRD for NIC configuration."),
            ("DCGM / DCGM exporter", "GPU telemetry exported to Prometheus-compatible monitoring."),
            ("MIG", "Multi-Instance GPU — partitioning one physical GPU into isolated instances."),
            ("Time-slicing", "Sharing one GPU among multiple pods via scheduler extension."),
        ],
        lecture_sections=[
            (
                "3.1 GPU enablement path (memorize this)",
                "**Driver** → **Container Toolkit** → **device plugin** → **GPU Operator automation** "
                "→ node shows `nvidia.com/gpu` allocatable. Pods request `resources.limits.nvidia.com/gpu: 1`. "
                "Scheduler places pod on node with free GPU. Container runtime hooks GPU into container namespace.",
            ),
            (
                "3.2 GPU Operator deep dive",
                "ClusterPolicy is the **single knob** for cluster-wide GPU software. Operands run on "
                "nodes matching selectors (e.g., `nvidia.com/gpu.present=true`). Upgrades roll "
                "through operand updates — plan maintenance windows. Driver/kernel mismatch is a "
                "top failure mode.",
            ),
            (
                "3.3 Network Operator and RDMA",
                "For GPUDirect RDMA and multi-node training, NICs must be configured consistently. "
                "Network Operator deploys drivers and CNI plugins. Without it, you may have "
                "Kubernetes networking but **not** AI-grade east-west performance.",
            ),
            (
                "3.4 DPU Operator and DOCA",
                "BlueField DPUs offload networking and storage processing. DPU Operator manages "
                "DPU lifecycle in K8s. Relevant for large-scale designs freeing host CPU and "
                "enabling advanced data paths (Lesson 1 hardware must include DPUs).",
            ),
            (
                "3.5 Observability at the infrastructure layer",
                "DCGM exporter surfaces GPU utilization, memory, temperature, and errors. "
                "Platform SREs alert here **before** application teams notice inference degradation.",
            ),
        ],
        diagram="""
GPU Operator reconciliation
  ClusterPolicy (CR)
        │
        ├── driver daemonset (or host driver)
        ├── toolkit on GPU nodes
        ├── device-plugin → kubelet advertises nvidia.com/gpu
        └── dcgm-exporter → metrics

Pod spec: resources.limits.nvidia.com/gpu: 1
        │
        ▼
  Scheduler → GPU node → container with GPU injected
""",
        worked_examples=[
            WorkedExample(
                title="Example 1 — Pod stuck Pending: 0/12 nodes available",
                scenario="ML engineer deploys NIM; pod events say insufficient nvidia.com/gpu.",
                solution=(
                    "1. `kubectl describe node <gpu-node>` — is `nvidia.com/gpu` allocatable?\n"
                    "2. If zero: check GPU Operator pods on node (driver, plugin).\n"
                    "3. If allocatable but full: capacity issue — scale nodes or queue jobs.\n"
                    "4. If node not labeled: ClusterPolicy node selector mismatch."
                ),
                takeaway="**Pending GPU pods** usually mean Layer 3 or Layer 4 — check allocatable resources first.",
            ),
            WorkedExample(
                title="Example 2 — MIG vs whole GPU",
                scenario="Ten small inference models, each needs ~10 GB; node has one H100 80GB.",
                solution=(
                    "1. Whole GPU per pod wastes memory.\n"
                    "2. Configure **MIG profiles** via GPU Operator to partition GPU.\n"
                    "3. Pods request MIG-specific resources (profile-dependent).\n"
                    "4. Alternative: **time-slicing** for dev/test (less isolation)."
                ),
                takeaway="Infrastructure layer configures **GPU sharing strategy**; apps request appropriate resource type.",
            ),
        ],
        practice=[
            PracticeProblem(
                prompt="Draw the GPU enablement path in five steps from bare metal to schedulable pod.",
                hint="Start at driver, end at running container.",
                answer="Install/configure driver → Container Toolkit → device plugin registers nvidia.com/gpu → GPU Operator manages lifecycle → pod requests GPU → scheduler binds → runtime injects GPU.",
            ),
            PracticeProblem(
                prompt="When is Network Operator required for a RAG deployment?",
                hint="Consider single-node vs multi-node and RDMA needs.",
                answer="Single-node RAG on one GPU may not need it. Required when using RDMA/GPUDirect, SR-IOV, or validated high-performance fabrics for multi-node or storage acceleration.",
            ),
        ],
        common_mistakes=[
            "Manually patching drivers on some nodes while GPU Operator manages others — **drift**.",
            "Ignoring **DCGM alerts** until users report slow inference.",
            "Enabling MIG without updating **pod resource requests** to match profiles.",
            "Installing Network Operator without **compatible NIC firmware and cabling** (Layer 1).",
        ],
        mini_summary=[
            "GPU Operator = automated GPU stack on K8s nodes.",
            "Network Operator = RDMA/high-performance networking.",
            "Device plugin exposes nvidia.com/gpu to scheduler.",
            "DCGM exporter = infrastructure-layer observability.",
        ],
        study_questions=[
            "What CRD configures GPU Operator cluster-wide behavior?",
            "How does GPU Operator differ from manually installing a device plugin?",
            "What breaks GPUDirect RDMA if Network Operator is misconfigured?",
        ],
        related_modules=[4, 5, 6, 7, 8, 18],
    ),
    ArchitectureLesson(
        layer_id="k8s_platform",
        lesson_number=4,
        title="Lesson 4: Kubernetes Platform Layer",
        subtitle="Scheduling, networking, tenancy, and cloud-native operations",
        key_takeaway=(
            "Kubernetes turns GPU-enabled nodes into a **multi-tenant AI platform**: namespaces, "
            "quotas, ingress, autoscaling, and scheduling policies. This layer translates "
            "infrastructure capacity into **governed services** application teams can consume."
        ),
        learning_objectives=[
            "Explain how resource quotas govern GPU consumption across teams.",
            "Describe scheduling constraints for GPU workloads (selectors, tolerations, topology).",
            "Map ingress patterns for NIM and KServe endpoints.",
            "Identify platform vs application ownership for K8s objects.",
        ],
        main_idea=(
            "Once nodes expose GPUs, platform engineers design **how teams share the cluster**. "
            "Namespaces isolate dev/staging/prod. ResourceQuota limits `nvidia.com/gpu` per team. "
            "PriorityClasses preempt lower-priority batch jobs. Ingress controllers or service mesh "
            "expose inference APIs. Cluster autoscaler adds GPU nodes when pending pods accumulate. "
            "This is standard Kubernetes — applied to expensive, scarce GPU resources."
        ),
        vocabulary=[
            ("Namespace", "Logical isolation boundary for teams or environments."),
            ("ResourceQuota", "Caps resources (including nvidia.com/gpu) per namespace."),
            ("LimitRange", "Default/min/max resources per pod in namespace."),
            ("Node selector / affinity", "Pin GPU workloads to labeled GPU nodes."),
            ("Taint / toleration", "Prevent non-GPU pods from landing on GPU nodes."),
            ("Ingress", "HTTP routing to services — external access to NIM APIs."),
            ("HPA / KEDA", "Horizontal scaling based on CPU, memory, or custom metrics."),
            ("PriorityClass", "Preemption order when cluster is saturated."),
        ],
        lecture_sections=[
            (
                "4.1 Multi-tenancy on GPU clusters",
                "GPU nodes are costly — platform teams **taint** them (`nvidia.com/gpu=true:NoSchedule`) "
                "so only workloads with tolerations schedule there. Quotas prevent one team from "
                "monopolizing all GPUs. Chargeback/showback often uses namespace labels.",
            ),
            (
                "4.2 Scheduling GPU pods",
                "Scheduler checks `resources.limits.nvidia.com/gpu`, node allocatable, affinity rules, "
                "and topology (spread replicas across racks for HA). **Topology-aware scheduling** "
                "matters for distributed jobs needing locality.",
            ),
            (
                "4.3 Networking and ingress",
                "Pod-to-pod traffic uses CNI. External clients reach NIM via Ingress or LoadBalancer. "
                "TLS termination, WAF, and rate limiting typically sit here — platform or security team owned.",
            ),
            (
                "4.4 Autoscaling",
                "HPA scales NIMService replicas on latency or GPU metrics (via Prometheus adapter). "
                "Cluster autoscaler provisions new GPU nodes when pending pods cannot schedule — "
                "depends on cloud provider or bare-metal provisioning integration.",
            ),
        ],
        diagram="""
Multi-tenant GPU platform
┌──────────── ns: team-a ────────────┐  ┌──────── ns: team-b ────────────┐
│  Quota: 4 GPUs                     │  │  Quota: 8 GPUs                     │
│  NIMService · Training jobs        │  │  RAG pipeline · NIMService         │
└────────────────────────────────────┘  └────────────────────────────────────┘
              │                                    │
              └──────────────┬─────────────────────┘
                             ▼
                    Scheduler + GPU nodes
                             │
                    Ingress → external users
""",
        worked_examples=[
            WorkedExample(
                title="Example 1 — Team exceeds GPU quota",
                scenario="Data science team applies NIMService requesting 4 GPUs; namespace quota allows 2.",
                solution=(
                    "1. API server rejects or pod stays Pending depending on admission.\n"
                    "2. Platform admin reviews ResourceQuota and usage.\n"
                    "3. Options: increase quota, optimize replicas, or queue via job scheduler.\n"
                    "4. Document **governance process** — not a NIM bug."
                ),
                takeaway="Quota exhaustion is a **Layer 4 governance** signal.",
            ),
            WorkedExample(
                title="Example 2 — Ingress to NIM",
                scenario="External app needs HTTPS access to OpenAI-compatible NIM endpoint inside cluster.",
                solution=(
                    "1. NIMService creates ClusterIP Service.\n"
                    "2. Platform exposes via Ingress with TLS cert.\n"
                    "3. Optional: API gateway for auth, rate limits.\n"
                    "4. DNS points to ingress controller load balancer."
                ),
                takeaway="**Exposure and security** of inference APIs are platform-layer decisions.",
            ),
        ],
        practice=[
            PracticeProblem(
                prompt="Design namespace strategy for dev, staging, and prod NIM deployments.",
                hint="Isolation, quotas, and promotion path.",
                answer="Separate namespaces per env; lower GPU quota in dev; network policies restricting prod ingress; promotion via GitOps updating NIMService in staging→prod namespaces.",
            ),
            PracticeProblem(
                prompt="Why taint GPU nodes?",
                hint="Cost and scheduling.",
                answer="GPU nodes are expensive; taints prevent general workloads from consuming GPU node CPU/memory without requesting GPUs, preserving capacity for AI jobs.",
            ),
        ],
        common_mistakes=[
            "No **ResourceQuota** — one team consumes entire cluster.",
            "Running GPU and non-GPU workloads on same nodes without **taints**.",
            "Exposing NIM **without TLS or authentication** on public ingress.",
            "Ignoring **topology** — all replicas on same failure domain.",
        ],
        mini_summary=[
            "K8s platform layer = governance + scheduling + exposure.",
            "Quotas and taints protect scarce GPU capacity.",
            "Ingress and autoscaling define production inference UX.",
            "Platform/SRE team owns this layer.",
        ],
        study_questions=[
            "What happens when a pod requests GPU but namespace quota is full?",
            "How do taints and tolerations protect GPU nodes?",
            "Who configures ingress for NIM — platform or ML team?",
        ],
        related_modules=[2, 16, 18],
    ),
    ArchitectureLesson(
        layer_id="model_deploy",
        lesson_number=5,
        title="Lesson 5: Model Deployment Layer",
        subtitle="NIM Operator, KServe, pipelines, and the path to production inference",
        key_takeaway=(
            "The model deployment layer turns **model artifacts into running APIs** on Kubernetes. "
            "**NIM Operator** (NIMCache, NIMService, NIMPipeline) and **KServe** provide "
            "GitOps-friendly, CRD-driven lifecycle — this is where MLOps meets the RA stack."
        ),
        learning_objectives=[
            "Explain the NIMCache → NIMService deployment flow.",
            "List main NIM Operator CRDs and their roles.",
            "Compare KServe InferenceService vs NIMService patterns.",
            "Describe how RAG pipelines compose multiple deployment objects.",
        ],
        main_idea=(
            "Application teams declare **desired inference state** via CRDs. NIM Operator "
            "reconciles: pull model to cache (NIMCache), deploy NIM containers (NIMService), "
            "chain steps (NIMPipeline), or custom builds (NIMBuild). KServe adds canary "
            "rollouts and scale-to-zero for mixed predictor types. Fine-tuning jobs also "
            "live here — batch Jobs or NeMo workflows scheduled on GPU quotas."
        ),
        vocabulary=[
            ("NIM Operator", "Kubernetes operator managing NIM CRDs and operands."),
            ("NIMCache", "Pre-pulls and stores model artifacts on cluster storage."),
            ("NIMService", "Declares desired NIM inference deployment (replicas, GPU, model)."),
            ("NIMPipeline", "Chains multiple NIM steps into a workflow."),
            ("NIMBuild", "Builds or customizes NIM images on cluster."),
            ("KServe", "Model serving framework with InferenceService CRD."),
            ("InferenceService", "KServe CRD for predictors, transformers, explainers."),
            ("Canary deployment", "Gradual traffic shift to new model version."),
        ],
        lecture_sections=[
            (
                "5.1 NIM deployment lifecycle",
                "1) Create **NIMCache** pointing to NGC model and storage class. "
                "2) Wait for cache Ready. "
                "3) Apply **NIMService** referencing cache. "
                "4) Operator creates Deployment, Service, optional HPA. "
                "5) Validate endpoint — OpenAI-compatible API for many LLM NIMs.",
            ),
            (
                "5.2 Why NIMCache matters",
                "Cold-start without cache pulls multi-GB artifacts at pod start — slow and "
                "fragile. Cache on fast PVC or local storage makes **restarts predictable**. "
                "Air-gapped sites preload caches from private registry mirrors.",
            ),
            (
                "5.3 KServe alongside NIM",
                "KServe abstracts serving for Triton, sklearn, or NIM backends. Use when you need "
                "**standardized InferenceService**, Knative scale-to-zero, or Istio canary splits. "
                "NIM Operator alone suffices for many enterprise NIM-only shops.",
            ),
            (
                "5.4 RAG as a deployment pattern",
                "RAG is not one CRD — it is **embedding NIM + vector DB + optional reranker + LLM NIM**, "
                "wired with services and ingress. NIMPipeline or Helm charts encode the pattern. "
                "Stateful components (vector DB) need persistent volumes and backup strategy.",
            ),
        ],
        diagram="""
NIM deployment flow
  NGC / private registry
         │
         ▼
    NIMCache (PVC) ── Ready?
         │
         ▼
    NIMService CR ──► Deployment (GPU) + Service + Ingress
         │
         ▼
    Clients (OpenAI-compatible API)
""",
        worked_examples=[
            WorkedExample(
                title="Example 1 — NIMService pending on cache",
                scenario="NIMService created but pods not starting; events mention cache not ready.",
                solution=(
                    "1. `kubectl get nimcache` — status and conditions.\n"
                    "2. Check PVC bound, NGC API key secret, network to registry.\n"
                    "3. Fix cache first; NIMService reconciles automatically.\n"
                    "4. Do not debug NIM pods until cache is **Ready**."
                ),
                takeaway="**NIMCache is a hard dependency** for NIMService — order matters.",
            ),
            WorkedExample(
                title="Example 2 — Canary with KServe",
                scenario="Team wants 10% traffic to new model version before full cutover.",
                solution=(
                    "1. Deploy InferenceService with canary trafficPercent.\n"
                    "2. Route 90% stable, 10% canary predictor.\n"
                    "3. Monitor error rate and latency via service mesh metrics.\n"
                    "4. Promote canary to 100% or rollback."
                ),
                takeaway="**Deployment layer** owns safe rollout mechanics; infra layer must provide metrics.",
            ),
        ],
        practice=[
            PracticeProblem(
                prompt="Order these steps for first NIM deployment: NIMService, NIMCache, test API, GPU quota check.",
                hint="Dependencies first.",
                answer="1) GPU quota/namespace ready 2) NIMCache created and Ready 3) NIMService applied 4) test API endpoint.",
            ),
            PracticeProblem(
                prompt="List three components of a RAG stack at the deployment layer.",
                hint="Retrieval + generation.",
                answer="Embedding NIM service; vector database (StatefulSet); LLM NIM service; optional reranker NIM; ingress/gateway tying them together.",
            ),
        ],
        common_mistakes=[
            "Skipping **NIMCache** — long cold starts and registry rate limits.",
            "Wrong **GPU profile** in NIMService for available SKU (ties to Layer 1).",
            "Storing **NGC credentials** in plain ConfigMap instead of Secret.",
            "No **health checks** — routing traffic to starting pods.",
        ],
        mini_summary=[
            "Model deployment = CRD-driven inference lifecycle.",
            "NIMCache before NIMService; KServe for advanced serving patterns.",
            "RAG composes multiple services at this layer.",
            "MLOps / platform-adjacent ML engineers own much of this layer.",
        ],
        study_questions=[
            "Which CRD do you inspect if NIM pods are not starting?",
            "When choose KServe over NIM Operator alone?",
            "Why is NIMCache critical in air-gapped environments?",
        ],
        related_modules=[9, 10, 11, 12, 15, 16],
    ),
    ArchitectureLesson(
        layer_id="app_layer",
        lesson_number=6,
        title="Lesson 6: AI Application Layer",
        subtitle="NIM, NeMo, Triton, and framework workloads",
        key_takeaway=(
            "The application layer is what **users and APIs actually run**: optimized **NIM** "
            "microservices, **NeMo** lifecycle tools, **Triton** for custom graphs, and "
            "frameworks like **PyTorch** and **TensorFlow**. It consumes everything below — "
            "it does not install GPU drivers."
        ),
        learning_objectives=[
            "Differentiate NIM, Triton, and raw framework containers.",
            "Map NeMo Curator → Customizer → Evaluator → Guardrails workflow.",
            "Explain when to stay on Triton vs migrate to NIM.",
            "Identify CUDA/framework version coupling at this layer.",
        ],
        main_idea=(
            "This is the **software students build and operate daily**. NIM packages models as "
            "enterprise inference microservices with consistent APIs. NeMo microservices handle "
            "data curation, fine-tuning, evaluation, and safety guardrails. Triton remains "
            "essential for bespoke multi-model servers and custom backends. Training jobs "
            "use PyTorch/TensorFlow/RAPIDS containers on the same GPU platform. **Version "
            "compatibility** (CUDA, framework, NIM branch) is critical here."
        ),
        vocabulary=[
            ("NIM (NVIDIA Inference Microservice)", "Pre-optimized inference container for specific models."),
            ("NIM profile", "Build variant matching GPU SKU and precision (e.g., FP16, INT8)."),
            ("Triton Inference Server", "Multi-model serving with dynamic batching and custom backends."),
            ("NeMo Curator", "Data cleaning and preparation for LLM training."),
            ("NeMo Customizer", "Fine-tuning microservice."),
            ("NeMo Guardrails", "Safety and policy enforcement for LLM outputs."),
            ("TensorRT", "Inference optimizer; often inside NIM/Triton paths."),
            ("RAPIDS", "GPU-accelerated data science (cuDF, cuML)."),
        ],
        lecture_sections=[
            (
                "6.1 NIM as the default inference path",
                "For supported models, NIM reduces time-to-production: NGC-hosted artifacts, "
                "tested profiles, OpenAI-compatible endpoints. Teams focus on **integration** "
                "(RAG, agents, apps) not building TensorRT pipelines from scratch.",
            ),
            (
                "6.2 Triton and custom models",
                "Custom architectures, legacy models, or multi-model fusion may need **Triton**. "
                "Same Kubernetes and GPU stack — different container and ops playbook. "
                "Hybrid platforms run NIM and Triton side by side in different namespaces.",
            ),
            (
                "6.3 NeMo and the LLM lifecycle",
                "Enterprise LLM programs use NeMo: **Curator** prepares data, **Customizer** "
                "fine-tunes, **Evaluator** measures quality, **Guardrails** enforce policy at "
                "inference. Deployed models may become **custom NIM builds** or NIMBuild outputs.",
            ),
            (
                "6.4 Framework training workloads",
                "Distributed training Jobs use PyTorch/TensorFlow with NCCL across GPU nodes. "
                "Requires healthy Layer 1 network and Layer 3 GPU/Network operators. "
                "Training and inference often share cluster with **separate quotas**.",
            ),
        ],
        diagram="""
Application layer options (same platform underneath)
  ┌─────────┐  ┌─────────┐  ┌──────────────┐  ┌─────────────┐
  │   NIM   │  │ Triton  │  │ NeMo services│  │ PyTorch Job │
  │  (LLM)  │  │ (custom)│  │ (fine-tune)  │  │ (training)  │
  └────┬────┘  └────┬────┘  └──────┬───────┘  └──────┬──────┘
       └────────────┴──────────────┴─────────────────┘
                         │
              Model Deployment Layer (Lesson 5)
""",
        worked_examples=[
            WorkedExample(
                title="Example 1 — NIM vs Triton decision",
                scenario="Team has a proprietary vision model with custom pre/post-processing.",
                solution=(
                    "1. Check NGC for NIM — likely none for proprietary model.\n"
                    "2. Package model in **Triton** with Python backend for preprocessing.\n"
                    "3. Deploy via KServe or raw Deployment on GPU nodes.\n"
                    "4. Revisit NIM if NVIDIA publishes profile or use NIMBuild for customization."
                ),
                takeaway="**NIM when available**; Triton/framework for custom or legacy paths.",
            ),
            WorkedExample(
                title="Example 2 — Guardrails placement",
                scenario="Chatbot must block PII leakage and off-topic responses.",
                solution=(
                    "1. Deploy **NeMo Guardrails** as middleware or sidecar.\n"
                    "2. User query → Guardrails → LLM NIM → Guardrails → response.\n"
                    "3. Policies updated without retraining base model.\n"
                    "4. Logs at Guardrails for compliance audit."
                ),
                takeaway="**Application-layer** policy enforcement complements model weights.",
            ),
        ],
        practice=[
            PracticeProblem(
                prompt="Place these on the application layer: GPU Operator, NIM LLM, NeMo Customizer, device plugin.",
                hint="Only user-facing AI software.",
                answer="Application layer: NIM LLM, NeMo Customizer. NOT application layer: GPU Operator, device plugin (infrastructure).",
            ),
            PracticeProblem(
                prompt="What is a NIM profile and why must it match your GPU?",
                hint="Artifact + hardware binding.",
                answer="A profile is a pre-built NIM variant for model size, precision, and GPU SKU; mismatch causes failed startup, OOM, or unsupported GPU errors.",
            ),
        ],
        common_mistakes=[
            "ML team trying to **patch GPU drivers** — that's infrastructure.",
            "**Framework/CUDA mismatch** after cluster upgrade without retesting images.",
            "Running training jobs in **production inference namespace** without isolation.",
            "Ignoring **Guardrails** until after production incident.",
        ],
        mini_summary=[
            "Application layer = NIM, NeMo, Triton, frameworks.",
            "NIM standardizes inference; Triton for custom; NeMo for LLM lifecycle.",
            "Apps consume platform services — they don't manage operators.",
            "ML engineers and data scientists primary users.",
        ],
        study_questions=[
            "NIM vs self-managed Triton — tradeoffs?",
            "Where do Guardrails sit relative to NIM inference?",
            "What breaks when CUDA version in container doesn't match driver?",
        ],
        related_modules=[9, 13, 14, 15],
    ),
    ArchitectureLesson(
        layer_id="users",
        lesson_number=7,
        title="Lesson 7: Users and Teams",
        subtitle="Roles, ownership, governance, and operating the RA in practice",
        key_takeaway=(
            "The top layer is **people and process**: who owns each RA layer, how teams request "
            "GPU capacity, how design reviews run, and how cost and security guardrails apply. "
            "Architecture fails without **clear RACI** across platform, ML, and application owners."
        ),
        learning_objectives=[
            "Assign typical enterprise roles to each RA layer.",
            "Define RACI for deployment, incident response, and upgrades.",
            "Explain cost guardrails and quota workflows for GPU consumers.",
            "Prepare for a design review using the layered model.",
        ],
        main_idea=(
            "Reference Architecture is a **communication tool** as much as a technical stack. "
            "Platform engineers own Layers 1–4 (with procurement for hardware). MLOps owns "
            "much of Layer 5. ML engineers and data scientists work primarily in Layers 6–7. "
            "Managers use the RA to align **SLAs, budgets, and roadmaps**. Runbooks and "
            "on-call rotations should map incidents to layers."
        ),
        vocabulary=[
            ("RACI", "Responsible, Accountable, Consulted, Informed — ownership matrix."),
            ("Platform engineer", "Owns K8s, operators, ingress, quotas, cluster lifecycle."),
            ("MLOps engineer", "Owns NIM deployment, CI/CD for models, monitoring integration."),
            ("ML engineer / data scientist", "Builds models, RAG apps, fine-tuning experiments."),
            ("SRE", "Reliability, alerting, incident response, capacity planning."),
            ("Design review", "Structured walkthrough of architecture before production."),
            ("Chargeback / showback", "Allocating GPU cost to consuming teams."),
        ],
        lecture_sections=[
            (
                "7.1 Role-to-layer mapping",
                "| Layer | Primary owner | Consumers |\n"
                "|-------|---------------|----------|\n"
                "| Hardware | Infrastructure / procurement | Platform, finance |\n"
                "| Platform base | Platform engineering | All teams |\n"
                "| NVIDIA infra SW | Platform + NVIDIA support | MLOps, SRE |\n"
                "| K8s platform | Platform / SRE | All teams |\n"
                "| Model deploy | MLOps / platform-adjacent ML | App teams |\n"
                "| Application | ML engineers, app developers | End users |\n"
                "| Users/teams | Engineering leadership | Everyone |",
            ),
            (
                "7.2 On-call and escalation",
                "GPU pod Pending → platform checks Layer 3–4 first. NIM 500 errors → MLOps checks "
                "NIMService and cache. Latency SLO breach → joint triage: DCGM metrics (Layer 3), "
                "HPA (Layer 4), model profile (Layer 6). **Escalation paths** should reference layers.",
            ),
            (
                "7.3 Design review template",
                "1) Workload description and SLOs. 2) Layer diagram with components labeled. "
                "3) GPU/network/storage sizing (Layer 1). 4) Namespace and quota plan (Layer 4). "
                "5) NIM/NeMo/Triton choice (Layer 6). 6) Security: secrets, ingress, Guardrails. "
                "7) Upgrade and lifecycle branch strategy.",
            ),
            (
                "7.4 Cost and governance",
                "GPUs are scarce — implement **request/approval** for quota increases, idle GPU "
                "alerts, and autoscaling down in dev. Executives care about **cost per inference** "
                "and **time to deploy model** — both improve with RA discipline.",
            ),
        ],
        diagram="""
RACI (simplified)
  Layer 1-4  ──► Platform Engineering (A) · SRE (R)
  Layer 5    ──► MLOps (R) · Platform (C)
  Layer 6    ──► ML Engineering (R) · MLOps (C)
  Layer 7    ──► Product / leadership (A) · All teams (I)
""",
        worked_examples=[
            WorkedExample(
                title="Example 1 — Incident ownership",
                scenario="At 2 AM, inference latency doubles for customer-facing chatbot.",
                solution=(
                    "1. SRE checks ingress and pod health (Layers 4–5).\n"
                    "2. DCGM: GPU util and memory (Layer 3).\n"
                    "3. MLOps: recent NIMService or model change (Layer 5–6).\n"
                    "4. If network timeouts — escalate to platform for Layer 1–3 fabric check.\n"
                    "5. Post-incident: update runbook with layer that root-caused."
                ),
                takeaway="**Layer-tagged runbooks** reduce finger-pointing and MTTR.",
            ),
            WorkedExample(
                title="Example 2 — New team onboarding",
                scenario="New product team wants GPU access for RAG prototype.",
                solution=(
                    "1. Platform creates namespace + GPU quota (Layer 4).\n"
                    "2. MLOps provides NIMCache/NIMService templates (Layer 5).\n"
                    "3. Team deploys RAG app consuming NIM APIs (Layer 6).\n"
                    "4. Architecture review validates Guardrails and data handling (Layer 7).\n"
                    "5. Chargeback tag applied to namespace."
                ),
                takeaway="Onboarding is a **workflow across layers**, not a single ticket.",
            ),
        ],
        practice=[
            PracticeProblem(
                prompt="Who should be on-call when GPU driver daemonsets crash on half the nodes?",
                hint="Which layer?",
                answer="Platform engineering / SRE owning GPU Operator (Layer 3) — not ML engineers.",
            ),
            PracticeProblem(
                prompt="List five agenda items for an RA design review.",
                hint="Use lesson template.",
                answer="Workload/SLOs; layer diagram; hardware sizing; namespace/quota plan; NIM vs Triton choice; security/secrets/ingress; lifecycle upgrade path.",
            ),
        ],
        common_mistakes=[
            "**Unclear ownership** — everyone assumes someone else fixes operators.",
            "No **cost guardrails** — dev clusters left at full GPU utilization.",
            "Skipping design review for 'small' pilots that become production.",
            "ML teams given **cluster-admin** instead of namespace-scoped RBAC.",
        ],
        mini_summary=[
            "RA success requires role clarity across all layers.",
            "Incidents and runbooks should reference layer numbers.",
            "Design reviews use the stack as a checklist.",
            "Governance (quota, cost, security) lives at the top.",
        ],
        study_questions=[
            "How does RA differ from 'just installing Kubernetes on GPU nodes'?",
            "Which layers would a platform engineer own vs an ML engineer?",
            "How would you explain the RA to a non-technical executive in two minutes?",
        ],
        related_modules=[1, 2, 17, 18],
    ),
]


def get_lesson(layer_id: str) -> ArchitectureLesson | None:
    return next((lesson for lesson in LESSONS if lesson.layer_id == layer_id), None)


def lessons_by_number() -> list[ArchitectureLesson]:
    return sorted(LESSONS, key=lambda lesson: lesson.lesson_number)
