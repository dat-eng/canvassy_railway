import os
import streamlit as st


# --------------------------------------------------
# Simple Password Protection
# --------------------------------------------------

def authenticate():

    PASSWORD = os.getenv("APP_PASSWORD")

    if not PASSWORD:
        try:
            PASSWORD = st.secrets["APP_PASSWORD"]
        except (KeyError, FileNotFoundError):
            st.error("APP_PASSWORD is not configured")
            st.stop()
    
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:

        password = st.text_input(
            "Enter Password",
            type="password"
        )

        if password == PASSWORD:
            st.session_state.authenticated = True
            st.rerun()

        elif password:
            st.error("Incorrect password")

        st.stop()