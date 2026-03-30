# Dokumentace k projektu: Piškvorky (Fáze 1)

Tento dokument slouží jako popis první vývojové fáze (soubor `piskvorky_faze1.py`) hry Piškvorky. V této počáteční fázi byly naprogramovány základní kameny pro pozdější interaktivní hru v terminálu, tedy samotná struktura hráčů, hrací plochy (mřížky) a nezbytná řídicí logika hry (propojení polí s hráči).

## Architektura kódu

Projekt je postaven na principech objektově orientovaného programování (OOP) a rozdělen do tří hlavních tříd:

### 1. Třída `Player` (Hráč)
Slouží k reprezentaci jednoho hráče (účastníka) hry.
* **Atribut `name`**: Jméno nebo přezdívka hráče.
* **Atribut `symbol`**: Povolený symbol zobrazení na herní ploše (standardně křížek "X" nebo kolečko "O").
* **Metoda `__init__`**: Přiřazuje hráči zadané jméno a symbol přímo při vytvoření instance třidy.
* **Metoda `__str__`**: Vrací "lidsky čitelnou" reprezentaci objektu (např. *Hráč: Hráč 1, Symbol: X*).

### 2. Třída `Board` (Hrací plocha)
Obstarává ukládání stavu jednotlivých políček (mřížky 3x3).
* **Atribut `grid`**: Pro ukládání samotné hrací plochy, která je uložena jako seznam seznamů (2D pole neboli matice). Inicializuje se jako tabulka 3x3 s 9 prázdnými prvky oddělenými mezerou.
* **Metoda `display`**: Vypíše (vyrenderuje) formálnější zobrazení matice `grid` do terminálu. Využívá pomocný výpisový formát společně se svislými (`|`) i vodorovnými (`---+---+---`) dělícími čarami.

### 3. Třída `Game` (Logika a řízení hry)
Sloučovací bod hry, kontroluje hráče i plochu a spravuje jejich provázanost.
* **Složení hry**: V inicializaci (`__init__`) vytvoří instanci `Board` (hrací plochu) a vygeneruje 2 instance `Player` (tedy hráče s "X" a hráče s "O").
* **Atribut `current_player`**: Ujistí se, který z dvojice hráčů je zrovna oprávněně na tahu (na startu typicky Hráč 1).
* **Metoda `start_game`**: Cílí pouze na zkušební vizualizaci (ukázku aktuální situace v první vývojové fázi), přičemž zobrazí prázdnou vymazanou hrací plochu.

## Konec souboru
Logika startu aplikace se ukrývá v bloku `if __name__ == "__main__":`. Zamezuje se tím nežádoucímu nechtěnému spuštění hry (pokud se kód programu případně importuje jinde do jiného souboru). Odsud dojde přímo na spuštění přes `game = Game()` a volání `game.start_game()`.

## Další kroky - co bude obnášet Fáze 2
Z této výchozí kostry se hra musí doplnit o základní interakci a interaktivní životní cyklus hry:
1. **Získávání vstupu**: Zeptat se uživatele (pomocí funkce `input`), kam chce hrát na jakou souřadnici.
2. **Herní smyčka (`while`)**: Hra nesmí skončit hned po zobrazení sítě, ale musí se nekonečně dotazovat tak dlouho dokud jeden z hráčů neprohraje nebo nedojde k remíze.
3. **Střídání tahů (Alternace)**: Po platném tahu se musí přepnout atribut `current_player`.
4. **Logika výhry / Remízy**: Kontrola po každém provedeném umístění na šachovnici, jestli není splněna vítězná situace 3 v řadě (horizontálně, vertikálně nebo diagonálně).
