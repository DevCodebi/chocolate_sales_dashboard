"""
App Streamlit: Vendas de Chocolate
Dashboard com filtros, cards, gráficos e tabelas.
Execute na raiz do projeto: streamlit run app.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import streamlit as st
import pandas as pd
import plotly.express as px

from src.config import DATA_DIR
from src.io import load_data
from src.cleaning import clean_sales_df

# Configuração da página
st.set_page_config(
    page_title="Vendas de Chocolate",
    page_icon="🍫",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Carregar dados (com cache)
@st.cache_data
def get_data():
    path = DATA_DIR / "chocolate_sales_2.csv"
    df = load_data(path)
    return clean_sales_df(df)

df_raw = get_data()

# Garantir coluna date em datetime para filtros
if "date" in df_raw.columns and not pd.api.types.is_datetime64_any_dtype(df_raw["date"]):
    df_raw["date"] = pd.to_datetime(df_raw["date"], format="%d/%m/%Y", errors="coerce")

# ---- Sidebar: Filtros ----
st.sidebar.header("Filtros")
st.sidebar.markdown("Selecione os critérios para filtrar o dashboard.")

# Filtro por país
countries = sorted(df_raw["country"].dropna().unique().tolist())
selected_countries = st.sidebar.multiselect(
    "País",
    options=countries,
    default=countries,
    key="country",
)

# Filtro por produto
products = sorted(df_raw["product"].dropna().unique().tolist())
selected_products = st.sidebar.multiselect(
    "Produto",
    options=products,
    default=products,
    key="product",
)

# Filtro por vendedor
sales_persons = sorted(df_raw["sales_person"].dropna().unique().tolist())
selected_persons = st.sidebar.multiselect(
    "Vendedor",
    options=sales_persons,
    default=sales_persons,
    key="sales_person",
)

# Filtro por período
df_with_date = df_raw.dropna(subset=["date"])
if not df_with_date.empty:
    min_date = df_with_date["date"].min().date()
    max_date = df_with_date["date"].max().date()
    date_range = st.sidebar.date_input(
        "Período",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date,
        key="date_range",
    )
    if isinstance(date_range, (list, tuple)) and len(date_range) == 2:
        start_date, end_date = date_range[0], date_range[1]
    elif hasattr(date_range, "year"):
        start_date = end_date = date_range
    else:
        start_date, end_date = min_date, max_date
else:
    start_date, end_date = None, None

# Aplicar filtros
df = df_raw.copy()
df = df[df["country"].isin(selected_countries)]
df = df[df["product"].isin(selected_products)]
df = df[df["sales_person"].isin(selected_persons)]
if start_date is not None and end_date is not None and "date" in df.columns:
    df = df[df["date"].notna() & (df["date"].dt.date >= start_date) & (df["date"].dt.date <= end_date)]

# ---- Título ----
st.title("🍫 Dashboard de Vendas de Chocolate")
st.markdown(f"**{len(df):,}** registros após filtros.")

# ---- Cards (KPIs) ----
col1, col2, col3, col4, col5 = st.columns(5)

total_sales = df["amount"].sum()
with col1:
    st.metric("Total de Vendas", f"${total_sales:,.0f}")

with col2:
    st.metric("Nº de Transações", f"{len(df):,}")

with col3:
    st.metric("Países", df["country"].nunique())

with col4:
    st.metric("Produtos", df["product"].nunique())

with col5:
    st.metric("Vendedores", df["sales_person"].nunique())

st.divider()

# ---- Gráficos ----
tab1, tab2, tab3, tab4 = st.tabs(["Vendas por país", "Vendas por produto", "Série temporal", "Top vendedores"])

with tab1:
    by_country = df.groupby("country", as_index=False)["amount"].sum().sort_values("amount", ascending=True)
    fig1 = px.bar(
        by_country,
        x="amount",
        y="country",
        orientation="h",
        title="Total de vendas por país",
        labels={"amount": "Vendas ($)", "country": "País"},
        color="amount",
        color_continuous_scale="Blues",
    )
    fig1.update_layout(showlegend=False, height=400)
    st.plotly_chart(fig1, use_container_width=True)

with tab2:
    by_product = df.groupby("product", as_index=False)["amount"].sum().sort_values("amount", ascending=True).tail(20)
    fig2 = px.bar(
        by_product,
        x="amount",
        y="product",
        orientation="h",
        title="Top 20 produtos por faturamento",
        labels={"amount": "Vendas ($)", "product": "Produto"},
        color="amount",
        color_continuous_scale="Greens",
    )
    fig2.update_layout(showlegend=False, height=500)
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    if "date" in df.columns and df["date"].notna().any():
        df_month = df.copy()
        df_month["month"] = df_month["date"].dt.to_period("M").astype(str)
        monthly = df_month.groupby("month", as_index=False)["amount"].sum()
        fig3 = px.line(
            monthly,
            x="month",
            y="amount",
            title="Evolução das vendas por mês",
            labels={"month": "Mês", "amount": "Vendas ($)"},
            markers=True,
        )
        fig3.update_layout(height=400)
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("Não há datas válidas para exibir a série temporal.")

with tab4:
    by_person = df.groupby("sales_person", as_index=False)["amount"].sum().sort_values("amount", ascending=True).tail(15)
    fig4 = px.bar(
        by_person,
        x="amount",
        y="sales_person",
        orientation="h",
        title="Top 15 vendedores por faturamento",
        labels={"amount": "Vendas ($)", "sales_person": "Vendedor"},
        color="amount",
        color_continuous_scale="Purples",
    )
    fig4.update_layout(showlegend=False, height=450)
    st.plotly_chart(fig4, use_container_width=True)

st.divider()

# ---- Tabelas ----
st.subheader("Tabelas resumidas")

col_a, col_b = st.columns(2)

with col_a:
    st.markdown("**Vendas por país**")
    table_country = df.groupby("country", as_index=False).agg(
        total_vendas=("amount", "sum"),
        transacoes=("amount", "count"),
    ).sort_values("total_vendas", ascending=False)
    table_country["total_vendas"] = table_country["total_vendas"].apply(lambda x: f"${x:,.0f}")
    st.dataframe(table_country, use_container_width=True, hide_index=True)

with col_b:
    st.markdown("**Vendas por produto (top 15)**")
    table_product = (
        df.groupby("product", as_index=False)["amount"]
        .sum()
        .sort_values("amount", ascending=False)
        .head(15)
    )
    table_product["amount"] = table_product["amount"].apply(lambda x: f"${x:,.0f}")
    table_product = table_product.rename(columns={"amount": "total_vendas"})
    st.dataframe(table_product, use_container_width=True, hide_index=True)

st.subheader("Dados filtrados (amostra)")
display_df = df.head(500).copy()
if "date" in display_df.columns:
    display_df["date"] = display_df["date"].dt.strftime("%d/%m/%Y")
display_df["amount"] = display_df["amount"].apply(lambda x: f"${x:,.2f}")
st.dataframe(display_df, use_container_width=True, hide_index=True)
if len(df) > 500:
    st.caption(f"Exibindo 500 de {len(df):,} registros. Ajuste os filtros na barra lateral para refinar.")
