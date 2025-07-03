import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import quote
from mistralai import Mistral
from mistralai.models.sdkerror import SDKError
# Initialise le client Mistral
from openai import OpenAI

false = False
true = True
model = "llama3-8b-8192"

def is_disambiguation_page(soup):
    texte = soup.get_text()
    phrases_homonymie = [
        "cette page d’homonymie répertorie différentes personnes",
        "Cette page d’homonymie répertorie différentes personnes",
        "répertorie différentes personnes portant le même nom",
    ]
    return any(phrase in texte for phrase in phrases_homonymie)

def fetch_wikipedia_page(nom_depute):
    base_url = "https://en.wikipedia.org/wiki/" #page en anglais
    nom_formatte = quote(nom_depute.replace(" ", "_"))
    url = base_url + nom_formatte
    try:
        r = requests.get(url, timeout=5)
        if r.status_code == 200:
            return r.text, url
        return None, url
    except requests.RequestException:
        return None, url


def extract_text(html):
    soup = BeautifulSoup(html, "html.parser")
    content_div = soup.find("div", {"class": "mw-parser-output"})
    if not content_div:
        return ""

    full_text = ""
    for tag in content_div.find_all(["h2", "p"]):
        text = tag.get_text(strip=True)
        if text:
            full_text += text + "\n\n"
    return full_text



def generate_summary(text, nom):
    url = "http://localhost:11434/api/generate"
    prompt = f"""
You are an assistant, here to summarize Wikipedia pages about french MPs
Here is a Wikipedia page about {nom} : 
{text}

Please, create a clear and structured summary under the following structure:

- Full name :
- Date of birth :
- Political party :
- Important mandates :
- Legal issues :
- Other key informations :

If one of those informations is not available in the text, say "Not available"
Warning: DO NOT invent any information and only act based on the given text
""" 
    try:
        payload = {
                "model": "mistral",
                "prompt": prompt,
                "stream": True,
                "max_tokens": 512,
                "temperature": 0.7,
            }
        response = requests.post(url, json=payload, stream=True)
        response.raise_for_status()
        #return response.json()['response']

        full_output = ""
        for line in response.iter_lines():
            if line:
                data = line.decode("utf-8")
                json_data = eval(data) if data.startswith("{") else {}
                token = json_data.get("response", "")
                full_output += token

        return full_output.strip()

    except Exception as e:
        print(e)
        return f"Erreur Ollama: {str(e)}"


''' 
        #return response.choices[0].message.content.strip()
    except Exception as e:
        print("Erreur Ollama:", e)
        return "Erreur Ollama"
'''



def get_depute_info(nom_depute):
    # 1. Essayer page simple
    html, url = fetch_wikipedia_page(nom_depute)
    if html:
        soup = BeautifulSoup(html, "html.parser")
        if not is_disambiguation_page(soup):
            texte = extract_text(html)
            summary = generate_summary(texte, nom)
            return summary, url
    # 2. Essayer avec suffixe (homme politique)
    nom_hp = nom_depute + " (homme politique)"
    html_hp, url_hp = fetch_wikipedia_page(nom_hp)
    if html_hp:
        soup_hp = BeautifulSoup(html_hp, "html.parser")
        if not is_disambiguation_page(soup_hp):
            texte_hp = extract_text(html_hp)
            summary_hp = generate_summary(texte_hp, nom)
            return summary_hp, url_hp

    return f"⚠️ Aucune page Wikipedia claire trouvée pour '{nom_depute}'.", None

if __name__ == "__main__":
    nom = input("Nom du député : ")
    résumé, page = get_depute_info(nom)
    print("\n--- Résumé ---\n")
    print(résumé)
    if page:
        print(f"\nSource : {page}")

