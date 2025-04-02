import streamlit as st import yfinance as yf import pandas as pd

def get_stock_data(ticker): stock = yf.Ticker(ticker) return stock.history(period="5y")

def calculate_metrics(ticker): stock = yf.Ticker(ticker) sector = stock.info.get("sector", "Unknown") metrics = {}

# Dados financeiros
try:
    financials = stock.financials
    balance_sheet = stock.balance_sheet
    cash_flow = stock.cashflow
except:
    st.error("Erro ao buscar dados financeiros")
    return None

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

def main(): st.title("Análise de Precificação de Ações") ticker = st.text_input("Digite o código da ação (ex: PETR4.SA)")

if ticker:
    metrics, sector = calculate_metrics(ticker)
    if metrics:
        st.subheader(f"Setor: {sector}")
        st.write("### Indicadores Financeiros")
        st.write(pd.DataFrame(metrics.items(), columns=["Indicador", "Valor"]))

        # Lógica de recomendação básica
        recommendation = ""
        if sector == "Technology" and metrics.get("P/S Ratio", 0) < 5:
            recommendation = "A ação pode estar barata."
        elif sector == "Energy" and metrics.get("EV/EBITDA", 10) < 5:
            recommendation = "A ação pode estar subvalorizada."
        elif sector == "Financial Services" and metrics.get("P/B Ratio", 1.5) < 1:
            recommendation = "A ação pode estar barata."
        elif sector == "Healthcare" and metrics.get("P/E Ratio", 20) < 15:
            recommendation = "A ação pode estar barata."
        else:
            recommendation = "Não há sinais claros de subvalorização."

        st.write("### Recomendação: ")
        st.success(recommendation)

if name == "main": main()

