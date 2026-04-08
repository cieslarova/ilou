# coin_collector_faze2.py
from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight, DirectionalLight, VBase4, WindowProperties
from panda3d.core import NodePath, PandaNode
from direct.actor.Actor import Actor
from panda3d.core import CollisionSphere, CollisionNode, CollisionHandlerQueue, CollisionTraverser, BitMask32
from direct.gui.OnscreenText import OnscreenText
import random

# Definice bitových masek pro kolize
# Každý typ objektu má svou masku, aby se určilo, s čím může kolidovat.
PLAYER_MASK = BitMask32(0x1) # Maska pro hráče
COIN_MASK = BitMask32(0x2)   # Maska pro mince

class Player:
    """
    Třída reprezentující hráče ve hře.
    Nyní obsahuje logiku pohybu a kolizní těleso.
    """
    def __init__(self, parent_node: ShowBase):
        """
        Inicializuje hráče, načte jeho 3D model, umístí ho do scény
        a nastaví kolizní těleso.
        :param parent_node: Instance ShowBase pro přístup k loaderu a renderu.
        """
        self.parent_node = parent_node
        self.model = parent_node.loader.loadModel("smiley")
        self.model.reparentTo(parent_node.render)
        self.model.setScale(0.5)
        self.model.setPos(0, 0, 0.5)
        self.model.setColor(0.8, 0.2, 0.2, 1)

        # Nastavení kolizního tělesa pro hráče
        # CollisionSphere(center_x, center_y, center_z, radius)
        collision_sphere = CollisionSphere(0, 0, 0, 0.5)
        collision_node = CollisionNode("player_collision")
        collision_node.addSolid(collision_sphere)
        collision_node.setFromCollideMask(PLAYER_MASK) # Hráč bude detekovat kolize s objekty s maskou PLAYER_MASK
        collision_node.setIntoCollideMask(BitMask32.allOff()) # Hráč nebude reagovat na kolize s jinými objekty (jen je detekuje)
        self.collision_np = self.model.attachNewNode(collision_node)
        # self.collision_np.show() # Pro ladění: zobrazí kolizní kouli
        print("Kolizní těleso hráče bylo nastaveno.")

        # Proměnné pro řízení pohybu
        self.move_forward = False
        self.move_backward = False
        self.move_left = False
        self.move_right = False
        self.speed = 10.0 # Rychlost pohybu hráče

    def update_movement(self, task):
        """
        Aktualizuje pozici hráče na základě stisknutých kláves.
        Tato metoda je volána v každém snímku hry.
        :param task: Objekt tasku z Panda3D.
        """
        dt = globalClock.getDt() # Čas od posledního snímku

        # Vypočet směru pohybu
        x_move = 0
        y_move = 0
        if self.move_forward:
            y_move += self.speed * dt
        if self.move_backward:
            y_move -= self.speed * dt
        if self.move_left:
            x_move -= self.speed * dt
        if self.move_right:
            x_move += self.speed * dt

        # Aplikace pohybu na model hráče
        self.model.setX(self.model, x_move)
        self.model.setY(self.model, y_move)

        return task.cont # Pokračovat v tasku

class Coin:
    """
    Třída reprezentující minci ve hře.
    Nyní obsahuje kolizní těleso a metodu pro odstranění.
    """
    def __init__(self, parent_node: ShowBase, position: tuple):
        """
        Inicializuje minci, načte její 3D model, umístí ji do scény
        a nastaví kolizní těleso.
        :param parent_node: Instance ShowBase pro přístup k loaderu a renderu.
        :param position: Trojice (x, y, z) určující pozici mince.
        """
        self.parent_node = parent_node
        self.model = parent_node.loader.loadModel("box")
        self.model.reparentTo(parent_node.render)
        self.model.setScale(0.2)
        self.model.setPos(position[0], position[1], position[2] + 0.1)
        self.model.setColor(0.9, 0.8, 0.1, 1)

        # Nastavení kolizního tělesa pro minci
        collision_sphere = CollisionSphere(0, 0, 0, 0.2)
        collision_node = CollisionNode("coin_collision")
        collision_node.addSolid(collision_sphere)
        collision_node.setFromCollideMask(COIN_MASK) # Mince bude detekovat kolize s objekty s maskou COIN_MASK
        collision_node.setIntoCollideMask(PLAYER_MASK) # Mince bude reagovat na kolize s objekty s maskou PLAYER_MASK
        self.collision_np = self.model.attachNewNode(collision_node)
        # self.collision_np.show() # Pro ladění: zobrazí kolizní kouli
        print(f"Kolizní těleso mince na pozici {position} bylo nastaveno.")

    def remove(self):
        """
        Odstraní model mince a její kolizní těleso ze scény.
        """
        if self.model:
            self.model.removeNode()
            self.model = None
        if self.collision_np:
            self.collision_np.removeNode()
            self.collision_np = None
        print("Mince byla odstraněna ze scény.")

class CoinCollectorGame(ShowBase):
    """
    Hlavní třída hry Coin Collector.
    Nyní obsahuje logiku pohybu hráče, generování mincí, detekci kolizí a skóre.
    """
    def __init__(self):
        """
        Konstruktor hry. Inicializuje Panda3D, nastaví scénu, načte objekty
        a nastaví herní logiku.
        """
        ShowBase.__init__(self)

        self.win.setClearColor(VBase4(0.5, 0.7, 1.0, 1))
        props = WindowProperties()
        props.setTitle("Coin Collector - Fáze 2")
        self.win.requestProperties(props)
        print("Panda3D okno bylo inicializováno.")

        # Nastavení kamery, aby sledovala hráče
        self.disableMouse() # Vypnutí defaultního ovládání kamery myší
        self.camera.setPos(0, -20, 15)
        self.camera.lookAt(0, 0, 0)
        self.taskMgr.add(self.update_camera, "update_camera_task")
        print("Kamera byla nastavena pro sledování hráče.")

        # Nastavení osvětlení scény
        ambient_light = AmbientLight("ambient_light")
        ambient_light.setColor(VBase4(0.6, 0.6, 0.6, 1))
        self.render.setLight(self.render.attachNewNode(ambient_light))

        directional_light = DirectionalLight("directional_light")
        directional_light.setColor(VBase4(0.8, 0.8, 0.7, 1))
        directional_light_node = self.render.attachNewNode(directional_light)
        directional_light_node.setHpr(45, -45, 0)
        self.render.setLight(directional_light_node)
        print("Osvětlení bylo nastaveno.")

        # Načtení modelu terénu (pole)
        try:
            self.field = self.loader.loadModel("models/plane")
            self.field.setScale(50, 50, 1)
        except Exception:
            from panda3d.core import CardMaker
            cm = CardMaker("plane")
            cm.setFrame(-25, 25, -25, 25)
            self.field = self.render.attachNewNode(cm.generate())
            self.field.setHpr(0, -90, 0)
        self.field.reparentTo(self.render)
        self.field.setPos(0, 0, -0.5)
        self.field.setColor(0.3, 0.6, 0.3, 1)
        print("Terén byl načten.")

        # Inicializace herních objektů
        self.player = Player(self)
        self.coins = []
        self.score = 0
        print("Hráč a seznam mincí byly inicializovány.")

        # Nastavení ovládání klávesnice pro pohyb hráče
        self.accept("w", self.set_move_forward, [True])
        self.accept("w-up", self.set_move_forward, [False])
        self.accept("s", self.set_move_backward, [True])
        self.accept("s-up", self.set_move_backward, [False])
        self.accept("a", self.set_move_left, [True])
        self.accept("a-up", self.set_move_left, [False])
        self.accept("d", self.set_move_right, [True])
        self.accept("d-up", self.set_move_right, [False])
        print("Ovládání klávesnice pro hráče bylo nastaveno.")

        # Přidání tasku pro aktualizaci pohybu hráče
        self.taskMgr.add(self.player.update_movement, "player_movement_task")

        # Inicializace kolizního traverseru a handleru
        self.cTrav = CollisionTraverser()
        self.cQueue = CollisionHandlerQueue()
        self.cTrav.addCollider(self.player.collision_np, self.cQueue)
        print("Kolizní systém byl inicializován.")

        # Přidání tasku pro detekci kolizí
        self.taskMgr.add(self.check_collisions, "check_collisions_task")

        # Generování mincí
        self.spawn_coins(10) # Vygeneruje 10 mincí na začátku hry
        print("Mince byly vygenerovány.")

        # Zobrazení skóre na obrazovce
        self.score_text = OnscreenText(text=f"Skóre: {self.score}",
                                       pos=(0.95, -0.95), scale=0.07,
                                       fg=(1, 1, 1, 1), align=TextNode.ARight,
                                       mayChange=True)
        print("Text skóre byl zobrazen na obrazovce.")

        print("Fáze 2 inicializace dokončena. Hra je interaktivní.")

    def set_move_forward(self, state: bool):
        """Nastaví stav pohybu vpřed."""
        self.player.move_forward = state

    def set_move_backward(self, state: bool):
        """Nastaví stav pohybu vzad."""
        self.player.move_backward = state

    def set_move_left(self, state: bool):
        """Nastaví stav pohybu vlevo."""
        self.player.move_left = state

    def set_move_right(self, state: bool):
        """Nastaví stav pohybu vpravo."""
        self.player.move_right = state

    def update_camera(self, task):
        """
        Aktualizuje pozici kamery tak, aby sledovala hráče.
        :param task: Objekt tasku z Panda3D.
        """
        player_pos = self.player.model.getPos()
        # Nastavení kamery za hráče a mírně nad něj
        self.camera.setPos(player_pos.getX(), player_pos.getY() - 15, player_pos.getZ() + 10)
        self.camera.lookAt(player_pos) # Kamera se dívá na hráče
        return task.cont

    def spawn_coins(self, count: int):
        """
        Vygeneruje zadaný počet mincí na náhodných pozicích.
        :param count: Počet mincí k vygenerování.
        """
        for _ in range(count):
            # Náhodné pozice v rámci terénu (např. -45 až 45 na X a Y)
            x = random.uniform(-45, 45)
            y = random.uniform(-45, 45)
            coin = Coin(self, (x, y, 0))
            self.coins.append(coin)
        print(f"{count} mincí bylo vygenerováno na náhodných pozicích.")

    def check_collisions(self, task):
        """
        Kontroluje kolize mezi hráčem a mincemi.
        :param task: Objekt tasku z Panda3D.
        """
        self.cTrav.traverse(self.render) # Provede průchod kolizním systémem

        # Zpracování kolizí
        for entry in self.cQueue.getEntries():
            from_node = entry.getFromNodePath().node()
            into_node = entry.getIntoNodePath().node()

            # Kontrola, zda hráč kolidoval s mincí
            if from_node.getName() == "player_collision" and into_node.getName() == "coin_collision":
                # Nalezení mince, která byla sebrána
                for coin in self.coins:
                    if coin.collision_np and coin.collision_np.node() == into_node:
                        coin.remove() # Odstranění mince ze scény
                        self.coins.remove(coin) # Odstranění mince ze seznamu
                        self.score += 1 # Zvýšení skóre
                        self.score_text.setText(f"Skóre: {self.score}") # Aktualizace textu skóre
                        print(f"Mince sebrána! Aktuální skóre: {self.score}")
                        break # Ukončení vnitřní smyčky po nalezení mince

        # Pokud dojdou mince, vygenerujeme nové (pro nekonečnou hru)
        if not self.coins:
            print("Všechny mince byly sebrány. Generuji nové.")
            self.spawn_coins(10)

        return task.cont

if __name__ == "__main__":
    # Import TextNode pro OnscreenText
    from panda3d.core import TextNode
    game = CoinCollectorGame()
    game.run()
