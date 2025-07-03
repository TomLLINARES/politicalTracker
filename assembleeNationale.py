import pandas as pd
import argparse
import matplotlib.pyplot as plt
import os, sys
plt.show()


addr = 'data/deputes-active.csv'
addr_corr = 'data/circo_composition.xlsx'

df = pd.read_csv(addr, sep=',', encoding='utf-8')
dfCirco = pd.read_excel(addr_corr, sheet_name='table')  # ou nom de la feuille

parser = argparse.ArgumentParser(description="Filtrer les députés par groupe, département ou circonscription.")
parser.add_argument("-g", "--groupe", help="Sigle du groupe parlementaire (ex: LFI-NFP, RN, DR...)")
parser.add_argument("-d", "--departement", help="Nom complet du département (ex: Yvelines)")
parser.add_argument("-ci", "--circo", type=int, help="Numéro de la circonscription dans le département")
parser.add_argument("-v", "--visual", action="store_true", help="Affiche un graphique de la repartition en fonction du critere choisi")
parser.add_argument("-n", "--nom", type=str, help="Recherche un depute par son nom")
parser.add_argument("-co", "--communes", type=str, help="entrez le nom de votre commune")
parser.add_argument("-cp", "--codePostal", type=int, help="entrez le code postal de votre commune")
parser.add_argument("-cd", "--codeDepartement", type=int, help="entrez le numéro de votre département") #colonne DEP (code departement)


args = parser.parse_args()
resultat = df.copy()

lookupCirco = ''
lookupDep = ''
flagD = False
flagC = False

if args.codeDepartement:
    ligne = dfCirco[dfCirco['DEP'].str.lower() == str(args.codeDepartement)]
    if not ligne.empty:
        pass


if args.communes:
    communeA = args.communes.lower()
    if communeA == 'paris':
        resultat = df[df['departementNom'].str.lower() == 'paris']
    elif communeA in ['marseille', 'lyon']:
        matching = dfCirco[dfCirco['LIBcom'].str.lower() == 'lyon']
        if matching.empty:
            print(f'Aucune correspondance trouvée pour {communeA}')
        else:
            resultat = pd.DataFrame()
            for _, row in matching.iterrows():
                dept_nom = row['libdep']
                circoNum = int(str(row['circo'][3:]))
                filtre = ((df['departementNom'].str.lower() == dept_nom.lower()) & (df['circo'] == circoNum))
                resultat=pd.concat([resultat, df[filtre]])
    else:    
        ligne = dfCirco[dfCirco['LIBcom'].str.lower() == args.communes.lower()]
        if not ligne.empty:
            circo = ligne['circo'].values[0]
            dep = ligne['libdep'].values[0]
            lookupCirco, lookupDep = int((circo)[3:]), str(dep)
            flagD, flagC = True, True
            print(f"Commune {args.communes} => Département : {dep}, Circonscription : {circo}")
        else:
            print(f"Commune {nom_commune} non trouvée")
        resultat = resultat[resultat['departementNom'] == lookupDep]
        resultat = resultat[resultat['circo'] == lookupCirco]

if args.groupe:
    resultat = resultat[resultat["groupeAbrev"] == args.groupe]

if args.departement:
    resultat = resultat[resultat["departementNom"] == args.departement]

if args.circo:
    resultat = resultat[resultat["circo"] == args.circo]

if args.visual:
    vis = True
    counts = df['groupeAbrev'].value_counts()
    plt.figure(figsize=(8,8))
    counts.plot.pie(autopct='%1.1f%%', startangle=90, cmap='tab20', legend=False)
    plt.title("Répartition des députés par groupe parlementaire")
    plt.ylabel("")  # Supprime le label y par défaut
    plt.show()
    sys.exit(0)

if resultat.empty:
    print("Aucun député trouvé avec ces critères.")
else:
    for _, row in resultat.iterrows():
        print(f"{row['prenom']} {row['nom']} – {row['groupeAbrev']} – {row['departementNom']} (circo {row['circo']})")


                    


