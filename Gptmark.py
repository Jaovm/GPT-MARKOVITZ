import streamlit as st
import yfinance as yf
import pandas as pd

def get_fundamentals(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    
    pe_ratio = info.get('trailingPE', None)
    pb_ratio = info.get('priceToBook', None)
    eps = info.get('epsTrailingTwelveMonths', None)
    eps_growth = info.get('earningsQuarterlyGrowth', None)
    
    if eps_growth is not None:
        eps_growth *= 100
    
    market_cap = info.get('marketCap', None)
    current_price = info.get('currentPrice', None)
    dividend_yield = info.get('dividendYield', None)
    target_mean_price = info.get('targetMeanPrice', None)
    sector = info.get('sector', None)
    
    return pe_ratio, pb_ratio, eps, eps_growth, market_cap, current_price, dividend_yield, target_mean_price, sector

def calculate_fair_price(sector, pe_ratio, pb_ratio, eps, roe):
    if sector == "Financial Services" and pb_ratio and roe:
        return pb_ratio * roe * 10
    elif pe_ratio and eps:
        return pe_ratio * eps
    return None

def main():
    st.title("Análise de Precificação de Ações")
    ticker = st.text_input("Digite o código da ação (ex: PETR4.SA)")
    
    if ticker:
        pe_ratio, pb_ratio, eps, eps_growth, market_cap, current_price, dividend_yield, target_mean_price, sector = get_fundamentals(ticker)
        fair_price = calculate_fair_price(sector, pe_ratio, pb_ratio, eps, pe_ratio)
        
        st.subheader(f"Setor: {sector if sector else 'Não disponível'}")
        st.write(f"Preço Justo Estimado: {fair_price if fair_price else 'Não disponível'}")
        st.write(f"Preço Atual: {current_price}")
        st.write(f"P/E Ratio: {pe_ratio}")
        st.write(f"P/B Ratio: {pb_ratio}")
        st.write(f"EPS: {eps}")
        st.write(f"Crescimento EPS: {eps_growth}%")
        st.write(f"Market Cap: {market_cap}")
        st.write(f"Dividend Yield: {dividend_yield}")
        st.write(f"Preço Alvo Médio: {target_mean_price}")

if __name__ == "__main__":
    main()
