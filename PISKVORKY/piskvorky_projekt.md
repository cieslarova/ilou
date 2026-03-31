# Dokumentace k projektu: Piškvorky

Tento dokument mapuje vývoj hry Piškvorky a průběžně popisuje její jednotlivé fáze.

---

## Fáze 1: Základní stavební kameny
*(Soubor: `piskvorky_faze1.py`)*

V první fázi byly naprogramovány základní kameny pro pozdější interaktivní hru v terminálu: samotná struktura hráčů, hrací plochy (mřížky) a nezbytná řídicí logika hry (propojení polí s hráči).

### Architektura kódu
Projekt je postaven na principech objektově orientovaného programování (OOP) a rozdělen do tří hlavních tříd.
1. **Třída `Player` (Hráč)**
   * **Atribut `name`**: Jméno nebo přezdívka hráče.
   * **Atribut `symbol`**: Povolený symbol zobrazení na herní ploše (standardně křížek "X" nebo kolečko "O").
   * **Metoda `__init__`**: Přiřazuje hráči zadané jméno a symbol přímo při vytvoření instance třidy.
2. **Třída `Board` (Hrací plocha)**
   * **Atribut `grid`**: Pro ukládání samotné hrací plochy (matice 3x3). Inicializuje se jako tabulka s 9 prázdnými prvky oddělenými mezerou.
   * **Metoda `display`**: Vypíše (vyrenderuje) formálnější zobrazení matice `grid` do terminálu.
3. **Třída `Game` (Logika a řízení hry)**
   * Sločovací bod hry, inicializuje instanci `Board` (hrací plochu) a 2 instance `Player`. Má metodu `start_game`, která pouze zkušebně zobrazí prázdnou vymazanou hrací plochu.

---

## Fáze 2: Interaktivní herní smyčka
*(Soubor: `piskvorky_faze2.py`)*

Ve druhé fázi se projekt rozšířil o získávaní vstupů a životní cyklus programu. Hra již nekončí po prvním vykreslení plochy, ale cyklicky se dotazuje hráčů na jejich tah.

### Nové a upravené funkce
1. **Třída `Board` - vkládání tahů:**
   * **`make_move(row, col, symbol)`**: Nová funkce obstarává tah. Přijme souřadnice od hráče, ověří, zda jsou v povoleném rozsahu `0-2` (aby nezadal neexistující políčko) a jestli tam náhodou už něco není. Pokud jsou podmínky splněny, znak se úspěšně vykreslí (vrátí `True`).
2. **Třída `Game` - interakce:**
   * **Atribut `game_over`**: Nová proměnná s hodnotou Boolean (`False`), která funguje jako přepínač držící herní smyčku aktivní.
   * **`get_player_move()`**: Ošetřený `while True` cyklus, který nutí hráče zadávat pomocí `input()` řádek i sloupec doté doby, než zadá platné číslo. Blokem `try-except` se brání spadnutí programu ve chvíli, kdyby hráč napsal omylem místo čísla například písmeno.
   * **`switch_player()`**: Rychlá a stručná funkce na prostřídání tahů obou protivníků (předá `current_player` druhému ze dvojice).
   * **`run()`**: Původní metodu *start_game* spouští plnohodnotná herní smyčka. Metoda udržuje program neustále v chodu a prohazuje tahy.

### Konec souboru a spouštění
Logika spuštění se stále ukrývá v bloku `if __name__ == "__main__":`. Zamezuje se tím nežádoucímu autostartu. Ve fázi 2 je samotné spuštění odesláno přes `game = Game()` a spuštěním samotné smyčky pomocí aktivační funkce `game.run()`.

---

## Další kroky - co bude obnášet Fáze 3
Zatím hra postrádá jakéhokoliv arbitra. Pro finální Fázi 3 bude třeba přidat:
1. **Logika výhry a kontroly**: Po každém úspěšném tahu se musí prohledat tabulka matice, zda tam neexistuje vítězná situace 3 v řadě (horizontální kontrola, vertikální kontrola, nebo kontrola úhlopříček - diagonálně).
2. **Ukončení hry (Remíza a Výhra)**: Rozpoznat situaci kdy nezbyde už žádné volné prázdné pole, anebo kdy padne vítěz, a následně cyklus `run()` zastavit změněním `game_over` na hodnotu `True`.
