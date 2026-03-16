# Flappy Pták

## Popis a cíl projektu
Projekt implementuje základ velmi známé a návykové hry Flappy Bird. Cílem je ovládat letícího ptáka (zatím reprezentován jako žlutý obdélník) a držet jej ve vzduchu. Aplikace slouží jednak jako trénink práce s herním rámcem Pygame, ale také poskytuje hráčům jednoduché procvičení postřehu. Cílovou skupinou je kdokoliv s chutí zahrát si oddychovou minihru.

## Funkcionalita programu
Hra se skládá z nekonečné herní smyčky (FPS omezovačem nastavené na 30), která zachytává události z klávesnice (skok postavy). 

**Technická část:**
* **Použité knihovny:** `pygame` (hlavní vizuální a herní logika – manipulace s okny, zachytávání mezerníku, časování cyklu, vykreslování základních tvarů).
* **Fyzika a algoritmy:** Ve smyčce je neustále uplatňována gravitace na hodnotu `ptak_y_zmena` zrychlující pád ptáka. Po stisku mezerníku je tato hodnota přepsána záporným vektorem vyslajícím hráče směrem vzhůru. Je implementována základní „kolize“ s hranicemi herní obrazovky.
* **Datové struktury a proměnné:** Objekt samotný se neskládá ze složitých datových třid a OOP v této fázi. K jeho pohybu postačí modifikace primitivních datových proměnných ukládajících jeho obdélníkové souřadnice a dynamicky se měnící rychlost pohybu.
