import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px



st.set_page_config(page_title="Simple Data Dashboard", layout="wide")


def render_basic_table():
    """Tabla simple y gráfico de barras."""
    st.subheader("Tabla simple")
    df = pd.DataFrame(
        {"A": [1, 2, 3, 4], "B": [5, 6, 7, 8], "C": [9, 10, 11, 12]}
    )
    st.dataframe(df)
    st.bar_chart(df)


def render_histogram():
    """Histograma usando Matplotlib."""
    st.subheader("Histograma (Matplotlib)")
    y = np.random.normal(0, 1, size=1000)
    fig, ax = plt.subplots()
    ax.hist(y, bins=20)
    st.pyplot(fig)


def render_plotly_example():
    """Ejemplo simple con Plotly Express."""
    st.subheader("Gráfico con Plotly")
    df = pd.DataFrame(
        {
            "categoria": ["A", "B", "C", "D"],
            "valor": np.random.randint(1, 10, size=4),
        }
    )
    fig = px.bar(df, x="categoria", y="valor", title="Valores por categoría")
    st.plotly_chart(fig, use_container_width=True)


def render_best_dessert():
    """Tabla editable de postres y selección del favorito."""
    st.subheader("Postres favoritos")
    df = pd.DataFrame(
        [
            {"postre": "pastel", "rating": 4, "is_widget": True},
            {"postre": "helado", "rating": 5, "is_widget": False},
            {"postre": "galletas", "rating": 3, "is_widget": True},
        ]
    )

    edited_df = st.data_editor(df)
    favorite_dessert = edited_df.loc[edited_df["rating"].idxmax(), "postre"]
    st.markdown(f"Tu postre favorito es: **{favorite_dessert}**")


def main():
    st.title("Simple Data Dashboard")
    st.write("Gráficas en contenedor")

    with st.container():
        render_basic_table()
        st.markdown("---")
        render_histogram()
        st.markdown("---")
        render_plotly_example()
        st.markdown("---")
        render_best_dessert()


if __name__ == "__main__":
    main()