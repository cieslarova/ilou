import os
import re

def najdi_emaily_v_souboru():
    """
    Funkce k nalezení všech platných e-mailových adres v textovém souboru (emaily.md).
    Využívá regulárních výrazů (regex) a odstraňuje případné duplicity před
    tím, než vypíše výsledky do terminálu.
    """
    # Získání absolutní cesty k souboru emaily.md, který by měl být ve stejné složce
    cesta_k_souboru = os.path.join(os.path.dirname(__file__), 'emaily.md')

    try:
        # Přečtení celého obsahu souboru s bezpečně definovaným kódováním
        with open(cesta_k_souboru, 'r', encoding='utf-8') as soubor:
            obsah = soubor.read()

        # Regulární výraz pro hledání e-mailových adres kdekoli v textu
        regex_vzor = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

        # Vyhledání všech e-mailů v textu (vrací seznam všech shod, re.findall)
        nalezene_emaily = re.findall(regex_vzor, obsah)

        print("--- Nalezené e-maily ---")
        if nalezene_emaily:
            # Odstranění případných duplicit pro přehlednější výpis 
            # (Dictionary zachovává pořadí prvního výskytu z dict.fromkeys)
            unikatni_emaily = list(dict.fromkeys(nalezene_emaily))
            
            # Cyklus slouží k výpisu nalezených záznamů jeden po druhém
            for email in unikatni_emaily:
                print(email)
            print(f"\nCelkem unikátních e-mailů: {len(unikatni_emaily)}")
        else:
            print("V souboru nebyly nalezeny žádné platné e-mailové adresy.")

    except FileNotFoundError:
        print(f"❌ Chyba: Soubor '{cesta_k_souboru}' nebyl nalezen.")
    except Exception as e:
        print(f"❌ Nastala chyba při zpracování souboru: {e}")

if __name__ == "__main__":
    najdi_emaily_v_souboru()
