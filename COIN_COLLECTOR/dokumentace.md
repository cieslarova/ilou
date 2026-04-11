# Dokumentace projektu Coin Collector

Tento dokument slouží jako technická dokumentace k projektu hry **Coin Collector**, která je postavena na 3D enginu **Panda3D**.

## Fáze 1 - Základní vykreslování (`coin_collector_faze1.py`)

Účelem první fáze bylo otestovat základní architekturu okna, napojení na knihovnu Panda3D, svícení a základní vizualizaci těles.

### Struktura kódu (Fáze 1)
Kód programu je objektově orientovaný a dělí se do tří hlavních tříd:
- **Třída `Player`**: Představuje hráče. Využívá zmenšený, červeně obarvený výchozí model obličeje enginu (`"smiley"`). Nastavuje pouze svou pozici nad terénem.
- **Třída `Coin`**: Model zastupující sbíratelnou položku (minci). Využívá jednoduchý model kvádru (`"box"`), který je menší velikosti, obarven do žluta a dovoluje inicializaci na specifické náhodné pozici.
- **Třída `CoinCollectorGame`**: Hlavní třída aplikace dědící od `ShowBase`. Připravuje okno, fixovanou kameru pro ptačí pohled, dvě formy osvětlení (ambientní a směrové), zelený terén tvořený plackou (`"models/plane"`), testovací instanci hráče a statické rozložení mincí na plochu.

---

## Fáze 2 - Interaktivita, kolize a skóre (`coin_collector_faze2.py`)

Druhá fáze rozšiřuje předchozí základy programu o reálnou herní logiku: sběr, ovládání, detekce průniků a adaptace scény na chování uživatele. 

### Nové mechanismy a chování

#### 1. Řízení a pohyb a sledování kamerou
- Třída `Player` byla vybavena proměnnými pro sledování stavu kláves (**W / A / S / D**).
- Pohyb hráče je aktualizován pravidelně ve snímkové smyčce (`update_movement`) s využitím uběhnutého času (`globalClock.getDt()`). Tím je docíleno plynulého pohybu nezávislého na výkonu počítače.
- Kamera již není fixována ve statickém pohledu. Metoda `update_camera` neustále přepočítává polohu a umisťuje kameru za hráče a mírně nad něj, s přímým pohledem (`lookAt`) na aktivní postavu.

#### 2. Kolizní modely a fyzikální masky
- Jak `Player`, tak `Coin` tělesa dostala neviditelné obrysy využívajících sferický hitbox `CollisionSphere`, ukotvený uzlem `CollisionNode`.
- K optimalizaci průniků jsou zavedeny binární filtry, tzv. bitové masky:
  - `PLAYER_MASK = BitMask32(0x1)` pro masku hráče
  - `COIN_MASK = BitMask32(0x2)` pro maskování mincí
- U hráče je aktivován takzvaný traverser (`CollisionTraverser`). Těleso hráče díky němu pravidelně zkoumá, do jakých objektů narazilo, a ukládá výsledky do fronty odeslaných informací, tzv. `CollisionHandlerQueue` (uvnitř úlohy `check_collisions`).

#### 3. Herní smyčka a nekonečný režim sbírání
- Pokud detekční vrstva zaznamená protnutí obrysů `player_collision` s objektem `coin_collision`, je dotčená mince programem zničena a uvolněna ze spuštěné scény metodou `removeNode()`.
- Hra eviduje uživatelské skóre coby celočíselnou proměnnou, jež je překladem vykreslována nástrojem `OnscreenText` v horním rohu herního okna.
- Účel nekonečného sběru zajišťují reinkarnační schopnosti hry (funkce `spawn_coins`). Jakmile pole aktivních mincí klesne k pomyslné nule a hráč jich sebral všech počátečních 10 kousků, hřiště vygeneruje na náhodných souřadnicích ihned k dispozici další várku čtverečků.

---

## Fáze 3 - Herní stavy, plně funkční sběr a UI (`coin_collector_fate3.py`)

Třetí fáze přidává robustnější logiku ovládání hry, cílové podmínky ukončení hry a ošetření běhových chyb.

### Nové mechanismy a chování

#### 1. Herní stavy a konec hry
- Z programu byl odstraněn čistě "nekonečný režim". Místo toho byla zavedena proměnná udávající cíl `max_coins_to_collect = 15`.
- Byl zaveden systém herních stavů prostřednictvím stavové proměnné (např. `"playing"` nebo `"game_over"`). Hráč může ovládat pohyb a spouštět kolize pouze pokud je hra ve stavu `"playing"`.
- Jakmile je dosaženo cílového skóre, funkce `game_over()` pozastaví ovládání a detekci kolizí vymazáním patřičných úloh (*tasks*) z paměti enginu. Současně se hra přepne do stavu ukončení. 

#### 2. Resetování hry a zpětná vazba
- U třídy `Player` a ve hře samotné najdeme novou metodu `reset()`, která navrací charakter do původních výchozích souřadnic.
- Hráči se zobrazují zprávy za pomoci komponenty `OnscreenText` přímo v prostředku obrazovky při ukončení kola, s nabídkou zmáčknutí klávesy **R** pro novou hru (`reset_game()` / `start_game()`).
- Upraveno načítání vizuálních modelů – aby hra ihned nespadla při případné absenci externích modelů, obsahují třídy bloky `try-except`. Ty dokážou operativně tvořit zástupné polygony (např. programově vytvořený `GeomNode`) nebo v nouzi vybudují desku terénu prostřednictvím modulu `CardMaker`.

#### 3. Oprava a kalibrace hitboxů
- Z důvodu špatně škálované velikosti objektů v enginu nedocházelo ke kolizím z předchozí fáze. Ve fázi 3 byly u `CollisionSphere` pro minci i hráče záměrně zvětšeny lokální poloměry (1.2 pro hráče a 1.5 pro minci). Protnutí těchto velikostí se skenery je nyní po globálním zmenšení modelu plně ověřeno, objekty tedy bez problémů zaznamenávají dotyk a mince mizí.
