import React, { useEffect, useRef } from "react";
import { AlertCircle, AlertTriangle, CheckCircle, User, Terminal } from "lucide-react";

export default function TraceInspector({ trace, verdict, selectedStepIndex, onSelectStep }) {
  const stepRefs = useRef({});

  useEffect(() => {
    if (selectedStepIndex !== null && stepRefs.current[selectedStepIndex]) {
      stepRefs.current[selectedStepIndex].scrollIntoView({
        behavior: "smooth",
        block: "center"
      });
    }
  }, [selectedStepIndex]);

  if (!trace || !trace.steps || trace.steps.length === 0) {
    return <div className="inspector-empty">No trace steps loaded.</div>;
  }

  const rootIndex = verdict ? verdict.decisive_step_index : -1;
  const symptomIndices = verdict ? verdict.propagated_symptom_indices || [] : [];

  return (
    <div className="trace-inspector-container">
      <div className="inspector-header">
        <h3><Terminal size={18} className="h-icon" aria-hidden="true" /> Forensic Execution Log <span className="num">({trace.steps.length} turns)</span></h3>
        <p className="inspector-sub">
          Click any turn or graph node to inspect agent payloads, prompts, and causal verdicts.
        </p>
      </div>

      <div className="step-list">
        {trace.steps.map((step) => {
          const isRoot = step.step_index === rootIndex;
          const isSymptom = symptomIndices.includes(step.step_index);
          const isSelected = selectedStepIndex === step.step_index;

          let cardClass = "step-card";
          if (isRoot) cardClass += " step-card-root";
          else if (isSymptom) cardClass += " step-card-symptom";
          else cardClass += " step-card-normal";

          if (isSelected) cardClass += " step-card-selected";

          return (
            <div
              key={step.step_index}
              ref={(el) => (stepRefs.current[step.step_index] = el)}
              className={cardClass}
              onClick={() => onSelectStep && onSelectStep(step.step_index)}
            >
              <div className="step-card-top">
                <div className="step-meta">
                  <span className="step-badge">Step {step.step_index}</span>
                  <span className="agent-badge">
                    <User size={13} style={{ marginRight: "4px" }} />
                    {step.agent_name}
                  </span>
                  {step.recipient && (
                    <span className="recipient-badge">→ {step.recipient}</span>
                  )}
                  <span className="action-type-badge">{step.action_type || "action"}</span>
                </div>

                <div className="status-pill-container">
                  {isRoot && (
                    <span className="badge-root">
                      <AlertCircle size={14} />
                      ROOT CAUSE ORIGIN
                    </span>
                  )}
                  {isSymptom && (
                    <span className="badge-symptom">
                      <AlertTriangle size={14} />
                      INHERITED SYMPTOM
                    </span>
                  )}
                  {!isRoot && !isSymptom && (
                    <span className="badge-normal">
                      <CheckCircle size={14} />
                      VALID TURN
                    </span>
                  )}
                </div>
              </div>

              <div className="step-card-content">
                <div className="content-block">
                  <div className="block-label">
                    <Terminal size={13} />
                    <span>Action Payload / Message</span>
                  </div>
                  <pre className="code-box">{step.action_payload || "No action payload."}</pre>
                </div>

                {step.output_state && (
                  <div className="content-block">
                    <div className="block-label">Environment / Tool Response State</div>
                    <pre className="code-box code-box-output">{step.output_state}</pre>
                  </div>
                )}

                {/* Step Judge Evaluation Details if available */}
                {verdict && verdict.graph_nodes && (
                  (() => {
                    const nodeInfo = verdict.graph_nodes.find((n) => n.step_index === step.step_index);
                    if (!nodeInfo) return null;
                    return (
                      <div className="evaluation-box">
                        <div className="eval-row">
                          <span className="eval-label">Health Score:</span>
                          <span className="eval-value score-val" style={{ color: nodeInfo.score < 0.7 ? "#ef4444" : "#10b981" }}>
                            {nodeInfo.score.toFixed(2)} / 1.00
                          </span>
                          <span className="eval-label" style={{ marginLeft: "16px" }}>Judge Finding:</span>
                          <span className="eval-value">{nodeInfo.reason}</span>
                        </div>
                      </div>
                    );
                  })()
                )}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
