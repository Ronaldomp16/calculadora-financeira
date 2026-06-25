#import matplotlib.pyplot as plt
import requests

# =====================================
# REQUISIÇÃO DA INFLAÇÃO (BANCO CENTRAL)
# =====================================

def requisicao_inflacao():

    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=json"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        dados = response.json()
        return float(dados[-1]["valor"]), False

    except:
        return 4.0, True #faalback para 4% de inflação caso a requisição falhe
    


# =====================
# JUROS SIMPLES
# =====================

def juros_simples(C, i, t):

    anos = []
    valores = []

    for ano in range(1, t + 1):

        M = C * (1 + i * ano)

        anos.append(ano)
        valores.append(M)

    return anos, valores

# =====================
# JUROS COMPOSTOS
# =====================

def juros_compostos(C, i, t):

    anos = []
    valores = []

    M = C

    for ano in range(1, t + 1):

        M *= (1 + i)
        anos.append(ano)
        valores.append(M)

    return anos, valores

# =====================
# JUROS COMPOSTOS + INFLAÇÃO
# =====================

def juros_compostos_inflacao(C, i, t):

    inflacao, fallback = requisicao_inflacao()
    inflacao = inflacao / 100

    anos = []
    nominal = []
    real = []

    M = C

    for ano in range(1, t + 1):

        M *= (1 + i)

        valor_real = M / ((1 + inflacao) ** ano)

        anos.append(ano)
        nominal.append(M)
        real.append(valor_real)

    return anos, nominal, real, inflacao, fallback

def juros_compostos_aporte(C, i, t, aporte):
    anos = []
    valores = []

    M = C

    for ano in range(1, t + 1):

        M *= (1 + i)
        M += aporte * 12  # Adiciona o aporte anual

        anos.append(ano)
        valores.append(M)

    return anos, valores
