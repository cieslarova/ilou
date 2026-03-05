# Duhový Had - Fáze 1

## Popis a cíl projektu
Cílem projektu je vytvořit klasickou arkádovou hru Had (Snake) v jazyce Python. V této první fázi je vytvořeno herní okno a je implementován základní pohyb hada (reprezentovaného jako jedna zelená kostka) po herní ploše. Projekt je vhodný pro demonstraci základních principů vývoje her a práce s událostmi v Pythonu.

## Funkcionalita programu
Program po spuštění otevře černé herní okno o rozměrech 600x400 pixelů. Hráč ovládá pohyb "hada" pomocí šipek na klávesnici (nahoru, dolů, doleva, doprava). V této rané fázi není implementováno sbírání potravy ani prodlužování hada. Hra končí (okno se zavře) ve chvíli, kdy had narazí do jakéhokoli okraje herního okna.

## Technická část
- **Použité knihovny**: 
  - `pygame` - hlavní knihovna pro tvorbu okna, vykreslování grafiky (obdélníku), čtení událostí z klávesnice a řízení frekvence snímků (pomocí `pygame.time.Clock`).
  - `time` - standardní knihovna pro práci s časem (zatím naimportována jako příprava pro další vývoj).
- **Struktura kódu a algoritmy**: 
  - Kód je řízen hlavní funkcí `herni_smycka()`, která obsahuje cyklus (`while not hra_konci`).
  - Každý průběh cyklem vyhodnotí stisk kláves, vypočítá novou pozici os X a Y a překreslí okno.
  - Ošetření kolize spočívá v jednoduché kontrole souřadnic hada oproti definované šířce a výšce okna.
- **Datové struktury**: 
  - Souřadnice a rychlost jsou uloženy v jednoduchých číselných proměnných. Formát barev využívá předdefinované tuple struktury (RGB hodnoty).

---

# Duhový Had - Fáze 2

## Popis a cíl projektu
Ve druhé fázi se projekt rozšiřuje o mechaniku sbírání jídla a s tím související prodlužování hada. Navíc je změněno ošetření kolize s krajem okna – herní okno je nyní "průjezdné" (had při přejetí okraje vyjede na protilehlé straně). Na závěr hra obdržela vizuální vylepšení ve formě "duhového efektu", kdy každý nový kousek těla hada získá náhodně vygenerovanou barvu, stejně jako nové jídlo.

## Funkcionalita programu
Hráč stále ovládá hada pomocí šipek. Hlavním cílem je nyní „sníst“ jídlo (barevný čtvereček), což hadovi přidá na délce a zvýší aktuální skóre zobrazené v levém horním rohu obrazovky. Pokud hlava hada přejede přes okraj obrazovky, had se plynule objeví na opačném kraji. Hra končí pouze ve chvíli, kdy had narazí do vlastního těla (což je možné od délky 5 a více).

## Technická část
- **Další použité knihovny**: Těženo ze standardní knihovny `random` pro generování pozice jídla a náhodných RGB barev pro jednotlivé díly hada.
- **Rozšíření algoritmů**: 
  - **Průchod zdmi**: Jednoduché ošetření pomocí podmínek if/elif přepisující X a Y souřadnice z jednoho kraje na druhý.
  - **Udržování délky**: Při každém kroku se nový bod (hlava) přidá do seznamu. Pokud velikost seznamu přesahuje definovanou délku hada (proměnná `delka_hada`), první (nejstarší) prvek ze seznamu se vymaže (pomocí `del seznam_hada[0]`). Působí to jako plynulý posun hadího těla vpřed.
  - **Náraz do těla**: Před každým vykreslením se zkontroluje, zda se souřadnice hlavy už nenachází ve zbylém seznamu pozic těla.
- **Nové datové struktury**:
  - `seznam_hada` - Seznam seznamů (list of lists/tuples) ukládající [X, Y] pozice každého dílu těla.
  - `barvy_hada` - Seznam tuple elementů uchovávající unikátní (RGB) barvu každého bloku hada v pořadí.
