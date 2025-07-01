import requests

url = "https://www.nosdeputes.fr/deputes/json"
response = requests.get(url)
data = response.json()


circo = 4 #a update
num_deptmt = 78 #a update
nom_circo = 'Yvelines'

for dep in data['deputes']:
    info = dep['depute']
    #print(f'{info} \n')
    #if info['num_circo'] == circo and info['num_deptmt'] == num_deptmt:
    if info['nom_circo'] == nom_circo and info['num_circo'] == circo:
        slug = info['slug']
        print(f'Député trouvé: {info["nom"]} ({slug}), groupe: {info["groupe_sigle"]}')




'''





{'id': 618, 'nom': 'Denis Bernaert', 'nom_de_famille': 'Bernaert', 'prenom': 'Denis', 'sexe': 'H', 'date_naissance': '1964-05-01', 'lieu_naissance': 'Saint-Mandé (Val-de-Marne)', 'num_deptmt': '78', 'nom_circo': 'Yvelines', 'num_circo': 4, 'mandat_debut': '2024-02-12', 'mandat_fin': '2024-06-09', 'ancien_depute': 1, 'groupe_sigle': 'REN', 'parti_ratt_financier': '', 'sites_web': [{'site': 'https://twitter.com/DenisBernaert'}], 'emails': [{'email': 'denis.bernaert@assemblee-nationale.fr'}], 'adresses': [{'adresse': "Assemblée nationale, 126 Rue de l'Université, 75355 Paris 07 SP"}, {'adresse': '11 Rue des ponts 78290 Croissy sur seine Téléphone : 07 72 29 57 97'}], 'collaborateurs': [], 'autres_mandats': [], 'anciens_autres_mandats': [], 'anciens_mandats': [{'mandat': '12/02/2024 / 09/06/2024 / fin de législature'}], 'profession': None, 'place_en_hemicycle': '404', 'url_an': 'https://www2.assemblee-nationale.fr/deputes/fiche/OMC_PA795572', 'id_an': '795572', 'slug': 'denis-bernaert', 'url_nosdeputes': 'https://www.nosdeputes.fr/denis-bernaert', 'url_nosdeputes_api': 'https://www.nosdeputes.fr/denis-bernaert/json', 'nb_mandats': 0, 'twitter': 'DenisBernaert'}
'''
