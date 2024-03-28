import streamlit as st

st.set_page_config(
    page_title="Global Public Debt By Years",
    page_icon="💰",
    layout="wide", 
    initial_sidebar_state="collapsed"
)

from views import DebtView 
from utils import load_css
from utils.data import public_sector_debt

load_css()

st.title("Global Public Debt By Years")

with st.container():
    DebtView().view(
            "Public Sector Debt",
            public_sector_debt
        )