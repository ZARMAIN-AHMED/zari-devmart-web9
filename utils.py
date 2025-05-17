
import streamlit as st

def require_login():
    if not st.session_state.user:
        st.error("Please log in to continue.")
        st.stop()
