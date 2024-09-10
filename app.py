import streamlit as st

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

# Função para determinar se é uma aposta +EV
def avaliar_ev(odd_input, odd_calculada):
    return "Aposta +EV" if odd_calculada < odd_input else "Não Apostar -EV"

# Interface com o Streamlit
st.title("Calculadora de Aposta de Valor (+EV)")

# Entradas do usuário para as odds das casas de apostas
st.header("Insira as Odds das Casas de Apostas:")
odd_casa = st.number_input("Odd da Casa", min_value=1.01, step=0.01)
odd_empate = st.number_input("Odd do Empate", min_value=1.01, step=0.01)
odd_visitante = st.number_input("Odd do Visitante", min_value=1.01, step=0.01)

# Entradas para o desempenho do time da casa e do visitante
st.header("Desempenho nos últimos 10 jogos:")
vitorias_casa_fora = st.number_input("Vitórias (Casa/Fora)", min_value=0, max_value=10, step=1)
empates_casa_fora = st.number_input("Empates (Casa/Fora)", min_value=0, max_value=10, step=1)
derrotas_casa_fora = st.number_input("Derrotas (Casa/Fora)", min_value=0, max_value=10, step=1)

vitorias_casa_casa = st.number_input("Vitórias (Casa/Casa)", min_value=0, max_value=10, step=1)
empates_casa_casa = st.number_input("Empates (Casa/Casa)", min_value=0, max_value=10, step=1)
derrotas_casa_casa = st.number_input("Derrotas (Casa/Casa)", min_value=0, max_value=10, step=1)

vitorias_fora_fora = st.number_input("Vitórias (Fora/Fora)", min_value=0, max_value=10, step=1)
empates_fora_fora = st.number_input("Empates (Fora/Fora)", min_value=0, max_value=10, step=1)
derrotas_fora_fora = st.number_input("Derrotas (Fora/Fora)", min_value=0, max_value=10, step=1)

# H2H dos últimos 5 jogos entre as equipes
st.header("Últimos 5 jogos entre as equipes (H2H):")
vitorias_h2h = st.number_input("Vitórias da Casa", min_value=0, max_value=5, step=1)
empates_h2h = st.number_input("Empates", min_value=0, max_value=5, step=1)
derrotas_h2h = st.number_input("Vitórias do Visitante", min_value=0, max_value=5, step=1)

# Cálculos das probabilidades médias
prob_casa_fora, prob_empate_fora, prob_derrota_fora = calcular_probabilidade(vitorias_casa_fora, empates_casa_fora, derrotas_casa_fora)
prob_casa_casa, prob_empate_casa, prob_derrota_casa = calcular_probabilidade(vitorias_casa_casa, empates_casa_casa, derrotas_casa_casa)
prob_fora_fora, prob_empate_fora_fora, prob_derrota_fora_fora = calcular_probabilidade(vitorias_fora_fora, empates_fora_fora, derrotas_fora_fora)
prob_h2h_casa, prob_h2h_empate, prob_h2h_fora = calcular_probabilidade(vitorias_h2h, empates_h2h, derrotas_h2h)

# Média ponderada das probabilidades
prob_total_casa = (prob_casa_fora + prob_casa_casa + prob_h2h_casa) / 3
prob_total_empate = (prob_empate_fora + prob_empate_casa + prob_h2h_empate) / 3
prob_total_fora = (prob_derrota_fora + prob_derrota_casa + prob_h2h_fora) / 3

# Cálculo das odds decimais
odd_calculada_casa = calcular_odd_decimal(prob_total_casa)
odd_calculada_empate = calcular_odd_decimal(prob_total_empate)
odd_calculada_fora = calcular_odd_decimal(prob_total_fora)

# Exibição dos resultados
st.header("Odds Calculadas com base nas Probabilidades:")
st.write(f"Odd da Casa: {odd_calculada_casa:.2f}")
st.write(f"Odd do Empate: {odd_calculada_empate:.2f}")
st.write(f"Odd do Visitante: {odd_calculada_fora:.2f}")

# Avaliação de +EV
st.header("Avaliação de Valor:")
resultado_casa = avaliar_ev(odd_casa, odd_calculada_casa)
resultado_empate = avaliar_ev(odd_empate, odd_calculada_empate)
resultado_fora = avaliar_ev(odd_visitante, odd_calculada_fora)

st.write(f"Aposta na Casa: {resultado_casa}")
st.write(f"Aposta no Empate: {resultado_empate}")
st.write(f"Aposta no Visitante: {resultado_fora}")
