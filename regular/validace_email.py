import re

def validuj_email():
    """
    Funkce k interaktivní validaci e-mailové adresy zadávané uživatelem přes terminál.
    Běží v nekonečné smyčce, dokud uživatel nezadá buď platný e-mail, nebo neukončí
    program klíčovým slovem 'konec'.
    """
    # Definice regex vzorce pro email
    # ^ = začátek řetězce
    # [a-zA-Z0-9._%+-]+ = local part emailu (může obsahovat písmena, čísla a spec. znaky včetně %)
    # @ = zavináč
    # [a-zA-Z0-9.-]+ = doména
    # \.[a-zA-Z]{2,} = koncovka (např. .cz, .com) o délce min. 2 znaky
    # $ = konec řetězce
    regex_vzor = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    print("--- Validátor e-mailových adres ---")
    print("(Pro ukončení napište 'konec')\n")

    # Hlavní smyčka pro opakované dotazování uživatele
    while True:
        uzivatel_vstup = input("Zadejte svůj e-mail: ").strip()

        # Ukončovací podmínka
        if uzivatel_vstup.lower() == 'konec':
            print("Nashledanou!")
            break

        # Srovnání vstupu s Regex vzorcem pomocí fuknce fullmatch (musí souhlasit celý řetězec)
        if re.fullmatch(regex_vzor, uzivatel_vstup):
            print(f"✅ Skvělé! '{uzivatel_vstup}' je validní e-mail.\n")
            # Úspěšné doložení platnosti - přerušení smyčky
            break 
        else:
            print(f"❌ Chyba: '{uzivatel_vstup}' není platná adresa. Zkuste to znovu.\n")

if __name__ == "__main__":
    validuj_email()