"""LangGraph mentor orchestration (Phase 1 — single-node graph, extensible)."""

from __future__ import annotations

from typing import TypedDict

from langgraph.graph import END, StateGraph


class MentorState(TypedDict, total=False):
    user_message: str
    personality: str
    project_context: str
    response: str


async def mentor_node(state: MentorState) -> MentorState:
    from app.services.llm.provider import LLMProvider

    llm = LLMProvider()
    system = (
        f"You are the {state.get('personality', 'teacher')} mentor for AI Forge. "
        "Guide with questions and hints. Do not give full solutions immediately."
    )
    if state.get("project_context"):
        system += f"\nProject context:\n{state['project_context']}"
    text = await llm.chat(
        [
            {"role": "system", "content": system},
            {"role": "user", "content": state["user_message"]},
        ]
    )
    return {"response": text}


def build_mentor_graph():
    graph = StateGraph(MentorState)
    graph.add_node("mentor", mentor_node)
    graph.set_entry_point("mentor")
    graph.add_edge("mentor", END)
    return graph.compile()
