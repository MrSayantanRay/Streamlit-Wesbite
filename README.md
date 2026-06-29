# COVID-19 Mental Health Impact Analysis & DASS-21 Dashboard

An interactive, production-grade analytics platform and professional portfolio built by **Sayantan Ray** (M.Sc. Mathematics & Computing, NIT Hamirpur). This project models the psychological impact of the COVID-19 pandemic on 978 respondents across six major Indian metro cities, tracking transition changes between Phase 1 (T1: early wave/lockdown) and Phase 2 (T2: subsequent wave/easing).

📊 **Live Portfolio & Dashboard App**  
Designed with a premium glassmorphic dark-theme UI, optimized caching, and mathematical statistical validation.

---

## 🧠 DASS-21 Scientific Framework

The project uses the **Depression, Anxiety, and Stress Scale (DASS-21)**:
*   **Depression (7 items)**: Assesses dysphoria, hopelessness, and devaluation of life.
*   **Anxiety (7 items)**: Assesses physiological arousal, situational anxiety, and subjective fear.
*   **Stress (7 items)**: Assesses tension, irritability, and non-specific arousal.

Scale scores are mapped to severity classifications (Normal, Mild, Moderate, Severe, Extremely Severe) using established psychological scoring rules.

---

## 🚀 Key Features

1.  **Portfolio Page**: Recruiter-friendly landing page with educational credentials (NIT Hamirpur), technical skill tags, and social profiles.
2.  **Interactive EDA Dashboard**: Full exploratory analysis of demographics, temporal shifts in socioeconomic factors (monthly expenditures, education status, job status), and mental health impact.
3.  **Dynamic Filtering**: Instantly slice the entire analysis by *Metro City, Gender, Age Group, and Education Level*.
4.  **Statistical Rigor**:
    *   **Spearman Rank Correlation Heatmap**: Demonstrates the interconnectedness of depression, anxiety, and stress across phases.
    *   **Live Chi-Square Test of Independence**: Validates whether socioeconomic disruptors have a statistically significant relationship with psychological outcomes.

---

## 🛠️ Installation & Local Usage

1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/MrSayantanRay/EDA-on-Mental-Health.git
    cd EDA-on-Mental-Health
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the Streamlit Dashboard**:
    ```bash
    streamlit run app.py
    ```

---

## 📂 Project Architecture

```
├── .streamlit/
│   └── config.toml               # Streamlit theme configuration (Dark Mode first)
├── app.py                         # Application router
├── utils/
│   ├── data_loader.py            # Caching-enabled CSV reader and transformer
│   └── theme.py                  # Custom glassmorphic CSS injectors
├── components/
│   └── cards.py                  # Custom metric and info card components
├── modules/
│   ├── portfolio.py              # Portfolio landing page
│   ├── dashboard.py              # Core interactive EDA and impact analysis
│   ├── statistical_insights.py   # Spearman correlation & Chi-Square testing
│   └── contact.py                # Connect form and links
├── requirements.txt               # Project dependencies
└── README.md                      # Documentation
```
