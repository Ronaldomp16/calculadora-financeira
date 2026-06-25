import streamlit as st
import matplotlib.pyplot as plt
from calculos import (
    juros_simples,
    juros_compostos,
    juros_compostos_inflacao,
    juros_compostos_aporte,
    juros_com_inflacao_manual
)

#Configuração da página

st.set_page_config(page_title="Calculadora Financeira", layout="wide")

st.title("Dashboard Financeiro")

st.markdown("---")

#Sidebar (Controles)

st.sidebar.title("Configurações")

C = st.sidebar.number_input("Capital inicial", value=1000.0)
i = st.sidebar.number_input("Taxa de juros (%)", value=10.0) / 100
t = st.sidebar.number_input("Anos", value=5, step=1)

considerar_inflacao = st.sidebar.checkbox("Considerar inflação")
considerar_aporte = st.sidebar.checkbox("Considerar aporte mensal")

#fonte_inflacao = st.sidebar.radio("Fonte de inflação", ["API", "Manual"])
#inflacao_manual = None
#if fonte_inflacao == "Manual":
    #inflacao_manual = st.sidebar.number_input("Inflação manual (%)", value=4.0, step=0.1) / 100

# Aporte
aporte = 0.0 
if considerar_aporte:
    aporte = st.sidebar.number_input("Aporte mensal", value=0.0, step = 50.0)

# Inflação
fonte_inflacao = None
inflacao_manual = 0.04

if considerar_inflacao:
    fonte_inflacao = st.sidebar.radio(
        "Fonte de inflação",
        ["Banco Central (API)", "Manual"]
    )

    if fonte_inflacao == "Manual":
        inflacao_manual = st.sidebar.number_input(
            "Inflação manual (%)", 
            value=4.0, 
            step=0.1
        ) / 100

# Menu
opcao = st.selectbox(
    "Escolha o tipo de simulação:",
    [
        "Simples",
        "Compostos", 
        "Compostos com aporte", 
        "Compostos com inflação"
    ]
)

# Botão
if st.button("Calcular"):

    #simples
    if opcao == "Simples":
        anos, valores = juros_simples(C, i, t)

        fig, ax = plt.subplots()
        ax.plot(anos, valores, label="Juros Simples")
        ax.set_title("Juros Simples")
        ax.set_xlabel("Anos")
        ax.set_ylabel("Valor")
        ax.legend()

        st.pyplot(fig)

        st.success(f"Montante final: R$ {valores[-1]:,.2f}")

    #compostos
    elif opcao == "Compostos":
        anos, valores = juros_compostos(C, i, t)

        st.subheader("Gráfico de Juros Compostos")

        fig, ax = plt.subplots()
        ax.plot(anos, valores, label="Juros Compostos")
        ax.set_title("Juros Compostos")
        ax.set_xlabel("Anos")
        ax.set_ylabel("Valor (R$)")
        ax.legend()

        st.pyplot(fig)

        st.success(f"Montante final: R$ {valores[-1]:,.2f}")

    #com aportes
    elif opcao == "Compostos com aporte":
        anos, valores = juros_compostos_aporte(C, i, t, aporte)

        st.subheader("Gráfico de Juros Compostos com Aporte")

        fig, ax = plt.subplots()
        ax.plot(anos, valores, label="Juros Compostos com Aporte")
        ax.set_title("Juros Compostos com Aporte")
        ax.set_xlabel("Anos")
        ax.set_ylabel("Valor (R$)")
        ax.legend()

        st.pyplot(fig)

        st.success(f"Montante final: R$ {valores[-1]:,.2f}")

#com inflação (dashboard completo)
    else:
        #escolha do tipo de inflação
        if not considerar_inflacao:
            st.warning("Ative 'Considerar inflação' para usar esse recurso.")
            st.stop()

        if fonte_inflacao == "Banco Central (API)":
            anos, nominal, real, inflacao, fallback = juros_compostos_inflacao(C, i, t)
        else:
            anos, nominal, real, inflacao, fallback = juros_com_inflacao_manual(
                C, i, t, inflacao_manual
            )

    #fallback aviso
        if fallback:
            st.warning("Dados de inflação indisponível. Usando fallback.")
        else:
            st.success(f"Inflação usada: {inflacao:.2%}")

#metricas

        montante_final = nominal[-1]
        lucro = montante_final - C
        rentabilidade = (lucro / C) * 100
        perda_inflacao = nominal[-1] - real[-1]

        st.subheader("Métricas Financeiras")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Montante Final", f"R$ {montante_final:,.2f}")

        with col2:
            st.metric("Lucro", f"R$ {lucro:,.2f}")

        with col3:
            st.metric("Rentabilidade", f"{rentabilidade:.2f}%")

        with col4:
            st.metric("Perda com Inflação", f"R$ {perda_inflacao:,.2f}")

#grafico

        fig, ax = plt.subplots()
        ax.plot(anos, nominal, label="Nominal")
        ax.plot(anos, real, label="Real (com inflação)")

        ax.set_xlabel("Anos")
        ax.set_ylabel("Valor (R$)")
        ax.legend()

        st.pyplot(fig)