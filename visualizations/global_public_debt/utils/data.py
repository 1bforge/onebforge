import pandas as pd
import xlrd
import pathlib
import streamlit as st


@st.cache_data
def load_data(filename: str) -> pd.DataFrame:
    filename = pathlib.Path(filename)
    if filename.suffix == ".html":
        data = pd.read_html(filename)[0]
    elif filename.suffix == ".csv":
        data = pd.read_csv(filename, low_memory=False)
    elif filename.suffix == ".parquet":
        data = pd.read_parquet(filename)
    elif filename.suffix == ".xlsx":
        data = pd.read_excel(filename)
    elif filename.suffix == ".xls":
        workbook = xlrd.open_workbook(filename, ignore_workbook_corruption=True)
        data = pd.read_excel(workbook)

    return data


public_sector_debt = load_data('./data/input_data/global_debt_database/public_sector_debt.xls')