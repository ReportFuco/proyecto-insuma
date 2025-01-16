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
    PAGINAS = ["Notas de venta", "Inicio", "Cotizaciones", "Producción", "Compras", "Mapa de ventas"]
    LOGO_PATH = Path("img", "insuma_logo.png")

    def __init__(self):
        locale.setlocale(locale.LC_TIME, "es_ES")
        st.set_page_config(
            page_title="Gestión operaciones - Insuma",
            page_icon=self.LOGO_PATH,
            initial_sidebar_state="collapsed",
            layout="wide"
        )     

    def render_logo(self):
        col1, col2 = st.columns([1,6])
        with col1:
            st.image(self.LOGO_PATH, use_container_width=True)
        with col2:
            st.title("Control de Gestión Insuma")

    @st.cache_data(show_spinner=False, ttl=60*5)
    def dataframe_ventas(_self):
        return sf.ExtraccionInsuma().main()

    def filtros(self, df):
        """
        función para filtrar el dataframe de ventas.
        """
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            filtro_fecha = st.selectbox("Fecha", ["Todas"] + df["FECHA"].unique().tolist())
        with col2:
            filtro_vendedor = st.selectbox("Vendedor", ["Todos"] + df["VENDEDOR"].unique().tolist())
        with col3:
            filtro_cliente = st.selectbox("Cliente", ["Todos"] + df["CLIENTE RS"].unique().tolist())
        with col4:
            filtro_sucursal = st.selectbox("Sucursal", ["Todos"] + df["SUCURSAL"].unique().tolist())
        with col5:
            filtro_estado = st.selectbox("Estado", ["Todas"] + df["ESTADO"].unique().tolist())
        df_filtrado = df.copy()
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
        return df_filtrado

    def main(self):
        self.render_logo()
        tab1, tab2,tab3, tab4, tab5, tab6 = st.tabs(self.PAGINAS)
        with tab1:
            with st.spinner("Extrayendo la información de Obuma..."):
                df_notas = self.dataframe_ventas()
            df_filtrado = self.filtros(df_notas)
            st.dataframe(df_filtrado)
        with tab2:
            st.write("Página de inicio")

if __name__=="__main__":
    InterfazObuma().main()