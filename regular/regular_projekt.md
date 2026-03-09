# Regulární Výrazy - Validace a Extrakce

## Popis a cíl projektu
Cílem tohoto projektu ve složce `regular` je demonstrovat využití **regulárních výrazů (Regex)** v jazyce Python. Projekt slouží ke dvěma účelům:
1. Skript interaktivně validuje správnost zápisu e-mailových adres skrze uživatelský vstup z terminálu.
2. Skript slouží jako parser doručující hromadnou extrakci e-mailových adres ze slohového textu (souboru `emaily.md`) a jejich výpis osekán on duplicity.

## Funkcionalita programu
Projekt sestává ze dvou spustitelných vizuálně oddělených skriptů k různému způsobu nasazení:
- `validace_email.py`: Spustí textový validátor, do nějž je uživatel vyzván vložit libovolný string. Program analyzuje kompatibilitu tvaru do e-mailového formátu a oznámí výsledek. Program běží v opakující se smyčce až do doby, než uživatel odepíše 'konec' či vloží validní e-mail adresu (s regulérně definovanou koncovkou a zavináčem).
- `najdi_email.py`: Na pozadí bez otázek otevře lokální soubor `emaily.md`, přečte jeho veškerý hrubý obsah od horního řádku po spodní a za pomocí funkce hledání ve vzorcích seskupí veškeré e-maily, filtruje je na výskyt pouhých unikatních adres a nakonec je vytiskne do terminálu s celkovým počtem záznamů.

## Technická část
- **Použité knihovny**: 
  - `re` - standardní knihovna jazyka Python umožňující výkon sofistikovaného vyhledávání prostřednictvím regulárních výrazů (včetně zachytávajících metod).
  - `os` - standardní knihovna pro čtení absolutní a relativní souborové cesty k textovému dokumentu pro správné navigování file systemem.
- **Struktura kódu a algoritmy**: 
  - Algoritmus extrakce `najdi_email` používá interním mechanismem funkci `re.findall()`, díky níž je možno vylistovat ze špagetového textu pole nezávislých celků splňující zadání. 
  - Regex řetězec `^[a-zA-Z0-9._%+-]+...` kontrolující strukturu s maximální precizností využívá tzv. Local part definice zahrnující znak `%`, i přes relativní zřídkavost výskytu (převážně k internímu routingu).
  - Skript zachovává chronologii výpisu pro čištění duplikátů hackem přetransformování přes datovou strukturu slovníku `dict.fromkeys()`, zaručujícím eliminaci totožných stringů před zpětnou redefinicí do proměnné Listu.
- **Datové struktury**: 
  - Veškeré extrakce jsou interně zacházeny formou seznamů struktur List of strings a procházené vnitřními loop cykly for-in k iteraci hodnot a formátování na výstupu terminálu. Položky si zachovávají přirozené defaultní datové typy.
