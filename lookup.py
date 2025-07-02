import requests
import argparse

url = "https://www.nosdeputes.fr/deputes/json"
response = requests.get(url)
data = response.json()

def get_depute(departement=None, circo=None, name=None):
    
    if name is not None:
        name = name.lower()
        for dep in data['deputes']:
            info = dep['depute']
            depute_nom = info['nom']
            depute_dep = info['nom_circo']
            depute_circo = info['num_circo']
            depute_groupe = info['groupe_sigle']
            slug = info['slug']
            #print(slug)
            if name in slug:
                print(f'Député trouvé: {depute_nom}, issu de la {depute_circo}ème circonscription du {departement} ({slug}), groupe: {depute_groupe}')
        return
            

    found = False
    for dep in data['deputes']:
        info = dep['depute']
        #print(f'{info} \n')
        #if info['num_circo'] == circo and info['num_deptmt'] == num_deptmt:
        depute_dep = info['nom_circo']
        depute_circo = info['num_circo']
        depute_nom = info['nom']
        depute_groupe = info['groupe_sigle']
        if depute_dep == departement:
            if depute_circo == circo or circo is None:
                slug = info['slug']
                print(f'Député trouvé: {depute_nom}, issu de la {depute_circo}ème circonscription du {departement} ({slug}), groupe: {depute_groupe}')


def get_deputeS(name):
    for dep in data['deputes']:
        info = dep['depute']
        depute_nom = info['nom']
        depute_dep = info['nom_circo']
        depute_circo = info['num_circo']
        depute_groupe = info['groupe_sigle']
        slug = info['slug']
        if name in slug:
            print(f'Député trouvé: {depute_nom}, issu de la {depute_circo}ème circonscription du {departement} ({slug}), groupe: {depute_groupe}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Récupère les infos d’un député par circonscription.")
    parser.add_argument("-d", "--departement", type=str, required=False, help="Nom du département (ex: Yvelines)")
    parser.add_argument("-c", "--circonscription", type=int, required=False, help="Numéro de la circonscription (ex: 5)")
    parser.add_argument("-n", "--nom", type=str, required=False, help="Nom ou morceau du nom du depute")
    args = parser.parse_args()
    get_depute(args.departement, args.circonscription, args.nom)



'''





{'id': 618, 'nom': 'Denis Bernaert', 'nom_de_famille': 'Bernaert', 'prenom': 'Denis', 'sexe': 'H', 'date_naissance': '1964-05-01', 'lieu_naissance': 'Saint-Mandé (Val-de-Marne)', 'num_deptmt': '78', 'nom_circo': 'Yvelines', 'num_circo': 4, 'mandat_debut': '2024-02-12', 'mandat_fin': '2024-06-09', 'ancien_depute': 1, 'groupe_sigle': 'REN', 'parti_ratt_financier': '', 'sites_web': [{'site': 'https://twitter.com/DenisBernaert'}], 'emails': [{'email': 'denis.bernaert@assemblee-nationale.fr'}], 'adresses': [{'adresse': "Assemblée nationale, 126 Rue de l'Université, 75355 Paris 07 SP"}, {'adresse': '11 Rue des ponts 78290 Croissy sur seine Téléphone : 07 72 29 57 97'}], 'collaborateurs': [], 'autres_mandats': [], 'anciens_autres_mandats': [], 'anciens_mandats': [{'mandat': '12/02/2024 / 09/06/2024 / fin de législature'}], 'profession': None, 'place_en_hemicycle': '404', 'url_an': 'https://www2.assemblee-nationale.fr/deputes/fiche/OMC_PA795572', 'id_an': '795572', 'slug': 'denis-bernaert', 'url_nosdeputes': 'https://www.nosdeputes.fr/denis-bernaert', 'url_nosdeputes_api': 'https://www.nosdeputes.fr/denis-bernaert/json', 'nb_mandats': 0, 'twitter': 'DenisBernaert'}
'''
