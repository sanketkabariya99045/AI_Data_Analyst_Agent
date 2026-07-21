# 🚀 AI Business Intelligence Platform

An AI-powered Business Intelligence platform that enables users to upload datasets, ask questions in natural language, generate SQL automatically, create interactive visualizations, and build executive dashboards using Generative AI.

---

## 🌐 Live Demo

**Frontend:** (https://sk-ai-data-analytics.streamlit.app/)

**Backend API:** https://ai-data-analyst-api-mui0.onrender.com

---

# 📸 Screenshots

> *(Add screenshots of your application here)*

- Home Page
- Upload Dataset
- AI Analysis
- Executive Summary
- Dashboard Builder
- Interactive Charts

---

# ✨ Features

## 📂 Dataset Upload

- Upload CSV and Excel datasets
- Automatic schema detection
- Dataset preview
- Data profiling
- Data quality analysis

---

## 🤖 AI Data Analyst

Ask business questions in plain English.

Examples:

- Show total sales by region
- Top 10 customers by revenue
- Monthly sales trend
- Highest profit products
- Average delivery time

The platform automatically:

- Understands your question
- Generates SQL
- Executes SQL
- Returns insights

---

## 📊 Interactive Visualizations

Automatically generates:

- Bar Charts
- Line Charts
- Pie Charts
- KPI Cards
- Tables

using Plotly.

---

## 📈 Executive Insights

AI automatically generates:

- Executive Summary
- Key Findings
- Business Recommendations
- Trend Analysis

---

## 📊 AI Dashboard Builder

Generate complete dashboards using natural language.

Example:

```
Create a Sales Dashboard
```

The platform automatically creates:

- KPIs
- Charts
- Tables
- Executive Summary

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
      ┌───────────┴───────────┐
      ▼                       ▼
   DuckDB                 Gemini AI
      │
      ▼
 Business Insights
```

---

# 🛠 Technology Stack

## Frontend

- Streamlit

## Backend

- FastAPI

## Database

- DuckDB

## AI

- Google Gemini

## Data Processing

- Pandas
- NumPy

## Visualization

- Plotly

## File Support

- CSV
- Excel

## Deployment

- Streamlit Community Cloud
- Render

---

# 📁 Project Structure

```
AI_Data_Analyst_Agent/

├── backend/
│   ├── api/
│   ├── agents/
│   ├── charts/
│   ├── dashboard/
│   ├── database/
│   ├── insights/
│   ├── llm/
│   ├── profiling/
│   ├── services/
│   └── suggestions/
│
├── frontend/
│   ├── components/
│   ├── pages/
│   ├── services/
│   ├── utils/
│   ├── assets/
│   └── app.py
│
├── requirements.txt
└── README.md
```

---

# ⚙ Installation

Clone the repository

```bash
git clone https://github.com/sanketkabariya99045/AI_Data_Analyst_Agent.git
```

Move into the project

```bash
cd AI_Data_Analyst_Agent
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```
GEMINI_API_KEY=YOUR_API_KEY
```

Run the backend

```bash
uvicorn backend.api.main:app --reload
```

Run the frontend

```bash
streamlit run frontend/app.py
```

---

# 🚀 Future Enhancements

- User Authentication
- Dashboard Export (PDF/PNG)
- Chat History
- Multiple Dataset Support
- Forecasting
- Database Connections
- Scheduled Reports
- Role-Based Access Control
- Docker Support
- Kubernetes Deployment

---

# 👨‍💻 Author

**Sanket Kabariya**

Aspiring Data Analyst | AI Developer

GitHub:
https://github.com/sanketkabariya99045

LinkedIn:
*(www.linkedin.com/in/sanket-kabariya-790a21366)*

---

# ⭐ Support

If you found this project useful, consider giving it a ⭐ on GitHub.
