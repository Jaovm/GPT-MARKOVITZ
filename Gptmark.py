import yfinance as yf
import streamlit as st
import requests
from bs4 import BeautifulSoup

# Função para buscar dados financeiros no Yahoo Finance
def get_fundamentals(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    
    # Retorna os dados que vamos usar
    pe_ratio = info.get('trailingPE', None)
    pb_ratio = info.get('priceToBook', None)
    eps = info.get('epsTrailingTwelveMonths', None)  # Lucro por ação (EPS)
    eps_growth = info.get('earningsQuarterlyGrowth', None) * 100  # EPS Growth em %
    market_cap = info.get('marketCap', None)
    current_price = info.get('currentPrice', None)
    dividend_yield = info.get('dividendYield', None)
    target_mean_price = info.get('targetMeanPrice', None)  # Preço alvo médio estimado
    sector = info.get('sector', None)  # Setor da empresa
    
    return pe_ratio, pb_ratio, eps, eps_growth, market_cap, current_price, dividend_yield, target_mean_price, sector

# Função para buscar dados adicionais do Fundamentus (ex: ROE e Dívida/Patrimônio)
def get_additional_data(ticker):
    url = f'https://www.fundamentus.com.br/detalhes.php?papel={ticker}'
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    try:
        roe = soup.find(text="ROE").find_next('td').text.strip().replace(",", ".")
        debt_to_equity = soup.find(text="Dívida/Patrimônio").find_next('td').text.strip().replace(",", ".")
        return float(roe), float(debt_to_equity)
    except AttributeError:
        return None, None

# Função para calcular o preço teto
def calculate_target_price(eps, pe_ratio_target=15):
    if eps is not None:
        target_price = eps * pe_ratio_target
        return target_price
    return None

# Função para realizar a análise de acordo com o setor
def analyze_sector(sector, pe_ratio, pb_ratio, eps_growth, market_cap, current_price, dividend_yield, roe, debt_to_equity, target_price):
    recommendations = []
    price_analysis = ""
    
    if sector == "Financials":
        if pe_ratio and pe_ratio < 15:
            recommendations.append("Recomendação de compra: Ação subvalorizada (P/E baixo)")
        if roe and roe > 15:
            recommendations.append("Recomendação: Ação com bom ROE")
        if debt_to_equity and debt_to_equity < 1:
            recommendations.append("Recomendação: Ação com boa relação dívida/patrimônio")

    elif sector == "Energy":
        if eps_growth and eps_growth > 5:
            recommendations.append("Recomendação: Ação com bom crescimento de lucros")
        if pe_ratio and pe_ratio < 10:
            recommendations.append("Recomendação de compra: Ação subvalorizada no setor de energia")
        if current_price < target_price:
            price_analysis = f"Ação está abaixo do preço teto de R${target_price:.2f} - Considerada barata para compra"

    elif sector == "Technology":
        if eps_growth and eps_growth > 15:
            recommendations.append("Recomendação: Ação com bom crescimento (EPS > 15%)")
        if pb_ratio and pb_ratio < 5:
            recommendations.append("Recomendação: Ação com bom múltiplo P/B")

    elif sector == "Consumer Defensive":
        if dividend_yield and dividend_yield > 0.05:
            recommendations.append("Recomendação: Ação com bom Dividend Yield")
        if roe and roe > 20:
            recommendations.append("Recomendação: Ação com excelente retorno sobre patrimônio")

    else:
        recommendations.append("Setor desconhecido, análise geral será fornecida.")
    
    # Recomendações de preço teto
    if current_price < target_price:
        price_analysis = f"Ação está abaixo do preço teto de R${target_price:.2f} - Considerada barata para compra"
    else:
        price_analysis = f"Ação está acima do preço teto de R${target_price:.2f} - Evite compra"
    
    return recommendations, price_analysis

# Streamlit UI
st.title("Analisador de Ação Brasileira - Análise Setorial")

# Input do ticker
ticker = st.text_input("Digite o ticker da ação (exemplo: ITUB4 para Itaú, PETR4 para Petrobras)", "PETR4").upper()

if ticker:
    # Buscar dados fundamentais da ação
    pe_ratio, pb_ratio, eps, eps_growth, market_cap, current_price, dividend_yield, target_price, sector = get_fundamentals(ticker)
    
    # Buscar dados adicionais do Fundamentus (ROE, Dívida/Patrimônio)
    roe, debt_to_equity = get_additional_data(ticker)
    
    # Calcular o preço teto
    target_price_calculated = calculate_target_price(eps)
    
    # Exibir os dados e análise
    st.write(f"**Setor:** {sector if sector else 'Não disponível'}")
    st.write(f"**P/E Ratio (Preço/Lucro):** {pe_ratio if pe_ratio else 'Dados não disponíveis'}")
    st.write(f"**P/VPA (Preço/Valor Patrimonial):** {pb_ratio if pb_ratio else 'Dados não disponíveis'}")
    st.write(f"**Crescimento de Lucros (EPS Growth):** {eps_growth if eps_growth else 'Dados não disponíveis'}%")
    st.write(f"**Dividend Yield:** {dividend_yield if dividend_yield else 'Dados não disponíveis'}")
    st.write(f"**Capitalização de Mercado:** {market_cap if market_cap else 'Dados não disponíveis'}")
    
    st.write("\n### Análise Completa")
    recommendations, price_analysis = analyze_sector(sector, pe_ratio, pb_ratio, eps_growth, market_cap, current_price, dividend_yield, roe, debt_to_equity, target_price_calculated)
    
    for rec in recommendations:
        st.write(f"**{rec}**")
    st.write(f"**Análise de Preço Teto:** {price_analysis}")
