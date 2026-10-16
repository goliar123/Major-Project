import React from "react";
import { GitFork, BarChart3, Upload, Zap, Server, Layers } from "lucide-react";

const TABS = [
  { id: "dag", label: "Causal DAG Explorer", Icon: GitFork },
  { id: "benchmarks", label: "Benchmark Matrix", Icon: BarChart3 },
  { id: "ingestion", label: "Trace Ingestion", Icon: Upload },
  { id: "telemetry", label: "Cache Telemetry", Icon: Zap },
];

export default function Navbar({ activeTab, onTabChange, backendHealth, totalTraces }) {
  const isOnline = backendHealth && backendHealth.status === "healthy";

  return (
    <header className="navbar-container">
      <div className="navbar-brand">
        <div className="brand-logo" aria-hidden="true">
          <GitFork size={22} />
        </div>
        <div className="brand-titles">
          <div className="brand-main">
            <h1>Failure Attribution Engine</h1>
            <span className="badge-batch">B12 · GRIET</span>
          </div>
          <p className="brand-sub">Causal root-cause localizer for LLM multi-agent traces</p>
        </div>
      </div>

      <nav className="navbar-links" aria-label="Primary">
        {TABS.map(({ id, label, Icon }) => (
          <button
            key={id}
            className={`nav-tab-btn ${activeTab === id ? "active" : ""}`}
            aria-current={activeTab === id ? "page" : undefined}
            onClick={() => onTabChange(id)}
          >
            <Icon size={16} aria-hidden="true" />
            <span>{label}</span>
          </button>
        ))}
      </nav>

      <div className="navbar-status">
        <div className="status-chip" title={isOnline ? "FastAPI backend reachable" : "Waiting for FastAPI backend"}>
          <span className={`status-indicator ${isOnline ? "indicator-online" : "indicator-offline"}`} aria-hidden="true" />
          <span>{isOnline ? "Backend :8000" : "Connecting…"}</span>
        </div>
        {typeof totalTraces === "number" && totalTraces > 0 && (
          <div className="status-chip" title="Loaded benchmark traces">
            <Layers size={13} aria-hidden="true" />
            <span className="num">{totalTraces} traces</span>
          </div>
        )}
        <div className="status-chip model-chip" title="Active judge model">
          <Server size={13} aria-hidden="true" />
          <span>Qwen2.5:7b</span>
        </div>
      </div>
    </header>
  );
}
