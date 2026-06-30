import streamlit as st
import requests
import base64
from components.cards import draw_glass_card

SVG_ICONS = {
    "mail": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#38BDF8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-8.97 5.7a1.94 1.94 0 0 1-2.06 0L2 7"/></svg>',
    "phone": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#38BDF8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>',
    "linkedin": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#38BDF8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"/><rect width="4" height="12" x="2" y="9"/><circle cx="4" cy="4" r="2"/></svg>',
    "github": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#38BDF8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M15 22v-4a4.8 4.8 0 0 0-1-3.5c3 0 6-2 6-5.5.08-1.25-.27-2.48-1-3.5.28-1.15.28-2.35 0-3.5 0 0-1 0-3 1.5-2.64-.5-5.36-.5-8 0C6 2 5 2 5 2c-.3 1.15-.3 2.35 0 3.5A5.403 5.403 0 0 0 4 9c0 3.5 3 5.5 6 5.5-.39.49-.68 1.05-.85 1.65-.17.6-.22 1.23-.15 1.85v4"/><path d="M9 18c-4.51 2-5-2-7-2"/></svg>',
    "location": '<svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#38BDF8" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z"/><circle cx="12" cy="10" r="3"/></svg>'
}

# 2. Helper function to compile SVGs into un-blockable browser strings
def get_svg_data_uri(svg_html):
    b64 = base64.b64encode(svg_html.encode("utf-8")).decode("utf-8")
    return f"data:image/svg+xml;base64,{b64}"

def render_contact_page():
    """
    Renders the contact page with a contact form and links, styled symmetrically.
    """
    # Inject Custom CSS to transform the default Streamlit Form into a Glass Card
    st.markdown("""
    <style>
    /* Target the Streamlit form container directly */
    [data-testid="stForm"] {
        background: linear-gradient(135deg, rgba(22,22,42,.72), rgba(18,18,35,.92)) !important;
        backdrop-filter: blur(16px) !important;
        border: 1px solid rgba(108,92,231,.16) !important;
        border-radius: 18px !important;
        box-shadow: 0 10px 35px rgba(0,0,0,.18) !important;
        padding: 22px 26px !important;
    }

    /* Style form inputs to look cleaner inside the glass layout */
    [data-testid="stForm"] input, [data-testid="stForm"] textarea {
        background-color: rgba(15, 17, 26, 0.5) !important;
        border: 1px solid rgba(108, 92, 231, 0.2) !important;
        color: #E2E8F0 !important;
    }

    /* Style the Form Submit Button to match portfolio themes */
    [data-testid="stForm"] button[kind="formSubmit"] {
        background: rgba(108, 92, 231, 0.15) !important;
        border: 1px solid rgba(108, 92, 231, 0.4) !important;
        color: #A8A5FF !important;
        padding: 0.4rem 1.5rem !important;
        transition: all 0.3s ease !important;
    }
    
    [data-testid="stForm"] button[kind="formSubmit"]:hover {
        background: rgba(108, 92, 231, 0.3) !important;
        color: #FFFFFF !important;
        border-color: rgba(108, 92, 231, 0.6) !important;
        box-shadow: 0 0 12px rgba(108, 92, 231, 0.2);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown('<h1 class="main-title" style="margin-bottom: 0;">Get in Touch</h1>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle" style="margin-bottom: 1rem;">'
        "Whether you want to talk about machine learning, collaborate on a passion project, or drop a great job offer in my inbox  :)<br>"
        "—I’m all ears. Let's build something impactful."
        '</div>', 
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            """
            <div style="height: 60px; margin-bottom: 1.5rem; display: flex; flex-direction: column; justify-content: flex-end;">
                <h3 style="color: #F8FAFC; font-family: -apple-system, BlinkMacSystemFont, sans-serif; font-size: 1.25rem; font-weight: 600; margin: 0; padding-bottom: 2px;">
                    Contact Details
                </h3>
            </div>
            """, 
            unsafe_allow_html=True
        )
        
        details_html = f"""
        <div style="height: 356px; display: flex; flex-direction: column; justify-content: space-between; margin: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; box-sizing: border-box;">
            
            <div style="display: flex; align-items: center;">
                <div style="width: 44px; height: 44px; background: rgba(14, 165, 233, 0.15); border: 1px solid rgba(14, 165, 233, 0.2); border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-right: 1rem; flex-shrink: 0;">
                    <img src="{get_svg_data_uri(SVG_ICONS['mail'])}" style="width: 20px; height: 20px;" alt="Email" />
                </div>
                <div style="display: flex; flex-direction: column;">
                    <span style="font-size: 0.8rem; color: #64748B; font-weight: 500; margin-bottom: 1px;">Email</span>
                    <a href="mailto:sayantanray429@gmail.com" style="color: #F8FAFC; font-weight: 600; text-decoration: none; font-size: 0.95rem;">sayantanray429@gmail.com</a>
                </div>
            </div>

            <div style="display: flex; align-items: center;">
                <div style="width: 44px; height: 44px; background: rgba(14, 165, 233, 0.15); border: 1px solid rgba(14, 165, 233, 0.2); border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-right: 1rem; flex-shrink: 0;">
                    <img src="{get_svg_data_uri(SVG_ICONS['phone'])}" style="width: 20px; height: 20px;" alt="Phone" />
                </div>
                <div style="display: flex; flex-direction: column;">
                    <span style="font-size: 0.8rem; color: #64748B; font-weight: 500; margin-bottom: 1px;">Phone</span>
                    <a href="tel:+919051222093" style="color: #F8FAFC; font-weight: 600; text-decoration: none; font-size: 0.95rem;">+91-9051222093</a>
                </div>
            </div>

            <div style="display: flex; align-items: center;">
                <div style="width: 44px; height: 44px; background: rgba(14, 165, 233, 0.15); border: 1px solid rgba(14, 165, 233, 0.2); border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-right: 1rem; flex-shrink: 0;">
                    <img src="{get_svg_data_uri(SVG_ICONS['linkedin'])}" style="width: 20px; height: 20px;" alt="LinkedIn" />
                </div>
                <div style="display: flex; flex-direction: column;">
                    <span style="font-size: 0.8rem; color: #64748B; font-weight: 500; margin-bottom: 1px;">LinkedIn</span>
                    <a href="https://www.linkedin.com/in/sayantan-ray-7a3a73350" target="_blank" style="color: #F8FAFC; font-weight: 600; text-decoration: none; font-size: 0.95rem;">Sayantan Ray</a>
                </div>
            </div>

            <div style="display: flex; align-items: center;">
                <div style="width: 44px; height: 44px; background: rgba(14, 165, 233, 0.15); border: 1px solid rgba(14, 165, 233, 0.2); border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-right: 1rem; flex-shrink: 0;">
                    <img src="{get_svg_data_uri(SVG_ICONS['github'])}" style="width: 20px; height: 20px;" alt="GitHub" />
                </div>
                <div style="display: flex; flex-direction: column;">
                    <span style="font-size: 0.8rem; color: #64748B; font-weight: 500; margin-bottom: 1px;">GitHub</span>
                    <a href="https://github.com/MrSayantanRay" target="_blank" style="color: #F8FAFC; font-weight: 600; text-decoration: none; font-size: 0.95rem;">MrSayantanRay</a>
                </div>
            </div>

            <div style="display: flex; align-items: center;">
                <div style="width: 44px; height: 44px; background: rgba(14, 165, 233, 0.15); border: 1px solid rgba(14, 165, 233, 0.2); border-radius: 12px; display: flex; align-items: center; justify-content: center; margin-right: 1rem; flex-shrink: 0;">
                    <img src="{get_svg_data_uri(SVG_ICONS['location'])}" style="width: 20px; height: 20px;" alt="Location" />
                </div>
                <div style="display: flex; flex-direction: column;">
                    <span style="font-size: 0.8rem; color: #64748B; font-weight: 500; margin-bottom: 1px;">Location</span>
                    <span style="color: #F8FAFC; font-weight: 600; font-size: 0.95rem;">Kolkata, West Bengal, India</span>
                </div>
            </div>
            
        </div>
        """
        draw_glass_card("", details_html)

    with col2:
        st.markdown(
            """
            <div style="height: 60px; margin-bottom: 1.5rem; display: flex; flex-direction: column; justify-content: flex-end;">
                <h3 style="color: #F8FAFC; font-family: -apple-system, BlinkMacSystemFont, sans-serif; font-size: 1.25rem; font-weight: 600; margin: 0; padding-bottom: 2px;">
                    Contact Form
                </h3>
            </div>
            """, 
            unsafe_allow_html=True
        )

        # Contact Form
        with st.form(
            key="contact_form",
            clear_on_submit=True
        ):

            user_name = st.text_input(
                "Name",
                placeholder="Your Name"
            )

            user_email = st.text_input(
                "Email",
                placeholder="Your Email Address"
            )

            user_message = st.text_area(
                "Message",
                placeholder="Write your message here...",
                height=150
            )

            submit = st.form_submit_button(
                "Send Message"
            )

            # Submit Logic
            if submit:

                # Validation
                if (
                    not user_name.strip()
                    or not user_email.strip()
                    or not user_message.strip()
                ):
                    st.error(
                        "Please fill out all fields."
                    )

                elif (
                    "@"
                    not in user_email
                    or "."
                    not in user_email
                ):
                    st.error(
                        "Please enter a valid email address.")

                else:
                    payload = {
                        "service_id": "service_y09zera",
                        "template_id": "template_mm68z4h",

                        "user_id": "12PEnlt7a5g841n0Y",

                        "accessToken": st.secrets["EMAILJS_PRIVATE_KEY"],

                        "template_params": {
                            "from_name": user_name,
                            "from_email": user_email,
                            "message": user_message
                        }
                    }

                    try:
                        with st.spinner("Sending message..."):
                            response = requests.post(
                                "https://api.emailjs.com/api/v1.0/email/send",
                                json=payload,
                                headers={"Content-Type":"application/json"},
                                timeout=10)

                        if response.ok:
                            st.success(
                                "Thank you! Your message has been sent successfully.")

                        else:
                            st.error(f"Email sending failed (Status {response.status_code})")
                            st.error(response.text)

                    except requests.Timeout:
                        st.error("Request timed out. Please try again.")

                    except Exception as e:
                        st.error("Unexpected error occurred.")
                        st.exception(e)
