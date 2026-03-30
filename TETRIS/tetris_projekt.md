# Dokumentace projektu: Tetris

Toto je projektová dokumentace ke hře **Tetris**, vytvářené v jazyce Python s využitím knihovny `pygame`. Vývoj probíhá v několika fázích.

---

## Fáze 1: Základní herní struktura a vykreslování (`tetris_faze1.py`)

Cílem první fáze bylo připravit vizuální stránku hry, definovat herní datové struktury a zprovoznit hlavní herní smyčku bez implementace fyziky a pohybu kostek.

### 1. Konstanty a konfigurace
- **Rozměry okna:** 800x700 pixelů.
- **Hrací plocha (mřížka):** 10x20 bloků (šířka 300px, výška 600px), velikost jednoho bloku je 30x30 pixelů.
- **Barvy:** Definice základních RGB barev použitých ve hře (černá pro pozadí, bílá, červená, zelená atd. pro jednotlivé typy kostek).

### 2. Tvary kostek (Tetromina)
Všechny klasické tvary z Tetrisu (S, Z, I, O, J, L, T) jsou definovány pomocí seznamů obsahujících textové matice 5x5.
- Každá matice představuje jednu možnou rotaci daného tvaru.
- Znak `0` značí blok, znak `.` značí prázdné místo.

### 3. Hlavní třídy

#### `Tetromino`
Reprezentuje jeden padající blok. 
- Uchovává počáteční souřadnice (X a Y v rámci herní mřížky).
- Uchovává informace o svém tvaru, aktuální rotaci a barvě (která je přiřazena na základě typu tvaru).
- Metoda `get_shape()` vrací aktuální matici podle momentální rotace bloku.

#### `Board`
Představuje samotnou herní desku, kam kostky padají.
- Mřížka (2D seznam) o velikosti 10 sloupů a 20 řádků. Prázdná mřížka je inicializována s barvou pozadí (černá).
- Metoda `draw(surface)` vykresluje hrací plochu na obrazovku včetně jejích bílých okrajů a obsahu mřížky.

#### `Game`
Hlavní správce stavu hry.
- Spojuje hrací desku (`Board`), aktuálně padající kostku (`current_piece`), následující kostku (`next_piece`) a skóre.
- Metoda `new_piece()` generuje novou náhodnou kostku, která se objeví uprostřed nahoře.
- Metoda `draw(surface)` se stará o vykreslení aktuálního stavu: pozadí, herní deska, padající kostka a texty pro skóre a oddíl pro zobrazení "Další kostky".

### 4. Herní smyčka
Funkce `main()` obsahuje základní smyčku s frameratem omezeným na 60 FPS. 
- Aktuálně řeší pouze udržení otevřeného okna, možnost jeho zavření přes událost `pygame.QUIT` a neustálé překreslování statického stavu hry (jedna kostka nahoře hracího pole).

### Závěr Fáze 1
Po spuštění skriptu se otevře okno, ve kterém je vykreslena funkční a ohraničená herní deska 10x20 polí, počítadlo skóre a jeden náhodně vybraný objekt (tetromino) čekající v základní horní pozici. Stavební kameny pro herní logiku (pohyb, otáčení, detekce kolizí a padání) jsou připraveny k implementaci v další fázi.

---

## Fáze 2: Herní logika a pohyb (`tetris_faze2.py`)

Cílem druhé fáze je přidat do vytvořené vizuální kostry herní mechaniky, díky nimž se Tetris stane kompletně hratelným. Tato fáze inkrementálně navazuje na zdrojový kód z Fáze 1 a přidává klíčové funkce nutné pro plnohodnotný zážitek.

### 1. Rozšíření třídy `Game` a `Board`
- **Třída `Game`:** Byla doplněna o evidenci `locked_positions` (slovník zaznamenávající zaplněná pole mřížky na základě souřadnic a jejich přiřazené barvy) a metodu `valid_space()`, která kontroluje, zda je pro padající tetromino dostatek místa (jestli nevybočuje z hrací plochy, nebo nenaráží do již spadlých kostek).
- **Metoda `check_lost()`:** Identifikuje "Game Over" stav. Hra končí, pokud jakýkoli zamčený blok překročí horní okraj obrazovky.
- **Odstranění plných řádků (`clear_rows`):** Pokaždé, když blok dopadne, projde se herní `grid`. Jakmile řádek neobsahuje prázdné políčko (černá barva), je odstraněn a nad ním ležící řádky se logicky posunou o jeden stupeň dolů. Odtud se také přičítá skóre.

### 2. Pohyb a rotace pomocí kláves
Ovládání hráče je zpracováno pomocí klávesových událostí knihovny pygame (`pygame.KEYDOWN`):
- **Šipka vlevo / vpravo:** Upravení osy `X` u padajícího tetromina, podmíněno ověřením, že cílové políčko je prázdné a nevypadne z plátna.
- **Šipka nahoru:** Rotace tetromina. Iteruje cyklem přes možné předdefinované mapy v seznamu rotací aktuální kostky.
- **Šipka dolů:** Zrychlení padání (při stisknutí se ignoruje běžný pádový časovač).

### 3. Zpracování času (Padání bloků)
V cyklu se využívá `pygame.time.Clock().get_rawtime()`, které sleduje intervaly plynutí času. Jakmile hodnota přesáhne naši specifikovanou `fall_speed` (rychlost padání), automaticky se tetromino posune po ose `Y` o +1. Rychlost se může v čase plynule zrychlovat v závislosti na dosaženém skóre nebo uplynulém herním čase (Level), ačkoli pro Fázi 2 ponecháváme model padání fixní.

### Závěr Fáze 2
Výsledkem této etapy je spolehlivě zkompletovaná arkáda Tetris! Uživatel může manipulovat s padajícími dílky v ohraničené síti, bloky se po dopadu ukládají a skládání celistvých čar generuje skóre. Celé chování programu bylo řádně okomentováno přesně zadáním v rámci hodnocení studentských repozitářů.

---

## Fáze 3: Nabídka, pauza a ukládání skóre (`tetris_faze3.py`)

Cílem třetí fáze je poskytnout hráči ucelenější uživatelský zážitek a profesionálnější chování aplikace, než jaké nabízel jednoduchý nekonečný cyklus z Fáze 2. Program se obohatil o možnost představit se, pozastavit průběh hry a porovnat své úspěchy na žebříčku nejlepších.

### 1. Úvodní Menu a zadávání jména
- Při spuštění skriptu se objeví `zobraz_menu()`, která hráče přivítá názvem titulu a výukou ovládání.
- Uživatelský vstup zachytává klávesy (`pygame.KEYDOWN`) do proměnné typu String. Je možná i korekce překlepů pomocí `Backspace`.
- Jakmile hráč stiskne `Enter`, začíná samotná hra.

### 2. Pauza a Game Over Screen
- Během plnohodnotné hry lze stisknout `Mezerník` (`SPACE`), čímž se vyvolá funkce `pauza()`. Ta vnoří program do podcyklu čekajícího pouze na další znovustisknutí Mezerníku, čímž pozastaví ubíhání jakýchkoli herních hodin a padání kostek.
- Při prohře je hra zachycena a hráč zůstává na obrazovce Game Over. Jsou mu nabídnuty dvě volby: `M - Návrat do Menu` nebo `R - Restart`. Zde byla také ošetřena dřívější chyba okamžitého pádu samotné aplikace. 

### 3. Záznam nejvyššího skóre (I/O operace)
- Při detekci prohry se automaticky přistupuje na pevný disk skrz modul `os`. 
- Kód přečte, roztřídí Top 3 a uloží hráče na základě jeho dosažených bodů napříč sezeními. Uskladnění probíhá pomocí jednoduché serializace do `skore.txt` (formát `Jméno,Punkty`).
- Žebříček nejlepších je zobrazen spolu se stavem "Game Over", čímž dává hráči silný motiv znovu se pokusit o překonání rekordu.

### Závěr Fáze 3
Aplikace díky logickému rozdělení cyklů mezi "Main Menu", "Hra" a "Pauza" již nepůsobí jen jako testovací plocha enginu, nýbrž jako dokončený a soběstačný herní produkt zabalující veškeré dílčí koncepty předchozích fází do sjednoceného balíčku (Příběhový rámec/Leaderboardy).
