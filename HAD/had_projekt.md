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
