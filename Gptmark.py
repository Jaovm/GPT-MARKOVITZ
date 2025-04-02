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
    
    return pe_ratio, pb_ratio, eps, eps_growth, market_cap, current_price, dividend_yield, target_mean_price

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

# Função para analisar se a ação está cara ou barata com base nos dados
def analyze_stock(pe_ratio, pb_ratio, eps_growth, market_cap, current_price, dividend_yield, roe, debt_to_equity, target_price):
    # Análise P/E Ratio
    if pe_ratio is None:
        pe_analysis = "P/E Ratio não disponível"
    elif pe_ratio < 15:
        pe_analysis = "Ação está barata (P/E baixo)"
    elif pe_ratio < 25:
        pe_analysis = "P/E está dentro de uma faixa razoável"
    else:
        pe_analysis = "Ação está cara (P/E alto)"
    
    # Análise P/VPA
    if pb_ratio is None:
        pb_analysis = "P/VPA não disponível"
    elif pb_ratio < 1:
        pb_analysis = "Ação está barata (P/VPA baixo)"
    else:
        pb_analysis = "Ação está cara (P/VPA alto)"
    
    # Análise de Crescimento de EPS (Lucros)
    if eps_growth is None:
        growth_analysis = "Crescimento de EPS não disponível"
    elif eps_growth > 10:
        growth_analysis = "Ação tem um bom crescimento de lucros"
    else:
        growth_analysis = "Ação com crescimento moderado ou negativo de lucros"
    
    # Análise de Dividendos (Dividend Yield)
    if dividend_yield is None:
        dividend_analysis = "Dividend Yield não disponível"
    elif dividend_yield > 0.06:
        dividend_analysis = "Ação com bom Dividend Yield"
    else:
        dividend_analysis = "Dividend Yield baixo"
    
    # Análise de ROE
    if roe is None:
        roe_analysis = "ROE não disponível"
    elif roe > 15:
        roe_analysis = "Ação com bom ROE"
    else:
        roe_analysis = "ROE baixo"
    
    # Análise de Dívida/Patrimônio
    if debt_to_equity is None:
        debt_analysis = "Dívida/Patrimônio não disponível"
    elif debt_to_equity < 1:
        debt_analysis = "Ação com boa relação dívida/patrimônio"
    else:
        debt_analysis = "Ação com alta dívida em relação ao patrimônio"
    
    # Mercado e Preço atual
    if market_cap is None or current_price is None:
        market_analysis = "Dados de mercado ou preço não disponíveis"
    else:
        market_analysis = f"Preço atual: R${current_price:.2f} | Capitalização de mercado: R${market_cap/1e9:.2f} bilhões"
    
    # Análise de Preço Teto
    if target_price is None:
        price_analysis = "Preço alvo não disponível"
    elif current_price < target_price:
        price_analysis = f"Ação está abaixo do preço teto (R${target_price:.2f}) - Considerada barata para compra"
    else:
        price_analysis = f"Ação está acima do preço teto (R${target_price:.2f}) - Evitar compra"
    
    return pe_analysis, pb_analysis, growth_analysis, dividend_analysis, roe_analysis, debt_analysis, market_analysis, price_analysis

# Streamlit UI
st.title("Analisador de Ação Brasileira - Barata ou Cara?")

# Input do ticker
ticker = st.text_input("Digite o ticker da ação (exemplo: ITUB4 para Itaú, PETR4 para Petrobras)", "PETR4").upper()

if ticker:
    # Buscar dados fundamentais da ação
    pe_ratio, pb_ratio, eps, eps_growth, market_cap, current_price, dividend_yield, target_price = get_fundamentals(ticker)
    
    # Buscar dados adicionais do Fundamentus (ROE, Dívida/Patrimônio)
    roe, debt_to_equity = get_additional_data(ticker)
    
    # Calcular o preço teto
    target_price_calculated = calculate_target_price(eps)
    
    # Exibir os dados e análise
    st.write(f"**P/E Ratio (Preço/Lucro):** {pe_ratio if pe_ratio else 'Dados não disponíveis'}")
    st.write(f"**P/VPA (Preço/Valor Patrimonial):** {pb_ratio if pb_ratio else 'Dados não disponíveis'}")
    st.write(f"**Crescimento de Lucros (EPS Growth):** {eps_growth if eps_growth else 'Dados não disponíveis'}%")
    st.write(f"**Dividend Yield:** {dividend_yield if dividend_yield else 'Dados não disponíveis'}")
    st.write(f"**Capitalização de Mercado:** {market_cap if market_cap else 'Dados não disponíveis'}")
    
    st.write("\n### Análise Completa")
    pe_analysis, pb_analysis, growth_analysis, dividend_analysis, roe_analysis, debt_analysis, market_analysis, price_analysis = analyze_stock(pe_ratio, pb_ratio, eps_growth, market_cap, current_price, dividend_yield, roe, debt_to_equity, target_price_calculated)
    st.write(f"**Análise P/E Ratio:** {pe_analysis}")
    st.write(f"**Análise P/VPA:** {pb_analysis}")
    st.write(f"**Análise de Crescimento dos Lucros:** {growth_analysis}")
    st.write(f"**Análise de Dividendos:** {dividend_analysis}")
    st.write(f"**Análise de ROE:** {roe_analysis}")
    st.write(f"**Análise de Dívida/Patrimônio:** {debt_analysis}")
    st.write(f"**Análise de Mercado e Preço Atual:** {market_analysis}")
    st.write(f"**Análise de Preço Teto:** {price_analysis}")
