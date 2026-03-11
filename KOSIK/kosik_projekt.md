# Košík

## Popis a cíl projektu
Jednoduchá arkádová hra pro procvičení základů knihovny Pygame. Hráč ovládá jezdící a skákací košík a jeho cílem je sbírat padající jídlo (v první fázi reprezentované kostkou). Hra je určena pro začínající programátory, kteří si na ní ukáží principy tvorby herního prostředí, pohybu a detekce kolizí.

## Funkcionalita programu
- Hráč se pohybuje pomocí šipek (doleva/doprava) po spodním okraji obrazovky.
- Z horní části okna padají objekty (kostky) náhodnou rychlostí z náhodných pozic (osa X).
- Hra detekuje kolize (náraz košíku do padajícího tělesa), při úspěšném zachycení objekt zmizí a nahoře vygeneruje nový.

### Technická část
- **Použité knihovny:** `pygame` pro vykreslování, herní okno a ovládání klávesnicí; `random` pro náhodné pozicování padajících objektů.
- **Hlavní prvky:**
  - Hlavní herní smyčka (Game Loop) starající se o aktualizaci snímků a obsluhu událostí (`pygame.event.get()`).
  - Systém kolizí řešený pomocí porovnávání souřadnic hran obdélníků (AABB - Axis-Aligned Bounding Box).
  - Ošetření hranic obrazovky (zastavení pohybu tak, aby hráč nemohl vyjet do strany).
