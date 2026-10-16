import React, { useState, useEffect } from "react";
import { fetchSyntheticPresets, parseRawLog, parseCustomJson, attributeTrace } from "../services/api";
import { Upload, Sparkles, Terminal, FileCode, Play, CheckCircle } from "lucide-react";

export default function CustomIngestionView({ onVerdictGenerated }) {
  const [activeTab, setActiveTab] = useState("presets");
  const [presets, setPresets] = useState([]);
  const [taskGoal, setTaskGoal] = useState("Diagnose multi-agent failure execution trace.");
  const [rawLogText, setRawLogText] = useState(
`[ProductManager -> DBArchitect]: Please migrate the user table to support Google OAuth without dropping data.
[DBArchitect -> BackendDev]: Executing: DROP TABLE users CASCADE; CREATE TABLE users (id SERIAL PRIMARY KEY, oauth_uid VARCHAR(100));
[BackendDev -> QATester]: User service updated. Querying existing user records for verification.
[QATester -> Supervisor]: CRITICAL: SELECT * FROM users returned 0 rows! All 1,500 historical user accounts have been deleted.`
  );
  const [jsonText, setJsonText] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [successMsg, setSuccessMsg] = useState(null);

  useEffect(() => {
    fetchSyntheticPresets()
      .then((data) => setPresets(data))
      .catch((err) => console.error("Could not load presets", err));
  }, []);

  const handleRunPreset = async (preset) => {
    setLoading(true);
    setError(null);
    setSuccessMsg(null);
    try {
      const tracePayload = {
        trace_id: preset.id,
        title: preset.title,
        environment_name: preset.environment_name,
        task_goal: preset.task_goal,
        steps: preset.steps
      };
      const verdict = await attributeTrace(tracePayload);
      setSuccessMsg(`Diagnosis Completed! Blamed agent: ${verdict.responsible_agent} (Step ${verdict.decisive_step_index})`);
      if (onVerdictGenerated) {
        onVerdictGenerated(tracePayload, verdict);
      }
    } catch (err) {
      setError(err.message || "Failed to attribute preset");
    } finally {
      setLoading(false);
    }
  };

  const handleParseRawLog = async () => {
    if (!rawLogText.trim()) {
      setError("Please paste a console log.");
      return;
    }
    setLoading(true);
    setError(null);
    setSuccessMsg(null);
    try {
      const verdict = await parseRawLog(taskGoal, rawLogText);
      setSuccessMsg(`Parsed & Attributed! Blamed agent: ${verdict.responsible_agent} (Step ${verdict.decisive_step_index})`);
      if (onVerdictGenerated) {
        const syntheticTrace = {
          trace_id: verdict.trace_id,
          title: "Custom Parsed Terminal Log",
          environment_name: "RawConsole",
          task_goal: taskGoal,
          steps: verdict.graph_nodes.map((n, idx) => ({
            step_index: idx,
            agent_name: n.agent_name,
            action_payload: n.reason || "Execution turn",
            action_type: "message"
          }))
        };
        onVerdictGenerated(syntheticTrace, verdict);
      }
    } catch (err) {
      setError(err.message || "Failed to parse raw log");
    } finally {
      setLoading(false);
    }
  };

  const handleParseJson = async () => {
    if (!jsonText.trim()) {
      setError("Please paste JSON payload.");
      return;
    }
    setLoading(true);
    setError(null);
    setSuccessMsg(null);
    try {
      const parsed = JSON.parse(jsonText);
      const verdict = await parseCustomJson(parsed);
      setSuccessMsg(`JSON Analyzed! Blamed agent: ${verdict.responsible_agent} (Step ${verdict.decisive_step_index})`);
      if (onVerdictGenerated) {
        const syntheticTrace = {
          trace_id: verdict.trace_id,
          title: parsed.title || "Custom JSON Workflow",
          environment_name: parsed.environment_name || "CustomAgent",
          task_goal: parsed.task_goal || "Custom Goal",
          steps: parsed.steps || []
        };
        onVerdictGenerated(syntheticTrace, verdict);
      }
    } catch (err) {
      setError(err.message || "Invalid JSON or evaluation failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="ingestion-container">
      <div className="section-hero">
        <div className="hero-text">
          <p className="eyebrow"><span className="arrow">↳</span> 03 — Ingest</p>
          <h2><Upload size={20} className="h-icon" aria-hidden="true" /> Custom Trace Ingestion & Playground</h2>
          <p>
            Test external traces from AutoGen, MetaGPT, ChatDev, CrewAI, or LangGraph.
            Use pre-configured failure scenarios or paste raw terminal transcripts directly.
          </p>
        </div>
      </div>

      <div className="ingest-tabs-nav">
        <button
          className={`ingest-tab-btn ${activeTab === "presets" ? "active" : ""}`}
          onClick={() => setActiveTab("presets")}
        >
          <Sparkles size={16} />
          <span>Curated Failure Presets (1-Click Viva Demos)</span>
        </button>

        <button
          className={`ingest-tab-btn ${activeTab === "raw_log" ? "active" : ""}`}
          onClick={() => setActiveTab("raw_log")}
        >
          <Terminal size={16} />
          <span>Raw Console Transcript Parser</span>
        </button>

        <button
          className={`ingest-tab-btn ${activeTab === "json" ? "active" : ""}`}
          onClick={() => setActiveTab("json")}
        >
          <FileCode size={16} />
          <span>Custom JSON Payload</span>
        </button>
      </div>

      {error && <div className="error-banner">{error}</div>}
      {successMsg && (
        <div className="success-banner">
          <CheckCircle size={16} />
          <span>{successMsg} — Open <strong>Causal DAG Explorer</strong> tab to inspect the graph!</span>
        </div>
      )}

      {/* Tab 1: Presets */}
      {activeTab === "presets" && (
        <div className="presets-grid">
          {presets.map((preset) => (
            <div key={preset.id} className="preset-card">
              <div className="preset-header">
                <h4>{preset.title}</h4>
                <span className="env-badge">{preset.environment_name}</span>
              </div>
              <p className="preset-goal"><strong>Goal:</strong> {preset.task_goal}</p>
              <div className="preset-meta-row">
                <span>Turns: <strong>{preset.steps.length}</strong></span>
                <span>Expected Blame: <strong style={{ color: "#ef4444" }}>{preset.expected_blame}</strong> (Step {preset.expected_step})</span>
              </div>
              <button
                className="btn-primary"
                style={{ width: "100%", marginTop: "14px" }}
                disabled={loading}
                onClick={() => handleRunPreset(preset)}
              >
                <Play size={15} />
                <span>Run Causal Attribution</span>
              </button>
            </div>
          ))}
        </div>
      )}

      {/* Tab 2: Raw Log */}
      {activeTab === "raw_log" && (
        <div className="raw-log-panel">
          <div className="form-group">
            <label>Task Objective / Goal:</label>
            <input
              type="text"
              value={taskGoal}
              onChange={(e) => setTaskGoal(e.target.value)}
              className="text-input"
              placeholder="e.g. Migrate database without deleting rows."
            />
          </div>

          <div className="form-group">
            <label>Paste Console Log (Supports [Sender -&gt; Recipient]: msg or [Sender]: msg):</label>
            <textarea
              rows={10}
              value={rawLogText}
              onChange={(e) => setRawLogText(e.target.value)}
              className="textarea-input"
            />
          </div>

          <button
            className="btn-primary"
            disabled={loading}
            onClick={handleParseRawLog}
            style={{ minWidth: "200px" }}
          >
            <Play size={16} />
            <span>{loading ? "Analyzing..." : "Segment & Attribute Log"}</span>
          </button>
        </div>
      )}

      {/* Tab 3: JSON */}
      {activeTab === "json" && (
        <div className="json-panel">
          <div className="form-group">
            <label>Paste Custom MultiAgent JSON Trace:</label>
            <textarea
              rows={12}
              value={jsonText}
              onChange={(e) => setJsonText(e.target.value)}
              className="textarea-input"
              placeholder={`{
  "title": "Custom AutoGen Test",
  "task_goal": "Deploy app to production",
  "steps": [
    { "step_index": 0, "agent_name": "Dev", "action_payload": "DROP TABLE users;" },
    { "step_index": 1, "agent_name": "Tester", "action_payload": "AssertionError: 0 rows found" }
  ]
}`}
            />
          </div>

          <button
            className="btn-primary"
            disabled={loading}
            onClick={handleParseJson}
            style={{ minWidth: "200px" }}
          >
            <Play size={16} />
            <span>{loading ? "Analyzing..." : "Attribute JSON Trace"}</span>
          </button>
        </div>
      )}
    </div>
  );
}
