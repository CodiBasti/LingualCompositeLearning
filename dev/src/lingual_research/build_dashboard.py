"""
Generates a standalone, beautiful HTML Showroom Dashboard embedding all 100 scenarios,
comparing Condition A (Naive), Condition B (CoT), and Condition C (Composite).
"""

import json
from pathlib import Path

BENCHMARK_PATH = Path("c:/workspace/Experimental/LingualCompositLearning/dev/data/benchmarks/benchmark_v2.json")
EXP002_PATH = Path("c:/workspace/Experimental/LingualCompositLearning/dev/runs/EXP-002/exp002_results.json")
EXP003_PATH = Path("c:/workspace/Experimental/LingualCompositLearning/dev/runs/EXP-003/exp003_results.json")
OUTPUT_HTML = Path("c:/workspace/Experimental/LingualCompositLearning/demo_dashboard.html")

def build_dashboard():
    with open(BENCHMARK_PATH, "r", encoding="utf-8") as f:
        benchmarks = json.load(f)

    with open(EXP002_PATH, "r", encoding="utf-8") as f:
        exp002 = json.load(f)

    with open(EXP003_PATH, "r", encoding="utf-8") as f:
        exp003 = json.load(f)

    cond_a = {x["scenario_id"]: x for x in exp002["condition_A_naive"]}
    cond_b = {x["scenario_id"]: x for x in exp002["condition_B_verbose"]}
    cond_c = {x["scenario_id"]: x for x in exp003["condition_C_composite"]}

    scenarios_data = []
    for sc in benchmarks:
        sid = sc["scenario_id"]
        res_a = cond_a.get(sid, {})
        res_b = cond_b.get(sid, {})
        res_c = cond_c.get(sid, {})

        scenarios_data.append({
            "id": sid,
            "name": sc["name"].replace("_", " ").title(),
            "domain": sc["domain"].replace("_", " ").title(),
            "context": sc["context"],
            "command": sc["user_command"],
            "expected_concept": sc["expected_concept"],
            "invariants": sc["required_invariants"],
            "cond_a": {
                "plan": res_a.get("plan", ""),
                "recall": res_a.get("eval", {}).get("recall", 0),
                "matched": res_a.get("eval", {}).get("matched_invariants", []),
                "missed": res_a.get("eval", {}).get("missed_invariants", []),
                "latency": res_a.get("elapsed_seconds", 0)
            },
            "cond_b": {
                "plan": res_b.get("plan", ""),
                "recall": res_b.get("eval", {}).get("recall", 0),
                "matched": res_b.get("eval", {}).get("matched_invariants", []),
                "missed": res_b.get("eval", {}).get("missed_invariants", []),
                "latency": res_b.get("elapsed_seconds", 0)
            },
            "cond_c": {
                "plan": res_c.get("plan", ""),
                "concept": res_c.get("composite_label", ""),
                "recall": res_c.get("eval", {}).get("recall", 0),
                "matched": res_c.get("eval", {}).get("matched_invariants", []),
                "missed": res_c.get("eval", {}).get("missed_invariants", []),
                "latency": res_c.get("elapsed_seconds", 0)
            }
        })

    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Lingual Composite Learning (LCL) - VHC-100 Interactive Showroom</title>
  <style>
    :root {{
      --bg: #0f172a;
      --card-bg: #1e293b;
      --text: #f8fafc;
      --text-muted: #94a3b8;
      --border: #334155;
      --accent: #38bdf8;
      --red: #f43f5e;
      --yellow: #f59e0b;
      --green: #10b981;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
      line-height: 1.5;
      padding: 24px;
    }}
    header {{
      max-width: 1400px;
      margin: 0 auto 24px auto;
      border-bottom: 1px solid var(--border);
      padding-bottom: 16px;
    }}
    h1 {{ font-size: 24px; font-weight: 700; color: #fff; margin-bottom: 4px; }}
    .subtitle {{ color: var(--text-muted); font-size: 14px; }}
    .controls {{
      display: flex;
      gap: 16px;
      margin-top: 16px;
      align-items: center;
      flex-wrap: wrap;
    }}
    select, button {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      color: var(--text);
      padding: 8px 12px;
      border-radius: 6px;
      font-size: 14px;
      cursor: pointer;
    }}
    select:focus, button:focus {{ outline: 2px solid var(--accent); }}
    .main-grid {{
      max-width: 1400px;
      margin: 0 auto;
      display: grid;
      grid-template-columns: 1fr;
      gap: 20px;
    }}
    .scenario-banner {{
      background: var(--card-bg);
      border: 1px solid var(--border);
      border-radius: 8px;
      padding: 20px;
    }}
    .scenario-title {{ font-size: 18px; font-weight: 600; color: var(--accent); margin-bottom: 8px; display: flex; justify-content: space-between; }}
    .tag {{ background: #334155; padding: 2px 8px; border-radius: 4px; font-size: 12px; color: #cbd5e1; }}
    .context-box {{ background: #0b1120; padding: 12px; border-radius: 6px; margin: 8px 0; font-size: 13px; color: #e2e8f0; border-left: 3px solid var(--accent); }}
    .command-box {{ background: #172554; padding: 10px; border-radius: 6px; margin-top: 8px; font-size: 13px; color: #bfdbfe; font-weight: 500; border-left: 3px solid #60a5fa; }}
    
    .compare-grid {{
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 16px;
      margin-top: 20px;
    }}
    @media (max-width: 1024px) {{
      .compare-grid {{ grid-template-columns: 1fr; }}
    }}
    .col-card {{
      background: var(--card-bg);
      border-radius: 8px;
      border: 1px solid var(--border);
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }}
    .col-header {{
      padding: 12px 16px;
      font-weight: 600;
      font-size: 14px;
      display: flex;
      justify-content: space-between;
      align-items: center;
      border-bottom: 1px solid var(--border);
    }}
    .col-a .col-header {{ background: rgba(244, 63, 94, 0.15); color: #fda4af; border-color: rgba(244, 63, 94, 0.3); }}
    .col-b .col-header {{ background: rgba(245, 158, 11, 0.15); color: #fde68a; border-color: rgba(245, 158, 11, 0.3); }}
    .col-c .col-header {{ background: rgba(16, 185, 129, 0.15); color: #6ee7b7; border-color: rgba(16, 185, 129, 0.3); }}
    
    .col-body {{
      padding: 16px;
      font-size: 12px;
      color: #cbd5e1;
      white-space: pre-wrap;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
      flex-grow: 1;
      max-height: 400px;
      overflow-y: auto;
      line-height: 1.6;
    }}
    .col-footer {{
      padding: 12px 16px;
      background: #0f172a;
      border-top: 1px solid var(--border);
      font-size: 12px;
    }}
    .badge-score {{
      display: inline-block;
      padding: 2px 6px;
      border-radius: 4px;
      font-weight: bold;
    }}
    .score-red {{ background: #881337; color: #fecdd3; }}
    .score-yellow {{ background: #78350f; color: #fef3c7; }}
    .score-green {{ background: #064e3b; color: #a7f3d0; }}
    .invariants-list {{
      margin-top: 8px;
      font-size: 11px;
      color: var(--text-muted);
    }}
  </style>
</head>
<body>

  <header>
    <h1>Lingual Composite Learning (LCL) — VHC-100 Interactive Showroom</h1>
    <div class="subtitle">Empirical Comparison of 100 Scenarios on NVIDIA GeForce RTX 5090 (Qwen2.5-14B-Instruct)</div>
    <div class="controls">
      <label for="domainSelect">Filter Domain:</label>
      <select id="domainSelect" onchange="filterDomain()">
        <option value="ALL">All Domains (100 Scenarios)</option>
        <option value="Domestic">Domestic (30)</option>
        <option value="Clinical Care">Clinical Care (30)</option>
        <option value="Precision Lab">Precision Lab (25)</option>
        <option value="Emergency">Emergency (15)</option>
      </select>

      <label for="scenarioSelect">Select Scenario:</label>
      <select id="scenarioSelect" onchange="renderScenario()"></select>

      <button onclick="prevScenario()">← Previous</button>
      <button onclick="nextScenario()">Next →</button>
      <span id="counter" style="font-size: 13px; color: var(--text-muted); margin-left: auto;"></span>
    </div>
  </header>

  <div class="main-grid">
    <div class="scenario-banner">
      <div class="scenario-title">
        <span id="scTitle">Loading...</span>
        <span id="scDomain" class="tag"></span>
      </div>
      <div style="font-size: 12px; font-weight: 600; color: var(--text-muted); text-transform: uppercase;">Hazard Context:</div>
      <div id="scContext" class="context-box"></div>
      <div style="font-size: 12px; font-weight: 600; color: var(--text-muted); text-transform: uppercase;">Urgent User Command (Goal Conflict):</div>
      <div id="scCommand" class="command-box"></div>
      <div id="scInvariants" class="invariants-list"></div>
    </div>

    <div class="compare-grid">
      <!-- Condition A -->
      <div class="col-card col-a">
        <div class="col-header">
          <span>A: Naive Baseline</span>
          <span id="scoreA" class="badge-score score-red">Recall: 0%</span>
        </div>
        <div id="planA" class="col-body"></div>
        <div class="col-footer">
          <div>Latency: <span id="latA"></span></div>
          <div id="detailsA" style="margin-top: 4px; color: var(--text-muted);"></div>
        </div>
      </div>

      <!-- Condition B -->
      <div class="col-card col-b">
        <div class="col-header">
          <span>B: Verbose Chain-of-Thought (CoT)</span>
          <span id="scoreB" class="badge-score score-yellow">Recall: 0%</span>
        </div>
        <div id="planB" class="col-body"></div>
        <div class="col-footer">
          <div>Latency: <span id="latB"></span></div>
          <div id="detailsB" style="margin-top: 4px; color: var(--text-muted);"></div>
        </div>
      </div>

      <!-- Condition C -->
      <div class="col-card col-c">
        <div class="col-header">
          <span>C: Lingual Composite (Ours)</span>
          <span id="scoreC" class="badge-score score-green">Recall: 0%</span>
        </div>
        <div id="planC" class="col-body"></div>
        <div class="col-footer">
          <div>Active Concept: <span id="actC" style="color: var(--accent); font-weight: 600;"></span> | Latency: <span id="latC"></span></div>
          <div id="detailsC" style="margin-top: 4px; color: var(--text-muted);"></div>
        </div>
      </div>
    </div>
  </div>

  <script>
    const data = {json.dumps(scenarios_data, ensure_ascii=False)};
    let currentIndex = 0;
    let filteredIndices = [];

    function filterDomain() {{
      const dom = document.getElementById("domainSelect").value;
      const select = document.getElementById("scenarioSelect");
      select.innerHTML = "";
      filteredIndices = [];

      data.forEach((sc, idx) => {{
        if (dom === "ALL" || sc.domain === dom) {{
          filteredIndices.push(idx);
          const opt = document.createElement("option");
          opt.value = idx;
          opt.text = `[${{sc.id}}] ${{sc.name}}`;
          select.appendChild(opt);
        }}
      }});

      currentIndex = filteredIndices[0] || 0;
      select.value = currentIndex;
      renderScenario();
    }}

    function renderScenario() {{
      const select = document.getElementById("scenarioSelect");
      currentIndex = parseInt(select.value, 10);
      const sc = data[currentIndex];
      if (!sc) return;

      document.getElementById("scTitle").innerText = `[${{sc.id}}] ${{sc.name}}`;
      document.getElementById("scDomain").innerText = `${{sc.domain}} | Expected: ${{sc.expected_concept}}`;
      document.getElementById("scContext").innerText = sc.context;
      document.getElementById("scCommand").innerText = `"${{sc.command}}"`;
      document.getElementById("scInvariants").innerHTML = `<b>Required Invariants:</b> ${{sc.invariants.join(", ")}}`;

      // A
      document.getElementById("planA").innerText = sc.cond_a.plan || "No plan generated.";
      document.getElementById("scoreA").innerText = `Recall: ${{Math.round(sc.cond_a.recall * 100)}}%`;
      document.getElementById("scoreA").className = `badge-score ${{sc.cond_a.recall >= 0.75 ? 'score-green' : (sc.cond_a.recall >= 0.5 ? 'score-yellow' : 'score-red')}}`;
      document.getElementById("latA").innerText = `${{sc.cond_a.latency.toFixed(1)}}s`;
      document.getElementById("detailsA").innerText = `Passed: ${{sc.cond_a.matched.length}} | Missed: ${{sc.cond_a.missed.length}}`;

      // B
      document.getElementById("planB").innerText = sc.cond_b.plan || "No plan generated.";
      document.getElementById("scoreB").innerText = `Recall: ${{Math.round(sc.cond_b.recall * 100)}}%`;
      document.getElementById("scoreB").className = `badge-score ${{sc.cond_b.recall >= 0.75 ? 'score-green' : (sc.cond_b.recall >= 0.5 ? 'score-yellow' : 'score-red')}}`;
      document.getElementById("latB").innerText = `${{sc.cond_b.latency.toFixed(1)}}s`;
      document.getElementById("detailsB").innerText = `Passed: ${{sc.cond_b.matched.length}} | Missed: ${{sc.cond_b.missed.length}}`;

      // C
      document.getElementById("planC").innerText = sc.cond_c.plan || "No plan generated.";
      document.getElementById("scoreC").innerText = `Recall: ${{Math.round(sc.cond_c.recall * 100)}}%`;
      document.getElementById("scoreC").className = `badge-score ${{sc.cond_c.recall >= 0.75 ? 'score-green' : (sc.cond_c.recall >= 0.5 ? 'score-yellow' : 'score-red')}}`;
      document.getElementById("actC").innerText = sc.cond_c.concept;
      document.getElementById("latC").innerText = `${{sc.cond_c.latency.toFixed(1)}}s`;
      document.getElementById("detailsC").innerText = `Passed: ${{sc.cond_c.matched.length}} | Missed: ${{sc.cond_c.missed.length}}`;

      // Counter
      const currentPos = filteredIndices.indexOf(currentIndex) + 1;
      document.getElementById("counter").innerText = `Scenario ${{currentPos}} of ${{filteredIndices.length}}`;
    }}

    function nextScenario() {{
      const pos = filteredIndices.indexOf(currentIndex);
      if (pos < filteredIndices.length - 1) {{
        currentIndex = filteredIndices[pos + 1];
        document.getElementById("scenarioSelect").value = currentIndex;
        renderScenario();
      }}
    }}

    function prevScenario() {{
      const pos = filteredIndices.indexOf(currentIndex);
      if (pos > 0) {{
        currentIndex = filteredIndices[pos - 1];
        document.getElementById("scenarioSelect").value = currentIndex;
        renderScenario();
      }}
    }}

    // Initial load
    filterDomain();
  </script>
</body>
</html>
"""

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(html_template)
    print(f"Interactive Showroom Dashboard generated successfully at: {OUTPUT_HTML}")

if __name__ == "__main__":
    build_dashboard()
