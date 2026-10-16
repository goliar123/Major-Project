import React, { useState, useEffect } from "react";
import Navbar from "./components/Navbar";
import DagVisualizer from "./components/DagVisualizer";
import TraceInspector from "./components/TraceInspector";
import BenchmarkView from "./components/BenchmarkView";
import CustomIngestionView from "./components/CustomIngestionView";
import TelemetryView from "./components/TelemetryView";
import { fetchHealth, fetchOverview, fetchTraces, fetchTraceById, attributeTrace } from "./services/api";
import { Play, AlertCircle, Clock, Zap, Layers, Target } from "lucide-react";
import "./App.css";

export default function App() {
  const [activeTab, setActiveTab] = useState("dag");
  const [backendHealth, setBackendHealth] = useState(null);
  const [overview, setOverview] = useState(null);
  const [traces, setTraces] = useState([]);
  const [selectedTraceId, setSelectedTraceId] = useState("");
  const [currentTrace, setCurrentTrace] = useState(null);
  const [verdict, setVerdict] = useState(null);
  const [selectedStepIndex, setSelectedStepIndex] = useState(null);
  const [isDiagnosing, setIsDiagnosing] = useState(false);
  const [error, setError] = useState(null);

  // Initial data loading
  useEffect(() => {
    fetchHealth().then(setBackendHealth);
    fetchOverview().then(setOverview).catch(() => {});
    
    fetchTraces(40)
      .then((data) => {
        setTraces(data);
        if (data.length > 0) {
          setSelectedTraceId(data[0].trace_id);
          setCurrentTrace(data[0]);
        }
      })
      .catch((err) => {
        console.error("Could not load initial traces", err);
      });
  }, []);

  // When selectedTraceId changes
  const handleSelectTrace = (traceId) => {
    setSelectedTraceId(traceId);
    setVerdict(null);
    setSelectedStepIndex(null);
    setError(null);
    const found = traces.find((t) => t.trace_id === traceId);
    if (found) {
      setCurrentTrace(found);
    } else {
      fetchTraceById(traceId).then(setCurrentTrace).catch(console.error);
    }
  };

  // Run diagnosis
  const handleRunDiagnosis = async () => {
    if (!currentTrace) return;
    setIsDiagnosing(true);
    setError(null);
    try {
      const res = await attributeTrace(currentTrace);
      setVerdict(res);
      setSelectedStepIndex(res.decisive_step_index);
    } catch (err) {
      setError(err.message || "Diagnosis failed");
    } finally {
      setIsDiagnosing(false);
    }
  };

  // Callback when ingestion creates a custom verdict
  const handleCustomVerdict = (trace, v) => {
    setCurrentTrace(trace);
    setVerdict(v);
    setSelectedStepIndex(v.decisive_step_index);
    setActiveTab("dag");
  };

  return (
    <div className="app-shell">
      <Navbar
        activeTab={activeTab}
        onTabChange={setActiveTab}
        backendHealth={backendHealth}
        totalTraces={overview ? overview.total_traces : traces.length}
      />

      <main className="app-main">
        <div key={activeTab} className="tab-enter">
        {/* TAB 1: Causal DAG Explorer */}
        {activeTab === "dag" && (
          <div className="dag-view-container">
            <div className="view-head">
              <p className="eyebrow"><span className="arrow">↳</span> 01 — Diagnose</p>
              <h2 className="view-title">Causal DAG explorer</h2>
            </div>
            {/* Top Selector Bar */}
            <div className="trace-selector-card">
              <div className="selector-left">
                <label className="selector-label">
                  <Target size={15} />
                  <span>Select Multi-Agent Trace to Diagnose:</span>
                </label>
                <select
                  value={selectedTraceId}
                  onChange={(e) => handleSelectTrace(e.target.value)}
                  className="trace-select-dropdown"
                >
                  {traces.map((t) => (
                    <option key={t.trace_id} value={t.trace_id}>
                      [{t.environment_name}] {t.title || t.task_goal.slice(0, 55)} ({t.steps.length} turns)
                    </option>
                  ))}
                </select>
              </div>

              <div className="selector-right">
                <button
                  className={`btn-primary${isDiagnosing ? " is-loading" : ""}`}
                  onClick={handleRunDiagnosis}
                  disabled={isDiagnosing || !currentTrace}
                >
                  <Play size={16} />
                  <span>{isDiagnosing ? "Traversing Causal DAG..." : "Run Root-Cause Diagnosis"}</span>
                </button>
              </div>
            </div>

            {/* Trace Meta Header */}
            {currentTrace && (
              <div className="trace-info-strip">
                <div className="info-item">
                  <span className="info-label">Task Objective:</span>
                  <span className="info-val">{currentTrace.task_goal}</span>
                </div>
                <div className="info-pills">
                  <span className="info-pill">Env: <strong>{currentTrace.environment_name}</strong></span>
                  <span className="info-pill">Turns: <strong>{currentTrace.steps.length}</strong></span>
                  {currentTrace.ground_truth && (
                    <span className="info-pill gt-pill">
                      GT Blame: <strong>{currentTrace.ground_truth.responsible_agent}</strong> (Step {currentTrace.ground_truth.decisive_step_index})
                    </span>
                  )}
                </div>
              </div>
            )}

            {error && (
              <div className="error-banner" role="alert">
                <AlertCircle size={15} aria-hidden="true" />
                <span>{error}</span>
              </div>
            )}

            {/* Diagnosis Verdict Banner */}
            {verdict && (
              <div className="verdict-banner">
                <div className="verdict-top">
                  <div className="verdict-badge-row">
                    <div className="v-card v-card-agent">
                      <span className="v-label"><AlertCircle size={13} aria-hidden="true" /> Responsible agent</span>
                      <strong className="v-value-agent">{verdict.responsible_agent}</strong>
                    </div>

                    <div className="v-card">
                      <span className="v-label"><Target size={13} aria-hidden="true" /> Decisive error step</span>
                      <strong className="v-value num">Step {verdict.decisive_step_index}</strong>
                    </div>

                    <div className="v-card">
                      <span className="v-label"><Clock size={13} aria-hidden="true" /> Diagnostic latency</span>
                      <strong className="v-value num">{verdict.execution_time_seconds.toFixed(3)} s</strong>
                    </div>

                    <div className="v-card">
                      <span className="v-label"><Zap size={13} aria-hidden="true" /> Cache queries hit</span>
                      <strong className="v-value num">{verdict.cache_hits} hits</strong>
                    </div>

                    {verdict.is_strictly_correct !== null && (
                      <div className={`v-card ${verdict.is_strictly_correct ? "v-card-pass" : "v-card-warn"}`}>
                        <span className="v-label">Ground Truth Match</span>
                        <strong className="v-value">
                          {verdict.is_strictly_correct ? "✓ 100% Match" : "Partial / Heuristic"}
                        </strong>
                      </div>
                    )}
                  </div>
                </div>

                <div className="verdict-explanation">
                  <strong>Causal Justification & Cascade Proof:</strong>
                  <pre className="justification-text">{verdict.explanation}</pre>
                </div>
              </div>
            )}

            {/* Main Workspace Layout: Visualizer & Inspector side by side or stacked */}
            <div className="workspace-split">
              <div className="dag-section">
                <div className="section-title-bar">
                  <h3><Layers size={17} aria-hidden="true" /> Causal dependency graph</h3>
                  <span className="sub-tag">Two-phase backward traversal</span>
                </div>
                <DagVisualizer
                  verdict={verdict}
                  onSelectStep={setSelectedStepIndex}
                  selectedStepIndex={selectedStepIndex}
                />
              </div>

              <div className="inspector-section">
                <TraceInspector
                  trace={currentTrace}
                  verdict={verdict}
                  selectedStepIndex={selectedStepIndex}
                  onSelectStep={setSelectedStepIndex}
                />
              </div>
            </div>
          </div>
        )}

        {/* TAB 2: Benchmarks */}
        {activeTab === "benchmarks" && <BenchmarkView />}

        {/* TAB 3: Custom Ingestion */}
        {activeTab === "ingestion" && (
          <CustomIngestionView onVerdictGenerated={handleCustomVerdict} />
        )}

        {/* TAB 4: Telemetry */}
        {activeTab === "telemetry" && <TelemetryView />}
        </div>
      </main>

      <footer className="app-footer">
        <span>Failure Attribution Engine · Batch B12 · Dept. of CSE, GRIET</span>
        <span className="app-footer-ports">app :5173 · api :8000 · isolated landing :8081</span>
      </footer>
    </div>
  );
}
