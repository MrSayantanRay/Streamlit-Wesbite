# 📋 Project Overview
Built by **Sayantan Ray**

---
An advanced data analytics platform and professional portfolio that models and predicts the psychological impact of the COVID-19 pandemic across urban India. By blending deep statistical tracking with predictive machine learning, this application provides data-driven insights into human resilience and psychological vulnerability during a global crisis. The application tracks, visualizes, and predicts critical shifts in mental well-being across two pivotal timelines:
* **Phase 1 (T1):** The initial wave and strict national lockdown constraints.
* **Phase 2 (T2):** Subsequent pandemic waves alongside phased policy easing.


Designed with a glassmorphic dark-theme UI, optimized caching, and statistical validation.

---

## DASS-21 Scientific Framework

The project uses the **Depression, Anxiety, and Stress Scale (DASS-21)**:

- **Depression (7 items)**: Dysphoria, hopelessness, and devaluation of life.
- **Anxiety (7 items)**: Physiological arousal, situational anxiety, and subjective fear.
- **Stress (7 items)**: Tension, irritability, and non-specific arousal.

Scale scores are mapped to severity classifications (Normal, Mild, Moderate, Severe, Extremely Severe) using established psychological scoring rules.

---

## Key Features

1. **Portfolio Landing Page** — Recruiter-friendly profile with credentials, skill tags, social links, and an embedded contact section.
2. **Interactive EDA Dashboard** — Exploratory analysis of demographics, socioeconomic shifts, and mental health impact across T1 and T2.
3. **Statistical Insights** — Spearman rank correlation heatmaps and live Chi-Square tests of independence.
4. **Mental Health Predictor & Analyzer** — **`Logistic regression`** pipelines trained on DASS-21 responses to classify depression, anxiety, and stress severity.
5. **Transparent Model Performance** — Live evaluation metrics displaying the accuracy, precision, and overall correctness of the predictive models, proving the statistical validity of the backend system.
6. **Dynamic Filtering** — Slice the dashboard by metro city, gender, age group, and education level.
7. **Premium Glassmorphism UI** — A gorgeous, customized Streamlit interface using glass-morphic design principles to deliver an immersive user experience that stands out from standard templates.

---

## Tech Stack
1. **Frontend Architecture** — Streamlit, Custom HTML5/CSS3 (Glassmorphism architecture)
2. **API & Integrations** — Native JavaScript async fetching, EmailJS email integration
3. **Data Science & ML Pipeline** — Python, Pandas, Scikit-Learn (or your specific ML package)
 
| Library | Version |
|---------|---------|
| Streamlit | 1.58.0 |
| Pandas | 3.0.3 |
| NumPy | 2.4.6 |
| Plotly | 6.8.0 |
| SciPy | 1.17.1 |
| scikit-learn | 1.9.0 |
| Requests | 2.34.2 |

---

## Installation & Local Usage

1. **Clone the repository**

   ```bash
   git clone https://github.com/MrSayantanRay/EDA-on-Mental-Health.git
   cd EDA-on-Mental-Health
   ```

2. **Create and activate a virtual environment** (recommended)

   ```bash
   python -m venv .venv

   # Windows
   .venv\Scripts\activate

   # macOS / Linux
   source .venv/bin/activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Add the dataset**

   Place the cleaned CSV in the project root:

   ```
   03_adult mental health in indian metro cities 2001-2021 (cleaned).csv
   ```

5. **Run the app**

   ```bash
   streamlit run app.py
   ```

---

## Project Structure

```
├── .streamlit/
│   └── config.toml               # Dark theme configuration
├── app.py                        # Entry point and sidebar navigation
├── utils/
│   ├── data_loader.py            # Cached CSV loader and transformations
│   └── theme.py                  # Custom glassmorphic CSS
├── components/
│   └── cards.py                  # Reusable metric and glass cards
├── modules/
│   ├── portfolio.py              # Landing page (includes contact section)
│   ├── dashboard.py              # Interactive EDA and impact analysis
│   ├── statistical_insights.py   # Spearman correlation and Chi-Square tests
│   ├── predictor.py              # DASS-21 severity classifier
│   └── contact.py                # Contact form and social links
├── requirements.txt
└── README.md
```

---

## Navigation

| Sidebar page | Description |
|---|---|
| Portfolio Landing Page | Profile, skills, and contact |
| Interactive EDA Dashboard | Main metrics view or Statistical Insights sub-view |
| Mental Health Predictor & Analyzer | DASS-21 survey input and ML-based severity prediction |

---

## Author

**Sayantan Ray** — M.Sc. Mathematics & Computing, NIT Hamirpur

© 2026 All rights reserved.
