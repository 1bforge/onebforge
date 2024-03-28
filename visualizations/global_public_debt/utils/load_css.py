import streamlit as st
import tomli

def load_css():
    with open(".streamlit/config.toml", "rb") as f:
        config = tomli.load(f)

    theme = config["theme"]
    
    with open("styles/principal.css") as f:
        st.markdown(
            f"""
                <style>
                    :root {{
                        --primarylColor: {theme["primaryColor"]};
                        --backgroundColor: {theme["backgroundColor"]};
                        --secondaryBackgroundColor: {theme["secondaryBackgroundColor"]};
                    }}
                    {f.read()}
                </style>
            """
            , unsafe_allow_html=True
        )