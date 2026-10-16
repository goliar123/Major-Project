/**
 * API Service for Automated Failure Attribution Engine
 * Default: local backend at http://localhost:8000/api/v1
 * Deployed: set VITE_API_BASE_URL at build time, e.g.
 *   https://your-backend.onrender.com/api/v1
 */
const API_BASE = (
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1"
).replace(/\/$/, "");

export async function fetchHealth() {
  try {
    const res = await fetch(`${API_BASE}/health`, { signal: AbortSignal.timeout(3000) });
    if (!res.ok) throw new Error("Health check failed");
    return await res.json();
  } catch (err) {
    return { status: "offline", error: err.message };
  }
}

export async function fetchOverview() {
  const res = await fetch(`${API_BASE}/overview`);
  if (!res.ok) throw new Error("Failed to fetch system overview");
  return await res.json();
}

export async function fetchTraces(limit = 50, subset = null) {
  let url = `${API_BASE}/traces?limit=${limit}`;
  if (subset) url += `&subset=${encodeURIComponent(subset)}`;
  const res = await fetch(url);
  if (!res.ok) throw new Error("Failed to load benchmark traces");
  return await res.json();
}

export async function fetchTraceById(traceId) {
  const res = await fetch(`${API_BASE}/traces/${encodeURIComponent(traceId)}`);
  if (!res.ok) throw new Error(`Failed to load trace ${traceId}`);
  return await res.json();
}

export async function attributeTrace(tracePayload) {
  const res = await fetch(`${API_BASE}/attribute`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(tracePayload)
  });
  if (!res.ok) {
    const errorData = await res.json().catch(() => ({}));
    throw new Error(errorData.detail || "Attribution computation failed");
  }
  return await res.json();
}

export async function fetchSyntheticPresets() {
  const res = await fetch(`${API_BASE}/synthetic/presets`);
  if (!res.ok) throw new Error("Failed to fetch synthetic presets");
  return await res.json();
}

export async function parseRawLog(taskGoal, logText) {
  const res = await fetch(`${API_BASE}/parse/raw_log`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ task_goal: taskGoal, log_text: logText })
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Failed to parse raw log");
  }
  return await res.json();
}

export async function parseCustomJson(payload) {
  const res = await fetch(`${API_BASE}/parse/custom_json`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "Failed to parse custom JSON");
  }
  return await res.json();
}

export async function runBenchmark(method = "proposed", maxTraces = 10) {
  const res = await fetch(`${API_BASE}/benchmark/run?method=${encodeURIComponent(method)}&limit=${maxTraces}`, {
    method: "POST"
  });
  if (!res.ok) throw new Error("Benchmark execution failed");
  return await res.json();
}

export async function fetchCacheStats() {
  const res = await fetch(`${API_BASE}/cache/stats`);
  if (!res.ok) throw new Error("Failed to fetch cache stats");
  return await res.json();
}

export async function clearCache() {
  const res = await fetch(`${API_BASE}/cache/clear`, { method: "POST" });
  if (!res.ok) throw new Error("Failed to clear cache");
  return await res.json();
}
