import streamlit as st

def draw_metric_card(label, value, card_type="default"):
    """
    Renders a custom glassmorphic metric card.
    card_type: 'depression', 'anxiety', 'stress', or 'default'
    """
    border_class = f"metric-{card_type}" if card_type in ['depression', 'anxiety', 'stress'] else ""
    
    html = f"""
    <div class="metric-container {border_class}">
        <div>
            <div class="metric-label">{label}</div>
            <div style="font-size: 0.8rem; color: #64748B; font-weight: 500; margin-top: 2px;">COVID-19 Analysis Metric</div>
        </div>
        <div class="metric-value">{value}</div>
    </div>
    """
    # FIX: Swapped from st.markdown to st.html to prevent source code leaks
    st.html(html)

def draw_glass_card(title, content_html):
    """
    Renders a custom glassmorphic content container card.
    """
    html = f"""
    <div class="glass-card">
        <h4 style="margin-top:0; color:#A8A5FF; font-weight:700; margin-bottom: 0.75rem; font-size: 1.1rem;">{title}</h4>
        <div style="color: #CBD5E1; font-size: 0.95rem; line-height: 1.6;">
            {content_html}
        </div>
    </div>
    """
    # FIX: Swapped from st.markdown to st.html to force native DOM rendering
    st.html(html)