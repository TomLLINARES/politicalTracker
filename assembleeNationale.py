import pandas as pd
import argparse
import matplotlib.pyplot as plt
plt.show()


addr = 'deputes-active.csv'


df = pd.read_csv(addr, sep=',', encoding='utf-8')


parser = argparse.ArgumentParser(description="Filtrer les députés par groupe, département ou circonscription.")
parser.add_argument("-g", "--groupe", help="Sigle du groupe parlementaire (ex: LFI-NFP, RN, DR...)")
parser.add_argument("-d", "--departement", help="Nom complet du département (ex: Yvelines)")
parser.add_argument("-c", "--circo", type=int, help="Numéro de la circonscription dans le département")
parser.add_argument("-v", "--visual", action="store_true", help="Affiche un graphique de la repartition en fonction du critere choisi")
parser.add_argument("-n", "--nom", type=str, help="Recherche un depute par son nom")

args = parser.parse_args()

resultat = df.copy()

if args.groupe:
    resultat = resultat[resultat["groupeAbrev"] == args.groupe]

if args.departement:
    resultat = resultat[resultat["departementNom"].str.contains(args.departement, case=False, na=False)]

if args.circo:
    resultat = resultat[resultat["circo"] == args.circo]

if args.visual:
    counts = df['groupeAbrev'].value_counts()
    plt.figure(figsize=(8,8))
    counts.plot.pie(autopct='%1.1f%%', startangle=90, cmap='tab20', legend=False)
    plt.title("Répartition des députés par groupe parlementaire")
    plt.ylabel("")  # Supprime le label y par défaut
    plt.show()


if resultat.empty:
    print("Aucun député trouvé avec ces critères.")
else:
    for _, row in resultat.iterrows():
        print(f"{row['prenom']} {row['nom']} – {row['groupeAbrev']} – {row['departementNom']} (circo {row['circo']})")



