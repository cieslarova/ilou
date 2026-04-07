# coin_collector_faze1.py
from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight, DirectionalLight, VBase4, WindowProperties
from panda3d.core import NodePath, PandaNode
from direct.actor.Actor import Actor # Pro animované modely, i když zde jen statické

class Player:
    """
    Třída reprezentující hráče ve hře.
    V této fázi pouze drží model hráče a jeho počáteční pozici.
    """
    def __init__(self, parent_node: NodePath):
        """
        Inicializuje hráče, načte jeho 3D model a umístí ho do scény.
        :param parent_node: NodePath, ke které bude model hráče připojen.
        """
        # Načtení jednoduchého modelu hráče (např. koule).
        # Pro reálnou hru by se zde načítal komplexnější model.
        self.model = parent_node.loader.loadModel("smiley")
        self.model.reparentTo(parent_node.render) # Připojení modelu k renderovacímu grafu
        self.model.setScale(0.5) # Nastavení velikosti hráče
        self.model.setPos(0, 0, 0.5) # Nastavení počáteční pozice hráče (nad zemí)
        self.model.setColor(0.8, 0.2, 0.2, 1) # Nastavení barvy hráče (červená)
        print("Hráč byl inicializován a umístěn do scény.")

class Coin:
    """
    Třída reprezentující minci ve hře.
    V této fázi pouze drží model mince a její počáteční pozici.
    """
    def __init__(self, parent_node: NodePath, position: tuple):
        """
        Inicializuje minci, načte její 3D model a umístí ji do scény.
        :param parent_node: NodePath, ke které bude model mince připojen.
        :param position: Trojice (x, y, z) určující pozici mince.
        """
        # Načtení jednoduchého modelu mince (např. válec).
        self.model = parent_node.loader.loadModel("box")
        self.model.reparentTo(parent_node.render) # Připojení modelu k renderovacímu grafu
        self.model.setScale(0.2) # Nastavení velikosti mince
        self.model.setPos(position[0], position[1], position[2] + 0.1) # Nastavení pozice mince (mírně nad zemí)
        self.model.setColor(0.9, 0.8, 0.1, 1) # Nastavení barvy mince (zlatá)
        print(f"Mince byla inicializována na pozici {position} a umístěna do scény.")

class CoinCollectorGame(ShowBase):
    """
    Hlavní třída hry Coin Collector, dědící od ShowBase z Panda3D.
    Obsahuje inicializaci 3D scény, kamery, osvětlení a herních objektů.
    """
    def __init__(self):
        """
        Konstruktor hry. Inicializuje Panda3D, nastaví scénu a načte objekty.
        """
        ShowBase.__init__(self) # Volání konstruktoru rodičovské třídy ShowBase

        # Nastavení názvu okna hry
        self.win.setClearColor(VBase4(0.5, 0.7, 1.0, 1)) # Světle modrá obloha
        props = WindowProperties()
        props.setTitle("Coin Collector - Fáze 1")
        self.win.requestProperties(props)
        print("Panda3D okno bylo inicializováno.")

        # Nastavení kamery
        # Kamera je umístěna výše a dívá se dolů na scénu.
        self.camera.setPos(0, -20, 15) # Pozice kamery (x, y, z)
        self.camera.lookAt(0, 0, 0) # Kamera se dívá na střed scény
        print("Kamera byla nastavena.")

        # Nastavení osvětlení scény
        # Ambientní světlo pro celkové prosvětlení scény.
        ambient_light = AmbientLight("ambient_light")
        ambient_light.setColor(VBase4(0.6, 0.6, 0.6, 1)) # Šedé ambientní světlo
        self.render.setLight(self.render.attachNewNode(ambient_light))
        print("Ambientní osvětlení bylo přidáno.")

        # Směrové světlo simulující slunce.
        directional_light = DirectionalLight("directional_light")
        directional_light.setColor(VBase4(0.8, 0.8, 0.7, 1)) # Nažloutlé směrové světlo
        directional_light_node = self.render.attachNewNode(directional_light)
        directional_light_node.setHpr(45, -45, 0) # Směr světla
        self.render.setLight(directional_light_node)
        print("Směrové osvětlení bylo přidáno.")

        # Načtení modelu terénu (pole)
        # Použijeme jednoduchou rovinu jako terén.
        try:
            self.field = self.loader.loadModel("models/plane")
            self.field.setScale(50, 50, 1)
        except Exception:
            from panda3d.core import CardMaker
            cm = CardMaker("plane")
            cm.setFrame(-25, 25, -25, 25)
            self.field = self.render.attachNewNode(cm.generate())
            self.field.setHpr(0, -90, 0)
        self.field.reparentTo(self.render) # Připojení terénu k renderovacímu grafu
        self.field.setPos(0, 0, -0.5) # Umístění terénu mírně pod nulovou výšku
        self.field.setColor(0.3, 0.6, 0.3, 1) # Nastavení barvy terénu (zelená)
        print("Terén (pole) byl načten a umístěn do scény.")

        # Inicializace herních objektů
        self.player = Player(self) # Vytvoření instance hráče
        self.coins = []
        # Vytvoření několika statických mincí pro ukázku
        self.coins.append(Coin(self, (5, 5, 0)))
        self.coins.append(Coin(self, (-5, -5, 0)))
        self.coins.append(Coin(self, (0, 7, 0)))
        print("Herní objekty (hráč a mince) byly inicializovány.")

        # Zde by v budoucích fázích byla implementována herní logika,
        # jako je pohyb hráče, detekce kolizí, správa skóre atd.
        print("Fáze 1 inicializace dokončena. Scéna je připravena.")

if __name__ == "__main__":
    # Vytvoření instance hry a její spuštění
    game = CoinCollectorGame()
    game.run()
