Gemini
Regex101: Vysvětlení a použití nástroje
Konverzace s Gemini
Váš pokyn
ahoj co to je vysvetli mi to ja nechapu k cemu to je https://regex101.com/

Odpověď Gemini
Ahoj! Stránka Regex101.com je interaktivní nástroj pro tvorbu, testování a ladění tzv. regulárních výrazů (zkráceně regex).

Abych ti to vysvětlil úplně jednoduše:

Co je to regulární výraz (Regex)?
Představ si, že v textu něco hledáš (jako když zmáčkneš Ctrl + F). Klasické hledání najde jen přesné slovo (např. „pes“). Regex je ale „vyhledávání na steroidech“. Pomocí speciálních značek a symbolů můžeš hledat vzor, ne jen konkrétní slovo.

Příklad:

Místo hledání konkrétního čísla „123“ můžeš říct: „Najdi mi v tomhle textu všechna místa, kde je 9 čísel za sebou“ (takže to najde všechna telefonní čísla).

Nebo: „Najdi všechna slova, která začínají velkým písmenem a končí tečkou.“

Nebo: „Ověř, jestli to, co uživatel zadal do formuláře, vypadá jako skutečný e-mail.“

K čemu je tedy Regex101?
Regulární výrazy vypadají pro lidské oko často jako náhodná směs závorek, lomítek a znaků (např. /^([a-z0-9_\.-]+)@([\da-z\.-]+)\.([a-z\.]{2,6})$/). Je velmi těžké se v tom vyznat.

Regex101 ti pomáhá takto:

Vysvětlení (Explanation): Vpravo nahoře ti stránka polopatě (v angličtině) rozebere, co každá část tvého výrazu dělá.

Testování: Do velkého pole (Test String) vložíš svůj text a nahoře píšeš regex. Okamžitě vidíš barevně zvýrazněné výsledky, které tvůj vzorec našel.

Knihovna (Library): Můžeš tam najít vzorce, které už vytvořili jiní (třeba pro ověření hesla, PSČ, kreditní karty atd.).

Generátor kódu: Když tvůj vzorec funguje, stránka ti vygeneruje kód, který jen zkopíruješ do svého programu (v Pythonu, JavaScriptu, PHP atd.).

Kdo to používá?
Hlavně programátoři, správci systémů nebo datoví analytici. Používají to, když potřebují rychle vyčistit data, hromadně něco přejmenovat nebo automaticky kontrolovat textové vstupy.

Zjednodušeně: Je to takové pískoviště, kde si zkoušíš složité vyhledávací vzorce, aby ses ujistil, že fungují správně, než je použiješ v praxi.

Váš pokyn
Vytvoř mi prosím nějaký konkrétní příklad pro https://regex101.com/

Odpověď Gemini
Rád ti ukážu konkrétní příklad. Pojďme si nasimulovat situaci, kdy máš dlouhý text a potřebuješ z něj vytáhnout všechny e-mailové adresy.

Otevři si regex101.com a postupuj podle těchto kroků:

1. Vlož testovací text (Pole "Test String")
Do toho velkého prostředního pole vlož tento text:

„Ahoj, napiš mi na email petr.novak@seznam.cz nebo na firmu info@firma.cz. Moje stará adresa byla pokus123@gmail.com, tu už nepoužívej.“

2. Zadej vyhledávací vzorec (Pole "Regular Expression")
Do horního řádku (vedle lomítek / /) vlož tento vzorec:
[\w.-]+@[\w.-]+\.[a-z]{2,}

3. Co se stane?
V textu: Okamžitě uvidíš, že všechny tři e-maily se barevně podbarvily. To znamená, že je tvůj Regex našel.

Vpravo (Explanation): Tam ti stránka přesně vysvětluje, co která část tvého vzorce dělá:

[\w.-]+ – najdi jedno nebo více písmen, teček nebo pomlček.

@ – pak tam musí být přesně zavináč.

[\w.-]+ – pak znovu nějaká písmena/tečky (doména).

\. – pak musí následovat tečka (musí před ní být zpětné lomítko, protože samotná tečka v regexu znamená „jakýkoliv znak“).

[a-z]{2,} – a na konci musí být aspoň 2 malá písmena (koncovka jako .cz, .com, .org).

Další rychlý tip: Vyhledání data
Zkus smazat vzorec nahoře a nahradit ho tímhle:
\d{1,2}\.\s?\d{1,2}\.\s?\d{4}

A do textu napiš: „Dnes je 24. 12. 2024 a příště se uvidíme 1.1.2025.“

\d{1,2} – znamená: najdi 1 až 2 číslice.

\. – pak tečku.

\s? – pak možná mezeru (otazník říká, že tam ta mezera může, ale nemusí být).

Proč je to super?
Kdybys měl dokument o 500 stránkách, tak pomocí tohoto krátkého kódu z něj během sekundy vytáhneš všechna data, e-maily nebo třeba částky v korunách.

Základní tutoriál pro práci s Regex101
Tento video-průvodce ti ukáže, jak se na stránce regex101.com orientovat a jak začít psát své první vyhledávací vzory krok za krokem.

Learn Regex Online: Basic Tryouts with Regex101 for Beginners - YouTube
LearnAwesome · 639 zhlédnutí


Váš pokyn
Vytvoř mi prosím jednoduchý úvodní tutoriál.

Odpověď Gemini
Jasně, pojďme na to! Uděláme si tvůj první „Regex pokus“ krok za krokem. Představ si, že jsi detektiv a hledáš v hromadě papírů všechna česká telefonní čísla.

Krok 1: Orientace na „place“
Otevři si Regex101.com. Stránka je rozdělená na několik důležitých zón:

Flavor (vlevo nahoře): Tady si vybíráš „nářečí“. Nejpoužívanější je PCRE2 (PHP) nebo JavaScript. Pro začátek to neřeš a nechej tam to, co tam je.

Regular Expression (horní lišta): Tady píšeš svůj „vzorec“ (to kouzlo).

Test String (velké pole uprostřed): Sem vložíš text, ve kterém chceš vyhledávat.

Explanation (vpravo nahoře): Tady ti web lidsky vysvětlí, co tvůj vzorec zrovna dělá.

Krok 2: Vložení dat (Test String)
Zkopíruj a vlož následující řádky do pole Test String:

Moje číslo je 777 123 456.
Kamarád má 608111222.
Tohle není číslo: 12345.
A tohle je stará pevná linka: 222 333 444.

Krok 3: Psaní vzorce (Regular Expression)
Teď budeme do horního pole postupně psát vzorec, abychom našli jen ty mobily (9 číslic). Sleduj, jak se text v poli Test String začne podbarvovat:

Napiš jen \d.

Co se stane: Podbarví se úplně každá číslice zvlášť. \d totiž znamená „digit“ (číslice).

Uprav to na \d{3}.

Co se stane: Podbarví se trojice čísel. {3} říká: „chci přesně tři číslice za sebou“.

Teď zkusíme najít celé číslo s mezerami: \d{3}\s\d{3}\s\d{3}.

Co se stane: Najde to „777 123 456“ a „222 333 444“. \s znamená „space“ (mezera).

Krok 4: Ladění (Tady začíná ta zábava)
Všimni si, že nám to nenašlo číslo 608111222, protože v něm nejsou mezery. Jak to opravit, aby to našlo obojí? Použijeme otazník, který říká: „tohle předemnou (mezera) tam může, ale nemusí být“.

Zadej do horního pole tohle:
\d{3}\s?\d{3}\s?\d{3}

Výsledek: Teď web označil všechny tři telefonní čísla! To krátké 12345 nechal být, protože jich není devět.

Rychlá nápověda (Cheat Sheet)
Když zapomeneš, co která zkratka znamená, koukni se v Regex101 do pravého dolního rohu (Quick Reference). Tady jsou ty nejčastější:

\d = jakákoliv číslice

\w = jakékoliv písmeno nebo číslo

\s = mezera nebo tabulátor

. = úplně jakýkoliv znak (tečka je žolík)

+ = jeden nebo vícekrát

* = nula nebo vícekrát

? = nula nebo jedenkrát (nepovinné)

Baví tě to? Pokud chceš, můžu ti dát „bojový úkol“ – třeba jak najít v textu všechny ceny v korunách (např. 150 Kč, 25,50 Kč atd.), nebo můžeme zkusit něco jiného!

Váš pokyn
Vytvoř mi krátký pyhon skript s demo daty

Odpověď Gemini
Tady máš jednoduchý skript, který ti ukáže, jak ty „kouzelné formule“, které jsi zkoušel na webu, přenést přímo do tvého počítače. V Pythonu k tomu používáme vestavěnou knihovnu re (zkratka pro Regular Expressions).

Python skript: Detektiv v textu
Tento skript vezme kousek textu a automaticky z něj „vytáhne“ všechny e-maily a data.

Python
import re

# 1. Demo data (text, ve kterém budeme hledat)
text = """
Dobrý den, 
posílám potvrzení objednávky ze dne 12.05.2024. 
V případě dotazů pište na podpora@eshop.cz nebo přímo mě na petr.novak@firma.com.
Další revize proběhne 01. 06. 2024.
"""

# 2. Definice vzorců (to jsou ty řetězce z Regex101)
# Hledáme e-maily
pattern_email = r"[\w\.-]+@[\w\.-]+\.[a-z]{2,}"

# Hledáme data (včetně těch s mezerami za tečkou)
pattern_datum = r"\d{1,2}\.\s?\d{1,2}\.\s?\d{4}"

# 3. Samotné vyhledávání
emaily = re.findall(pattern_email, text)
data = re.findall(pattern_datum, text)

# 4. Výpis výsledků
print("--- Nalezené e-maily ---")
for email in emaily:
    print(f"Nalezeno: {email}")

print("\n--- Nalezena data ---")
for d in data:
    print(f"Datum: {d}")
Co se v kódu děje?
import re: Načteš nástroje pro práci s regulárními výrazy.

r"...": To písmeno r před uvozovkami znamená „raw string“. V Pythonu je to u regexu důležité, aby si program nepletl zpětná lomítka (třeba \d) s jinými příkazy.

re.findall(vzorec, text): Tohle je ta nejdůležitější funkce. Prohledá celý text a vrátí ti seznam (list) všeho, co odpovídá tvému vzorci.

Jak si to vyzkoušet?
Máš-li nainstalovaný Python, ulož kód do souboru (např. hledac.py) a spusť ho.

Můžeš si zkusit upravit proměnnou text nebo změnit vzorce a sledovat, co to najde.

Chceš, abych ti pomohl upravit ten skript tak, aby hledal něco jiného? Třeba ceny, rodná čísla nebo odkazy na webové stránky?

Váš pokyn
Prosím skript, který ověří, že uživatel zadal v terminálu validní email

Odpověď Gemini
Tady je skript, který běží v nekonečné smyčce a neustále se uživatele ptá na e-mail, dokud nezadá takový, který odpovídá našemu pravidlu.

Všimni si, že ve vzorci používáme znaky ^ (začátek) a $ (konec), aby skript kontroloval celý zadaný text a ne jen jeho část.

Python skript pro validaci v terminálu
Python
import re

def validuj_email():
    # Definice regex vzorce pro email
    # ^ = začátek řetězce
    # $ = konec řetězce
    regex_vzor = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    print("--- Validátor e-mailových adres ---")
    print("(Pro ukončení napište 'konec')\n")

    while True:
        uzivatel_vstup = input("Zadejte svůj e-mail: ").strip()

        if uzivatel_vstup.lower() == 'konec':
            print("Nashledanou!")
            break

        # re.fullmatch kontroluje, zda celý text odpovídá vzorci
        if re.fullmatch(regex_vzor, uzivatel_vstup):
            print(f"✅ Skvělé! '{uzivatel_vstup}' je validní e-mail.\n")
            # Tady by kód normálně pokračoval dál (např. uložení do databáze)
            break 
        else:
            print(f"❌ Chyba: '{uzivatel_vstup}' není platná adresa. Zkuste to znovu.\n")

if __name__ == "__main__":
    validuj_email()
Co je v tomto skriptu jinak než minule?
input(): Standardní funkce Pythonu, která zastaví program a čeká, až uživatel něco napíše a zmáčkne Enter.

.strip(): Užitečná drobnost, která ze vstupu odstraní nechtěné mezery na začátku nebo na konci (častá chyba při kopírování textu).

re.fullmatch(): Zatímco re.findall hledá všechny výskyty kdekoliv v textu, fullmatch vyžaduje, aby vzorci odpovídal úplně celý zadaný řetězec. To je pro formuláře ideální.

^[a-zA-Z0-9._%+-]+...: Tento vzorec je o něco robustnější než ten předchozí – povoluje v první části e-mailu i znaky jako %, + nebo -, které jsou v e-mailech legální.

Malá výzva pro tebe:
Zkusil bys do skriptu přidat podmínku, která uživatele nepustí dál, pokud je e-mail z konkrétní domény? Například pokud bys chtěl zakázat všechny e-maily končící na @seznam.cz? (Hint: stačí přidat další if před nebo za regex kontrolu).

Mám ti ukázat, jak takové zakázání konkrétní domény v kódu udělat?

Váš pokyn
Vygeneruj mi prosím soubor s textem, obchodní dopis, který bude obsahovat minimálně 3 emaily a 400 slov na téma zdravá výživa a výživové doplňky a vitamíny, atd.

Odpověď Gemini
Tady je tvůj obchodní dopis. Obsah jsem vyladil tak, aby působil profesionálně, a zároveň jsem do něj „schoval“ požadované e-maily pro tvé další testování v Pythonu nebo na Regex101.

Soubor si můžeš stáhnout níže.
Ikona aplikace TXT
 obchodni_d...pis_zdravi 
TXT






Gemini není člověk. Gemini může dělat chyby (i co se týče lidí), proto je potřeba si odpovědi kontrolovat. Vaše soukromí a GeminiOtevře se v novém okně

Předmět: Návrh strategického partnerství v oblasti moderní suplementace a holistického zdraví

Vážený pane řediteli,

obracím se na Vás jménem společnosti BioVita Solutions s.r.o., která se již desátým rokem specializuje na vývoj a distribuci prémiových doplňků stravy a komplexních vitamínových řešení. Vzhledem k Vašim aktivitám v oblasti fitness a wellness center věříme, že by naše portfolio mohlo výrazně obohatit nabídku pro Vaše klienty, kteří hledají vědecky podloženou cestu k optimálnímu zdraví.

Současná doba klade na lidský organismus extrémní nároky. Chronický stres, nedostatek spánku a environmentální toxiny vyčerpávají naše vnitřní zásoby mikroživin rychleji, než je dokážeme doplňovat běžnou stravou. I při dodržování zásad zdravé výživy se často potýkáme s deficity klíčových látek. Naše společnost proto klade důraz na maximální biodostupnost. Například naše liposomální technologie u vitamínu C a D3 umožňuje vstřebatelnost přesahující 90 %, což je u běžných tabletových forem prakticky nedosažitelné. Pro technické dotazy ohledně složení můžete kontaktovat naše laboratorní oddělení na adrese: laborator@biovita-solutions.cz.

Zdravá výživa není jen o kaloriích, ale o palivu pro naše buňky. Zaměřujeme se na synergii látek – naše komplexy hořčíku jsou obohaceny o vitamín B6 v aktivní formě P-5-P, což zajišťuje okamžitý transport do tkání. Kromě základních minerálů a vitamínů se věnujeme i adaptogenům, jako je Ashwagandha či Rhodiola, které pomáhají organismu adaptovat se na fyzickou i psychickou zátěž. V případě zájmu o velkoobchodní ceník či vzorky produktů se prosím obraťte na naše obchodní oddělení: obchodni.referent@zdrava-linia.cz.

Věříme, že prevence je nejlevnější a nejúčinnější formou medicíny. Naše doplňky stravy podléhají přísným klinickým testům a neobsahují zbytečná plnidla, barviva ani konzervanty. Jsme hrdí na to, že spolupracujeme s předními nutričními terapeuty po celé Evropě, se kterými konzultujeme každou novou recepturu. Cílem je vytvořit ekosystém, kde doplňky stravy nejsou jen náhodnými nákupy, ale logickou součástí promyšleného životního stylu.

Pokud byste měl zájem o osobní schůzku nebo prezentaci našich produktů přímo ve Vašem centru, neváhejte mě kontaktovat. Rád Vám představím možnosti věrnostního programu pro Vaše trenéry a klienty. Naše zákaznická podpora je Vám k dispozici pro jakékoli operativní dotazy na e-mailu: podpora.klienti@bio-wellness-premium.com.

Těším se na případnou budoucí spolupráci a přeji Vám mnoho úspěchů ve Vašem podnikání i v cestě za lepším zdravím.

S úctou a přáním pevného zdraví,

Mgr. Marek Vitamínský
Senior konzultant pro strategický rozvoj
BioVita Solutions s.r.o.
obchodni_dopis_zdravi.txt
Zobrazuje se položka obchodni_dopis_zdravi.txt