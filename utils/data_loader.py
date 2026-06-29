import pandas as pd
import numpy as np
import streamlit as st
import os

@st.cache_data
def load_clean_data():
    """
    Loads and caches the cleaned DASS-21 mental health dataset.
    Performs basic transformations like age binning.
    """
    # Use relative path so that it runs locally and on Streamlit Cloud
    filename = "03_adult mental health in indian metro cities 2001-2021 (cleaned).csv"
    
    if not os.path.exists(filename):
        # Fallback to absolute path just in case
        filename = r"c:\Users\Mr. Sayantan\Documents\DS\Streamlit Portfolio\03_adult mental health in indian metro cities 2001-2021 (cleaned).csv"
        
    df = pd.read_csv(filename)
    
    # Pre-calculate age groups to align with notebook analysis
    bins = [20, 30, 40, 50, 60]
    labels = ['20-30', '30-40', '40-50', '50-60']
    df['age_group'] = pd.cut(df['age'], bins=bins, labels=labels)
    
    # Add numerical mapping for DASS-21 severity levels for correlation heatmaps
    severity_map = {
        'Normal': 0, 
        'Mild': 1, 
        'Moderate': 2, 
        'Severe': 3, 
        'Extremely severe': 4
    }
    
    # Map for Phase 1
    df['depression_num T1'] = df['depression_level T1'].map(severity_map)
    df['anxiety_num T1'] = df['anxiety_level T1'].map(severity_map)
    df['stress_num T1'] = df['stress_level T1'].map(severity_map)
    
    # Map for Phase 2
    df['depression_num T2'] = df['depression_level T2'].map(severity_map)
    df['anxiety_num T2'] = df['anxiety_level T2'].map(severity_map)
    df['stress_num T2'] = df['stress_level T2'].map(severity_map)
    
    return df

def get_dass_info():
    """
    Returns standard information about how DASS-21 is calculated and interpreted.
    """
    return {
        "description": (
            "The DASS-21 is a 21-item self-report questionnaire designed to measure the "
            "severity of core symptoms of Depression, Anxiety, and Stress. It is a shortened "
            "version of Lovibond & Lovibond's 42-item scale."
        ),
        "scoring": (
            "Each of the three subscales (Depression, Anxiety, Stress) contains 7 items. "
            "Respondents rate items from 0 ('Did not apply to me at all') to 3 ('Applied to me "
            "very much or most of the time'). The raw scores are summed and multiplied by 2 "
            "to correspond to the DASS-42 scale scores."
        ),
        "scales": {
            "Depression": {
                "Normal": "0 - 9",
                "Mild": "10 - 13",
                "Moderate": "14 - 20",
                "Severe": "21 - 27",
                "Extremely Severe": "28+"
            },
            "Anxiety": {
                "Normal": "0 - 7",
                "Mild": "8 - 9",
                "Moderate": "10 - 14",
                "Severe": "15 - 19",
                "Extremely Severe": "20+"
            },
            "Stress": {
                "Normal": "0 - 14",
                "Mild": "15 - 18",
                "Moderate": "19 - 25",
                "Severe": "26 - 33",
                "Extremely Severe": "34+"
            }
        }
    }
