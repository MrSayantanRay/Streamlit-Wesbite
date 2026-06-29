import streamlit as st
from components.cards import draw_glass_card
import base64

def render_portfolio_page():
    def get_base64(path):
        with open(path, "rb") as f:
            return base64.b64encode(f.read()).decode()

    banner = get_base64("assets/ds_banner.png")

    st.markdown(
    f"""
    <style>

    .hero-banner {{

        height:42vh;              /* smaller hero */
        min-height:260px;
        max-height:420px;

        width:100vw;

        margin-left:calc(-50vw + 50%);
        margin-top:-1rem;

        /* slightly overlap content */
        margin-bottom:-60px;

        position:relative;

        overflow:hidden;

        background:

            /* ultra smooth fade */

            linear-gradient(
                180deg,

                rgba(15,17,26,0.00) 0%,
                rgba(15,17,26,0.03) 20%,
                rgba(15,17,26,0.08) 40%,
                rgba(15,17,26,0.18) 58%,
                rgba(15,17,26,0.35) 72%,
                rgba(15,17,26,0.60) 84%,
                rgba(15,17,26,0.82) 92%,
                rgba(15,17,26,0.96) 97%,
                #0F111A 100%

            ),

            url("data:image/png;base64,{banner}");

        background-size:cover;

        background-position:center 40%;

        background-repeat:no-repeat;

    }}

    /* soft blur transition */

    .hero-banner::after {{

        content:"";

        position:absolute;

        inset:auto 0 -30px 0;

        height:160px;

        background:
            linear-gradient(
                to bottom,
                rgba(15,17,26,0),
                rgba(15,17,26,.25),
                rgba(15,17,26,.55),
                rgba(15,17,26,.80),
                #0F111A
            );

        filter:blur(18px);

        transform:scaleY(1.4);

    }}

    </style>

    <div class="hero-banner"></div>
    """,
    unsafe_allow_html=True
    )

    # spacing after hero
    st.markdown(
        "<div style='height:10px'></div>",
        unsafe_allow_html=True
    )

# ---------- HEADER COLUMNS ----------
    header_left, header_right = st.columns([1, 3.4], vertical_alignment="top")

    with header_left:
        st.markdown("""
        <style>
        button[kind="header"]{
            display:none !important;
        }

        [data-testid="stElementToolbar"]{
            display:none !important;
        }

        [data-testid="stImage"] img {
            width: 270px !important;
            height: 400px !important;
            object-fit: cover;
            object-position: center top;
            border-radius: 22px;
            border: 2px solid rgba(108, 92, 231, 0.18);
            box-shadow: 0 12px 40px rgba(108, 92, 231, 0.15);
        }
        </style>
        """, unsafe_allow_html=True)

        st.image(
            "assets/profile.jpg",
            use_container_width=False
        )

    with header_right:
        st.html("""
        <h1 class="main-title"
            style="
            margin-top: 0;
            margin-bottom: 4px;
            font-size: 2.5rem;
            line-height: 1.1;">
            Sayantan Ray
        </h1>
        """)

        st.html("""
        <div class="subtitle"
            style="
            margin-top: 0;
            margin-bottom: 16px;
            line-height: 1.3;
            font-size: 1.05rem;
            color: #A8A5FF;">
            Aspiring Data Scientist | Machine Learning Enthusiast | Statistical Analyst
        </div>
        """)
        
        # Introduction Card: Scaled to hit exactly 370px total layout height
        st.markdown("""
        <div style='
            background: linear-gradient(135deg, rgba(22,22,42,.72), rgba(18,18,35,.92));
            backdrop-filter: blur(16px);
            padding: 22px 26px;
            border-radius: 18px;
            border: 1px solid rgba(108,92,231,.16);
            color: #D8D8E6;
            line-height: 1.7;
            font-size: 1rem;
            box-shadow: 0 10px 35px rgba(0,0,0,.18);
            margin-top: 0;
            min-height: 150px;
            display: flex;
            flex-direction: column;
            justify-content: center;
        '>
            <span style="color: #FFFFFF;font-size: 1.05rem; font-weight: 500;">
                <strong>I am a Mathematics graduate currently pursuing an M.Sc. in Mathematics & Computing</strong>, driven by a growing passion for Data Science, Machine Learning, and analytical problem solving.
                <br>
                Coming from a strong mathematical background, I was always fascinated by understanding how complex systems work. 
                My interest in technology accelerated during the post-COVID AI wave, when advances in intelligent systems sparked a deeper curiosity about what powers modern innovation behind the scenes. 
                That curiosity eventually evolved into a clear realization: before building intelligent systems, you must first understand data.<br>
                Today, I focus on combining mathematical reasoning, statistical thinking, and computational tools to extract meaningful insights from complex datasets and solve real-world problems. My goal is to bridge the gap between abstract theory and practical intelligence—turning data into decisions and ideas into impact.
            </span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(
        "<div style='height:20px'></div>",
        unsafe_allow_html=True)
    
    # --------------------------------------------------
    # 2. JOURNEY & CAREER GOALS (Vision & Technical Execution)
    # --------------------------------------------------
    st.subheader("Career Goals")
    journey_html = """
        <div>
            <p style="margin: 0.3rem 0 0 0; font-size: 1.05rem; line-height: 1.7; color: #CBD5E1;">
                My target is to thrive as a core Data Analyst / Statistical Specialist within forward-thinking technical environments. 
                I aim to leverage predictive algorithms, hypothesis testing, and interactive dashboard architectures (like Streamlit and PowerBI) 
                to translate raw computational data into bulletproof, enterprise-level strategic roadmaps.
            </p>
        </div>
    """
    draw_glass_card("", journey_html)
        
    # --------------------------------------------------
    # 3. EDUCATION JOURNEY
    # --------------------------------------------------
    st.subheader("Education Journey")
    edu_html = """
    <div style="position: relative; padding-left: 1.2rem; border-left: 3px solid #6C5CE7; margin-bottom: 1.5rem;">
        <span style="font-weight: 700; color: #FFFFFF; font-size: 1.1rem;">M.Sc. in Mathematics & Computing</span><br>
        <span style="color: #A8A5FF; font-size: 0.95rem; font-weight: 500;">National Institute of Technology (NIT) Hamirpur</span><br>
        <span style="color: #94A3B8; font-size: 0.85rem;">Post Graduation Year: 2027</span>
    </div>
    <div style="position: relative; padding-left: 1.2rem; border-left: 3px solid #475569; margin-bottom: 0;">
        <span style="font-weight: 700; color: #FFFFFF; font-size: 1.1rem;">B.Sc. in Mathematics</span><br>
        <span style="color: #A8A5FF; font-size: 0.95rem; font-weight: 500;">Calcutta University</span><br>
        <span style="color: #94A3B8; font-size: 0.85rem;">Graduation Year: 2024</span>
    </div>
    """
    draw_glass_card("", edu_html)
        
    # --------------------------------------------------
    # 5. TECHNOLOGY STACK & SKILLS
    # --------------------------------------------------
    st.subheader("Technology Stack & Skills")
    
    sc1, sc2, sc3 = st.columns(3)
    
    with sc1:
        skills_lang = """
        <div style="margin-top: 0.5rem; margin-bottom: 0;">
            <span class="tech-tag">Python</span>
            <span class="tech-tag">SQL</span>
            <span class="tech-tag">C / C++</span>
        </div>
        """
        draw_glass_card("Programming Languages", skills_lang)
        
    with sc2:
        skills_ds = """
        <div style="margin-top: 0.5rem; margin-bottom: 0;">
            <span class="tech-tag">NumPy</span>
            <span class="tech-tag">Pandas</span>
            <span class="tech-tag">Matplotlib</span>
            <span class="tech-tag">Seaborn</span>
            <span class="tech-tag">Streamlit</span>
            <span class="tech-tag">Scikit-Learn</span>
        </div>
        """
        draw_glass_card("Data Science & ML Libraries", skills_ds)
        
    with sc3:
        skills_tools = """
        <div style="margin-top: 0.5rem; margin-bottom: 0;">
            <span class="tech-tag">MS Office</span>
            <span class="tech-tag">PowerBI</span>
            <span class="tech-tag">Git & GitHub</span>
        </div>
        """
        draw_glass_card("Analytical Tools & Systems", skills_tools)


    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

# --------------------------------------------------
# CONTACT SECTION
# --------------------------------------------------
    st.markdown(
        """
        <style>
            /* Target the main content area wrapper */
            div[data-testid="stAppViewBlockContainer"] {
                padding-top: 10px !important; /* Adjust this lower or higher to perfectly dial in your gap */
                padding-bottom: 0.1rem !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )

    from modules.contact import render_contact_page
    render_contact_page()