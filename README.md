# FTU Career Navigator 🎓

> **Final Project — TINH304 | Foreign Trade University**
> A Streamlit web application that helps FTU business students match their university courses with real-world job market requirements.

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ftu-career-navigator.streamlit.app)

---

## ✨ Features

| Feature | Description |
|---|---|
| 📊 **Market Insights Dashboard** | Visualize top in-demand skills per job role, entry-level salary data, and a skill heatmap across the job market |
| 🎯 **Skill Matching Engine** | Select your completed FTU courses → get a personalized **Fit Score** (%) + dual-trace Radar Chart |
| 💡 **Course Recommender** | Auto-detected skill gaps surface curated Udemy / Coursera / DataCamp course cards |

## 🚀 Quick Start (Local)

```bash
# Clone the repo
git clone https://github.com/nahtlinh/ftu-career-navigator.git
cd ftu-career-navigator

# Install dependencies
pip install -r requirements.txt

# Run
streamlit run app.py
```

App will open at **http://localhost:8501**

## 🛠️ Tech Stack

- **Frontend / App**: [Streamlit](https://streamlit.io) 1.35+
- **Data**: [Pandas](https://pandas.pydata.org) 2.0+
- **Charts**: [Plotly](https://plotly.com/python) 5.20+ (Bar, Radar, Heatmap)
- **Styling**: Custom CSS (glassmorphism dark theme, Inter font)

## 📁 Project Structure

```
ftu-career-navigator/
├── app.py              # Main Streamlit application (all logic + UI)
├── requirements.txt    # Python dependencies
└── README.md           # This file
```

## 📊 Mock Data Overview

| DataFrame | Rows | Description |
|---|---|---|
| `df_job_market` | 40 | 5 jobs × 8 skills each with `Required_Score` |
| `df_ftu_dict` | 22 | FTU courses mapped to acquired skills + `Granted_Score` |

**Job roles covered:** Data Analyst · Marketing Executive · Financial Analyst · Business Development · Supply Chain Analyst

## 🎓 About

Built as the final project for **TINH304 — Information Technology in Business** at **Foreign Trade University (FTU)**, Vietnam.

---

*Data is mock / illustrative and for academic purposes only.*
