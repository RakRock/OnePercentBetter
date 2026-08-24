"""Harshit Biology — concept navigation and MCQ remediation state."""

from __future__ import annotations

from dataclasses import dataclass, field

from . import content as hpc


@dataclass
class ConceptSessionState:
    """Tracks one concept-learning session (Stage 1)."""

    day_id: int
    concept_index: int = 0
    show_simpler: bool = False
    show_example: bool = False
    show_visual_again: bool = False
    marked_review: set[str] = field(default_factory=set)
    viewed: set[str] = field(default_factory=set)

    def current_concept(self) -> dict | None:
        concepts = hpc.concepts_for_day(self.day_id)
        if 0 <= self.concept_index < len(concepts):
            return concepts[self.concept_index]
        return None

    def advance(self) -> bool:
        concepts = hpc.concepts_for_day(self.day_id)
        cur = self.current_concept()
        if cur:
            self.viewed.add(cur["id"])
        if self.concept_index + 1 >= len(concepts):
            return False
        self.concept_index += 1
        self.show_simpler = False
        self.show_example = False
        self.show_visual_again = False
        return True

    def toggle_review(self, concept_id: str) -> None:
        if concept_id in self.marked_review:
            self.marked_review.discard(concept_id)
        else:
            self.marked_review.add(concept_id)

    def to_dict(self) -> dict:
        return {
            "day_id": self.day_id,
            "concept_index": self.concept_index,
            "show_simpler": self.show_simpler,
            "show_example": self.show_example,
            "show_visual_again": self.show_visual_again,
            "marked_review": list(self.marked_review),
            "viewed": list(self.viewed),
        }

    @classmethod
    def from_dict(cls, data: dict) -> ConceptSessionState:
        return cls(
            day_id=int(data.get("day_id", 1)),
            concept_index=int(data.get("concept_index", 0)),
            show_simpler=bool(data.get("show_simpler")),
            show_example=bool(data.get("show_example")),
            show_visual_again=bool(data.get("show_visual_again")),
            marked_review=set(data.get("marked_review") or []),
            viewed=set(data.get("viewed") or []),
        )


@dataclass
class MCQSessionState:
    """Stage 2 MCQ flow with remediation."""

    day_id: int
    question_index: int = 0
    pending_review_concept: str | None = None
    parallel_retry: dict | None = None
    attempts: list[dict] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "day_id": self.day_id,
            "question_index": self.question_index,
            "pending_review_concept": self.pending_review_concept,
            "parallel_retry": self.parallel_retry,
            "attempts": self.attempts,
        }

    @classmethod
    def from_dict(cls, data: dict) -> MCQSessionState:
        return cls(
            day_id=int(data.get("day_id", 17)),
            question_index=int(data.get("question_index", 0)),
            pending_review_concept=data.get("pending_review_concept"),
            parallel_retry=data.get("parallel_retry"),
            attempts=list(data.get("attempts") or []),
        )
