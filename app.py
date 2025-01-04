from scraping_facturas import ExtraccionInsuma
import streamlit as st
import scraping_facturas as sf
from pathlib import Path
import locale
import funciones as fn


class InterfazObuma:
    """
    # Interfaz de la app de Insuma
    App para la extracción de información y control de la producción a
    través de Streamlit.

    ## principales Objetivos:
    
    - Relaizar WebScraping a  la plataforma "Obuma" para la extracción de guías.
    - mantener el control de los pedidos realizados.

    mas detalles revisar con Gonzalo.
    """
    
    def __init__(self):
        locale.setlocale(locale.LC_TIME, "es_ES")
        st.set_page_config(
            page_title="Gestión operaciones - Insuma",
            page_icon="img\\insuma_logo.png",
            initial_sidebar_state="collapsed",
            layout="wide"
        )
        
    def main(self):
        """
        Código fuente de la pág.
        """
        col1, col2 = st.columns([1,6])
        with col1:
            st.image(
                Path("img", "insuma_logo.png"),
                use_container_width=True)
        with col2:
            st.title("Control de Gestión Insuma")

        tab1, tab2,tab3, tab4, tab5, tab6 = st.tabs(
            ["Notas de venta", "Inicio", "Cotizaciones", "Producción", "Compras", "Mapa de ventas"]
            )
        
        with tab6:
            st.header("Inicio loco aca está el Inicio de la app")
        with tab2:
            st.header("Esta es de cotizaciones que sucede realmente?")
        
        with tab1:
            with st.spinner("Espera que se descargue la información"):
                df_notas = ExtraccionInsuma().main()
                # lo que falta acá revisar en el proyecto de streamlit "Dashboard CDE"
            st.dataframe(df_notas)

if __name__=="__main__":
    InterfazObuma().main()