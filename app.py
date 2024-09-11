import streamlit as st
import pandas as pd

# Função para calcular a probabilidade com base nas vitórias, empates e derrotas
def calcular_probabilidade(vitorias, empates, derrotas):
    total_jogos = vitorias + empates + derrotas
    prob_vitoria = vitorias / total_jogos if total_jogos > 0 else 0
    prob_empate = empates / total_jogos if total_jogos > 0 else 0
    prob_derrota = derrotas / total_jogos if total_jogos > 0 else 0
    return prob_vitoria, prob_empate, prob_derrota

# Função para calcular a odd decimal a partir da probabilidade
def calcular_odd_decimal(probabilidade):
    return 1 / probabilidade if probabilidade > 0 else float('inf')

# Função para determinar se é uma aposta +EV no mercado 1X2
def avaliar_ev(odd_input, odd_calculada):
    return "Aposta +EV" if odd_calculada < odd_input else "Não Apostar -EV"

# Função para calcular +EV no mercado DNB
def avaliar_ev_dnb(odd_dnb_input, prob_vitoria, prob_empate, prob_derrota):
    # Fórmula ajustada para DNB (considerando devolução em caso de empate)
    ev_dnb = (prob_vitoria * (odd_dnb_input - 1)) + (prob_empate * 0) + (prob_derrota * -1)
    return "+EV" if ev_dnb > 0 else "-EV"

# Interface com o Streamlit
st.title("Calculadora de Aposta de Valor (+EV)")

# Entradas do usuário para as odds das casas de apostas
st.header("Insira as Odds das Casas de Apostas:")
odd_casa = st.number_input("Odd da Casa", min_value=1.01, step=0.01)
odd_empate = st.number_input("Odd do Empate", min_value=1.01, step=0.01)
odd_visitante = st.number_input("Odd do Visitante", min_value=1.01, step=0.01)
odd_dnb_casa = st.number_input("Odd DNB (Casa)", min_value=1.01, step=0.01)
odd_1x = st.number_input("Odd 1X (Casa ou Empate)", min_value=1.01, step=0.01)

# Entradas para o desempenho do time da casa e do visitante
st.header("Desempenho nos últimos 10 jogos casa:")

vitorias_casa_casa = st.number_input("Vitórias (Casa/Casa)", min_value=0, max_value=10, step=1)
empates_casa_casa = st.number_input("Empates (Casa/Casa)", min_value=0, max_value=10, step=1)
derrotas_casa_casa = st.number_input("Derrotas (Casa/Casa)", min_value=0, max_value=10, step=1)

st.header("Desempenho nos últimos 10 jogos fora:")

vitorias_fora_fora = st.number_input("Vitórias (Fora/Fora)", min_value=0, max_value=10, step=1)
empates_fora_fora = st.number_input("Empates (Fora/Fora)", min_value=0, max_value=10, step=1)
derrotas_fora_fora = st.number_input("Derrotas (Fora/Fora)", min_value=0, max_value=10, step=1)

# H2H dos últimos 5 jogos entre as equipes
st.header("Últimos 5 jogos entre as equipes (H2H):")
vitorias_h2h = st.number_input("Vitórias da Casa", min_value=0, max_value=5, step=1)
empates_h2h = st.number_input("Empates", min_value=0, max_value=5, step=1)
derrotas_h2h = st.number_input("Vitórias do Visitante", min_value=0, max_value=5, step=1)

# Cálculos das probabilidades médias
prob_casa_casa, prob_empate_casa, prob_derrota_casa = calcular_probabilidade(vitorias_casa_casa, empates_casa_casa, derrotas_casa_casa)
prob_fora_fora, prob_empate_fora_fora, prob_derrota_fora_fora = calcular_probabilidade(vitorias_fora_fora, empates_fora_fora, derrotas_fora_fora)
prob_h2h_casa, prob_h2h_empate, prob_h2h_fora = calcular_probabilidade(vitorias_h2h, empates_h2h, derrotas_h2h)

# Média ponderada das probabilidades
prob_total_casa = (prob_casa_casa + prob_h2h_casa) / 2
prob_total_empate = (prob_empate_casa + prob_h2h_empate) / 2
prob_total_fora = (prob_derrota_casa + prob_h2h_fora) / 2

# Cálculo das odds decimais
odd_calculada_casa = calcular_odd_decimal(prob_total_casa)
odd_calculada_empate = calcular_odd_decimal(prob_total_empate)
odd_calculada_fora = calcular_odd_decimal(prob_total_fora)

# Cálculo dos mercados especiais
prob_dnb = prob_total_casa  # DNB (Draw No Bet) considera apenas a vitória do time da casa
prob_1x = prob_total_casa + prob_total_empate  # Probabilidade de 1X (Casa ou Empate)

# Cálculo das odds para os mercados especiais
odd_calculada_dnb = calcular_odd_decimal(prob_dnb)
odd_calculada_1x = calcular_odd_decimal(prob_1x)

# Exibição dos resultados
st.header("Odds Calculadas com base nas Probabilidades:")
st.write(f"Odd da Casa: {odd_calculada_casa:.2f}")
st.write(f"Odd do Empate: {odd_calculada_empate:.2f}")
st.write(f"Odd do Visitante: {odd_calculada_fora:.2f}")
st.write(f"Odd DNB (Casa): {odd_calculada_dnb:.2f}")
st.write(f"Odd 1X (Casa ou Empate): {odd_calculada_1x:.2f}")

# Avaliação de +EV para os mercados 1x2, DNB e 1X
avaliacao_mercados = {
    "Mercado": ["1x2 Casa", "1x2 Empate", "1x2 Visitante", "DNB Casa", "1X (Casa ou Empate)"],
    "Odd Calculada": [f"{odd_calculada_casa:.2f}", f"{odd_calculada_empate:.2f}", f"{odd_calculada_fora:.2f}", f"{odd_calculada_dnb:.2f}", f"{odd_calculada_1x:.2f}"],
    "Odd Informada": [f"{odd_casa:.2f}", f"{odd_empate:.2f}", f"{odd_visitante:.2f}", f"{odd_dnb_casa:.2f}", f"{odd_1x:.2f}"],
    "Aposta +EV": [
        avaliar_ev(odd_casa, odd_calculada_casa),
        avaliar_ev(odd_empate, odd_calculada_empate),
        avaliar_ev(odd_visitante, odd_calculada_fora),
        avaliar_ev_dnb(odd_dnb_casa, prob_total_casa, prob_total_empate, prob_total_fora),
        avaliar_ev(odd_1x, odd_calculada_1x)
    ]
}

# Exibir a tabela de avaliação de valor
df_avaliacao = pd.DataFrame(avaliacao_mercados)
st.header("Avaliação de Valor dos Mercados:")
st.table(df_avaliacao)
