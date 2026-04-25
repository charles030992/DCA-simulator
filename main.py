import os

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt


def get_monthly_prices(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)

    if data.empty:
        raise ValueError("No se han encontrado datos para ese ticker o rango de fechas.")

    if isinstance(data.columns, pd.MultiIndex):
        prices = data[("Close", ticker)].dropna()
    else:
        prices = data["Close"].dropna()

    return prices.resample("ME").last()


def calculate_max_drawdown(values):
    series = pd.Series(values)
    running_max = series.cummax()
    drawdowns = (series / running_max) - 1
    return drawdowns.min() * 100


def calculate_cagr(final_value, total_invested, start_date, end_date):
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    years = (end - start).days / 365.25

    if years <= 0:
        return 0

    return ((final_value / total_invested) ** (1 / years) - 1) * 100


def simulate_dca(ticker, start_date, end_date, monthly_investment):
    monthly_prices = get_monthly_prices(ticker, start_date, end_date)

    total_invested = 0
    shares = 0
    portfolio_values = []
    invested_values = []
    shares_values = []

    for date, price in monthly_prices.items():
        shares_bought = monthly_investment / price
        shares += shares_bought
        total_invested += monthly_investment

        portfolio_value = shares * price

        portfolio_values.append(portfolio_value)
        invested_values.append(total_invested)
        shares_values.append(shares)

    final_value = portfolio_values[-1]
    total_return = (final_value / total_invested - 1) * 100
    cagr = calculate_cagr(final_value, total_invested, start_date, end_date)
    max_drawdown = calculate_max_drawdown(portfolio_values)

    print("\n--- RESULTADO DCA v0.1 ---")
    print(f"Activo: {ticker}")
    print(f"Periodo: {start_date} → {end_date}")
    print(f"Aportación mensual: ${monthly_investment:.2f}")
    print(f"Invertido total: ${total_invested:.2f}")
    print(f"Valor final: ${final_value:.2f}")
    print(f"Rentabilidad total: {total_return:.2f}%")
    print(f"CAGR aproximado: {cagr:.2f}%")
    print(f"Drawdown máximo cartera: {max_drawdown:.2f}%")
    print(f"Unidades acumuladas: {shares:.6f}")

    results_df = pd.DataFrame({
        "Fecha": monthly_prices.index,
        "Precio": monthly_prices.values,
        "Aportado_Mes": [monthly_investment] * len(monthly_prices),
        "Capital_Acumulado": invested_values,
        "Unidades_Acumuladas": shares_values,
        "Valor_Cartera": portfolio_values,
    })

    plt.figure(figsize=(10, 5))
    plt.plot(monthly_prices.index, portfolio_values, label="Valor cartera")
    plt.plot(monthly_prices.index, invested_values, label="Capital aportado")
    plt.legend()
    plt.title(f"DCA en {ticker}: {start_date} a {end_date}")
    plt.xlabel("Fecha")
    plt.ylabel("Valor ($)")
    plt.grid()
    plt.show()

    return results_df


def export_csv(df, ticker, start_date, end_date):
    os.makedirs("outputs", exist_ok=True)

    filename = f"outputs/{ticker}_{start_date}_{end_date}.csv"

    df.to_csv(
        filename,
        index=False,
        sep=";",
        decimal=",",
        encoding="utf-8-sig",
        float_format="%.6f"
    )

    print(f"CSV guardado como: {filename}")


def main():
    print("=== DCA SIMULATOR v0.1 ===")
    print("Ejemplos de ticker: SPY, BTC-USD, QQQ, GLD, AAPL")

    while True:
        ticker = input("\nTicker: ").strip().upper()
        start_date = input("Fecha inicial (YYYY-MM-DD): ").strip()
        end_date = input("Fecha final (YYYY-MM-DD): ").strip()
        monthly_investment = float(input("Aportación mensual en USD: ").strip())

        try:
            results_df = simulate_dca(ticker, start_date, end_date, monthly_investment)

            export = input("\n¿Quieres exportar CSV con los datos del gráfico? (s/n): ").strip().lower()
            if export == "s":
                export_csv(results_df, ticker, start_date, end_date)

        except Exception as e:
            print(f"\nError: {e}")

        again = input("\n¿Quieres hacer otra simulación? (s/n): ").strip().lower()
        if again != "s":
            print("Programa finalizado.")
            break


if __name__ == "__main__":
    main()