# DCA Simulator

Simulador histórico de DCA para activos financieros usando datos de Yahoo Finance.

## Versión actual

v0.1 - Basic DCA simulator with CAGR and max drawdown

## Funciones

- Simulación DCA mensual
- Soporte para tickers de Yahoo Finance:
  - SPY
  - QQQ
  - AAPL
  - BTC-USD
  - GLD
  - Cualquier valor en YahooFinance, utilizando el TICKER correcto
- Entrada interactiva por terminal
- Cálculo de:
  - capital total invertido
  - valor final
  - rentabilidad total
  - CAGR aproximado
  - drawdown máximo de cartera
  - unidades acumuladas
- Gráfico de capital aportado vs valor de cartera

-Despues te pide si quieres exportar un CSV para comprobarlo con numeros y jugar ocn las graficas,,,
Esta optimizado par apoder gestionarlo desde excel en ESPAÑA.

## Instalación

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt

```md
## Uso

```bash
python main.py

## Ejemplo

Ticker: SPY
Fecha inicial: 1997-01-01
Fecha final: 2008-12-31
Aportación mensual: 100

## Roadmap

- v0.2 - DCA reforzado por caídas
- v0.3 - Comparador de activos
- v0.4 - Refactor del código
- v0.5 - Exportación de resultados
- v0.6 - Interfaz web