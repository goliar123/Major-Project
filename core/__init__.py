"""
Core attribution and diagnostic components for LLM Multi-Agent Systems.
"""
from core.engine import attribution_engine, AttributionEngine
from core.segmentation import trace_segmenter, TraceSegmenter
from core.step_judge import step_judge, StepJudge
from core.dependency_linker import dependency_linker, DependencyLinker
from core.backward_traversal import backward_traversal_resolver, BackwardTraversalResolver
from core.cache import cache_manager, AttributionCache
from core.llm_client import llm_client, LLMClient

__all__ = [
    "attribution_engine",
    "AttributionEngine",
    "trace_segmenter",
    "TraceSegmenter",
    "step_judge",
    "StepJudge",
    "dependency_linker",
    "DependencyLinker",
    "backward_traversal_resolver",
    "BackwardTraversalResolver",
    "cache_manager",
    "AttributionCache",
    "llm_client",
    "LLMClient"
]
