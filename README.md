# 🚀 AI Business Intelligence Platform

An enterprise-grade AI-powered Business Intelligence platform that enables users to upload datasets, ask business questions in natural language, automatically generate SQL queries, build interactive dashboards, and receive AI-generated business insights.

> Built as a portfolio project inspired by modern BI tools like **Power BI Copilot**, **ThoughtSpot Sage**, and **Tableau Pulse**.

---

# 📸 Project Overview

The AI Business Intelligence Platform allows users to:

- 📂 Upload CSV and Excel datasets
- 🤖 Ask questions in natural language
- 🧠 Generate SQL using AI
- 🗄 Execute SQL on DuckDB
- 📊 Build interactive dashboards
- 📈 Generate charts automatically
- 💡 Produce AI-powered business insights
- 📋 Generate executive summaries
- 🤖 Explain business trends using AI
- 📥 Export SQL, CSV, JSON, and dashboards

---

# ✨ Features

## 📂 Dataset Management

- CSV Upload
- Excel Upload
- Multiple Sheet Support
- Automatic Dataset Detection
- Metadata Generation
- Dataset Preview
- Upload Validation

---

## 🤖 AI Data Analyst

Ask questions such as:

> Which category generated the highest sales?

> Show monthly revenue trend.

> Compare profit by region.

The platform automatically:

- Understands the question
- Generates SQL
- Executes SQL
- Builds charts
- Generates KPIs
- Produces AI explanations

---

## 📊 AI Dashboard Builder

Automatically creates executive dashboards including:

- KPI Cards
- Interactive Charts
- Business Tables
- Executive Summary
- Recommendations
- Trend Analysis

---

## 📈 Business Visualizations

Supports AI-generated visualizations including:

- Bar Charts
- Line Charts
- Pie Charts
- Area Charts
- Scatter Charts
- Horizontal Charts

Built using Plotly for interactive analytics.

---

## 💻 SQL Workspace

Features include:

- AI Generated SQL
- SQL Validation
- SQL Download
- Query Execution Statistics
- DuckDB Integration

---

## 📄 Result Workspace

- Interactive Data Tables
- Search Functionality
- Dataset Statistics
- CSV Export
- JSON Export

---

## 📋 Executive Summary

Automatically generates:

- Executive Summary
- Business Overview
- Trend Summary
- Risk Analysis
- Recommendations

---

## 🤖 AI Business Explanation

Provides:

- Business Overview
- Trend Explanation
- Risk Analysis
- Opportunities
- Recommendations
- Final Conclusion

---

# 🏗 Architecture

```
                    User
                      │
                      ▼
              Streamlit Frontend
                      │
                      ▼
               FastAPI Backend
                      │
      ┌───────────────┼────────────────┐
      ▼               ▼                ▼
 AI Dashboard     AI Data Analyst    Upload Engine
      │               │
      ▼               ▼
 Dashboard Planner   SQL Generator
      │               │
      ▼               ▼
 Dashboard SQL     DuckDB Engine
      │               │
      ▼               ▼
 KPI Engine       Query Executor
      │
      ▼
 Chart Engine
      │
      ▼
 Summary Engine
      │
      ▼
 Explanation Engine
```

---

# 🛠 Technology Stack

### Frontend

- Streamlit
- Plotly

### Backend

- FastAPI
- Python

### Database

- DuckDB

### AI

- Google Gemini API

### Data Processing

- Pandas
- NumPy

### Visualization

- Plotly

---

# 📁 Project Structure

```
AI_Business_Intelligence_Platform/

├── backend/
│   ├── agents/
│   ├── api/
│   ├── charts/
│   ├── dashboard/
│   ├── database/
│   ├── insights/
│   ├── llm/
│   ├── models/
│   ├── services/
│   └── utils/
│
├── frontend/
│   ├── components/
│   ├── dashboard/
│   ├── layout/
│   ├── pages/
│   ├── services/
│   ├── state/
│   ├── styles/
│   └── utils/
│
├── data/
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/AI_Data_Analyst_Agent.git

cd AI_Data_Analyst_Agent
```

Create virtual environment

```bash
python -m venv .venv
```

Activate environment

Windows

```bash
.venv\Scripts\activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Run Backend

```bash
uvicorn backend.api.main:app --reload
```

Backend:

```
http://127.0.0.1:8000
```

Swagger:

```
http://127.0.0.1:8000/docs
```

---

# ▶️ Run Frontend

```bash
streamlit run frontend/app.py
```

---

# 🎯 Workflow

```
Upload Dataset
        │
        ▼
Ask Business Question
        │
        ▼
AI Generates SQL
        │
        ▼
Execute Query
        │
        ▼
Generate KPIs
        │
        ▼
Generate Charts
        │
        ▼
Generate Insights
        │
        ▼
Executive Summary
        │
        ▼
Business Explanation
```

---

# 📌 Current Features

- AI SQL Generation
- Interactive Dashboard Builder
- KPI Dashboard
- AI Executive Summary
- AI Business Explanation
- Interactive Charts
- Query Workspace
- Dataset Explorer
- CSV & Excel Upload
- Multi-sheet Support
- Export Results
- Enterprise UI

---

# 🚀 Future Enhancements

- Conversational AI with Memory
- Dashboard Persistence
- User Authentication
- Scheduled Reports
- PDF & PowerPoint Export
- Multi-user Workspace
- Database Connectors (MySQL, PostgreSQL, Snowflake)
- Role-based Access Control
- Dashboard Sharing
- AI Chat Assistant

---

# 👨‍💻 Author

**Sanket Kabariya**

Aspiring Data Analyst | AI Engineer | Python Developer

GitHub:
https://github.com/sanketkabariya99045

---

# ⭐ Support

If you found this project useful, please consider giving it a ⭐ on GitHub.
