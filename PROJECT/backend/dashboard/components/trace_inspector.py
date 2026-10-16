import sys
import os
from pathlib import Path

# Add project root directory to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from typing import List, Optional
import streamlit as st
from dataset.schema import ExecutionStep, AttributionVerdict, MultiAgentTrace

class TraceInspector:
    @staticmethod
    def render_inspector(trace: MultiAgentTrace, verdict: Optional[AttributionVerdict] = None):
        st.subheader("📋 Step-by-Step Execution Log Inspector")

        if not trace.steps:
            st.warning("This trace has no steps to inspect.")
            return

        status_map = {}
        if verdict and verdict.graph_nodes:
            for n in verdict.graph_nodes:
                status_map[n.step_index] = n

        for step in trace.steps:
            idx = step.step_index
            node = status_map.get(idx)
            
            # Determine card header badge
            if node and node.status == "root_cause":
                badge = "🔴 **ROOT CAUSE DETECTED**"
                card_title = f"Step {idx}: {step.agent_name} (Responsible Agent) 🚨"
                expanded = True
            elif node and node.status == "propagated_symptom":
                badge = "🟠 **PROPAGATED SYMPTOM (Inherited Error)**"
                card_title = f"Step {idx}: {step.agent_name} (Downstream Symptom) ⚠️"
                expanded = False
            else:
                badge = "🟢 **NORMAL EXECUTION**"
                card_title = f"Step {idx}: {step.agent_name} ✅"
                expanded = False

            with st.expander(card_title, expanded=expanded):
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.markdown(f"**Agent:** `{step.agent_name}`")
                    st.markdown(f"**Recipient:** `{step.recipient}`")
                    st.markdown(f"**Action Type:** `{step.action_type}`")
                with col2:
                    st.markdown(f"**Diagnostic Status:** {badge}")
                    if node:
                        st.markdown(f"**Step Health Score:** `{node.score:.2f} / 1.00`")

                if node and node.reason:
                    st.info(f"**Judge Diagnosis:** {node.reason}")

                st.markdown("**Input Context:**")
                st.code(step.input_context or "[No prior context / initial prompt]", language="text")

                st.markdown("**Action Payload (Generated Content / Code):**")
                # Auto detect if python or sql or json
                payload_lower = step.action_payload.lower()
                lang = "python" if "def " in payload_lower or "import " in payload_lower else ("sql" if "drop table" in payload_lower or "create table" in payload_lower or "select " in payload_lower else "text")
                st.code(step.action_payload, language=lang)

                if step.output_state:
                    st.markdown("**Output / Environment State:**")
                    st.code(step.output_state, language="text")

trace_inspector = TraceInspector()
