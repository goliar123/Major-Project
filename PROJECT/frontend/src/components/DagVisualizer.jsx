import React, { useEffect, useRef, useState } from "react";
import { Network } from "vis-network/standalone";
import { ZoomIn, ZoomOut, Maximize2, Target, GitFork } from "lucide-react";

export default function DagVisualizer({ verdict, onSelectStep, selectedStepIndex }) {
  const containerRef = useRef(null);
  const networkInstanceRef = useRef(null);
  const [isolated, setIsolated] = useState(false);

  useEffect(() => {
    if (!containerRef.current || !verdict || !verdict.graph_nodes || verdict.graph_nodes.length === 0) {
      return;
    }

    const chain = Array.isArray(verdict.causal_dependency_chain) ? verdict.causal_dependency_chain : [];
    const hasChain = chain.length > 0;
    const chainSet = new Set([...chain, verdict.decisive_step_index]);

    const nodesData = verdict.graph_nodes.map((node) => {
      const isRoot = node.status === "root_cause";
      const isSymptom = node.status === "propagated_symptom";
      const isSelected = selectedStepIndex === node.step_index;

      let bgColor = "#10b981"; // normal: emerald
      let borderColor = "#059669";
      let shape = "dot";
      let size = 26;

      if (isRoot) {
        bgColor = "#ef4444"; // crimson red
        borderColor = "#991b1b";
        shape = "box";
        size = 38;
      } else if (isSymptom) {
        bgColor = "#f97316"; // warning amber
        borderColor = "#c2410c";
        shape = "dot";
        size = 30;
      } else if (node.status === "unreached") {
        bgColor = "#64748b";
        borderColor = "#475569";
        size = 20;
      }

      if (isSelected) {
        borderColor = "#6f86ff"; // indigo selection highlight
      }

      return {
        id: node.step_index,
        label: `Step ${node.step_index}\n[${node.agent_name}]\n${typeof node.score === "number" ? node.score.toFixed(2) : "\u2014"}`,
        hidden: isolated && hasChain && !chainSet.has(node.step_index),
        title: `Step ${node.step_index}: ${node.agent_name} (${node.status.toUpperCase()})\nScore: ${node.score.toFixed(2)}\n${node.reason}`,
        shape: shape,
        size: size,
        color: {
          background: bgColor,
          border: borderColor,
          highlight: {
            background: isRoot ? "#f87171" : "#6f86ff",
            border: "#ffffff"
          }
        },
        borderWidth: isRoot ? 3 : (isSelected ? 3 : 1.5),
        font: {
          color: "#ffffff",
          face: "monospace",
          size: 15,
          bold: isRoot || isSelected
        },
        shadow: isRoot
          ? { enabled: true, color: "rgba(239, 68, 68, 0.7)", size: 15, x: 0, y: 0 }
          : false
      };
    });

    const edgesData = (verdict.graph_edges || []).map((edge, idx) => {
      const isCausalPath =
        verdict.causal_dependency_chain &&
        verdict.causal_dependency_chain.includes(edge.source_step_index) &&
        verdict.causal_dependency_chain.includes(edge.target_step_index);

      const isRootSource = edge.source_step_index === verdict.decisive_step_index;

      return {
        id: `e_${idx}`,
        from: edge.source_step_index,
        to: edge.target_step_index,
        hidden: isolated && hasChain && !(chainSet.has(edge.source_step_index) && chainSet.has(edge.target_step_index)),
        arrows: "to",
        color: isRootSource || isCausalPath ? "#ef4444" : "#6f86ff",
        width: isRootSource ? 3.5 : (isCausalPath ? 2.5 : 1.5),
        label: edge.data_variable && edge.data_variable !== "execution_flow" ? edge.data_variable.slice(0, 16) : "",
        font: { color: "#94a3b8", size: 12, align: "top" },
        smooth: { type: "cubicBezier", forceDirection: "horizontal", roundness: 0.3 }
      };
    });

    const data = {
      nodes: nodesData,
      edges: edgesData
    };

    const options = {
      layout: {
        hierarchical: {
          enabled: true,
          direction: "LR",
          sortMethod: "directed",
          levelSeparation: 170,
          nodeSpacing: 130
        }
      },
      physics: {
        enabled: false // hierarchical static layout is super clean and stable
      },
      interaction: {
        hover: true,
        tooltipDelay: 100,
        selectable: true,
        zoomView: true,
        dragView: true
      }
    };

    const network = new Network(containerRef.current, data, options);
    networkInstanceRef.current = network;
    network.fit();
    const raf = requestAnimationFrame(() => network.fit({ animation: { duration: 350, easingFunction: "easeInOutQuad" } }));

    network.on("click", (params) => {
      if (params.nodes && params.nodes.length > 0) {
        const clickedStep = params.nodes[0];
        if (onSelectStep) {
          onSelectStep(clickedStep);
        }
      }
    });

    return () => {
      cancelAnimationFrame(raf);
      network.destroy();
    };
  }, [verdict, selectedStepIndex, isolated]);

  const handleZoomIn = () => {
    if (!networkInstanceRef.current) return;
    const scale = networkInstanceRef.current.getScale();
    networkInstanceRef.current.moveTo({ scale: scale * 1.25 });
  };

  const handleZoomOut = () => {
    if (!networkInstanceRef.current) return;
    const scale = networkInstanceRef.current.getScale();
    networkInstanceRef.current.moveTo({ scale: scale * 0.8 });
  };

  const handleFit = () => {
    if (!networkInstanceRef.current) return;
    networkInstanceRef.current.fit({ animation: { duration: 400, easingFunction: "easeInOutQuad" } });
  };

  const hasChain = !!(verdict && Array.isArray(verdict.causal_dependency_chain) && verdict.causal_dependency_chain.length > 0);

  if (!verdict || !verdict.graph_nodes || verdict.graph_nodes.length === 0) {
    return (
      <div className="dag-empty-placeholder">
        <GitFork size={26} aria-hidden="true" />
        <p><strong>No graph yet.</strong></p>
        <p>Select a trace and run diagnosis to render the causal dependency graph.</p>
      </div>
    );
  }

  return (
    <div className="dag-container-wrapper">
      <div className="dag-toolbar">
        <div className="dag-legend">
          <span className="legend-item">
            <span className="dot dot-red"></span>
            <strong>Root cause (s*)</strong>
          </span>
          <span className="legend-item">
            <span className="dot dot-orange"></span>
            <strong>Propagated Symptom</strong>
          </span>
          <span className="legend-item">
            <span className="dot dot-green"></span>
            <strong>Normal Step</strong>
          </span>
          <span className="legend-item">
            <span className="line-red"></span>
            <strong>Causal Cascade</strong>
          </span>
        </div>
        <div className="dag-controls">
          <button
            className={`icon-btn${isolated ? " on" : ""}`}
            onClick={() => setIsolated((v) => !v)}
            title={isolated ? "Show full graph" : "Isolate causal chain"}
            aria-pressed={isolated}
            disabled={!hasChain}
          >
            <Target size={16} />
          </button>
          <button className="icon-btn" onClick={handleZoomIn} title="Zoom In">
            <ZoomIn size={16} />
          </button>
          <button className="icon-btn" onClick={handleZoomOut} title="Zoom Out">
            <ZoomOut size={16} />
          </button>
          <button className="icon-btn" onClick={handleFit} title="Fit Graph">
            <Maximize2 size={16} />
          </button>
        </div>
      </div>
      <div ref={containerRef} className="dag-canvas" style={{ height: "600px", width: "100%" }} />
    </div>
  );
}
