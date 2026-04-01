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

---

## Fáze 3: Vyhodnocování výhry a ukončení hry
*(Soubor: `piskvorky_faze3.py`)*

Třetí (konečná) verze hry přináší kompletní funkční pravidla. Po každém odehraném tahu program v reálném čase zkontroluje, jestli nebyla naplněna podmínka pro výhru (tři stejné znaky za sebou) nebo naopak remízu (zcela plné hrací pole bez volného místa).

### Přidané kontrolní metody
1. **Třída `Board` - kontroly:**
   * **`check_win(symbol)`**: Tato metoda prohledává herní plán a snaží se objevit symbol 3x v řadě na celkem 4 typech míst:
     * Kontrola všech **řádků**.
     * Kontrola všech **sloupců**.
     * Kontrola **hlavní diagonály** (zleva nahoře doprava dolů).
     * Kontrola **vedlejší diagonály** (zprava nahoře doleva dolů).
   * **`is_full()`**: Zjišťuje skrze vyhledávání, jestli už není náhodou deska úplně plná. Pokud nikde nestojí mezera `' '` a nikdo doposud přes `check_win` nevyhrál, zahlásí metoda nakonec stav `True` (čímž prokáže plnou plochu).
   
2. **Třída `Game` - rozuzlení konců:**
   * **Změna metody `run()`**: Na samotný chvost kontrolního procesu (místo kde se tahy reálně dělají) navázala metoda logiku testů `check_win` a `is_full` s využitím zjišťovací větve (`if - elif - else`). 
   Díky tomu jakmile dojde k situaci výhry nebo remízy přes tyto funkce: změní smyčka Boolean přepínač `self.game_over = True`, zahlásí na celou obrazovku výsledek ukončení hry, a vyruší tak konečně čekání uvnitř `while` pro další nekonečné kolo tahů.
