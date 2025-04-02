import streamlit as st 
import yfinance as yf 
import pandas as pd

def get_fundamentals(ticker): stock = yf.Ticker(ticker) info = stock.info

pe_ratio = info.get('trailingPE', None)
pb_ratio = info.get('priceToBook', None)
eps = info.get('epsTrailingTwelveMonths', None)
eps_growth = info.get('earningsQuarterlyGrowth', None)
if eps_growth is not None:
    eps_growth = eps_growth * 100
market_cap = info.get('marketCap', None)
current_price = info.get('currentPrice', None)
dividend_yield = info.get('dividendYield', None)
target_mean_price = info.get('targetMeanPrice', None)
sector = info.get('sector', None)
roe = info.get('returnOnEquity', None)

return pe_ratio, pb_ratio, eps, eps_growth, market_cap, current_price, dividend_yield, target_mean_price, sector, roe

def calculate_fair_price(sector, pb_ratio, pe_ratio, eps, roe): if sector == "Financial Services" and pb_ratio and roe: return pb_ratio * roe * 10  # Exemplo de precificação baseada em P/B e ROE elif pe_ratio and eps: return eps * pe_ratio  # Multiplicando EPS pelo P/E médio como proxy para valor justo return None

def main(): st.title("Análise de Precificação de Ações") ticker = st.text_input("Digite o código da ação (ex: PETR4.SA)")

if ticker:
    pe_ratio, pb_ratio, eps, eps_growth, market_cap, current_price, dividend_yield, target_mean_price, sector, roe = get_fundamentals(ticker)
    fair_price = calculate_fair_price(sector, pb_ratio, pe_ratio, eps, roe)
    
    st.write(f"### Setor: {sector if sector else 'Não disponível'}")
    st.write(f"P/E Ratio: {pe_ratio}")
    st.write(f"P/B Ratio: {pb_ratio}")
    st.write(f"EPS: {eps}")
    st.write(f"EPS Growth: {eps_growth}%")
    st.write(f"Market Cap: {market_cap}")
    st.write(f"Preço Atual: {current_price}")
    st.write(f"Dividend Yield: {dividend_yield}")
    st.write(f"Preço Alvo Médio (targetMeanPrice): {target_mean_price}")
    st.write(f"ROE: {roe}")
    
    if fair_price:
        st.success(f"Preço Justo Estimado: R${fair_price:.2f}")
    else:
        st.warning("Não foi possível calcular o preço justo.")

if name == "main": main()

