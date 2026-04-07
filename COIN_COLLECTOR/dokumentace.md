# Dokumentace projektu Coin Collector - Fáze 1

Tento dokument slouží jako technická dokumentace k první fázi projektu hry **Coin Collector** (soubor `coin_collector_faze1.py`), která je postavena na 3D enginu **Panda3D**.

## Struktura kódu

Kód programu je plně objektově orientovaný a dělí se do tří hlavních tříd:

### 1. Třída `Player`
Představuje hlavní postavu, kterou bude hráč v budoucnu tvořit a ovládat.
- **Inicializace (`__init__`)**: Přijímá odkaz na nadřazený uzel (`parent_node`), přes který se modely vykreslují.
- **Model**: Namísto komplexního modelu využívá výchozí model obličeje enginu (`"smiley"`).
- **Vzhled a pozice**: Model je zmenšen interní funkcí `setScale(0.5)`, zbarven dočervena (`setColor(0.8, 0.2, 0.2, 1)`) a posazen nepatrně nad povrch terénu (`setPos(0, 0, 0.5)`).

### 2. Třída `Coin`
Objekt zastupující sbíratelnou položku (minci) roztroušenou po mapě.
- **Inicializace (`__init__`)**: Narozdíl od hráče navíc přijímá parametr `position` ve formě tuple (x,y,z), díky kterému můžeme snadno distribuovat mince.
- **Model**: Aktuálně se používá jednoduchý kvádr (`"box"`).
- **Vzhled a pozice**: Model je poměrově menší (`setScale(0.2)`), disponuje zlatistou barvou a je umístěn mírně nad mapou pro viditelnost.

### 3. Třída `CoinCollectorGame`
Hlavní třída aplikace dědící od `ShowBase`. Překrývá výchozí chování Panda3D modulu a zakládá konkrétní scénu hry.
- **Konfigurace Okna**: Pozadí se čistí do bleděmodra evokujícího oblohu a do titulků se aplikuje "Coin Collector - Fáze 1".
- **Kamera**: Fixována z vyvýšené pozice a pohlížející do středu – zajišťuje klasický ptačí pohled nad hřištěm.
- **Světla (Lighting)**: Ošetřeno dvojím způsobem:
    1. **Ambientní světlo**: Pro základní neostrou viditelnost těles.
    2. **Směrové světlo**: Simulující vrhání slunečních stínů z konkrétního úhlu (45° rotace).
- **Terén (Ground)**: Zeleně obarvená velká plocha (`"models/plane"`) připnutá na souřadnice `(0,0,-0.5)`, aby nekolidovala přímo s centrem scény. Nachází se v ní také pojistka (try/except `CardMaker`) v případě nenačtení předpřipraveného modelu.
- **Příprava herní smyčky**: Generuje prozatím jednu instanci hráče doprostřed a seznam `self.coins` plní 3 statickými kusy mincí.

## Účel fáze 1
Tato fáze slouží výlučně jako testovací render základní architektury do okna, tedy otestování knihovny Panda3D, svícení a viditelnosti objektů. Modifikace vstupu od uživatele pro ovládání míče a odchytávání fyzikálních kolizí na sběr bude součástí až dalších vývojových fází.
