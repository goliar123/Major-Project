# Automated Failure Attribution for LLM-Based Multi-Agent Systems
**B.Tech Major Project Phase-1 · Batch B12 · Department of CSE · Gokaraju Rangaraju Institute of Engineering and Technology (GRIET)**

---

## 👥 Project Team & Credentials
- **Rachapalli S Prabhaadhithya** (23241A05Q3)
- **Rathod Ajay** (23241A05Q4)
- **Noel Paul** (23241A05Q6)
- **Talagapu Niranjan** (23241A05R1)
- **Internal Guide:** Dr. D. Ushasree, Assistant Professor, Dept of CSE, GRIET

---

## 📁 Repository Organization

The repository has been neatly segregated into two main directories:

### 1. `media/` — Presentation Decks, Reports, Diagrams & Reference Material
- **`media/presentations/`**: Contains Review-3 slide decks (`D1_Review_3_PW.pptx`, `D1_Review_3_PW.pdf`, `Review_3_Automated_Failure_Attribution_B12.pptx`, `Review_3_Automated_Failure_Attribution_B12.pdf`).
- **`media/reports/`**: Complete 56-page Phase-1 Project Report (`Major_Project_Phase1_Report_B12.docx`, `Major_Project_Phase1_Report_B12.pdf`, and Markdown source).
- **`media/diagrams/`**: High-resolution diagrams for Architecture, UML (Use Case, Class, Sequence), DFD Levels 0 & 1, and ERD.
- **`media/report_builders/`**: Python and Pandoc compilation scripts for automated report generation.
- **`media/notes/`**: Theoretical research notes, literature surveys, and Viva Voce preparation guides.

### 2. `PROJECT/` — Full-Stack Software Engineering System
- **`PROJECT/backend/`**: FastAPI backend featuring the 5-stage Neuro-Symbolic attribution pipeline (Token Budgeting, StepJudge, Information Dependency DAG, Backward Causal Traversal, Root-Cause vs Symptom Resolution, and Deterministic SHA-256 Prompt Caching).
- **`PROJECT/frontend/`**: Modern React + Vite + Tailwind single-page application with interactive VisNetwork DAG visualization, forensic turn inspector, Who&When benchmark matrix, custom log ingestion, and telemetry dashboard.
- **Launchers**:
  - `PROJECT/start_all.sh`: Launches both FastAPI backend (`http://localhost:8000`) and React frontend (`http://localhost:5173`).
  - `PROJECT/start_dashboard.sh`: Launches Python-native Streamlit dashboard (`http://localhost:8501`).
  - `PROJECT/run_tests.sh`: Runs the full automated test suite (27 passing pytest tests).
  - `PROJECT/test_all_who_and_when.sh`: Runs empirical evaluation over all 184 Who&When benchmark traces.

---

## 🚀 Quickstart: Running the System

```bash
# 1. Enter the project directory
cd PROJECT

# 2. Run both Backend & Frontend with a single command:
./start_all.sh

# 3. Run Who&When Benchmark Suite (All 184 Traces):
./test_all_who_and_when.sh

# 4. Run Pytest Test Suite (27 Unit & Integration Tests):
./run_tests.sh
```

- **Interactive Web App:** [http://localhost:5173](http://localhost:5173)
- **Backend API Docs (Swagger):** [http://localhost:8000/docs](http://localhost:8000/docs)
- **Streamlit Alternative:** `cd PROJECT && ./start_dashboard.sh` ([http://localhost:8501](http://localhost:8501))
- **Benchmark Evaluation:** `cd PROJECT && ./test_all_who_and_when.sh`
- **Automated Tests:** `cd PROJECT && ./run_tests.sh`
