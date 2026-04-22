# 🐼 Můj Panda3D Tahák a Slovníček

Tento soubor ti poslouží jako výukový materiál, abys rozuměla tomu, co se píše tvém kódu. Procházej si ho, kdykoliv budeš tápat, co nějaký termín znamená.

## 1. Základy hry (Založení okna a světa)

* **`ShowBase`**: Tlukoucí srdce tvé hry. Třída, která zastupuje základní rámec - "zapíná hru". Spouští herní okno, aktivuje 3D kameru a nastavuje takzvanou "Game Loop" (hlavní smyčku, která běží pořád dokola - třeba i 60x za vteřinu, aby hra vypadala plynule). Od ní se odvíjí všechno ostatní.
* **`WindowProperties`**: Nástroje pro úpravu chování samotného počítačového okna, ve kterém se tvá hra hraje. Můžeš jimi změnit titulek okna, uzamknout šipku myši uprostřed obrazovky (což je ve 3D hrách často nutné) nebo naprogramovat okno, aby nešlo zvětšovat.

## 2. Světlo a barvy (Aby nebyla černočerná tma)

Bez těchto objektů by byly tvé krásné 3D modely pravděpodobně úplně černé, protože by na ně nedopadalo žádné světlo.
* **`AmbientLight`**: Okolní světlo. Podobné malinké slabé žárovce, která ti ozařuje roh místnosti - zajišťuje, že žádné stíny na modelu nebudou úplně 100% černé.
* **`DirectionalLight`**: Směrové světlo. Chová se de-facto přesně jako slunce – střílí souběžné paprsky světla jedním jediným směrem dle tvého zadání. Strana modelu vystavená tomuto světlu je krásně osvícená a naopak.
* **`VBase4`**: Slouží k ukládání prvků, které mají rovnou čtyři hodnoty. Typicky se to používá pro míchání barev, kde čtyři hodnoty tvoří `(Červená, Zelená, Modrá, Průhlednost)`. Například zápis `1, 0, 0, 1` vytvoří jasnou absolutně neprůhlednou čistě červenou. Zápisy barev takto dosahují od 0 do 1.

## 3. Předměty a objekty ve hře (Strom uzlů)

Panda3D vidí celý svůj obrovský 3D svět jako jeden strom (tomu říkáme *Scene Graph*). Na neviditelný kořen se pak větví (napojuje) vše dál.
* **`PandaNode`**: Samotný uzel z tohoto obrovského vesmírného stromu. Vším, co má hra evidovat, se stává PandaNode (stromeček, hráčovka, tvoje kamera atd...).
* **`NodePath`**: Cesta k uzlu - je to jakýsi magický ovladač v tvé ruce. S tímto objektem v kódu měníš svět: když ho potáhneš za metodu `setPos()`, celý 3D model změní svoji X-Y-Z souřadnici ve světě.
* **`TextureStage`**: Slouží na složitější věci kolem "textur" (obrázků pokrytých na 3D model). Dává se dohromady třeba tehdy, když tvůj model potřebuje textury hned dvě na sobě a ty jim potřebuješ nastavit různou hodnotu "viditelnosti/stínu" přes sebe.

## 4. Animované postavy a modely

* **`Actor`**: Zvláštní herní postavička. Zatímco kámen je nepohyblivý statický soubor a načte se jen tak, tvůj hráč, který umí pohybovat nohama, potřebuje vlastní kosti (kostru postavy/modelu). Třída `Actor` načte tenhle složitější 3D soubor kosti i masa, vyvolává pohyby a umožňuje ti pustit animaci chůze povelem jako `actor.loop("chůze")`.

## 5. Jak do sebe věci naráží (Práce se srážkami / Collisions)

Jedna z nejdůležitějších kapitol – bez ní by jsi jen proletěla zemí do prázdna, protože by tě počítač nechal. Věci se samy o sobě nedotýkají.
* **`CollisionSphere`**: Matematická bublina/koule. Ta se obepne jako neviditelný plášť kolem tvého hráče nebo samotné mince a stará se o odhalení toho, "jestli už do sebe ty dvě věci právě teď nedrcly". Pro moderní počítače je výpočet koule s jinou koulí úplně to nejrychlejší zjišťování nárazu na světě.
* **`CollisionNode`**: Další náš speciální "uzel" do stromu - díky němu přivážeme výše zmíněnou srážkovou bublinu či jiný tvar tak, aby fyzicky patřil na svou minci/objekt se kterým chceme počítat náraz.
* **`CollisionHandlerQueue`**: Seznam, co se zrovna rozbilo / bouchlo (Fronta nárazů). Herní engine si odškrtne každým 1 políčkem záznam "Něco narazilo do Mince!". Ty pak tuhle listinu vezmeš a v Pythonu naprogramuješ: "Super! Hráč narazil do Mince, zvýšíme mu Skóre!"
* **`CollisionTraverser`**: Zlatý pracant, tzv. "kontrolor" na zkušebně. Prolézá celou tvou hru za kratší dobu než ty stihneš mrknout, neustále se dívá do 3D prostoru na neviditelné bubliny a neustále hlídá, jestli se přes sebe nenarušily/nepřekřížily.
* **`BitMask32`**: Třídění kategorií - koho se mají překážky všimnout a koho ne (Masky). Abychom počítači moc nekomplikovali už tak dost složitou detekci nárazů, nastavíme masku jedné zdi tak, že do ní může vrazit hráč. Ale zároveň tu samou masku vymažeme Mrakům, takže pokud se těma Mrakama prolétáváš, engine dokonce odmítne detekci nárazů s nimi řešit a sníží tím plynulost výkonu!

## 6. Texty přes celou obrazovku

* **`OnscreenText` a `TextNode`**: Rychlé nástroje do ruky, se kterými vyrobíš Obyčejný jednoduchý Text, například do horního okraje obrazovky ("GAME OVER", "SKORE: 100"). Jedná se o 2D výpis psaného textu - nestojí přímo uvnitř herního světa jako strom, ale leží "přilepený přímo čelem na 3D kameře".

## 7. Pomocníci od čistého jazyka Python

* **`random`**: Balíček sloužící k čisté náhodě a nahodilosti. Ať se rozptýlí nová mince zrovna zde, ať má mrak náhodně roztahaný tvar, atd - balíček Random si převezme čísla a vymyslí s nimi něco nepředvídatelného.
* **`math`**: Vyšší matematika v kostce - Sinus, Kosinus, práce s trojúhelníky, mocniny. Bez matematických operací tohoto balíčku bys ani náhodou přesně nevypočítala směr a naklonění, kvůli čemu má "tahle kulka rotovat určitým divným směrem, kam kouká hráč".
