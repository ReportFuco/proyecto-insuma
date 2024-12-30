import pandas as pd
import streamlit as st


def pie_pag(titulo: str, descripcion: str):
    col1, col2 = st.columns([1,4])

    with col1:
        st.image("img\\insuma.jpeg", use_column_width=True)

    with col2:
        st.title(titulo)
        st.text(descripcion)
