import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from scipy.stats import spearmanr, chi2_contingency
from components.cards import draw_glass_card

def render_statistical_page(df):
    """
    Renders the correlation heatmaps and live statistical tests page.
    """
    st.markdown(
    '<h1 class="main-title">Rigorous statistical analysis of DASS-21 correlations and hypothesis testing</h1>', 
    unsafe_allow_html=True)

    st.markdown(
    '<h4 class="subtitle">Applying mathematical rigour to survey data allows us to confirm whether observed patterns are statistically significant or merely random fluctuations.</h4>', 
    unsafe_allow_html=True)
    
    # Tabs for different analyses
    tab1, tab2 = st.tabs(["Spearman Rank Correlation", "Chi-Square Test of Independence"])
    
    # --------------------------------------------------
    # TAB 1: SPEARMAN CORRELATION
    # --------------------------------------------------
    with tab1:
        st.subheader("Correlation Heatmap (Depression, Anxiety, Stress)")
        
        phase_sel = st.radio(
            "Select Phase for Correlation Heatmap",
            ["Phase 1 (T1) - 2020", "Phase 2 (T2) - 2021"],
            key="corr_phase"
        )
        
        sfx = "T1" if "Phase 1" in phase_sel else "T2"
        
        # Select data columns
        corr_cols = [f'depression_num {sfx}', f'anxiety_num {sfx}', f'stress_num {sfx}']
        labels_map = {
            f'depression_num {sfx}': 'Depression',
            f'anxiety_num {sfx}': 'Anxiety',
            f'stress_num {sfx}': 'Stress'
        }
        
        # Calculate Spearman correlation
        sub_df = df[corr_cols].dropna()
        corr_matrix, p_matrix = spearmanr(sub_df)
        
        # Convert to DataFrame
        corr_df = pd.DataFrame(corr_matrix, 
            index=['Depression', 'Anxiety', 'Stress'], 
            columns=['Depression', 'Anxiety', 'Stress']
            )
        
        fig_heat = px.imshow(
            corr_df,
            text_auto=".3f",
            aspect="auto",
            color_continuous_scale="RdBu_r",
            range_color=[-1, 1],
            title=f"Spearman Rank Correlation Heatmap - {phase_sel}"
        )
        
        fig_heat.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font_color="#E2E8F0"
        )
        
        st.plotly_chart(fig_heat, width="stretch")
        
        # Insight Text
        if sfx == "T1":
            insight_html = """
            <p>In Phase 1, we observe strong positive Spearman correlations:
            <ul>
                <li><b>Depression ↔ Stress:</b> 0.824</li>
                <li><b>Stress ↔ Anxiety:</b> 0.820</li>
                <li><b>Depression ↔ Anxiety:</b> 0.793</li>
            </ul>
            This suggests that during the initial outbreak and lockdown phase, symptoms of depression, 
            anxiety, and stress were highly concurrent—elevated scores in one domain were strongly associated 
            with elevations in the others.</p>
            """
        else:
            insight_html = """
            <p>In Phase 2, the correlations remain strongly positive, although slightly lower:
            <ul>
                <li><b>Depression ↔ Stress:</b> 0.771</li>
                <li><b>Stress ↔ Anxiety:</b> 0.763</li>
                <li><b>Depression ↔ Anxiety:</b> 0.730</li>
            </ul>
            This marginal decrease suggests that over time, the specific profiles of psychological distress 
            began to differentiate slightly as individuals adapted or faced distinct stressors.</p>
            """
        draw_glass_card(f"Interpretation: {phase_sel}", insight_html)
        
    # --------------------------------------------------
    # TAB 2: CHI-SQUARE TEST
    # --------------------------------------------------
    with tab2:
        st.subheader("Chi-Square Test of Independence")
        st.markdown("""
        The Chi-Square test determines whether there is a statistically significant association between 
        a chosen socioeconomic factor and a DASS-21 severity level. 
        
        * **Null Hypothesis ($H_0$):** The socioeconomic factor and the DASS-21 severity level are independent (no relationship).
        * **Alternative Hypothesis ($H_1$):** The socioeconomic factor and the DASS-21 severity level are dependent (statistically significant relationship).
        """)
        
        phase_chi = st.selectbox(
            "Select Phase for Test",
            ["Phase 1 (T1) - 2020", "Phase 2 (T2) - 2021"],
            key="chi_phase"
        )
        sfx_chi = "T1" if "Phase 1" in phase_chi else "T2"
        
        # 1. Map beautiful UI names to your actual base column formats
        # NOTE: Keeping the exact spelling/typos from your columns so pandas doesn't throw a KeyError
        factor_mapping = {
            "Family Economically Affected": "family_economicaly_affected",
            "Education of Children": "education_of_children",
            "Covid Case in Family": "covid_case",
            "Family Members with Chronic Illness (Hypertension/BP/Diabetes/Cancer)": "fam_mem_suff_hyp-tens/bp/dbts/canc"
        }
        
        outcome_mapping = {
            "Depression Severity Level": "depression_level",
            "Anxiety Severity Level": "anxiety_level",
            "Stress Severity Level": "stress_level"
        }
        
        # 2. Feed the dictionary keys into the selectboxes
        chosen_factor_label = st.selectbox(
            "Select Independent Variable (Socioeconomic Factor)",
            options=list(factor_mapping.keys()),
            key="chi_factor"
        )
        
        chosen_outcome_label = st.selectbox(
            "Select Dependent Variable (Psychological Outcome)",
            options=list(outcome_mapping.keys()),
            key="chi_outcome"
        )
        
        # 3. Retrieve the backend column values based on user choice
        col_factor = factor_mapping[chosen_factor_label]
        col_outcome = outcome_mapping[chosen_outcome_label]
        
        # 4. Construct exact DataFrame column signatures
        var_x = f"{col_factor} {sfx_chi}"
        var_y = f"{col_outcome} {sfx_chi}"
        
        # Filter and drop NaNs
        chi_data = df[[var_x, var_y]].dropna()
        
        # Build Contingency Table with clean UI labels instead of raw column strings
        contingency_table = pd.crosstab(
            chi_data[var_x], 
            chi_data[var_y],
            rownames=[f"{chosen_factor_label} ({sfx_chi})"],
            colnames=[f"{chosen_outcome_label} ({sfx_chi})"]
        )
        st.write("#### Observed Contingency Table (Counts)")
        st.dataframe(contingency_table, width="stretch")
        
        # Run test
        try:
            chi2, p_val, dof, expected = chi2_contingency(contingency_table)
            
            # Display results in columns
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Chi-Square Statistic (χ²)", f"{chi2:.4f}")
            with c2:
                st.metric("Degrees of Freedom (dof)", dof)
            with c3:
                # Format p-value nicely
                p_text = f"{p_val:.4e}" if p_val < 0.001 else f"{p_val:.4f}"
                st.metric("p-value", p_text)
                
            # Interpretation
            is_significant = p_val < 0.05
            
            if is_significant:
                result_html = f"""
                <span style="color: #00B894; font-weight: bold; font-size: 1.1rem;">Result: Reject Null Hypothesis (H₀)</span><br>
                <p style="margin-top: 0.5rem; color: #CBD5E1; margin-bottom: 0;">
                    The p-value of <b>{p_text}</b> is less than the significance level α = 0.05. 
                    Therefore, we have strong statistical evidence to conclude that <b>{chosen_factor_label}</b> 
                    and <b>{chosen_outcome_label}</b> are 
                    <span style="color: #A8A5FF; font-weight: 600;">statistically dependent</span> in {phase_chi}.
                </p>
                """
            else:
                result_html = f"""
                <span style="color: #FF7675; font-weight: bold; font-size: 1.1rem;">Result: Fail to Reject Null Hypothesis (H₀)</span><br>
                <p style="margin-top: 0.5rem; color: #CBD5E1; margin-bottom: 0;">
                    The p-value of <b>{p_text}</b> is greater than the significance level α = 0.05. 
                    There is insufficient evidence to conclude that <b>{chosen_factor_label}</b> 
                    and <b>{chosen_outcome_label}</b> are dependently associated. 
                    They appear to be statistically independent.
                </p>
                """
            draw_glass_card("Statistical Interpretation", result_html)
            
        except Exception as e:
            st.error(f"Error performing Chi-Square Test: {e}. Check if data is sufficient.")
