"""System-design drills for NVIDIA AI Enterprise RA."""

from __future__ import annotations

from .models import DesignDrill

DESIGN_DRILLS: list[DesignDrill] = [
    DesignDrill(
        id="nim-multi-team",
        title="NIM inference for three internal teams",
        difficulty="intermediate",
        requirements=[
            "Three teams share one GPU cluster",
            "Each team deploys 2+ NIM models",
            "Dev/staging/prod isolation required",
            "Cost allocation per team",
        ],
        clarifying_questions=[
            "GPU SKU and count per node?",
            "Air-gapped or NGC-connected?",
            "Expected QPS and latency SLOs?",
            "Shared or dedicated ingress?",
        ],
        architecture_outline=(
            "Namespaces per team × env; NIMCache per namespace or shared read-only cache; "
            "NIMService per model; ResourceQuota + LimitRange; GPU Operator cluster-wide; "
            "ingress controller with team routes; DCGM + Prometheus per namespace labels."
        ),
        components=["GPU Operator", "NIM Operator", "NIMCache", "NIMService", "Ingress", "DCGM", "RBAC"],
        tradeoffs=[
            "Shared NIMCache saves disk but complicates RBAC",
            "Dedicated GPU nodes vs shared pool with quotas",
            "MIG for small models vs whole GPUs",
        ],
        failure_modes=[
            "One team exhausts GPU quota blocking others",
            "Cache miss causes multi-minute cold starts",
            "NGC pull secret expired in one namespace",
        ],
        rubric=[
            "Clear tenancy model",
            "NIM CRD usage correct",
            "Quota and RBAC specified",
            "Observability and upgrade path mentioned",
        ],
        sample_answer=(
            "Create namespaces team-a-{dev,stg,prod} etc. Install GPU Operator once cluster-wide. "
            "Per namespace: NIMCache on fast local storage, NIMService with GPU requests matching profiles, "
            "ResourceQuota for nvidia.com/gpu and CPU/mem. Use NetworkPolicy default-deny with allow ingress. "
            "Label metrics by namespace for chargeback. Document PB upgrade via staged namespace rollout."
        ),
    ),
    DesignDrill(
        id="gpu-operator-rollout",
        title="GPU Operator rollout across 20 GPU nodes",
        difficulty="intermediate",
        requirements=[
            "20 new GPU nodes joining existing cluster",
            "Zero impact to running inference pods",
            "Driver version pinned to AI Enterprise PB",
            "Rollback plan required",
        ],
        clarifying_questions=[
            "Same OS/kernel on all nodes?",
            "Driver container or pre-installed driver?",
            "Node labels / taints for GPU?",
        ],
        architecture_outline=(
            "Label new nodes; cordon/drain strategy; install GPU Operator ClusterPolicy matching PB matrix; "
            "validate DCGM and device plugin; uncordon in batches; monitor nvidia.com/gpu allocatable."
        ),
        components=["GPU Operator", "ClusterPolicy", "node labels", "DCGM exporter", "driver container"],
        tradeoffs=["Big-bang vs canary node pools", "Driver container vs host driver"],
        failure_modes=["Driver/kernel mismatch", "Device plugin not registering", "Pods scheduled before GPU ready"],
        rubric=["Phased rollout", "Compatibility matrix cited", "Validation steps", "Rollback defined"],
        sample_answer=(
            "Add nodes to gpu-node-pool with taint nvidia.com/gpu=present. Apply ClusterPolicy version from "
            "AI Enterprise PB matrix. Canary 2 nodes, verify `kubectl describe node` shows allocatable GPU. "
            "Roll 5-node batches. Keep previous ClusterPolicy YAML for rollback. Alert on DCGM scrape failures."
        ),
    ),
    DesignDrill(
        id="rag-platform",
        title="Enterprise RAG platform with NIM",
        difficulty="advanced",
        requirements=[
            "Embedding + rerank + LLM NIMs",
            "Vector DB HA",
            "PII-aware guardrails",
            "Sub-2s p95 for typical queries",
        ],
        clarifying_questions=["Document volume?", "On-prem only?", "Multi-region?", "Auth model?"],
        architecture_outline=(
            "Ingest pipeline → embed NIM → vector DB cluster → query API → rerank NIM → LLM NIM → "
            "NeMo Guardrails optional → audit log. Separate GPU pools for embed vs LLM."
        ),
        components=["NIM embedding", "NIM LLM", "vector DB", "NIMPipeline", "Guardrails", "ingress", "observability"],
        tradeoffs=["Inline vs async indexing", "Shared vs dedicated LLM GPUs", "Cache hot documents"],
        failure_modes=["Stale embeddings", "Vector DB overload", "LLM OOM on long context"],
        rubric=["End-to-end data flow", "Scaling strategy", "Security/guardrails", "Latency budget"],
        sample_answer=(
            "Use NIMPipeline for embed+store batch jobs. Online path: API gateway → rerank NIM (small GPU pool) "
            "→ LLM NIM (H100 pool). Milvus/etcd HA. Guardrails filter on output. HPA on NIMService from latency metric."
        ),
    ),
    DesignDrill(
        id="safe-upgrade",
        title="Safe AI Enterprise release branch upgrade",
        difficulty="intermediate",
        requirements=[
            "Upgrade PB to next PB",
            "GPU Operator + NIM Operator + drivers aligned",
            "Minimal inference downtime",
        ],
        clarifying_questions=["Current branch?", "Maintenance window?", "Mixed GPU generations?"],
        architecture_outline=(
            "Read lifecycle matrix → upgrade operators → rolling node driver updates → "
            "validate NIM profiles → blue/green NIMService cutover."
        ),
        components=["lifecycle policy", "GPU Operator", "NIM Operator", "NIMCache refresh"],
        tradeoffs=["In-place vs new node pool", "Parallel clusters for validation"],
        failure_modes=["Version skew between operator and driver", "Unsupported NIM profile after upgrade"],
        rubric=["Matrix referenced", "Ordered steps", "Validation gates", "Rollback"],
        sample_answer=(
            "Stage lab cluster on target PB. Upgrade GPU Operator ClusterPolicy, then Network Operator if used. "
            "Rolling reboot GPU nodes. Upgrade NIM Operator. Refresh NIMCache artifacts. Blue/green Inference routes."
        ),
    ),
    DesignDrill(
        id="troubleshoot-gpu-pending",
        title="Pod pending: nvidia.com/gpu unavailable",
        difficulty="beginner",
        requirements=["Diagnose why GPU workloads cannot schedule", "Provide fix steps"],
        clarifying_questions=["New cluster or regression?", "MIG enabled?", "Pod events?"],
        architecture_outline="Check pod events → node allocatable → device plugin → driver → GPU Operator → labels/taints",
        components=["device plugin", "GPU Operator", "node labels", "ResourceQuota"],
        tradeoffs=[],
        failure_modes=[
            "GPU Operator not installed on node",
            "Node missing gpu label",
            "Quota already exhausted",
            "Device plugin crash loop",
        ],
        rubric=["Systematic triage order", "kubectl commands", "Root cause", "Preventive monitoring"],
        sample_answer=(
            "`kubectl describe pod` → insufficient nvidia.com/gpu. Check node `allocatable`. "
            "If zero: verify GPU Operator pods on node, driver loaded, device plugin logs. "
            "Confirm node label and no taint blocking. Check namespace ResourceQuota."
        ),
    ),
    DesignDrill(
        id="troubleshoot-nimcache",
        title="NIMService fails: model cache unavailable",
        difficulty="intermediate",
        requirements=["NIMService not ready", "NIMCache related errors in events"],
        clarifying_questions=["NGC connectivity?", "PVC bound?", "Enough disk?"],
        architecture_outline="NIMCache status → PVC → pull secrets → NGC → NIMService modelRef alignment",
        components=["NIMCache", "NIMService", "PVC", "NGC secret"],
        tradeoffs=[],
        failure_modes=["PVC pending storage class", "Invalid NGC API key", "Model profile mismatch", "Incomplete prefetch"],
        rubric=["CRD status inspection", "Storage and secrets", "Fix and verify"],
        sample_answer=(
            "`kubectl describe nimcache` and nim service events. Verify PVC Bound and free space. "
            "Check ngc-secret in namespace. Confirm cache spec model list matches NIMService profile. "
            "Reconcile NIMCache and wait for Ready before NIMService."
        ),
    ),
    DesignDrill(
        id="multi-tenancy-gpu",
        title="Multi-tenancy with namespaces, quotas, RBAC, GPU sharing",
        difficulty="advanced",
        requirements=[
            "5 tenants on shared cluster",
            "No cross-tenant data access",
            "Fair GPU scheduling",
            "Audit logging",
        ],
        clarifying_questions=["Hard or soft multi-tenancy?", "MIG/time-slicing?", "Compliance requirements?"],
        architecture_outline=(
            "Namespace + RBAC + NetworkPolicy per tenant; ResourceQuota GPU/CPU/mem; "
            "optional MIG profiles; separate ingress certs; centralized logging with tenant label."
        ),
        components=["RBAC", "ResourceQuota", "NetworkPolicy", "MIG", "DCGM", "audit logs"],
        tradeoffs=["Shared nodes cost vs isolation", "MIG complexity vs whole GPU per tenant"],
        failure_modes=["Cluster-admin over-permission", "Missing NetworkPolicy", "Quota race at scale"],
        rubric=["Isolation layers", "GPU fairness", "Security controls", "Ops visibility"],
        sample_answer=(
            "Role per tenant scoped to namespace. Default-deny NetworkPolicy. ResourceQuota nvidia.com/gpu. "
            "Use PriorityClass for prod over dev. DCGM metrics labeled by namespace. No cluster-admin for tenants."
        ),
    ),
    DesignDrill(
        id="observability-capacity",
        title="Observability and capacity planning for GPU fleet",
        difficulty="intermediate",
        requirements=[
            "Dashboards for utilization",
            "Alerts before exhaustion",
            "Forecast for 6-month growth",
        ],
        clarifying_questions=["Metrics stack?", "GPU generations mixed?", "Chargeback needed?"],
        architecture_outline="DCGM exporter → Prometheus → Grafana dashboards → alerts on util/memory/temp → capacity model",
        components=["DCGM", "Prometheus", "Grafana", "alertmanager", "GPU Operator"],
        tradeoffs=["Metric cardinality vs detail", "Central vs per-team dashboards"],
        failure_modes=["Missing DCGM labels", "Alert fatigue", "Not tracking MIG slice util"],
        rubric=["Key metrics listed", "Alert thresholds sensible", "Capacity formula", "Tenant visibility"],
        sample_answer=(
            "Scrape DCGM: GPU util, mem used, power, XID errors. Alert util>85% for 30m, XID>0, "
            "pending GPU pods>10. Capacity: track requested vs allocatable GPUs weekly; forecast from job submission trends."
        ),
    ),
]


def get_drill(drill_id: str) -> DesignDrill | None:
    return next((d for d in DESIGN_DRILLS if d.id == drill_id), None)
