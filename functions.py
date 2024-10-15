import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 1. Función para importar los datos históricos
def importar_datos(empresas, inicio, fin, intervalo="1d"):
    """
    Descarga los datos históricos de las empresas en la lista.
    
    :param empresas: Listado de tickers de las empresas.
    :param inicio: Fecha de inicio en formato 'YYYY-MM-DD'.
    :param fin: Fecha de fin en formato 'YYYY-MM-DD'.
    :param intervalo: Intervalo de tiempo de los datos ('1d', '1wk', '1mo', etc).
    :return: DataFrame con los precios ajustados.
    """
    data = yf.download(empresas, start=inicio, end=fin, interval=intervalo)
    precios_cierre = data['Adj Close']
    return precios_cierre

# 2. Función para calcular la rentabilidad de la cartera
def calcular_rentabilidad(precios_cierre, capital_inicial=100000):
    """
    Calcula la rentabilidad diaria de la cartera con inversión equitativa.
    
    :param precios_cierre: DataFrame con precios de cierre ajustados.
    :param capital_inicial: Capital inicial invertido en la cartera.
    :return: Serie con la rentabilidad diaria de la cartera.
    """
    n_empresas = precios_cierre.shape[1]  # Número de empresas en la cartera
    peso_cartera = 1 / n_empresas  # Inversión equitativa por empresa
    inversion_por_empresa = capital_inicial * peso_cartera

    # Calcular la rentabilidad diaria
    rentabilidad_diaria = precios_cierre.pct_change().dropna()

    # Multiplicar por los pesos de la cartera
    rentabilidad_cartera = rentabilidad_diaria.dot([peso_cartera] * n_empresas)

    return rentabilidad_cartera

# 3. Función para calcular los indicadores financieros
def calcular_indicadores(rentabilidad_cartera, dias_trading=252, rendimiento_sin_riesgo=0.01):
    """
    Calcula los principales indicadores financieros de la cartera.
    
    :param rentabilidad_cartera: Serie con la rentabilidad diaria de la cartera.
    :param dias_trading: Número de días de trading en un año (por defecto 252).
    :param rendimiento_sin_riesgo: Tasa de retorno sin riesgo anual.
    :return: DataFrame con indicadores de rentabilidad anualizada, volatilidad y ratio de Sharpe.
    """
    # Rentabilidad anualizada
    rentabilidad_anualizada = (1 + rentabilidad_cartera.mean()) ** dias_trading - 1

    # Volatilidad anualizada (desviación estándar)
    volatilidad_anualizada = rentabilidad_cartera.std() * np.sqrt(dias_trading)

    # Ratio de Sharpe
    sharpe_ratio = (rentabilidad_anualizada - rendimiento_sin_riesgo) / volatilidad_anualizada

    # Retorno acumulado total
    retorno_acumulado = (rentabilidad_cartera + 1).prod() - 1

    # Máximo drawdown (pérdida máxima en un período)
    wealth_index = (1 + rentabilidad_cartera).cumprod()  # Valor acumulado
    previous_peaks = wealth_index.cummax()
    drawdown = (wealth_index - previous_peaks) / previous_peaks
    max_drawdown = drawdown.min()

    # Crear un DataFrame con los indicadores
    df_indicadores = pd.DataFrame({
        'Rentabilidad Anualizada': [rentabilidad_anualizada],
        'Volatilidad Anualizada': [volatilidad_anualizada],
        'Ratio de Sharpe': [sharpe_ratio],
        'Retorno Acumulado': [retorno_acumulado],
        'Máximo Drawdown': [max_drawdown]
    })

    return df_indicadores

# 4. Función para graficar la evolución de la cartera y las acciones
def graficar_rentabilidad_cartera(rentabilidad_cartera):
    """
    Genera gráficos de la evolución histórica de la cartera y de las acciones individuales.
    
    :param precios_cierre: DataFrame con los precios de cierre ajustados.
    :param rentabilidad_cartera: Serie con la rentabilidad diaria de la cartera.
    """
    # Gráfico de la evolución de la rentabilidad acumulada de la cartera
    plt.figure(figsize=(10, 6))
    plt.plot((1 + rentabilidad_cartera).cumprod(), label="Cartera", color='blue')
    plt.title('Evolución de la Rentabilidad Acumulada de la Cartera')
    plt.xlabel('Fecha')
    plt.ylabel('Rentabilidad Acumulada')
    plt.legend()
    plt.grid(True)
    plt.show()
def graficar_precios_cierre(precios_cierre):
    # Gráfico de la evolución de los precios de cierre de cada empresa
    plt.figure(figsize=(10, 6))
    for empresa in precios_cierre.columns:
        plt.plot(precios_cierre[empresa], label=empresa)
    plt.title('Evolución de los Precios de las Acciones')
    plt.xlabel('Fecha')
    plt.ylabel('Precio de Cierre Ajustado')
    plt.legend(loc='best')
    plt.grid(True)
    plt.show()


