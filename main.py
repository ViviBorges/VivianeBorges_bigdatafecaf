import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()


# Função para conectar no banco
def get_db_connection():
    return create_engine(os.getenv("DATABASE_URL"))


# Função para criar tabela
def create_table(engine, df):
    df.to_sql('temperature_logs', engine, if_exists='replace', index=False)


# Interface do Streamlit
st.title("Upload de Arquivo CSV")
uploaded_file = st.file_uploader("Escolha um arquivo CSV", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("Estrutura do Dataset:")
    st.write(df.head())

    engine = get_db_connection()
    create_table(engine, df)
    st.success("Dados enviados para o banco de dados.")

    query = "SELECT * FROM temperature_logs"
    data = pd.read_sql(query, engine)

    st.title("Visualização dos Dados")
    fig = px.line(data,
                  x='noted_date',
                  y='temp',
                  title='Série Temporal de Temperaturas')
    st.plotly_chart(fig)
