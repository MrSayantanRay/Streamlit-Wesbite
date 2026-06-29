import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder, StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from components.cards import draw_glass_card
from utils.data_loader import load_clean_data

# Define the 21 survey items in standard order
ordinal_cols = [
    'finding_hard_to_wind_down',
    'dry_mouth',
    'not_experiencing_+ve_felling',
    'breathing_difficulty',
    'difficulty_in_initiative_to_do_things',
    'overreaction_in_situations',
    'experienced_trembling',
    'felt_used_lotsof_nrvs_engy',
    'panic_in_situations&make_fool_of_own',
    'felt_had_nothing_to_look_forward',
    'getting_agitated',
    'difficulty_in_relax',
    'felt_downhearted_and_blue',
    'intolerant_of_anything_gotin_my_way',
    'felt_like_panicking',
    'unable_to_become_enthusiastic',
    'felt_unworthy_as_a_person',
    'felt_being_touchy',
    'abnormal_heart_rate',
    'felt_scared_without_reason',
    'felt_life_is_meaningless'
]

# Map items to friendly DASS-21 question text
dass_questions = {
    'finding_hard_to_wind_down': "I found it hard to wind down",
    'dry_mouth': "I was aware of dryness of my mouth",
    'not_experiencing_+ve_felling': "I couldn't seem to experience any positive feeling at all",
    'breathing_difficulty': "I experienced breathing difficulty (e.g., excessively rapid breathing, breathlessness in the absence of physical exertion)",
    'difficulty_in_initiative_to_do_things': "I found it difficult to work up the initiative to do things",
    'overreaction_in_situations': "I tended to over-react to situations",
    'experienced_trembling': "I experienced trembling (e.g., in the hands)",
    'felt_used_lotsof_nrvs_engy': "I felt that I was using a lot of nervous energy",
    'panic_in_situations&make_fool_of_own': "I was worried about situations in which I might panic and make a fool of myself",
    'felt_had_nothing_to_look_forward': "I felt that I had nothing to look forward to",
    'getting_agitated': "I found myself getting agitated",
    'difficulty_in_relax': "I found it difficult to relax",
    'felt_downhearted_and_blue': "I felt sad, emotionally low, or discouraged",
    'intolerant_of_anything_gotin_my_way': "I was intolerant of anything that kept me from getting on with what I was doing",
    'felt_like_panicking': "I felt I was close to panic",
    'unable_to_become_enthusiastic': "I was unable to become enthusiastic about anything",
    'felt_unworthy_as_a_person': "I felt I wasn't worth much as a person",
    'felt_being_touchy': "I felt that I was rather touchy",
    'abnormal_heart_rate': "I was aware of the action of my heart in the absence of physical exertion (e.g., sense of heart rate increase, heart skipping a beat)",
    'felt_scared_without_reason': "I felt scared without any good reason",
    'felt_life_is_meaningless': "I felt that life was meaningless"
}

# Map subscale items
depression_items = [
    'not_experiencing_+ve_felling',
    'difficulty_in_initiative_to_do_things',
    'felt_had_nothing_to_look_forward',
    'felt_downhearted_and_blue',
    'unable_to_become_enthusiastic',
    'felt_unworthy_as_a_person',
    'felt_life_is_meaningless'
]
anxiety_items = [
    'dry_mouth',
    'breathing_difficulty',
    'experienced_trembling',
    'panic_in_situations&make_fool_of_own',
    'felt_like_panicking',
    'abnormal_heart_rate',
    'felt_scared_without_reason'
]
stress_items = [
    'finding_hard_to_wind_down',
    'overreaction_in_situations',
    'felt_used_lotsof_nrvs_engy',
    'getting_agitated',
    'difficulty_in_relax',
    'intolerant_of_anything_gotin_my_way',
    'felt_being_touchy'
]

# Options list
options = [
        "Did not apply to me at all",
        "Applied to me to some degree, or some of the time",
        "Applied to me to a considerable degree, or a good part of time",
        "Applied to me very much, or most of the time"
    ]

categories = [options] * len(ordinal_cols)

# Static pre-computed metrics to show validation performance
validation_metrics = {
    'depression': {'accuracy': 0.9132, 'cv_accuracy': 0.9233, 'f1(weighted)': 0.9157, 'cv_f1(weighted)': 0.9258},
    'anxiety': {'accuracy': 0.9438, 'cv_accuracy': 0.9207, 'f1(weighted)': 0.9471, 'cv_f1(weighted)': 0.9241},
    'stress': {'accuracy': 0.9489, 'cv_accuracy': 0.9271, 'f1(weighted)': 0.9517, 'cv_f1(weighted)': 0.9296}
}


@st.cache_resource
def train_dass_pipelines():

    df = load_clean_data()

    # Split columns based on suffix
    t1_cols = [
        c for c in df.columns
        if c.endswith(' T1') or c.endswith('_T1')
    ]

    common_cols = [
        c for c in df.columns
        if not (c.endswith(' T1') or c.endswith('_T1') or c.endswith(' T2')or c.endswith('_T2'))
    ]

    # Create Phase 1 dataframe FIRST
    mh_T1 = df[common_cols + t1_cols].copy()

    # Remove suffix
    new_cols = []

    for c in mh_T1.columns:
        if c.endswith(' T1') or c.endswith('_T1'):
            new_cols.append(c[:-3])
        else:
            new_cols.append(c)

    mh_T1.columns = new_cols

    # Normalize category labels
    category_mapping = {
        "Applied to me to some degree of some of the time":
            "Applied to me to some degree, or some of the time",

        "Applied to me to a considerable time or good part of time":
            "Applied to me to a considerable degree, or a good part of time",

        "Applied to me very much or most of the time":
            "Applied to me very much, or most of the time"
    }

    mh_T1[ordinal_cols] = (
        mh_T1[ordinal_cols]
        .replace(category_mapping)
    )


    print(
        mh_T1[ordinal_cols]
        .stack()
        .unique()
    )


    preprocessor = ColumnTransformer(
        transformers=[
            (
                'ordinal',
                OrdinalEncoder(categories=categories),
                ordinal_cols
            )
        ],
        remainder='drop'
    )

    pipelines = {}

    for target in [
        'depression_level',
        'anxiety_level',
        'stress_level'
    ]:

        pipeline = Pipeline([
            ('preprocess', preprocessor),
            ('scale', StandardScaler()),
            (
                'model',
                LogisticRegression(
                    solver='newton-cholesky',
                    max_iter=3000,
                    class_weight='balanced',
                    random_state=42
                )
            )
        ])

        X = mh_T1[ordinal_cols]
        y = mh_T1[target]
        
        pipeline.fit(X, y)

        pipelines[target] = pipeline

    return pipelines

def calculate_dass_severity(score, scale_type):
    """
    Returns clinical severity category based on standard DASS-21 score ranges.
    """
    if scale_type == 'depression':
        if score <= 9: return 'Normal'
        elif score <= 13: return 'Mild'
        elif score <= 20: return 'Moderate'
        elif score <= 27: return 'Severe'
        else: return 'Extremely severe'
    elif scale_type == 'anxiety':
        if score <= 7: return 'Normal'
        elif score <= 9: return 'Mild'
        elif score <= 14: return 'Moderate'
        elif score <= 19: return 'Severe'
        else: return 'Extremely severe'
    elif scale_type == 'stress':
        if score <= 14: return 'Normal'
        elif score <= 18: return 'Mild'
        elif score <= 25: return 'Moderate'
        elif score <= 33: return 'Severe'
        else: return 'Extremely severe'
    return 'Normal'

def render_predictor_page():
    """
    Renders the DASS-21 Predictor page.
    """
    st.markdown('<h1 class="main-title">DASS-21 Diagnostic Playground</h1>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Calculate DASS-21 scores and check the predictions of a Logistic Regression model trained on survey data.</div>', unsafe_allow_html=True)
    
    # Train/Retrieve models
    try:
        pipelines = train_dass_pipelines()
    except Exception as e:
        st.error(f"Error initializing diagnostic models: {e}")
        return
        
    st.markdown("""
    This interactive diagnostic tool evaluates psychological distress levels along three distinct axes. 
    Complete the 21-item questionnaire by selecting how much each statement applied to you **over the past week**.
    """)
    
    # Questionnaire Form
    st.markdown("### DASS-21 Questionnaire")
    
    # Tabs for the three scales to reduce layout clutter
    tab_dep, tab_anx, tab_str = st.tabs(["Depression Symptoms", "Anxiety Symptoms", "Stress Symptoms"])
    
    user_inputs = {}
    
    with tab_dep:
        st.info("💡 Depression scale assesses dysphoria, hopelessness, devaluation of life, and self-deprecation.")
        for item in depression_items:
            friendly_text = dass_questions[item]
            user_inputs[item] = st.selectbox(friendly_text, options, index=0, key=f"q_{item}")
            
    with tab_anx:
        st.info("💡 Anxiety scale assesses autonomic arousal, skeletal muscle effects, situational anxiety, and subjective anxious affect.")
        for item in anxiety_items:
            friendly_text = dass_questions[item]
            user_inputs[item] = st.selectbox(friendly_text, options, index=0, key=f"q_{item}")
            
    with tab_str:
        st.info("💡 Stress scale assesses chronic non-specific arousal, nervous tension, irritability, and impatience.")
        for item in stress_items:
            friendly_text = dass_questions[item]
            user_inputs[item] = st.selectbox(friendly_text, options, index=0, key=f"q_{item}")
            
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
    
    # Submit Button
    if st.button("Generate Diagnostic Report & Run ML Model", type="primary", use_container_width=True):
        # Convert user options to numerical scores (0 to 3)
        option_scores = {
            options[0]: 0,
            options[1]: 1,
            options[2]: 2,
            options[3]: 3
        }
        
        # Calculate raw scores
        dep_raw = sum(option_scores[user_inputs[item]] for item in depression_items)
        anx_raw = sum(option_scores[user_inputs[item]] for item in anxiety_items)
        str_raw = sum(option_scores[user_inputs[item]] for item in stress_items)
        
        # Scale to DASS-42 equivalent
        dep_score = dep_raw * 2
        anx_score = anx_raw * 2
        str_score = str_raw * 2
        
        # Clinical Categories
        dep_clinical = calculate_dass_severity(dep_score, 'depression')
        anx_clinical = calculate_dass_severity(anx_score, 'anxiety')
        str_clinical = calculate_dass_severity(str_score, 'stress')
        
        # Machine Learning Predictions
        # Build input dataframe with same shape as training features
        input_df = pd.DataFrame([user_inputs])
        
        dep_pred = pipelines['depression_level'].predict(input_df)[0]
        dep_prob = pipelines['depression_level'].predict_proba(input_df)[0]
        dep_conf = dep_prob.max() * 100
        
        anx_pred = pipelines['anxiety_level'].predict(input_df)[0]
        anx_prob = pipelines['anxiety_level'].predict_proba(input_df)[0]
        anx_conf = anx_prob.max() * 100
        
        str_pred = pipelines['stress_level'].predict(input_df)[0]
        str_prob = pipelines['stress_level'].predict_proba(input_df)[0]
        str_conf = str_prob.max() * 100

        
        # Display Results
        st.markdown("### Diagnostic & Predictive Report")
        
        res_col1, res_col2, res_col3 = st.columns(3)
        
        # Severity color maps for premium text highlighting
        severity_colors = {
            'Normal': '#00B894',
            'Mild': '#0984E3',
            'Moderate': '#FDCB6E',
            'Severe': '#E17055',
            'Extremely severe': '#D63031'
        }
        
        with res_col1:
            color_c = severity_colors.get(dep_clinical, '#FFFFFF')
            color_p = severity_colors.get(dep_pred, '#FFFFFF')
            match_status = '<span style="color:#00B894; font-weight:700;">CONSISTENT</span>' if dep_clinical == dep_pred else '<span style="color:#FF7675; font-weight:700;">DIFFERENT</span>'            
            dep_html = f"""
            <div style="line-height:1.8;">
                <div style="margin-bottom:0.75rem;">
                    <b style="color:#A8A5FF;">DASS-21 Score:</b> <span style="font-size:1.1rem; font-weight:700; color:#FFFFFF;">{dep_score} / 42</span>
                </div>
                <div style="margin-bottom:0.75rem;">
                    <b style="color:#A8A5FF;">Clinical Category:</b> <span style="font-size:1.1rem; font-weight:700; color:{color_c};">{dep_clinical}</span>
                </div>

                <div style="margin-bottom:0.75rem;">
                    <b style="color:#A8A5FF;">ML Prediction:</b>
                    <span style="font-size:1.1rem; font-weight:700; color:{color_p};">
                        {dep_pred}
                    </span>
                </div>

                <div style="margin-bottom:0.75rem;">
                    <b style="color:#A8A5FF;">Confidence:</b>
                    <span style="font-size:1.1rem;font-weight:700;color:#FFFFFF;">
                        {dep_conf:.1f}%
                    </span>
                </div>

                <div>
                    <b style="color:#A8A5FF;">Status:</b> {match_status}
                </div>
            </div>
            """
            draw_glass_card("Depression Profile", dep_html)
            
        with res_col2:
            color_c = severity_colors.get(anx_clinical, '#FFFFFF')
            color_p = severity_colors.get(anx_pred, '#FFFFFF')
            match_status = '<span style="color:#00B894; font-weight:700;">CONSISTENT</span>' if anx_clinical == anx_pred else '<span style="color:#FF7675; font-weight:700;">DIFFERENT</span>'
            
            anx_html = f"""
            <div style="line-height:1.8;">
                <div style="margin-bottom:0.75rem;">
                    <b style="color:#A8A5FF;">DASS-21 Score:</b> <span style="font-size:1.1rem; font-weight:700; color:#FFFFFF;">{anx_score} / 42</span>
                </div>
                <div style="margin-bottom:0.75rem;">
                    <b style="color:#A8A5FF;">Clinical Category:</b> <span style="font-size:1.1rem; font-weight:700; color:{color_c};">{anx_clinical}</span>
                </div>

                <div style="margin-bottom:0.75rem;">
                    <b style="color:#A8A5FF;">ML Prediction:</b>
                    <span style="font-size:1.1rem; font-weight:700; color:{color_p};">{anx_pred}
                    </span>
                </div>

                <div style="margin-bottom:0.75rem;">
                    <b style="color:#A8A5FF;">Confidence:</b>

                    <span style="font-size:1.1rem;font-weight:700;color:#FFFFFF;">
                        {anx_conf:.1f}%
                    </span>
                </div>

                <div>
                    <b style="color:#A8A5FF;">Status:</b> {match_status}
                </div>
            </div>
            """
            draw_glass_card("Anxiety Profile", anx_html)
            
        with res_col3:
            color_c = severity_colors.get(str_clinical, '#FFFFFF')
            color_p = severity_colors.get(str_pred, '#FFFFFF')
            match_status = '<span style="color:#00B894; font-weight:700;">CONSISTENT</span>' if str_clinical == str_pred else '<span style="color:#FF7675; font-weight:700;">DIFFERENT</span>'
            
            str_html = f"""
            <div style="line-height:1.8;">
                <div style="margin-bottom:0.75rem;">
                    <b style="color:#A8A5FF;">DASS-21 Score:</b> <span style="font-size:1.1rem; font-weight:700; color:#FFFFFF;">{str_score} / 42</span>
                </div>
                <div style="margin-bottom:0.75rem;">
                    <b style="color:#A8A5FF;">Clinical Category:</b> <span style="font-size:1.1rem; font-weight:700; color:{color_c};">{str_clinical}</span>
                </div>

                <div style="margin-bottom:0.75rem;">
                    <b style="color:#A8A5FF;">ML Prediction:</b>
                    <span style="font-size:1.1rem; font-weight:700; color:{color_p};">
                        {str_pred}
                    </span>
                </div>

                <div style="margin-bottom:0.75rem;">
                    <b style="color:#A8A5FF;">Confidence:</b>
                    <span style="font-size:1.1rem;font-weight:700;color:#FFFFFF;">
                        {str_conf:.1f}%
                    </span>
                </div>

                <div>
                    <b style="color:#A8A5FF;">Status:</b> {match_status}
                </div>
            </div>
            """
            draw_glass_card("Stress Profile", str_html)
            
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        st.info(
            """
            DASS-21 severity categories are calculated using the official DASS-21 scoring framework.

            Machine learning predictions are shown as an additional predictive layer trained on historical survey responses and should not be interpreted as an independent clinical assessment.
            """)
        
        # Section: Explainable AI - Coefficients Visualization
        st.subheader("Explainable AI: Model Coefficients (Feature Weights)")
        st.markdown("""
        The charts below show the logistic regression coefficients associated
        with the predicted class. Larger absolute values indicate that the
        question was more influential for that class in the trained model.
        These coefficients describe global model behavior and do not represent
        individual-level causal effects.
        """)
        
        exp_col1, exp_col2, exp_col3 = st.columns(3)
        
        with exp_col1:
            # Depression Coefficients Chart
            model_dep = pipelines['depression_level'].named_steps['model']

            dep_class_idx = (
                list(model_dep.classes_)
                .index(dep_pred)
            )

            # Get transformed feature names
            feature_names = (
                pipelines['depression_level']
                .named_steps['preprocess']
                .get_feature_names_out()
            )

            # Create named coefficient series
            dep_coefs = pd.Series(
                model_dep.coef_[dep_class_idx],
                index=feature_names
            )

            # Extract only depression-related items
            dep_item_coefs = [
                dep_coefs[f'ordinal__{item}']
                for item in depression_items
            ]

            # Human-readable labels
            friendly_dep_labels = [
                dass_questions[item]
                for item in depression_items
            ]

            # Build dataframe
            df_dep_coef = pd.DataFrame({
                'Question': friendly_dep_labels,
                'Weight': dep_item_coefs
            })

            df_dep_coef['Abs_Weight'] = (
                df_dep_coef['Weight']
                .abs()
            )

            df_dep_coef = (
                df_dep_coef
                .sort_values(
                    by='Abs_Weight',
                    ascending=True
                )
            )

            fig_dep_c = px.bar(
                df_dep_coef,
                x='Weight',
                y='Question',
                orientation='h',
                title=f"Most Influential Depression Items ({dep_pred})",
                color='Weight',
                color_continuous_scale='RdBu_r'
            )

            fig_dep_c.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#E2E8F0",
                coloraxis_showscale=False,
                height=350,
                margin=dict(
                    l=10,
                    r=10,
                    t=40,
                    b=10
                )
            )

            fig_dep_c.update_yaxes(
                showticklabels=False,
                title_text=''
            )

            fig_dep_c.update_xaxes(
                title_text='Standardized Weight'
            )

            st.plotly_chart(
                fig_dep_c,
                width="stretch"
            )
            
        with exp_col2:
            # Anxiety Coefficients Chart
            model_anx = pipelines['anxiety_level'].named_steps['model']
            anx_class_idx = list(model_anx.classes_).index(anx_pred)

            # Get transformed feature names from anxiety pipeline
            feature_names = (
                pipelines['anxiety_level']
                .named_steps['preprocess']
                .get_feature_names_out()
            )

            # Create coefficient series
            anx_coefs = pd.Series(
                model_anx.coef_[anx_class_idx],
                index=feature_names
            )

            # Extract only anxiety-related item coefficients
            anx_item_coefs = [
                anx_coefs[f'ordinal__{item}']
                for item in anxiety_items
            ]

            # Human-readable labels
            friendly_anx_labels = [
                dass_questions[item]
                for item in anxiety_items
            ]

            # Build dataframe
            df_anx_coef = pd.DataFrame({
                'Question': friendly_anx_labels,
                'Weight': anx_item_coefs
            })

            df_anx_coef['Abs_Weight'] = (
                df_anx_coef['Weight']
                .abs()
            )

            df_anx_coef = (
                df_anx_coef
                .sort_values(
                    by='Abs_Weight',
                    ascending=True
                )
            )
            
            fig_anx_c = px.bar(
                df_anx_coef, x='Weight', y='Question', orientation='h',
                title=f"Anxiety scale items for class: '{anx_pred}'",
                color='Weight', color_continuous_scale="RdBu_r"
            )
            fig_anx_c.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#E2E8F0",
                coloraxis_showscale=False,
                height=350,
                margin=dict(l=10, r=10, t=40, b=10)
            )
            fig_anx_c.update_yaxes(showticklabels=False, title_text='')
            fig_anx_c.update_xaxes(title_text='Standardized Weight')
            st.plotly_chart(fig_anx_c, width="stretch")
            
        with exp_col3:
            # Stress Coefficients Chart
            model_str = pipelines['stress_level'].named_steps['model']
            str_class_idx = list(model_str.classes_).index(str_pred)

            # Get transformed feature names from stress pipeline
            feature_names = (
                pipelines['stress_level']
                .named_steps['preprocess']
                .get_feature_names_out()
            )

            # Create coefficient series with feature names
            str_coefs = pd.Series(
                model_str.coef_[str_class_idx],
                index=feature_names
            )

            # Extract only stress-related item coefficients
            str_item_coefs = [
                str_coefs[f'ordinal__{item}']
                for item in stress_items
            ]

            # Human-readable labels
            friendly_str_labels = [
                dass_questions[item]
                for item in stress_items
            ]

            # Build dataframe for plotting
            df_str_coef = pd.DataFrame({
                'Question': friendly_str_labels,
                'Weight': str_item_coefs
            })

            df_str_coef['Abs_Weight'] = df_str_coef['Weight'].abs()

            df_str_coef = (
                df_str_coef
                .sort_values(
                    by='Abs_Weight',
                    ascending=True
                )
            )
            
            fig_str_c = px.bar(
                df_str_coef, x='Weight', y='Question', orientation='h',
                title=f"Stress scale items for class: '{str_pred}'",
                color='Weight', color_continuous_scale="RdBu_r"
            )
            fig_str_c.update_layout(
                plot_bgcolor="rgba(0,0,0,0)",
                paper_bgcolor="rgba(0,0,0,0)",
                font_color="#E2E8F0",
                coloraxis_showscale=False,
                height=350,
                margin=dict(l=10, r=10, t=40, b=10)
            )
            fig_str_c.update_yaxes(showticklabels=False, title_text='')
            fig_str_c.update_xaxes(title_text='Standardized Weight')

            st.plotly_chart(fig_str_c, width="stretch")

        st.markdown(
            "*Hover over bars to see the question and coefficient value.*"
        )
            
        st.markdown('<div class="divider"></div>', unsafe_allow_html=True)
        
        # Section: Model Performance Details
        st.subheader("Model Rigour & Validation Metrics")
        st.markdown("""
        Below are the validation metrics calculated on the Phase 1 test subset using 15-fold Stratified Cross-Validation.
        """)
        
        mc1, mc2, mc3 = st.columns(3)
        with mc1:
            st.metric("Depression Model Accuracy", f"{validation_metrics['depression']['accuracy']*100:.2f}%", 
                      delta=f"CV: {validation_metrics['depression']['cv_accuracy']*100:.2f}%", delta_color="off")
        with mc2:
            st.metric("Anxiety Model Accuracy", f"{validation_metrics['anxiety']['accuracy']*100:.2f}%", 
                      delta=f"CV: {validation_metrics['anxiety']['cv_accuracy']*100:.2f}%", delta_color="off")
        with mc3:
            st.metric("Stress Model Accuracy", f"{validation_metrics['stress']['accuracy']*100:.2f}%", 
                      delta=f"CV: {validation_metrics['stress']['cv_accuracy']*100:.2f}%", delta_color="off")
