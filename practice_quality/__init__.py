"""Shared practice quality pipeline: validate, deduplicate, assemble, analyze, report."""

from practice_quality.assembler import qa_and_assemble
from practice_quality.dedup import fingerprints_for_question, is_duplicate_of_any
from practice_quality.report import build_learning_report
from practice_quality.validator import ValidationResult, validate_question

__all__ = [
    "ValidationResult",
    "build_learning_report",
    "fingerprints_for_question",
    "is_duplicate_of_any",
    "qa_and_assemble",
    "validate_question",
]
