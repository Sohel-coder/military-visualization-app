import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from sklearn.linear_model import LinearRegression

st.set_page_config(
    page_title='The Art of War: A Comprehensive Visualization of World Military Strength',
    page_icon='🛡️',
    layout='wide',
    initial_sidebar_state='expanded',
)

# Background styling
st.markdown(
    """
    <style>
    .stApp {
        background-image: url('https://ssbcrackexams.com/wp-content/uploads/2024/06/Indian-Army.jpg');
        background-attachment: fixed;
        background-size: cover;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🛡️ The Art of War")
st.markdown("""
**An interactive data visualization that unveils the hidden dynamics of global defense. By seamlessly integrating trade data, missile inventories, military manpower, defense budgets, and power indexes.**

**Join us as we decode complex defense data into an engaging visual story of strength, strategy, and global influence.**
""", unsafe_allow_html=True)

