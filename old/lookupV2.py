import json
import os
import argparse
import sys

def initDep():
    chemin = "json/acteur/"
    deputeData = []
    for filename in os.listdir(chemin):
        if filename.endswith(".json"):
            pathIndiv = os.path.join(chemin,filename)
            with open(pathIndiv, "r", encoding='utf-8') as f:
                data = json.load(f)
                deputeData.append(data)
    print(f"{len(deputeData)} fichiers JSON chargés.")
    #print("Exemple de données du premier député :")
    #print(deputeData[0])
    return deputeData

def initGroupes():
    chemin = 'json/organe'
    groupeData = []
    groupes = {}
    for filename in os.listdir(chemin):
        if filename.endswith('.json'):
            pathIndiv = os.path.join(chemin,filename)
            with open(pathIndiv, 'r', encoding='utf-8') as f:
                data = json.load(f)
                organe = data.get("organe", {})
                if organe.get("codeType") == "GP":
                    uid = organe["uid"]
                    libelle = organe.get("libelle", "Inconnu")
                    groupes[uid] = libelle
    print(f"{len(groupes)} groupes parlementaires trouvés.")
    return groupes


def get_depute(data, groupes, departement=None, circo=None, name=None):
    
    if name is not None:
        name = name.lower()
        #for dep in data['deputes']:
        for dep in data:
            d = dep['acteur']
            #print(dep)
            depute_id = d.get('etatCivil').get('ident')
            mandats = d.get('mandats').get('mandat')
            #print(mandats)
            #print(mandats[0].get('typeOrgane'))
            for i in range(len(mandats)):
                m = mandats[i]
                if m.get('typeOrgane') == 'ASSEMBLEE':
                    organe_uid = m.get('organes').get('organeRef')

                    groupe = groupes.get(organe_uid)
                    #print(groupes)
                    print(organe_uid)
                    print(groupe)
                    print(groupes)

            depute_nom = depute_id['civ'] + ' ' + depute_id['prenom'] + ' ' + depute_id['nom']
            print(f'{depute_nom} | du groupe {groupe} \n ==================')
'''
            

        return
            

    found = False
    for dep in data:
        depute_id = dep['ident']
        depute_nom = depute_id['civ'] + ' ' + depute_id['prenom'] + ' ' + depute_id['nom']

        #print(f'{info} \n')
        #if info['num_circo'] == circo and info['num_deptmt'] == num_deptmt:
        #depute_dep = info['nom_circo']
        #depute_circo = info['num_circo']
        #depute_nom = info['nom']
        #depute_groupe = info['groupe_sigle']
        if depute_dep == departement:
            if depute_circo == circo or circo is None:
                slug = info['slug']
                print(f'Député trouvé: {depute_nom}, issu de la {depute_circo}ème circonscription du {departement} ({slug}), groupe: {depute_groupe}')
'''

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
    deputeData = initDep()
    groupes = initGroupes()
    get_depute(deputeData, groupes, args.departement, args.circonscription, args.nom)







