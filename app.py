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
        Función para filtrar el dataframe de ventas.
        """
        filtros = {
            "Fecha": ("FECHA", "Todas"),
            "Vendedor": ("VENDEDOR", "Todos"),
            "Cliente": ("CLIENTE RS", "Todos"),
            "Sucursal": ("SUCURSAL", "Todos"),
            "Estado": ("ESTADO", "Todas")
        }

        seleccionados = {}
        cols = st.columns(len(filtros))
        for col, (label, (columna, default)) in zip(cols, filtros.items()):
            with col:
                seleccionados[columna] = st.selectbox(label, [default] + df[columna].unique().tolist())

        for columna, valor in seleccionados.items():
            if valor not in ["Todas", "Todos"]:
                df = df[df[columna] == valor]

        return df

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