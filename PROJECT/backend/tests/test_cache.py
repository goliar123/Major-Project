"""
Unit tests for SHA256 Prompt Caching Layer.
"""
import pytest
from core.cache import AttributionCache

def test_prompt_hash_determinism():
    cache = AttributionCache()
    prompt1 = "Evaluate step 1: database migration drop table"
    prompt2 = "Evaluate step 1: database migration drop table"
    prompt3 = "Evaluate step 2: database migration alter table"

    h1 = cache.compute_hash(prompt1, "model-qwen")
    h2 = cache.compute_hash(prompt2, "model-qwen")
    h3 = cache.compute_hash(prompt3, "model-qwen")

    assert h1 == h2
    assert h1 != h3

def test_cache_get_set():
    cache = AttributionCache()
    prompt = "Test unique prompt for caching evaluation"
    model = "mock-judge"
    
    # Initial get should be miss or None
    cache.get(prompt, model)
    initial_misses = cache.misses

    # Set cache
    response_data = {"is_valid": False, "score": 0.0, "justification": "Detected test bug."}
    cache.set(prompt, response_data, model)

    # Subsequent get should hit
    hit_data = cache.get(prompt, model)
    assert hit_data is not None
    assert hit_data["score"] == 0.0
    assert hit_data["justification"] == "Detected test bug."
