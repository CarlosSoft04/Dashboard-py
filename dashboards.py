import pandas as pd
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="Dashboard com python",layout="wide")


df = pd.read_csv("supermarket_sales.csv", sep=";", decimal=",")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")
df["Month"] = df["Date"].apply(lambda x: str(x.year) + "-" + str(x.month))

month = st.sidebar.selectbox("Selecione o Mes: ", df["Month"].unique())


options = st.sidebar.multiselect("Selecione o grafico: ", options=["Faturamento por dia","Faturamento por tipo de produto", "Faturamento por cidade", "Faturamento por pagamento", "Avaliacao media"],
                                 default=["Faturamento por dia", "Faturamento por cidade"])

df_filtred = df[df["Month"] == month]


columns = [st.columns(2), st.columns(3)]


def faturamento_por_dia():
    fig_date = px.bar(df_filtred, x="Date", y="Total", color="City", title="Faturamento por dia")
    columns[0][0].plotly_chart(fig_date, use_container_width=True)
def faturamento_tipo_dia():
    fig_prod = px.bar(df_filtred, x="Date", y="Product line", color="City", title="Faturamento por tipo de produto", orientation="h")
    columns[0][1].plotly_chart(fig_prod, use_container_width=True)

def faturamento_cidade():
    fat_total = df_filtred.groupby("City") [["Total"]].sum().reset_index()
    fig_cid = px.bar(fat_total, x="City", y="Total", title="Faturamento por cidade")
    columns[1][0].plotly_chart(fig_cid, use_container_width=True)

def faturamento_pagamento():
    fig_kind = px.pie(df_filtred, values="Total", names="Payment", title="Faturamento por pagamento")
    columns[1][1].plotly_chart(fig_kind, use_container_width=True)
def avaliacao_media():
    cit_total = df_filtred.groupby("City")[["Rating"]].mean().reset_index()
    fig_rating = px.bar(df_filtred, x="City", y="Rating", title="Avaliacao media")
    columns[1][2].plotly_chart(fig_rating, use_container_width=True)

graficos = {
    "Faturamento por dia": faturamento_por_dia,
     "Faturamento por tipo de produto": faturamento_tipo_dia,
      "Faturamento por cidade": faturamento_cidade,
       "Faturamento por pagamento": faturamento_pagamento,
       "Avaliacao media": avaliacao_media,

}

for opcao in options : graficos[opcao]()