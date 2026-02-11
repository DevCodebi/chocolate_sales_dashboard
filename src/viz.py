import pandas as pd
import matplotlib.pyplot as plt

def plot_numeric_hist(df: pd.DataFrame, col: str, bins: int = 30) -> None:
    s = df[col].dropna()
    plt.figure()
    plt.hist(s, bins=bins)
    plt.title(f"Histograma: {col}")
    plt.xlabel(col)
    plt.ylabel("Frequência")
    plt.show()
