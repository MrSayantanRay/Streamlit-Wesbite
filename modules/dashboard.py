import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from components.cards import draw_metric_card, draw_glass_card
from modules.contact import render_contact_page

def render_dashboard_page(df):
    """
    Renders the interactive EDA dashboard and DASS-21 impact analysis with integrated tabs.
    All introduction elements, metrics filters, and tabs are safely encapsulated here.
    """
    # --------------------------------------------------
    # 1. MAIN TITLE & SUBTITLE
    # --------------------------------------------------
    st.markdown('<h1 class="main-title">Interactive Analysis</h1>', unsafe_allow_html=True)    
    # --------------------------------------------------
    # 2. DASHBOARD RESEARCH INTRODUCTION (OVERVIEW)
    # --------------------------------------------------
    st.html('<h2 style="color: #6C5CE7; font-weight: 800; margin-top: 1.5rem; margin-bottom: 0.5rem;">Crisis & Cognition: Mental Health Analytics</h2>')

    # Executive Summary Glass Container
    st.markdown(
        """
        <div class="glass-card" style="padding: 1.5rem; margin-bottom: 2rem; line-height: 1.7; color: #CBD5E1; font-size: 1.05rem;">
            Welcome to the <b>Interactive Analytics Workspace</b>. This platform presents an empirical exploratory study 
            investigating the longitudinal psychological toll of the COVID-19 pandemic across major Indian metropolitan populations. 
            By mapping standard clinical psychometric scales against deep household changes, this analysis uncovers how 
            macro-level socioeconomic shocks directly translated into micro-level mental health crises.
        </div>
        """, 
        unsafe_allow_html=True
    )

    # Core Analytical Focus Pillars (3-Column Layout)
    st.markdown('<p style="color: #94A3B8; font-size: 0.95rem; font-weight: 600; margin-bottom: 0.8rem;">Core Research Pillars</p>', unsafe_allow_html=True)
    intro_col1, intro_col2, intro_col3 = st.columns(3)

    with intro_col1:
        st.markdown(
            """
            <div class="glass-card" style="height: 100%; border-top: 3px solid #6C5CE7; padding: 1.2rem;">
                <h4 style="color: #A8A5FF; margin-top:0; font-size: 1.05rem;">The DASS Framework</h4>
                <p style="font-size: 0.88rem; color: #94A3B8; margin:0; line-height: 1.6;">
                    Utilizes the psychometric <b>Depression, Anxiety, and Stress Scale (DASS)</b> framework to evaluate and track standard clinical distress profiles across varying age cohorts.
                </p>
            </div>
            """, unsafe_allow_html=True
        )
        
    with intro_col2:
        st.markdown(
            """
            <div class="glass-card" style="height: 100%; border-top: 3px solid #00B894; padding: 1.2rem;">
                <h4 style="color: #55E6C1; margin-top:0; font-size: 1.05rem;">Economic Shocks</h4>
                <p style="font-size: 0.88rem; color: #94A3B8; margin:0; line-height: 1.6;">
                    Examines the direct correlations between corporate pay cuts, family business declines, shifting expenditure boundaries, and escalating severe depression thresholds.
                </p>
            </div>
            """, unsafe_allow_html=True
        )
        
    with intro_col3:
        st.markdown(
            """
            <div class="glass-card" style="height: 100%; border-top: 3px solid #0984E3; padding: 1.2rem;">
                <h4 style="color: #74B9FF; margin-top:0; font-size: 1.05rem;">Domestic Instability</h4>
                <p style="font-size: 0.88rem; color: #94A3B8; margin:0; line-height: 1.6;">
                    Uncovers a critical cross-phase finding regarding how educational disruptions and instability for children heavily triggered stress development inside families.
                </p>
            </div>
            """, unsafe_allow_html=True
        )
        
    # Academic Foundation & Attribution Tag
    st.markdown(
        """
        <div style="text-align: right; font-size: 0.8rem; color: #64748B; margin-top: 1rem; margin-bottom: 2.5rem; font-style: italic;">
            Data curated from Mendeley Data Repository | Academic Guidance: Prof. Zakir Hussain
        </div>
        """, 
        unsafe_allow_html=True
    )

    # --------------------------------------------------
    # 3. SIDEBAR FILTERING (Global for EDA Tab)
    # --------------------------------------------------
    st.sidebar.markdown("### Demographic Filters")
    
    cities = ['All'] + sorted(list(df['city'].unique()))
    selected_city = st.sidebar.selectbox("Metro City", cities, index=0)
    
    genders = ['All'] + sorted(list(df['sex'].unique()))
    selected_gender = st.sidebar.selectbox("Gender", genders, index=0)
    
    age_groups = ['All'] + sorted(list(df['age_group'].dropna().unique()))
    selected_age = st.sidebar.selectbox("Age Group", age_groups, index=0)
    
    study_levels = ['All'] + sorted(list(df['study_level'].unique()))
    selected_study = st.sidebar.selectbox("Education Level", study_levels, index=0)
    
    # Filter Data Intersections
    filtered_df = df.copy()
    if selected_city != 'All':
        filtered_df = filtered_df[filtered_df['city'] == selected_city]
    if selected_gender != 'All':
        filtered_df = filtered_df[filtered_df['sex'] == selected_gender]
    if selected_age != 'All':
        filtered_df = filtered_df[filtered_df['age_group'] == selected_age]
    if selected_study != 'All':
        filtered_df = filtered_df[filtered_df['study_level'] == selected_study]

    # --------------------------------------------------
    # 4. INTERACTIVE TABBED CONTAINER (With Custom CSS Injection)
    # --------------------------------------------------
    st.markdown("""
        <style>
            /* Make the tab buttons larger and bold */
            .stTabs [data-baseweb="tab"] {
                font-size: 1.3rem !important;
                font-weight: 700 !important;
                padding-top: 10px !important;
                padding-bottom: 10px !important;
            }
            /* Ensure the text inside the tab scales perfectly across Streamlit versions */
            .stTabs [data-baseweb="tab"] p {
                font-size: 1.3rem !important;
                font-weight: 700 !important;
            }
        </style>
    """, unsafe_allow_html=True)

    tab_eda, = st.tabs(["📊 Exploratory Data Analysis"])

    with tab_eda:
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            draw_metric_card("Total Sample Size", len(filtered_df))
            
        with col2:
            if not filtered_df.empty and 'age' in filtered_df.columns:
                draw_metric_card("Average Age", f"{filtered_df['age'].mean():.1f} yrs")
            else:
                draw_metric_card("Average Age", "N/A")
                
        with col3:
            if not filtered_df.empty and 'depression_level T2' in filtered_df.columns:
                t2_dep_pct = (filtered_df['depression_level T2'].isin(['Moderate', 'Severe', 'Extremely severe']).sum() / len(filtered_df) * 100)
                draw_metric_card("Depressive Distress T2", f"{t2_dep_pct:.1f}%", "depression")
            else:
                draw_metric_card("Depressive Distress T2", "N/A", "depression")

        st.markdown("<br>", unsafe_allow_html=True)


        chart_col1, chart_col2, chart_col3 = st.columns([1, 1, 0.3])
        
        with chart_col3:
            st.markdown("<div style='padding-top: 85px;'></div>", unsafe_allow_html=True)
            
            selected_phase = st.radio(
                label="Phase Selector",        # Required by Streamlit but hidden from UI
                options=["Phase 1 (T1)", "Phase 2 (T2)"],
                horizontal=False,              # Stacked vertically next to the chart
                label_visibility="collapsed",  # Strips away the widget label space completely
                key="covid_phase_selector"
            )
        
        # Map choice to exact dataframe column targets
        column_mapping = {
            "Phase 1 (T1)": "covid_case T1",
            "Phase 2 (T2)": "covid_case T2"
        }
        target_column = column_mapping[selected_phase]

        # --- COLUMN 1: Sex Ratio Donut Chart ---
        with chart_col1:
            if not filtered_df.empty and 'sex' in filtered_df.columns:
                gender_counts = filtered_df['sex'].value_counts().reset_index()
                gender_counts.columns = ['sex', 'Count']
                
                fig_sex = px.pie(
                    gender_counts, 
                    names='sex', 
                    values='Count',
                    hole=0.4,
                    color_discrete_sequence=['#4F46E5', '#EC4899'],
                    title="Overall Sex Ratio"
                )
                
                fig_sex.update_layout(
                    title_font=dict(size=24, family="Arial"),
                    margin=dict(t=50, b=10, l=10, r=10),
                    height=270,
                    showlegend=True,
                    legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
                )
                
                st.plotly_chart(fig_sex, use_container_width=True)
        
        # --- COLUMN 2: COVID-19 Impact Breakdown Chart ---
        with chart_col2:
            if not filtered_df.empty:
                if target_column in filtered_df.columns:
                    case_counts = filtered_df[target_column].value_counts().reset_index()
                    case_counts.columns = ['Status', 'Count']
                    
                    fig_covid = px.pie(
                        case_counts, 
                        names='Status', 
                        values='Count',
                        hole=0.4,
                        color_discrete_sequence=['#E11D48', '#10B981', '#F59E0B', '#6366F1'], 
                        title="COVID-19 Impact Breakdown"
                    )
                    
                    fig_covid.update_layout(
                        title_font=dict(size=24, family="Arial"),
                        margin=dict(t=50, b=10, l=10, r=10),
                        height=270,  # Exact height match for perfect alignment
                        showlegend=True,
                        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
                    )
                    
                    st.plotly_chart(fig_covid, use_container_width=True)
                else:
                    st.error(f"Column '{target_column}' missing from dataset.")
            
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # DASS-21 Reference Box
        with st.expander("ℹ️ How are DASS-21 Scores Calculated? (Scientific Reference)", expanded=False):
            st.markdown("""
            **DASS-21 (Depression Anxiety Stress Scale - 21 items)** is a quantitative measure of distress along three axes:
            
            *   **Depression Subscale (7 items)**: Assesses dysphoria, hopelessness, devaluation of life, self-deprecation, and lack of interest/initiation.
            *   **Anxiety Subscale (7 items)**: Assesses autonomic arousal, skeletal muscle effects, situational anxiety, and subjective experience of anxious affect.
            *   **Stress Subscale (7 items)**: Assesses chronic non-specific arousal, difficulty relaxing, nervous tension, irritability, and impatience.
                
            **Scoring**: Each item is scored $0-3$ (Likert Scale). The sum for each subscale is **multiplied by 2** (converting to DASS-42 equivalent) for final severity categorization:
            """)
            
            sc1, sc2, sc3 = st.columns(3)
            with sc1:
                st.markdown("""
                | Depression Level | Score Range |
                | :--- | :--- |
                | **Normal** | 0 - 9 |
                | **Mild** | 10 - 13 |
                | **Moderate** | 14 - 20 |
                | **Severe** | 21 - 27 |
                | **Extremely Severe** | 28+ |
                """)
            with sc2:
                st.markdown("""
                | Anxiety Level | Score Range |
                | :--- | :--- |
                | **Normal** | 0 - 7 |
                | **Mild** | 8 - 9 |
                | **Moderate** | 10 - 14 |
                | **Severe** | 15 - 19 |
                | **Extremely Severe** | 20+ |
                """)
            with sc3:
                st.markdown("""
                | Stress Level | Score Range |
                | :--- | :--- |
                | **Normal** | 0 - 14 |
                | **Mild** | 15 - 18 |
                | **Moderate** | 19 - 25 |
                | **Severe** | 26 - 33 |
                | **Extremely Severe** | 34+ |
                """)
                
        # Demographic Overview
        st.subheader("1. Demographics")
        demo_tab1, demo_tab2 = st.columns(2)
        
        with demo_tab1:
            fig_age = px.histogram(
                filtered_df, x="age", nbins=15,
                title="Respondent Age Distribution",
                labels={"age": "Age (Years)", "count": "Frequency"},
                color_discrete_sequence=["#6C5CE7"]
            )
            fig_age.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#E2E8F0", bargap=0.08)
            st.plotly_chart(fig_age, use_container_width=True)
            
        with demo_tab2:
            city_sex = filtered_df.groupby(['city', 'sex']).size().reset_index(name='count')
            fig_city = px.bar(
                city_sex, x="city", y="count", color="sex",
                title="Geographic and Gender Breakdown",
                labels={"city": "Metro City", "count": "Respondents", "sex": "Gender"},
                color_discrete_map={"Male": "#0984E3", "Female": "#FF7675"},
                barmode="group"
            )
            fig_city.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#E2E8F0")
            st.plotly_chart(fig_city, use_container_width=True)
            
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # ==================================================
        # SECTION 2: Pandemic Disruption: Phase 1 (T1) vs Phase 2 (T2)
        # ==================================================
        st.subheader("2. Pandemic Disruption: Phase 1 (T1) vs Phase 2 (T2)")
        disruptor_option = st.selectbox(
            "Choose Socioeconomic Factor for Temporal Comparison",
            ["Family Economically Affected", "Children's Education Affected", "Leisure Time Changes", "COVID-19 Cases in Family"],
            index=0
        )
        
        col_mapping = {
            "Family Economically Affected": ('family_economicaly_affected T1', 'family_economicaly_affected T2'),
            "Children's Education Affected": ('education_of_children T1', 'education_of_children T2'),
            "Leisure Time Changes": ('leisure_time T1', 'leisure_time T2'),
            "COVID-19 Cases in Family": ('covid_case T1', 'covid_case T2')
        }
        c_t1, c_t2 = col_mapping[disruptor_option]
        
        df_melt = filtered_df.melt(value_vars=[c_t1, c_t2], var_name="Phase", value_name="Status").dropna(subset=['Status'])
        df_melt['Phase'] = df_melt['Phase'].replace({c_t1: 'Phase 1 (T1)', c_t2: 'Phase 2 (T2)'})
        grp = df_melt.groupby(['Status', 'Phase']).size().reset_index(name='count')
        
        custom_order = {
            "Family Economically Affected": ['Reduced income due to poor business', 'Pay cut', 'Irregular pay', 'Lost job', 'Any other way', 'No / No Applicable'],
            "Children's Education Affected": ['Not affected', 'Somewhat affected', 'Severely affected'],
            "Leisure Time Changes": ['Increased', 'Decreased', 'No change'],
            "COVID-19 Cases in Family": ['No', 'Only Covid cases', 'Covid deaths']
        }
        if disruptor_option in custom_order:
            grp['Status'] = pd.Categorical(grp['Status'], categories=custom_order[disruptor_option], ordered=True)
            grp = grp.sort_values('Status')
            
        fig_temporal = px.bar(
            grp, x="Status", y="count", color="Phase", barmode="group",
            title=f"Shift in {disruptor_option} Across Phases",
            color_discrete_sequence=["#6C5CE7", "#00B894"],
            labels={"Status": "Severity / Category", "count": "Number of Households"}
        )
        fig_temporal.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#E2E8F0")
        st.plotly_chart(fig_temporal, use_container_width=True)
        
        if disruptor_option == "Family Economically Affected":
            eco_insight = "💡 Key Insight: While most families experienced no change in their overall status, families reporting 'Reduced income due to poor business' were the second largest group. Loss of jobs was less frequent but represents a high-impact shock."
            st.markdown(f'<div class="glass-card">{eco_insight}</div>', unsafe_allow_html=True)
        elif disruptor_option == "Children's Education Affected":
            edu_insight = "💡 Key Insight: Disruptions to children's education deteriorated significantly from Phase 1 to Phase 2, with 'Severely affected' reports increasing, reflecting the cumulative strain of prolonged virtual learning and school closures."
            st.markdown(f'<div class="glass-card">{edu_insight}</div>', unsafe_allow_html=True)

        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        # --------------------------------------------------
        # NEW SUBSECTION: Family Expenditure
        # --------------------------------------------------
        st.subheader("3. Monthly Expenditure Distribution Across Phases")

        if 'monthly_expenditure T1' in filtered_df.columns and 'monthly_expenditure T2' in filtered_df.columns:
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Melt and format the expenditure columns
            exp_melt = filtered_df.melt(
                value_vars=['monthly_expenditure T1', 'monthly_expenditure T2'], 
                var_name='Phase', 
                value_name='Expenditure'
            ).dropna(subset=['Expenditure'])
            
            exp_melt['Phase'] = exp_melt['Phase'].replace({
                'monthly_expenditure T1': 'Phase 1 (T1)', 
                'monthly_expenditure T2': 'Phase 2 (T2)'
            })
            
            # Create clean range buckets to prevent visual overcrowding
            bins = [0, 10000, 20000, 30000, 40000, 50000, 100000, 150000, 250000]
            exp_melt['Expenditure Range'] = pd.cut(exp_melt['Expenditure'], bins=bins).astype(str)
            
            # Group and count occurrences
            grp_exp = exp_melt.groupby(['Expenditure Range', 'Phase']).size().reset_index(name='count')
            
            # Plot using the exact same format rules
            fig_exp = px.bar(
                grp_exp, x="Expenditure Range", y="count", color="Phase", barmode="group",
                color_discrete_sequence=["#6C5CE7", "#00B894"],
                labels={"Expenditure Range": "Expenditure Range", "count": "Number of Households"}
            )
            fig_exp.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#E2E8F0")
            st.plotly_chart(fig_exp, use_container_width=True)
            st.markdown(
                            '<div class="glass-card">💡 Key Insight: It is possible that families reduced their expenditure due to fear of being affected by COVID-19 again. Statistical evidence suggests that most families may have adopted greater saving behaviour, which is consistent with our finding that a higher proportion of households fall within the lower and medium expenditure ranges. Rate of expenditure did not made a huge change in the families with comparitively higher income.</div>', 
                            unsafe_allow_html=True
                        )
            
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # Core Correlation Playground
        st.subheader("4. Core Correlation: Socioeconomic Impacts on DASS-21 Levels")
        phase_selection = st.radio("Select Pandemic Phase for Severity Profile", ["Phase 1 (T1) - Aug/Sept 2020", "Phase 2 (T2) - July/Aug 2021"], horizontal=True)
        suffix = "T1" if "Phase 1" in phase_selection else "T2"
        
        mh_dimension = st.selectbox("Select Psychological Axis", ["Depression", "Anxiety", "Stress"]).lower()
        mh_level_col = f"{mh_dimension}_level {suffix}"
        
        influence_factor = st.selectbox("Select Explanatory Factor", ["Economic Condition", "Children's Education Impact", "COVID-19 Case Severity", "Chronic Illness Pre-existence"], key="influence")
        factor_col_map = {
            "Economic Condition": f"family_economicaly_affected {suffix}",
            "Children's Education Impact": f"education_of_children {suffix}",
            "COVID-19 Case Severity": f"covid_case {suffix}",
            "Chronic Illness Pre-existence": f"fam_mem_suff_hyp-tens/bp/dbts/canc {suffix}"
        }
        factor_col = factor_col_map[influence_factor]
        
        sub_df = filtered_df[[mh_level_col, factor_col]].dropna()
        crosstab = pd.crosstab(sub_df[factor_col], sub_df[mh_level_col], normalize='index') * 100
        crosstab = crosstab.reset_index()
        
        severity_order = ['Normal', 'Mild', 'Moderate', 'Severe', 'Extremely severe']
        available_severity = [col for col in severity_order if col in crosstab.columns]
        crosstab_melt = crosstab.melt(id_vars=factor_col, value_vars=available_severity, var_name="Severity Level", value_name="Percentage")
        
        dass_palette = {'Normal': '#00B894', 'Mild': '#0984E3', 'Moderate': '#FDCB6E', 'Severe': '#E17055', 'Extremely severe': '#D63031'}
        fig_impact = px.bar(
            crosstab_melt, x=factor_col, y="Percentage", color="Severity Level",
            title=f"Psychological Impact ({mh_dimension.capitalize()}) vs {influence_factor} - {phase_selection}",
            labels={"Percentage": "Percentage of Respondents (%)", factor_col: influence_factor},
            color_discrete_map=dass_palette, category_orders={"Severity Level": severity_order}
        )
        fig_impact.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)", font_color="#E2E8F0", legend_title_text="DASS Severity")
        st.plotly_chart(fig_impact, use_container_width=True)
        
        if influence_factor == "Economic Condition" and mh_dimension == "depression":
            obs = "📉 Observation: Extremely severe depression rates are exceptionally high among families reporting 'Reduced income due to poor business' or 'Pay cut'. Conversely, respondents from families that were 'not affected economically' show predominant 'Normal' depression ratings across both phases."
            st.markdown(f'<div class="glass-card">{obs}</div>', unsafe_allow_html=True)
        elif influence_factor == "Children's Education Impact":
            obs = "📉 Observation: There is a clear dose-response relationship: as children's education disruption increases from 'Not affected' to 'Severely affected', the percentage of parents experiencing 'Severe' or 'Extremely severe' mental distress increases significantly."
            st.markdown(f'<div class="glass-card">{obs}</div>', unsafe_allow_html=True)
