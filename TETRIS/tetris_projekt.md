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
