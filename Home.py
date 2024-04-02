import streamlit as st
import os
st.set_page_config(
    page_title="Student AI Application Agent",
    page_icon="👋",
)

st.sidebar.success("Select a demo above.")

st.markdown(
    """
    # Student AI Application Assistant
    #### Your AI-powered guide for a smoother, affordable, and fair application journey, supporting every student, every step of the way to apply dream schools
    **👈 Select a demo from the sidebar** to see some examples of our AI agents
"""
)
os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
os.environ['gmail_username'] = st.secrets['gmail_username']
os.environ['gmail_password'] = st.secrets['gmail_password']