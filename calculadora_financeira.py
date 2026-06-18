import matplotlib.pyplot as plt
import requests


# =====================================
# REQUISIÇÃO DA INFLAÇÃO (BANCO CENTRAL)
# =====================================

def requisicao_inflacao():

    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json"

    response = requests.get(url)

    dados = response.json()

    inflacao = float(dados[-1]["valor"])

    return inflacao


# =====================
# JUROS SIMPLES
# =====================

def juros_simples():

    C = float(input("Qual seu capital inicial? "))
    i = float(input("Qual a taxa de juros (%)? ")) / 100
    t = int(input("Quantos anos pretende deixar seu dinheiro guardado? "))

    anos_simples = []
    valores_simples = []

    print("\n📈 Evolução do investimento:")

    for ano in range(1, t + 1):

        M = C * (1 + i * ano)

        anos_simples.append(ano)
        valores_simples.append(M)

        print(f"Ano {ano}: R${M:.2f}")

    print(f"\nMontante Final: R${M:.2f}")

    plt.clf()

    plt.plot(anos_simples, valores_simples, label="Juros Simples")

    plt.title("Evolução do Investimento (Juros Simples)")
    plt.xlabel("Anos")
    plt.ylabel("Valor (R$)")
    plt.legend()

    plt.show()


# =====================
# JUROS COMPOSTOS
# =====================

def juros_compostos():

    C = float(input("Capital inicial: "))
    i = float(input("Taxa de juros (%): ")) / 100
    t = int(input("Quantos anos? "))

    M = C

    anos = []
    valores = []

    print("\n📈 Evolução do investimento:")

    for ano in range(1, t + 1):

        M = M * (1 + i)

        anos.append(ano)
        valores.append(M)

        print(f"Ano {ano}: R${M:.2f}")

    lucro = M - C

    print("\n💰 Resultado final:")
    print(f"Montante final: R${M:.2f}")
    print(f"Lucro total: R${lucro:.2f}")

    plt.clf()

    plt.plot(anos, valores, label="Juros Compostos")

    plt.title("Evolução do Investimento")
    plt.xlabel("Anos")
    plt.ylabel("Valor (R$)")
    plt.legend()

    plt.show()


# =====================
# JUROS COMPOSTOS + INFLAÇÃO
# =====================

def juros_compostos_inflacao():

    C = float(input("Capital inicial: "))
    i = float(input("Taxa de juros (%): ")) / 100

    inflacao = requisicao_inflacao() / 100

    print(f"\nInflação utilizada: {inflacao*100:.2f}%")

    t = int(input("Quantos anos? "))

    M = C

    anos = []
    valores_nominais = []
    valores_reais = []

    print("\n📈 Evolução do investimento (com inflação):")

    for ano in range(1, t + 1):

        M = M * (1 + i)

        valor_real = M / ((1 + inflacao) ** ano)

        anos.append(ano)
        valores_nominais.append(M)
        valores_reais.append(valor_real)

        print(
            f"Ano {ano}: Nominal = R${M:.2f} | Real = R${valor_real:.2f}"
        )

    plt.clf()

    plt.plot(
        anos,
        valores_nominais,
        label="Valor Nominal"
    )

    plt.plot(
        anos,
        valores_reais,
        label="Valor Real (com inflação)"
    )

    plt.title("Investimento: Valor Nominal vs Real")
    plt.xlabel("Anos")
    plt.ylabel("Valor (R$)")
    plt.legend()

    plt.show()


# =====================
# MENU PRINCIPAL
# =====================

def calculadora_financeira():

    while True:

        x = input(
            "\nQual sua modalidade de juros (simples ou compostos)? "
        ).lower()

        if x == "simples":

            juros_simples()

        elif x == "compostos":

            considerar_inf = input(
                "Você deseja considerar inflação? (s/n) "
            ).lower()

            if considerar_inf == "s":

                juros_compostos_inflacao()

            else:

                juros_compostos()

        else:

            print("Opção inválida.")
            continue

        continuar = input(
            "\nDeseja continuar? (s/n) "
        ).lower()

        if continuar == "n":

            print("Obrigado por usar minha calculadora!")
            break


# =====================
# INICIAR PROGRAMA
# =====================

calculadora_financeira()

