import streamlit as st
import matplotlib.pyplot as plt
from calculos import (
    juros_simples,
    juros_compostos,
    juros_compostos_inflacao,
    juros_compostos_aporte
)

st.sidebar.title("Configurações")

# -------------------------
# Inputs
# -------------------------
C = st.sidebar.number_input("Capital inicial", value=1000.0)
i = st.sidebar.number_input("Taxa de juros (%)", value=10.0) / 100
t = st.sidebar.number_input("Anos", value=5, step=1)
aporte = st.sidebar.number_input("Aporte mensal", value=0.0, step = 50)
# -------------------------
# Menu
# -------------------------
opcao = st.selectbox(
    "Escolha o tipo de juros:",
    ["Simples", "Compostos", "Compostos + Inflação", "Compostos com aporte"]
)

# -------------------------
# Botão
# -------------------------
if st.button("Calcular"):

    if opcao == "Simples":
        anos, valores = juros_simples(C, i, t)

        fig, ax = plt.subplots()
        ax.plot(anos, valores, label="Juros Simples")
        ax.set_title("Juros Simples")
        ax.set_xlabel("Anos")
        ax.set_ylabel("Valor")

        ax.legend()
        st.pyplot(fig)

    elif opcao == "Compostos":
        anos, valores = juros_compostos(C, i, t)

        fig, ax = plt.subplots()
        ax.plot(anos, valores, label="Juros Compostos")
        ax.set_title("Juros Compostos")
        ax.set_xlabel("Anos")

        ax.set_ylabel("Valor (R$)")
        ax.legend()
        st.pyplot(fig)

    elif opcao == "Compostos com aporte":
        anos, valores = juros_compostos_aporte(C, i, t, aporte)

        st.line_chart({"Com aporte": valores})


    else:
        anos, nominal, real, inflacao, fallback = juros_compostos_inflacao(C, i, t)

        if fallback:
            st.warning("Dados de inflação indisponíveis. Utilizando fallback de 4%.")
        else: st.success("Dados de inflação obtidos com sucesso.")

        st.write(f"Inflação usada: {inflacao:.2%}")


#metricas

        montante_final = nominal[-1]
        lucro = montante_final - C
        rentabilidade = (lucro / C) * 100
        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Montante Final", f"R$ {montante_final:,.2f}")

        with col2:
            st.metric("Lucro", f"R$ {lucro:,.2f}")

        with col3:
            st.metric("Rentabilidade", f"{rentabilidade:.2f}%")

    #grafico

        fig, ax = plt.subplots()
        ax.plot(anos, nominal, label="Nominal")
        ax.plot(anos, real, label="Real")

        ax.set_title("Juros Compostos com Inflação")
        ax.set_xlabel("Anos")
        ax.set_ylabel("Valor")

        ax.legend()

        st.pyplot(fig)