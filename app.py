import streamlit as st
from utils.data_loader import load_clean_data
from utils.theme import inject_custom_css
from modules.portfolio import render_portfolio_page
from modules.dashboard import render_dashboard_page
from modules.statistical_insights import render_statistical_page
from modules.predictor import render_predictor_page

# --------------------------------------------------
# 1. INITIALIZE PAGE CONFIG (MUST BE ABSOLUTE FIRST)
# --------------------------------------------------
st.set_page_config(
    page_title="Sayantan Ray - Mental Health Analysis Portfolio",
    page_icon="icon design.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# 2. INJECT CLEANUP CSS (NOW RECOGNIZED PROPERLY)
# --------------------------------------------------
custom_style = """
            <style>
            /* Completely erase top header and avatar frame */
            header, [data-testid="stHeader"] {
                display: none !important;
                visibility: hidden !important;
                height: 0px !important;
            }
            
            /* Completely erase hamburger menu and deploy buttons */
            #MainMenu, [data-testid="stMainMenu"], .stDeployButton {
                display: none !important;
                visibility: hidden !important;
            }
            
            /* Completely erase standard footer */
            footer, [data-testid="stFooter"] {
                display: none !important;
                visibility: hidden !important;
            }
            
            /* 🚫 OBLITERATE THE "HOSTED WITH STREAMLIT" FLOATING BADGE */
            .viewerBadge, [data-testid="stViewerBadge"], div[data-testid="stStatusWidget"] {
                display: none !important;
                visibility: hidden !important;
            }
            
            /* Mobile adjustments */
            @media (max-width: 768px) {
                .glass-card {
                    padding: 15px;
                    font-size: 14px;
                }
                h1 {
                    font-size: 24px !important;
                }
            }
            </style>
            """
st.markdown(custom_style, unsafe_allow_html=True)


def main():
    # Inject premium custom CSS styles from your theme module
    inject_custom_css()
    
    # Load and cache survey dataset
    try:
        df = load_clean_data()
    except Exception as e:
        st.error(f"Error loading survey dataset: {e}")
        return
        
    # --------------------------------------------------
    # NAVIGATION SIDEBAR (Main Menu)
    # --------------------------------------------------
    main_menu_options = [
        "👤 Portfolio Landing Page",
        "📊 Interactive EDA Dashboard",
        "🔮 Psychometric Predictor & Analyzer"
    ]
    
    selected_page = st.sidebar.radio("Navigation Menu", main_menu_options)
    
    # --------------------------------------------------
    # CONDITIONAL SUB-MENU (Only shows for Dashboard)
    # --------------------------------------------------
    selected_sub_page = None
    if selected_page == "📊 Interactive EDA Dashboard":
        selected_sub_page = st.sidebar.radio(
            "Dashboard View:",
            ["📈 Main Metrics View", "🔬 Statistical Insights"],
            index=0
        )
    
    # Sidebar footer
    st.sidebar.markdown('<div class="divider" style="margin: 1.5rem 0;"></div>', unsafe_allow_html=True)
    st.sidebar.markdown(
        """
        <div style="text-align: center; color: #64748B; font-size: 0.75rem;">
            Created by Sayantan Ray<br>
            © 2026 All rights reserved.
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # --------------------------------------------------
    # EXPLICIT PAGE ROUTING
    # --------------------------------------------------
    if selected_page == "👤 Portfolio Landing Page":
        render_portfolio_page()
        
    elif selected_page == "📊 Interactive EDA Dashboard":
        if selected_sub_page == "🔬 Statistical Insights":
            render_statistical_page(df)
        else:
            render_dashboard_page(df)
            
    elif selected_page == "🔮 Psychometric Predictor & Analyzer":
        render_predictor_page()

if __name__ == "__main__":
    main()
