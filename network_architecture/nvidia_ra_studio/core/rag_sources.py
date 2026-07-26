"""Official NVIDIA documentation links (canonical sources)."""

from __future__ import annotations

OFFICIAL_DOCS = {
    "ra_index": "https://docs.nvidia.com/ai-enterprise/reference-architecture/latest/index.html",
    "platform_overview": "https://docs.nvidia.com/ai-enterprise/reference-architecture/latest/platform-overview.html",
    "software_stack": "https://docs.nvidia.com/ai-enterprise/reference-architecture/latest/software-stack.html",
    "target_workloads": "https://docs.nvidia.com/ai-enterprise/reference-architecture/latest/target-workloads.html",
    "lifecycle": "https://docs.nvidia.com/ai-enterprise/lifecycle/latest/index.html",
    "gpu_operator": "https://docs.nvidia.com/datacenter/cloud-native/gpu-operator/latest/index.html",
    "nim_operator": "https://docs.nvidia.com/nim-operator/latest/index.html",
    "network_operator": "https://docs.nvidia.com/datacenter/cloud-native/network-operator/latest/index.html",
    "kserve": "https://kserve.github.io/website/",
    "dcgm": "https://docs.nvidia.com/datacenter/dcgm/latest/index.html",
}

ALL_DOC_LINKS = [
    {"key": k, "title": k.replace("_", " ").title(), "url": v}
    for k, v in OFFICIAL_DOCS.items()
]


def doc_url(key: str) -> str:
    return OFFICIAL_DOCS.get(key, OFFICIAL_DOCS["ra_index"])
