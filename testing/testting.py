import scraping_facturas as sf
import streamlit as st
from pathlib import Path
import locale


class InterfazObuma:
    LOGO_PATH = Path("img", "insuma_logo.png")
    PAGINAS = ["Notas de venta", "Inicio", "Cotizaciones", "Producción", "Compras", "Mapa de ventas"]

    def __init__(self):
        locale.setlocale(locale.LC_TIME, "es_ES")
        st.set_page_config(
            page_title="Gestión operaciones - Insuma",
            page_icon=self.LOGO_PATH,
            initial_sidebar_state="collapsed",
            layout="wide"
        )

    def render_logo(self):
        col1, col2 = st.columns([1, 6])
        with col1:
            st.image(self.LOGO_PATH, use_container_width=True)
        with col2:
            st.title("Control de Gestión Insuma")

    def render_tabs(self):
        return st.tabs(self.PAGINAS)

    def render_filters(self, df):
        col1, col2, col3, col4, col5 = st.columns(5)
        return (
            self.create_filter(col1, "Fecha", ["Todas"] + df["FECHA"].unique().tolist()),
            self.create_filter(col2, "Vendedor", ["Todos"] + df["VENDEDOR"].unique().tolist()),
            self.create_filter(col3, "Cliente", ["Todos"] + df["CLIENTE RS"].unique().tolist()),
            self.create_filter(col4, "Sucursal", ["Todos"] + df["SUCURSAL"].unique().tolist()),
            self.create_filter(col5, "Estado", ["Todas"] + df["ESTADO"].unique().tolist())
        )

    @staticmethod
    def create_filter(col, label, options):
        return col.selectbox(label, options)

    def apply_filters(self, df, filters):
        filtro_fecha, filtro_vendedor, filtro_cliente, filtro_sucursal, filtro_estado = filters
        if filtro_fecha != "Todas":
            df = df[df["FECHA"] == filtro_fecha]
        if filtro_vendedor != "Todos":
            df = df[df["VENDEDOR"] == filtro_vendedor]
        if filtro_cliente != "Todos":
            df = df[df["CLIENTE RS"] == filtro_cliente]
        if filtro_sucursal != "Todos":
            df = df[df["SUCURSAL"] == filtro_sucursal]
        if filtro_estado != "Todas":
            df = df[df["ESTADO"] == filtro_estado]
        return df

    def fetch_data(self):
        try:
            with st.spinner("Espera que se descargue la información"):
                return sf.ExtraccionInsuma().main()
        except Exception as e:
            st.error(f"Error al cargar los datos: {e}")
            return None

    def main(self):
        self.render_logo()
        tabs = self.render_tabs()

        with tabs[0]:  # Notas de venta
            df_notas = self.fetch_data()
            if df_notas is not None:
                filters = self.render_filters(df_notas)
                df_filtrado = self.apply_filters(df_notas, filters)
                st.dataframe(df_filtrado)
        with tabs[1]:
            st.header("Inicio loco aca está el Inicio de la app")
        with tabs[2]:
            st.header("Esta es de cotizaciones que sucede realmente?")


if __name__ == "__main__":
    InterfazObuma().main()
