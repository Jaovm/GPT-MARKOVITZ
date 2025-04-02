import streamlit as st
import yfinance as yf
import pandas as pd

def get_fundamentals(ticker):
    stock = yf.Ticker(ticker)
    info = stock.info
    
    pe_ratio = info.get('trailingPE', None)
    pb_ratio = info.get('priceToBook', None)
    eps = info.get('epsTrailingTwelveMonths', None)  # Lucro por ação (EPS)
    
    eps_growth = info.get('earningsQuarterlyGrowth', None)
    if eps_growth is not None:
        eps_growth = eps_growth * 100  # Converter para porcentagem
    market_cap = info.get('marketCap', None)
    current_price = info.get('currentPrice', None)
    dividend_yield = info.get('dividendYield', None)
    target_mean_price = info.get('targetMeanPrice', None)  # Preço alvo médio estimado
    sector = info.get('sector', None)  # Setor da empresa
    
    return pe_ratio, pb_ratio, eps, eps_growth, market_cap, current_price, dividend_yield, target_mean_price, sector

def get_additional_data(ticker):
    # Exemplo para pegar dados adicionais, se necessário (não implementado aqui)
    return None, None

def calculate_target_price(eps, pe_ratio_target=15):
    if eps is not None:
        return eps * pe_ratio_target
    return None

def analyze_sector(sector, pe_ratio, pb_ratio, eps_growth, market_cap, current_price, dividend_yield, roe, debt_to_equity, target_price):
    recommendations = []
    price_analysis = ""
    
    if sector == "Financial Services":
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
        if current_price and target_price and current_price < target_price:
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
    elif sector == "Healthcare":
        if pe_ratio and pe_ratio < 15:
            recommendations.append("Recomendação: Ação com P/E atrativo")
        if pb_ratio and pb_ratio < 3:
            recommendations.append("Recomendação: Ação com bom múltiplo P/B")
    elif sector == "Basic Materials":
        if current_price and target_price and current_price < target_price:
            price_analysis = f"Ação está abaixo do preço teto de R${target_price:.2f} - Possível oportunidade"
    else:
        recommendations.append("Setor desconhecido, análise geral será fornecida.")
    
    if current_price and target_price:
        if current_price < target_price:
            price_analysis = f"Ação está abaixo do preço teto de R${target_price:.2f} - Considerada barata para compra"
        else:
            price_analysis = f"Ação está acima do preço teto de R${target_price:.2f} - Evite compra"
    
    return recommendations, price_analysis

def calculate_metrics(ticker):
    stock = yf.Ticker(ticker)
    sector = stock.info.get("sector", "Unknown")
    metrics = {}
    
    # Seleção de métricas por setor
    if sector == "Financial Services":
        metrics["P/B Ratio"] = stock.info.get("priceToBook", "N/A")
        metrics["ROE"] = stock.info.get("returnOnEquity", "N/A")
        metrics["Dividend Yield"] = stock.info.get("dividendYield", "N/A")
    elif sector == "Energy":
        metrics["P/FCF"] = stock.info.get("priceToFreeCashFlows", "N/A")
        metrics["EV/EBITDA"] = stock.info.get("enterpriseToEbitda", "N/A")
        metrics["Debt/EBITDA"] = stock.info.get("debtToEquity", "N/A")
    elif sector == "Technology":
        metrics["P/S Ratio"] = stock.info.get("priceToSalesTrailing12Months", "N/A")
        metrics["Revenue Growth"] = stock.info.get("revenueGrowth", "N/A")
        metrics["Gross Margin"] = stock.info.get("grossMargins", "N/A")
    elif sector == "Consumer Defensive":
        metrics["P/E Ratio"] = stock.info.get("trailingPE", "N/A")
        metrics["Dividend Yield"] = stock.info.get("dividendYield", "N/A")
        metrics["EBITDA Margin"] = stock.info.get("ebitdaMargins", "N/A")
    elif sector == "Healthcare":
        metrics["P/E Ratio"] = stock.info.get("trailingPE", "N/A")
        metrics["P/S Ratio"] = stock.info.get("priceToSalesTrailing12Months", "N/A")
        metrics["R&D Expense"] = stock.info.get("researchAndDevelopmentExpense", "N/A")
    elif sector == "Basic Materials":
        metrics["EV/EBITDA"] = stock.info.get("enterpriseToEbitda", "N/A")
        metrics["P/FCF"] = stock.info.get("priceToFreeCashFlows", "N/A")
        metrics["Production Cost"] = stock.info.get("costOfRevenue", "N/A")
    else:
        metrics["General P/E"] = stock.info.get("trailingPE", "N/A")
    
    return metrics, sector

def main():
    st.title("Análise de Precificação de Ações")
    ticker = st.text_input("Digite o código da ação (ex: PETR4.SA)")
    
    if ticker:
        pe_ratio, pb_ratio, eps, eps_growth, market_cap, current_price, dividend_yield, target_mean_price, sector = get_fundamentals(ticker)
        additional_data = get_additional_data(ticker)  # Exemplo: pode retornar ROE e Debt/Equity se necessário
        # Para este exemplo, vamos supor que ROE e Debt/Equity não foram obtidos, logo serão None.
        roe, debt_to_equity = additional_data
        
        target_price_calculated = calculate_target_price(eps)
        metrics, sector_from_metrics = calculate_metrics(ticker)
        
        st.subheader(f"Setor: {sector if sector else 'Não disponível'}")
        st.write("### Indicadores Fundamentais")
        st.write(pd.DataFrame(list(metrics.items()), columns=["Indicador", "Valor"]))
        
        st.write("### Dados Adicionais")
        st.write(f"P/E Ratio: {pe_ratio}")
        st.write(f"P/B Ratio: {pb_ratio}")
        st.write(f"EPS: {eps}")
        st.write(f"EPS Growth: {eps_growth}%")
        st.write(f"Market Cap: {market_cap}")
        st.write(f"Preço Atual: {current_price}")
        st.write(f"Dividend Yield: {dividend_yield}")
        st.write(f"Preço Alvo Médio (targetMeanPrice): {target_mean_price}")
        st.write(f"Preço Teto Calculado (EPS x 15): {target_price_calculated}")
        
        recommendations, price_analysis = analyze_sector(sector, pe_ratio, pb_ratio, eps_growth, market_cap, current_price, dividend_yield, roe, debt_to_equity, target_price_calculated)
        
        st.write("### Recomendações:")
        for rec in recommendations:
            st.write(f"- {rec}")
        st.write(f"### Análise de Preço Teto:")
        st.success(price_analysis)

if __name__ == "__main__":
    main()
