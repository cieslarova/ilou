# Flappy Pták - Fáze 1

## Popis a cíl projektu
Projekt implementuje základ velmi známé a návykové hry Flappy Bird. Cílem je ovládat letícího ptáka (zatím reprezentován jako žlutý obdélník) a držet jej ve vzduchu. Aplikace slouží jednak jako trénink práce s herním rámcem Pygame, ale také poskytuje hráčům jednoduché procvičení postřehu. Cílovou skupinou je kdokoliv s chutí zahrát si oddychovou minihru.

## Funkcionalita programu
Hra se skládá z nekonečné herní smyčky (FPS omezovačem nastavené na 30), která zachytává události z klávesnice (skok postavy). 

## Technická část
* **Použité knihovny:** `pygame` (hlavní vizuální a herní logika – manipulace s okny, zachytávání mezerníku, časování cyklu, vykreslování základních tvarů).
* **Fyzika a algoritmy:** Ve smyčce je neustále uplatňována gravitace na hodnotu `ptak_y_zmena` zrychlující pád ptáka. Po stisku mezerníku je tato hodnota přepsána záporným vektorem vyslajícím hráče směrem vzhůru. Je implementována základní „kolize“ s hranicemi herní obrazovky.
* **Datové struktury a proměnné:** Objekt samotný se neskládá ze složitých datových třid a OOP v této fázi. K jeho pohybu postačí modifikace primitivních datových proměnných ukládajících jeho obdélníkové souřadnice a dynamicky se měnící rychlost pohybu.

---

# Flappy Pták - Fáze 2

## Popis a cíl projektu
Ve druhé fázi hry se přidávají do cesty překážky v podobě klasických zelených trubek a s nimi i počítání úspěšně překonaných překážek v podobě skóre. Hra je rozšířena o princip smrti postavičky (náraz do trubky) a možnost opakovat hru.

## Funkcionalita programu
Hra se rozšířila o překážky letící z pravé strany obrazovky na levou. Hráč musí ptáka přesně navigovat do mezery mezi horní a dolní trubkou. Při každém proskočení se přičte 1 bod. V případě nárazu ptáka do trubky, dotyku s horním okrajem obrazovky nebo propadnutí dolní hranicí hra končí, pohyb se zastaví a vyskočí informační text instruující hráče o možnosti restartu hry stisknutím mezerníku.

## Technická část
* **Použité knihovny:** Přibyl modul `random` k náhodné generaci výšky mezer mezi trubkami.
* **Rozšíření algoritmů:**
  - **Detekce kolizí:** Je využita třída `pygame.Rect` obalující souřadnice ptáka i trubek do samostatných obdélníků, nad kterými je volána dedikovaná matematická knihovní funkce `colliderect()` počítající průsečík dvou čtverců.
  - **Restart hry:** Oddělení herního stavu do pomocné stavové proměnné `hra_bezi` na kterou reaguje herní loop vyhodnocováním (hráč žije = počítá se fyzika kolizí i skóre / hráč nežije = okno čeká na stisk mezerníku a zavolání vytvořené resetovací funkce do původního stavu).
* **Nové proměnné a prvky:** Proměnné pro rozměry a posouvání trubek na ose X a celkové herní skóre, plus grafické vykreslení (rendering) písma ve formátu z knihovny `pygame.font`.
