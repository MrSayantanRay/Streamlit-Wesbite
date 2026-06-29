import streamlit as st

def inject_custom_css():
    css = """
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght=300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
    /* Main App Layout Styling */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
        height: 8px;
    }
    ::-webkit-scrollbar-track {
        background: #0F0C1B;
    }
    ::-webkit-scrollbar-thumb {
        background: #3B3B6D;
        border-radius: 4px;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: #6C5CE7;
    }
    
    /* Header Gradient Title */
    .main-title {
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #A8A5FF 0%, #6C5CE7 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        text-align: left;
    }
    
    .subtitle {
        font-size: 1.2rem;
        color: #94A3B8;
        margin-bottom: 2rem;
    }
    
    /* Card Styles */
    .glass-card {
        background: rgba(29, 25, 50, 0.45);
        border: 1px solid rgba(108, 92, 231, 0.15);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        backdrop-filter: blur(8px);
        -webkit-backdrop-filter: blur(8px);
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-2px);
        border-color: rgba(108, 92, 231, 0.4);
    }
    
    /* Custom Gradient Metrics */
    .metric-container {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 1rem;
        border-radius: 12px;
        background: linear-gradient(135deg, rgba(108, 92, 231, 0.1) 0%, rgba(29, 25, 50, 0.6) 100%);
        border-left: 5px solid #6C5CE7;
        margin-bottom: 0.75rem;
    }
    
    .metric-depression { border-left-color: #FF7675; }
    .metric-anxiety { border-left-color: #FDCB6E; }
    .metric-stress { border-left-color: #0984E3; }
    
    .metric-label {
        font-size: 0.9rem;
        color: #94A3B8;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: #FFFFFF;
    }
    
    /* Tech Tag Styling */
    .tech-tag {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        background-color: rgba(108, 92, 231, 0.12);
        color: #A8A5FF;
        border: 1px solid rgba(108, 92, 231, 0.3);
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 500;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
        transition: all 0.2s ease;
    }
    
    .tech-tag:hover {
        background-color: rgba(108, 92, 231, 0.25);
        border-color: #6C5CE7;
    }
    
    /* Section Divider */
    .divider {
        height: 1px;
        background: linear-gradient(90deg, rgba(108, 92, 231, 0) 0%, rgba(108, 92, 231, 0.3) 50%, rgba(108, 92, 231, 0) 100%);
        margin: 2rem 0;
    }
    
    /* Highlight text */
    .highlight-text {
        color: #A8A5FF;
        font-weight: 600;
    }
    </style>
    """
    # FIX: Use st.html instead of st.markdown
    st.html(css)