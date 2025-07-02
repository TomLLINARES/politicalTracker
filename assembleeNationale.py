import pandas as pd

addr = 'deputes-active.csv'

df = pd.read_csv(addr, sep=';', encoding='utf-8')

# Affiche les 5 premières lignes
print(df.head())

# Liste des colonnes
print(df.columns.tolist())

