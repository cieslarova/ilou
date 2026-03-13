# Košík - Fáze 1

## Popis a cíl projektu
Cílem projektu je vytvořit jednoduchou arkádovou hru Košík pro procvičení základů knihovny Pygame. V této první fázi je vytvořeno herní okno, kde hráč ovládá jezdící čtvereček (košík) dole na obrazovce. Z horní části padá dolů jedna náhodně umístěná kostka (jídlo). Hra je určena pro začínající programátory, kteří si na ní ukáží principy herního prostředí, pohybu hráče a detekce kolizí. Tady se ještě nepočítá skóre ani životy.

## Funkcionalita programu
Program otevře malé herní okno o rozměrech 300x300 pixelů. Hráč se pohybuje pomocí šipek (doleva/doprava) po spodním okraji obrazovky, přičemž nevyjede mimo obrazovku. Z horní hrany mezitím konstantní rychlostí padá jedna kostka na náhodném místě osy X. Jakmile se košík dotkne kostky, kostka "zmizí" a je instantně vygenerována nová opět nahoře. Pokud košík kostku mine a ta propadne dolů, hra nevyhodí chybu ani neukončí běh, jen vygeneruje novou kostku nahoře.

## Technická část
- **Použité knihovny:** 
  - `pygame` pro vykreslování tvarů (obdélníky pro košík a padající jídlo), herní okno, obsluhu událostí a ovládání klávesnicí. 
  - `random` pro náhodné (`randint`) generování souřadnice X u jídla nahoře na obrazovce.
- **Struktura kódu a algoritmy:**
  - Hlavní herní smyčka (Game Loop) starající se o aktualizaci snímků, s frekvencí 60 FPS ovládanou přes `clock.tick(60)`.
  - Systém kolizí řešený pomocí statického porovnávání souřadnic a šířky hran obdélníků (AABB - Axis-Aligned Bounding Box).
  - Ošetření hranic obrazovky proti "odjetí" mimo monitor pomocí jednoduchých podmínek (`< 0` a `> sirka_okna`).
- **Datové struktury:**
  - Základní konvence – uchovávání souřadnic X a Y, společně s šířkou a rychlostí hráče (i kostky) v normálních datových proměnných. 

---

# Košík - Fáze 2

## Popis a cíl projektu
Ve druhé fázi se projekt výrazně rozšiřuje. Do hry je zavedeno počítání bodů (skóre) a zároveň i penalizace v podobě životů pro hráče, což poskytuje reálný konec hry. Mechanika padajících předmětů se proměnila – už nepadá jen jedna kostka, ale z oblohy se v zadaných intervalech generuje celá série malých kostek lišících se barvami.

## Funkcionalita programu
Hráč (košík) nyní musí chytat barevné kostky pro získání +1 skóre. Objevila se ale i nechtěná "zkažená" černá kostka. Pokud střetne košík černou kostku, hráč ztrácí 1 život. Stejně tak přijde o život tehdy, když nechá v pořádku propadnout jakoukoli jinou barevnou (dobrou) kostku na zem. Při ztrátě všech 5 životů obrazovka zešedne a vypíše se text zvěstující konec hry s výzvou, jestli si chce hráč pustit hru znovu klávesou `R` nebo hru ukončit klávesou `Q`. Na obrazovce je nově viditelný text vyčíslující v rozích aktuální počty Životů a Skóre.

## Technická část
- **Rozšíření algoritmů:**
  - **Práce s Pygame Fontem:** Zapracování nativních textur po okrajích okna (pomocí `pygame.font.SysFont` a `okno.blit()`).
  - **Spawnování s využitím časovače:** Generování kostek již není vázáno pouze na pád jedné jediné, ale je řízeno reálným počtem milisekund přes `pygame.time.get_ticks()`. Každých cca 1,8 vteřiny se vytvoří nová kostka.
  - **Pokročilé detekce kolizí s Listem a odpočet indexů:** Namísto jedné proměnné pro kostku se prochází celé pole aktuálně nakreslených kostek v cyklu. Aby při odmazávání nepadal kód vlivem snížení celkového pořadí indexu, všechny dotčené zachycené/propadlé kostky se zaznamenají do separátního listu a promažou se následně *zpětně odzadu* (`reverse=True`).
- **Nové datové struktury:**
  - `kostky` – Vícedimenzionální list polí (seznam), kde každý záznam nese pod sebou trojici pro jednotlivou kostičku: `[X, Y, RGB_barva]`.
  - `odstranene` – List kumulující indexové číslovky kostek, které se mají v aktuálním framu vymazat.
- **Úpravy a rozvoj:** 
  - Během Fáze 2 byl herní kód ošetřen o podrobné komentáře k logice prohledávání v cyklu `enumerate` a docstringy k interním funkcím pro zobrazení tak, aby projekt splňoval kritéria hodnocení a technické srozumitelnosti.
