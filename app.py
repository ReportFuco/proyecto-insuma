import scraping_facturas as sf
import streamlit as st
from pathlib import Path
import locale



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
        self.paginas = [
            "Notas de venta", "Inicio", "Cotizaciones", 
            "Producción", "Compras", "Mapa de ventas"
            ]
        locale.setlocale(locale.LC_TIME, "es_ES")
        st.set_page_config(
            page_title="Gestión operaciones - Insuma",
            page_icon="img\\insuma_logo.png",
            initial_sidebar_state="collapsed",
            layout="wide"
        )

        
    def main(self):

        col1, col2 = st.columns([1,6])
        with col1:
            st.image(
                Path("img", "insuma_logo.png"),
                use_container_width=True)
        with col2:
            st.title("Control de Gestión Insuma")

        tab1, tab2,tab3, tab4, tab5, tab6 = st.tabs(self.paginas)
        

        # Código principal
        with tab6:
            st.header("Inicio loco aca está el Inicio de la app")
        with tab2:
            st.header("Esta es de cotizaciones que sucede realmente?")
        
        with tab1:
            with st.spinner("Espera que se descargue la información"):
                df_notas = sf.ExtraccionInsuma().main()
            
            col1, col2, col3, col4, col5 = st.columns(5)
            with col1:
                filtro_fecha = st.selectbox("Fecha", ["Todas"] + df_notas["FECHA"].unique().tolist())
            with col2:
                filtro_vendedor = st.selectbox("Vendedor", ["Todos"] + df_notas["VENDEDOR"].unique().tolist())
            with col3:
                filtro_cliente = st.selectbox("Cliente", ["Todos"] + df_notas["CLIENTE RS"].unique().tolist())
            with col4:
                filtro_sucursal = st.selectbox("Sucursal", ["Todos"] + df_notas["SUCURSAL"].unique().tolist())
            with col5:
                filtro_estado = st.selectbox("Estado", ["Todas"] + df_notas["ESTADO"].unique().tolist())

            df_filtrado = df_notas.copy()

            if filtro_fecha != "Todas":
                df_filtrado = df_filtrado[df_filtrado["FECHA"] == filtro_fecha]
            if filtro_vendedor != "Todos":
                df_filtrado = df_filtrado[df_filtrado["VENDEDOR"] == filtro_vendedor]
            if filtro_cliente != "Todos":
                df_filtrado = df_filtrado[df_filtrado["CLIENTE RS"] == filtro_cliente]
            if filtro_sucursal != "Todos":
                df_filtrado = df_filtrado[df_filtrado["SUCRUSAL"] == filtro_sucursal]
            if filtro_estado != "Todas":
                df_filtrado = df_filtrado[df_filtrado["ESTADO"] == filtro_estado]
            st.dataframe(df_filtrado)

if __name__=="__main__":
    InterfazObuma().main()