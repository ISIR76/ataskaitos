"""Evaluator registry and loading system."""

from .base import EvaluatorRegistry, get_registry
from .loader import (
    initialize_default_evaluators,
    load_evaluators_from_dict,
    load_evaluators_from_json,
)

__all__ = [
    "EvaluatorRegistry",
    "get_registry",
    "load_evaluators_from_json",
    "load_evaluators_from_dict",
    "initialize_default_evaluators",
]
