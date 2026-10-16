import sys
import os
from pathlib import Path

# Add project root directory to sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from typing import List
import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
import tempfile
from dataset.schema import AttributionVerdict, NodeStatus, DependencyEdge

class DAGViewer:
    @staticmethod
    def render_dag(verdict: AttributionVerdict, height: str = "480px"):
        """Generates and displays an interactive Pyvis network graph."""
        if not verdict.graph_nodes:
            st.info("No dependency graph nodes available for this trace.")
            return

        net = Network(height=height, width="100%", directed=True, bgcolor="#1e1e2e", font_color="#cdd6f4")
        
        # Color mapping
        colors = {
            "root_cause": {"background": "#f38ba8", "border": "#d20f39", "highlight": "#eba0ac"},
            "propagated_symptom": {"background": "#fab387", "border": "#fe640b", "highlight": "#f9e2af"},
            "normal": {"background": "#a6e3a1", "border": "#40a02b", "highlight": "#94e2d5"},
            "unreached": {"background": "#6c7086", "border": "#585b70", "highlight": "#7f849c"}
        }

        # Add Nodes
        for node in verdict.graph_nodes:
            status = node.status
            c = colors.get(status, colors["normal"])
            
            label_text = f"Step {node.step_index}\n[{node.agent_name}]"
            title_tooltip = (
                f"<b>Step {node.step_index}: {node.agent_name}</b><br>"
                f"<b>Status:</b> {status.upper().replace('_', ' ')}<br>"
                f"<b>Health Score:</b> {node.score:.2f}<br>"
                f"<b>Reason:</b> {node.reason}"
            )
            
            size = 32 if status == "root_cause" else (26 if status == "propagated_symptom" else 20)
            shape = "box" if status == "root_cause" else "dot"

            net.add_node(
                n_id=node.step_index,
                label=label_text,
                title=title_tooltip,
                color=c["background"],
                borderWidth=3 if status == "root_cause" else 1.5,
                borderColor=c["border"],
                shape=shape,
                size=size,
                font={"size": 13, "face": "monospace", "color": "#11111b" if status != "root_cause" else "#ffffff"}
            )

        # Add Edges
        for edge in verdict.graph_edges:
            edge_color = "#f38ba8" if edge.source_step_index == verdict.decisive_step_index else "#89b4fa"
            width = 3.0 if edge.source_step_index == verdict.decisive_step_index else 1.5
            
            title_text = f"Type: {edge.dependency_type} | Passed: {edge.data_variable or 'execution_flow'}"
            
            net.add_edge(
                source=edge.source_step_index,
                to=edge.target_step_index,
                title=title_text,
                label=edge.data_variable[:15] if edge.data_variable and edge.data_variable != "execution_flow" else "",
                color=edge_color,
                width=width,
                arrows="to",
                arrowStrikethrough=False,
                font={"size": 10, "color": "#a6adc8", "align": "top"}
            )

        # Set physics layout for clean hierarchical DAG view
        net.set_options("""
        var options = {
          "layout": {
            "hierarchical": {
              "enabled": true,
              "direction": "LR",
              "sortMethod": "directed",
              "nodeSpacing": 160,
              "levelSeparation": 180
            }
          },
          "physics": {
            "hierarchicalRepulsion": {
              "centralGravity": 0.0,
              "springLength": 100,
              "springConstant": 0.01,
              "nodeDistance": 160,
              "damping": 0.09
            },
            "solver": "hierarchicalRepulsion"
          },
          "interaction": {
            "hover": true,
            "tooltipDelay": 100
          }
        }
        """)

        # Generate HTML and render
        with tempfile.NamedTemporaryFile(delete=False, suffix=".html", mode="w", encoding="utf-8") as tmp:
            net.save_graph(tmp.name)
            tmp_path = tmp.name

        with open(tmp_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        try:
            os.remove(tmp_path)
        except Exception:
            pass

        components.html(html_content, height=520, scrolling=True)

dag_viewer = DAGViewer()
