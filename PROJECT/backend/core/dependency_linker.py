"""
Information Dependency Linker and Directed Acyclic Graph (DAG) Builder.
Constructs a typed causal dependency graph mapping data flow, variable passing, and message flow across agent turns.
"""
from typing import List, Dict, Set, Tuple, Any
import networkx as nx
import re
from dataset.schema import ExecutionStep, DependencyEdge, MultiAgentTrace
from config.logging_config import logger

class DependencyLinker:
    def __init__(self):
        pass

    def build_dependency_dag(self, steps: List[ExecutionStep]) -> Tuple[nx.DiGraph, List[DependencyEdge]]:
        """
        Constructs a Directed Acyclic Graph (DAG) representing information dependencies across steps.
        Nodes are step indices (0, 1, ..., N-1).
        Edges (u -> v) indicate step 'u' produced information or state consumed by step 'v'.
        """
        G = nx.DiGraph()
        edges: List[DependencyEdge] = []

        # Initialize nodes
        for s in steps:
            G.add_node(
                s.step_index,
                step_id=s.step_id,
                agent=s.agent_name,
                action_type=s.action_type
            )

        # Build edges based on conversational and data dependencies
        for target_idx in range(len(steps)):
            target_step = steps[target_idx]
            target_text = f"{target_step.input_context} {target_step.action_payload}".lower()
            
            # 1. Immediate predecessor sequential link
            if target_idx > 0:
                # Add default sequential dialogue edge
                source_idx = target_idx - 1
                edge_obj = DependencyEdge(
                    source_step_index=source_idx,
                    target_step_index=target_idx,
                    source_step_id=steps[source_idx].step_id,
                    target_step_id=target_step.step_id,
                    data_variable="execution_flow",
                    dependency_type="data_flow",
                    confidence=0.85
                )
                G.add_edge(source_idx, target_idx, **edge_obj.model_dump())
                edges.append(edge_obj)

            # 2. Variable and entity reuse from earlier steps (long-range dependencies)
            for source_idx in range(0, target_idx - 1):
                source_step = steps[source_idx]
                source_payload = source_step.action_payload.lower()
                source_output = (source_step.output_state or "").lower()

                # Extract notable tokens / identifiers (e.g., function names, variable names, tables)
                extracted_entities = self._extract_key_entities(source_payload + " " + source_output)
                matched_entities = [ent for ent in extracted_entities if ent in target_text and len(ent) > 4]

                # Check if recipient matches target agent
                is_addressed = (source_step.recipient.lower() == target_step.agent_name.lower()) if source_step.recipient else False

                if matched_entities or is_addressed:
                    var_desc = ", ".join(matched_entities[:3]) if matched_entities else "direct_message"
                    edge_type = "shared_state" if matched_entities else "message_reply"
                    
                    if not G.has_edge(source_idx, target_idx):
                        edge_obj = DependencyEdge(
                            source_step_index=source_idx,
                            target_step_index=target_idx,
                            source_step_id=source_step.step_id,
                            target_step_id=target_step.step_id,
                            data_variable=var_desc,
                            dependency_type=edge_type,
                            confidence=0.95 if matched_entities else 0.8
                        )
                        G.add_edge(source_idx, target_idx, **edge_obj.model_dump())
                        edges.append(edge_obj)

        logger.debug(f"Constructed Dependency DAG with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges.")
        return G, edges

    def _extract_key_entities(self, text: str) -> List[str]:
        """Extracts identifier-like tokens, function names, and keywords."""
        # Match function calls like def foo(), class Bar, or variables with underscores
        identifiers = re.findall(r"\b[a-z_][a-z0-9_]{3,}\b", text)
        stop_words = {"this", "that", "with", "from", "have", "return", "step", "task", "agent", "please", "output", "input"}
        return [i for i in set(identifiers) if i not in stop_words]

dependency_linker = DependencyLinker()
