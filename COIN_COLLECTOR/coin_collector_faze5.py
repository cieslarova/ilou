# coin_collector_faze4.py
from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight, DirectionalLight, VBase4, WindowProperties
from panda3d.core import NodePath, PandaNode, Filename, TextureStage
from direct.actor.Actor import Actor
from panda3d.core import CollisionSphere, CollisionNode, CollisionHandlerQueue, CollisionTraverser, BitMask32
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode
import random
import math

# Definice bitových masek pro kolize
PLAYER_MASK = BitMask32(0x1)
COIN_MASK = BitMask32(0x2)

# Cesty k vygenerovaným texturám
GRASS_TEX_PATH = Filename.fromOsSpecific(r"C:\Users\elen\.gemini\antigravity\brain\924f0dd1-e107-4b0c-b348-7cf7b4768e90\grass_texture_1776182405669.png")
COIN_TEX_PATH = Filename.fromOsSpecific(r"C:\Users\elen\.gemini\antigravity\brain\924f0dd1-e107-4b0c-b348-7cf7b4768e90\coin_texture_1776182388693.png")

class Player:
    """
    Třída reprezentující hráče ve hře.
    Ve Fázi 4 přidáno kutálení pro lepší vizuální efekt.
    """
    def __init__(self, parent_node: ShowBase):
        self.parent_node = parent_node
        try:
            self.model = parent_node.loader.loadModel("smiley")
        except Exception:
            self.model = parent_node.render.attachNewNode("player_placeholder")
            from panda3d.core import GeomNode, GeomVertexFormat, GeomVertexData, Geom, GeomTriangles, GeomVertexWriter
            format = GeomVertexFormat.getV3n3cpt2()
            vdata = GeomVertexData('sphere', format, Geom.UHDynamic)
            vertex = GeomVertexWriter(vdata, 'vertex')
            vertex.addData3f(0, 0, 0)
            geom = Geom(vdata)
            snode = GeomNode('sphere_node')
            snode.addGeom(geom)
            self.model = parent_node.render.attachNewNode(snode)

        self.model.reparentTo(parent_node.render)
        self.model.setScale(0.5)
        self.initial_pos = (0, 0, 0.5)
        self.model.setPos(self.initial_pos)
        self.model.setColor(0.8, 0.2, 0.2, 1)

        # Uzly pro oddělení pohybu a rotace, aby se mohla kulička správně odvalovat
        # self.model_root = parent_node.render.attachNewNode("player_root")
        # self.model.reparentTo(self.model_root)
        
        collision_sphere = CollisionSphere(0, 0, 0, 1.5)
        collision_node = CollisionNode("player_collision")
        collision_node.addSolid(collision_sphere)
        collision_node.setFromCollideMask(PLAYER_MASK)
        collision_node.setIntoCollideMask(BitMask32.allOff())
        self.collision_np = self.model.attachNewNode(collision_node)
        # self.collision_np.show() # Skryto ve Fázi 4 pro hezčí vizuál

        self.move_forward = False
        self.move_backward = False
        self.move_left = False
        self.move_right = False
        self.speed = 10.0

    def update_movement(self, task):
        """Aktualizuje pozici hráče a simuluje jeho kutálení."""
        dt = globalClock.getDt()

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

        # Posun v prostoru
        curr_pos = self.model.getPos()
        self.model.setPos(curr_pos[0] + x_move, curr_pos[1] + y_move, curr_pos[2])

        # Efekt kutálení (rotace modelu podle směru a vzdálenosti pohybu)
        if x_move != 0 or y_move != 0:
            speed_factor = 250 # Přibližný faktor rychlosti odvalování
            # Rotace směrem dopředu znamená naklánění vpřed (Pitch), směrem do boku naklánění doboku (Roll)
            self.model.setHpr(self.model, 0, -y_move * speed_factor, x_move * speed_factor)

        return task.cont

    def reset(self):
        """Resetuje pozici hráče a jeho natočení."""
        self.model.setPos(self.initial_pos)
        self.model.setHpr(0, 0, 0) # Reset rotace
        self.move_forward = False
        self.move_backward = False
        self.move_left = False
        self.move_right = False


class Coin:
    """
    Třída reprezentující minci.
    Fáze 4: Textury, rotace a skákavá animace (vznášení).
    """
    def __init__(self, parent_node: ShowBase, position: tuple):
        self.parent_node = parent_node
        self.initial_z = position[2] + 0.3 # Zvýšíme základní posazení
        self.random_offset = random.random() * 10 # Náhodný offset pro animaci, aby všechny mince nepulzovaly stejně
        
        try:
            self.model = parent_node.loader.loadModel("box")
        except Exception:
            self.model = parent_node.render.attachNewNode("coin_placeholder")

        self.model.reparentTo(parent_node.render)
        self.model.setScale(0.3) # Mírně zvětšeno
        self.model.setPos(position[0], position[1], self.initial_z)
        
        # Fáze 4: Použití zlaté textury
        try:
            tex = parent_node.loader.loadTexture(COIN_TEX_PATH)
            self.model.setTexture(tex)
            self.model.setColor(1, 1, 1, 1) # Vyresetování barvy pod texturou
        except:
            self.model.setColor(0.9, 0.8, 0.1, 1) # Nouzová zlatá barva

        collision_sphere = CollisionSphere(0, 0, 0, 1.5)
        collision_node = CollisionNode("coin_collision")
        collision_node.addSolid(collision_sphere)
        collision_node.setFromCollideMask(COIN_MASK)
        collision_node.setIntoCollideMask(PLAYER_MASK)
        self.collision_np = self.model.attachNewNode(collision_node)
        # self.collision_np.show() # Skryto ve fázi 4

    def update_animation(self, dt, current_time):
        """Animuje minci: Rotace a vznášení (pulzování)."""
        if self.model:
            # 1. Rotace dokola
            self.model.setH(self.model, 90 * dt)
            
            # 2. Vznášení nahoru a dolů (Sinusoida)
            # current_time udává plynulý čas od startu hry
            new_z = self.initial_z + math.sin(current_time * 3.0 + self.random_offset) * 0.2
            self.model.setZ(new_z)

    def remove(self):
        """Odstraní model mince a její kolizní těleso ze scény."""
        if self.model:
            self.model.removeNode()
            self.model = None
        if self.collision_np:
            self.collision_np.removeNode()
            self.collision_np = None


class CoinCollectorGame(ShowBase):
    """
    Hlavní třída hry Coin Collector - Fáze 4.
    """
    def __init__(self):
        ShowBase.__init__(self)

        # Hezčí jasnější barva oblohy (Skyblue - kreslený styl)
        self.win.setClearColor(VBase4(0.4, 0.7, 0.9, 1))
        
        props = WindowProperties()
        props.setTitle("Coin Collector - Fáze 4 (Vylepšená Grafika)")
        props.setSize(1024, 768) # Pro jistotu nastavíme pěkné rozlišení
        self.win.requestProperties(props)

        self.disableMouse()
        
        # Kamera bude umístěna později v metodě update_camera, dáme jí počáteční hodnotu
        self.camera.setPos(0, -20, 15)
        self.camera.lookAt(0, 0, 0)
        self.taskMgr.add(self.update_camera, "update_camera_task")

        # Fáze 4: Osvětlení se stíny (Shader Generator)
        self.render.setShaderAuto() # Zapne generování shaderů, nutné pro normální mapy, stíny atd.

        ambient_light = AmbientLight("ambient_light")
        ambient_light.setColor(VBase4(0.4, 0.4, 0.45, 1)) # Lehce chladnější ambient, ať vynikne nasvícení
        self.render.setLight(self.render.attachNewNode(ambient_light))

        directional_light = DirectionalLight("directional_light")
        directional_light.setColor(VBase4(0.9, 0.9, 0.8, 1))
        # Zapneme vráskání hran pro hezké vržené stíny
        directional_light.setShadowCaster(True, 1024, 1024)
        # Zvětšíme "kameru" vržených stínů, aby stínilo celé hřiště
        dl_lens = directional_light.getLens()
        dl_lens.setFilmSize(100, 100)
        
        directional_light_node = self.render.attachNewNode(directional_light)
        directional_light_node.setHpr(45, -45, 0)
        self.render.setLight(directional_light_node)

        # Generování / Načtení hřiště
        try:
            self.field = self.loader.loadModel("models/plane")
            self.field.setScale(50, 50, 1)
        except Exception:
            from panda3d.core import CardMaker
            cm = CardMaker("plane")
            cm.setFrame(-50, 50, -50, 50)
            self.field = self.render.attachNewNode(cm.generate())
            self.field.setHpr(0, -90, 0)
            
        self.field.reparentTo(self.render)
        self.field.setPos(0, 0, -0.5)
        
        # Fáze 4: Textura a její opakování (tiling)
        try:
            grass_tex = self.loader.loadTexture(GRASS_TEX_PATH)
            self.field.setTexture(grass_tex)
            # Vzorek zopakujeme (vytvoří velkou louku)
            self.field.setTexScale(TextureStage.getDefault(), 8, 8)
            self.field.setColor(1, 1, 1, 1)
        except:
            self.field.setColor(0.3, 0.8, 0.3, 1)

        self.player = Player(self)
        self.coins = []
        self.score = 0
        self.max_coins_to_collect = 15

        self.accept("w", self.set_move_forward, [True])
        self.accept("w-up", self.set_move_forward, [False])
        self.accept("s", self.set_move_backward, [True])
        self.accept("s-up", self.set_move_backward, [False])
        self.accept("a", self.set_move_left, [True])
        self.accept("a-up", self.set_move_left, [False])
        self.accept("d", self.set_move_right, [True])
        self.accept("d-up", self.set_move_right, [False])

        self.cTrav = CollisionTraverser()
        self.cQueue = CollisionHandlerQueue()
        self.cTrav.addCollider(self.player.collision_np, self.cQueue)

        # Cesty k hezčímu Fontu by se zde daly vložit, zatím použijeme default
        self.score_text = OnscreenText(text=f"Skore: {self.score}/{self.max_coins_to_collect}",
                                       pos=(0.95, -0.95), scale=0.08,
                                       fg=(1, 0.8, 0.2, 1), shadow=(0,0,0,0.8), align=TextNode.ARight,
                                       mayChange=True)
                                       
        self.game_message = OnscreenText(text="", pos=(0, 0.8), scale=0.1,
                                         fg=(1, 1, 1, 1), shadow=(0,0,0,0.8), align=TextNode.ACenter,
                                         mayChange=True)

        self.game_state = "playing"
        self.start_game()

    def start_game(self):
        """Inicializuje nebo restartuje herní komponenty."""
        self.score = 0
        self.score_text.setText(f"Skore: {self.score}/{self.max_coins_to_collect}")
        self.game_message.setText("")
        self.player.reset()
        self.clear_coins()
        self.spawn_coins(10)

        self.game_state = "playing"
        
        # Kamera na začátku nebude uskočená, raději ji umístím hned k hráči
        if self.player.model:
            p_pos = self.player.model.getPos()
            self.camera.setPos(p_pos.getX(), p_pos.getY() - 15, p_pos.getZ() + 10)

        self.taskMgr.add(self.player.update_movement, "player_movement_task")
        self.taskMgr.add(self.check_collisions, "check_collisions_task")
        self.taskMgr.add(self.animate_objects, "animate_objects_task") # Pro animování prostředí
        
        self.accept("r", self.reset_game)
        self.ignore("r")

    def reset_game(self):
        """Resetuje hru do počátečního stavu."""
        self.start_game()

    def game_over(self):
        """Nastaví hru do stavu game_over."""
        self.game_state = "game_over"
        self.taskMgr.remove("player_movement_task")
        self.taskMgr.remove("check_collisions_task")
        # Animace běží i po game over
        
        self.game_message.setText(f"Skvele, vyhral jsi!\nSebral jsi {self.score} minci.\nStiskni 'R' pro novou hru.")
        self.accept("r", self.reset_game)

    def animate_objects(self, task):
        """Fáze 4 úkol: Animuje mince atd."""
        dt = globalClock.getDt()
        curr_time = globalClock.getFrameTime()
        for coin in self.coins:
            coin.update_animation(dt, curr_time)
        return task.cont

    def set_move_forward(self, state: bool):
        if self.game_state == "playing":
            self.player.move_forward = state

    def set_move_backward(self, state: bool):
        if self.game_state == "playing":
            self.player.move_backward = state

    def set_move_left(self, state: bool):
        if self.game_state == "playing":
            self.player.move_left = state

    def set_move_right(self, state: bool):
        if self.game_state == "playing":
            self.player.move_right = state

    def update_camera(self, task):
        """
        Fáze 4: Plynulé sledování kamery s tlumicím pohybem (Smooth follow).
        Kamera už nebude rigidly "přilepená" k postavě.
        """
        player_pos = self.player.model.getPos()
        # Vypočítáme cílovou pozici pro kameru
        target_pos = (player_pos.getX(), player_pos.getY() - 15, player_pos.getZ() + 10)
        curr_pos = self.camera.getPos()
        
        # Plynulý (damped) přesun pomocí jednoduché interpolace
        dt = globalClock.getDt()
        lerp_speed = 5.0 * dt
        
        new_x = curr_pos[0] + (target_pos[0] - curr_pos[0]) * lerp_speed
        new_y = curr_pos[1] + (target_pos[1] - curr_pos[1]) * lerp_speed
        new_z = curr_pos[2] + (target_pos[2] - curr_pos[2]) * lerp_speed
        
        self.camera.setPos(new_x, new_y, new_z)
        self.camera.lookAt(player_pos)
        
        return task.cont

    def clear_coins(self):
        """Odstraní existující mince ze scény."""
        for coin in list(self.coins):
            coin.remove()
        self.coins.clear()

    def spawn_coins(self, count: int):
        """Vygeneruje mince."""
        for _ in range(count):
            x = random.uniform(-40, 40)
            y = random.uniform(-40, 40)
            coin = Coin(self, (x, y, 0))
            self.coins.append(coin)

    def check_collisions(self, task):
        """Kontroluje kolize."""
        if self.game_state != "playing":
            return task.cont

        self.cTrav.traverse(self.render)

        for entry in self.cQueue.getEntries():
            from_node = entry.getFromNodePath().node()
            into_node = entry.getIntoNodePath().node()

            if from_node.getName() == "player_collision" and into_node.getName() == "coin_collision":
                for coin in self.coins:
                    if coin.collision_np and coin.collision_np.node() == into_node:
                        coin.remove()
                        self.coins.remove(coin)
                        self.score += 1
                        self.score_text.setText(f"Skore: {self.score}/{self.max_coins_to_collect}")
                        
                        if self.score >= self.max_coins_to_collect:
                            self.game_over()
                        break

        if not self.coins and self.score < self.max_coins_to_collect:
            self.spawn_coins(random.randint(5, 10))

        return task.cont

if __name__ == "__main__":
    game = CoinCollectorGame()
    game.run()
