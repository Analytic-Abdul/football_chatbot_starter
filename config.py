import streamlit as st


def load_secrets():
    st.secrets["NEO4J_URI"]
    st.secrets["NEO4J_USER"]
    st.secrets["NEO4J_PASSWORD"]
