"""
Pydantic Data Models and Schemas for Multi-Agent Failure Attribution.
"""
from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field
import uuid
from datetime import datetime, timezone

class DependencyEdge(BaseModel):
    """Represents an information or state dependency between two execution steps."""
    dependency_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    source_step_index: int  # The upstream step providing information
    target_step_index: int  # The downstream step consuming information
    source_step_id: Optional[str] = None
    target_step_id: Optional[str] = None
    data_variable: Optional[str] = None  # Specific variable, file, or topic passed
    dependency_type: Literal["data_flow", "message_reply", "shared_state", "instruction"] = "data_flow"
    confidence: float = 1.0

class StepEvaluation(BaseModel):
    """Result of step-wise LLM evaluation on a single turn."""
    step_index: int
    step_id: str
    is_valid: bool
    score: float = Field(..., ge=0.0, le=1.0, description="1.0 is completely normal/correct, 0.0 is complete failure")
    anomaly_detected: bool
    error_category: Optional[str] = None  # e.g., "hallucination", "syntax_error", "logic_flaw", "corrupted_input_propagation"
    justification: str
    prompt_hash: Optional[str] = None
    cached: bool = False

class ExecutionStep(BaseModel):
    """Represents a discrete turn/step in a multi-agent execution trace."""
    step_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:8])
    step_index: int
    agent_name: str
    recipient: Optional[str] = "All"
    action_type: str = "message"  # e.g., "message", "tool_call", "code_execution", "plan_generation"
    input_context: str = ""  # Context received by the agent
    action_payload: str = ""  # The content generated or action taken
    output_state: Optional[str] = None  # Result returned by tool/environment or response
    timestamp: Optional[str] = None
    evaluation: Optional[StepEvaluation] = None

class GroundTruth(BaseModel):
    """Human-verified or benchmark ground-truth failure attribution."""
    responsible_agent: str
    decisive_step_index: int
    failure_reason: str
    failure_category: Optional[str] = None

class MultiAgentTrace(BaseModel):
    """Represents a complete multi-agent execution trace."""
    trace_id: str = Field(default_factory=lambda: str(uuid.uuid4())[:12])
    title: Optional[str] = None
    environment_name: str = "AutoGen"  # AutoGen, ChatDev, MetaGPT, GAIA, AssistantBench
    task_goal: str
    total_steps: int = 0
    steps: List[ExecutionStep] = Field(default_factory=list)
    final_outcome: Optional[str] = "failed"
    ground_truth: Optional[GroundTruth] = None
    raw_payload: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class NodeStatus(BaseModel):
    step_index: int
    step_id: str
    agent_name: str
    status: Literal["normal", "root_cause", "propagated_symptom", "unreached"]
    score: float
    reason: str

class AttributionVerdict(BaseModel):
    """The final diagnosis returned by the attribution engine."""
    trace_id: str
    method_name: str
    responsible_agent: str
    decisive_step_index: int
    decisive_step_id: Optional[str] = None
    failure_type: str
    explanation: str
    root_cause_step: Optional[ExecutionStep] = None
    propagated_symptom_indices: List[int] = Field(default_factory=list)
    causal_dependency_chain: List[int] = Field(default_factory=list)
    graph_nodes: List[NodeStatus] = Field(default_factory=list)
    graph_edges: List[DependencyEdge] = Field(default_factory=list)
    is_correct_agent: Optional[bool] = None
    is_correct_step: Optional[bool] = None
    is_strictly_correct: Optional[bool] = None
    execution_time_seconds: float = 0.0
    cache_hits: int = 0
    cache_misses: int = 0
    total_tokens_used: int = 0

class BenchmarkResult(BaseModel):
    """Summary of benchmark evaluation run across multiple traces."""
    benchmark_name: str
    total_traces: int
    evaluated_traces: int
    agent_level_accuracy: float
    step_level_accuracy: float
    strict_joint_accuracy: float
    avg_execution_time_per_trace: float
    cache_hit_rate: float
    total_token_count: int
    method_comparisons: Optional[Dict[str, Dict[str, float]]] = None
    individual_verdicts: List[AttributionVerdict] = Field(default_factory=list)
