# coin_collector_faze4.py
from direct.showbase.ShowBase import ShowBase
from panda3d.core import AmbientLight, DirectionalLight, VBase4, WindowProperties
from panda3d.core import NodePath, PandaNode
from direct.actor.Actor import Actor
from panda3d.core import CollisionSphere, CollisionNode, CollisionHandlerQueue, CollisionTraverser, BitMask32
from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode # Potřebné pro OnscreenText
import random

# Definice bitových masek pro kolize
PLAYER_MASK = BitMask32(0x1)
COIN_MASK = BitMask32(0x2)

class Player:
    """
    Třída reprezentující hráče ve hře.
    """
    def __init__(self, parent_node: ShowBase):
        self.parent_node = parent_node
        try:
            self.model = parent_node.loader.loadModel("smiley") # Zabudovaná žlutá kulička v Panda3D
        except Exception as e:
            print(f"Chyba při načítání modelu hráče: {e}. Používám zástupný objekt.")
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
        self.initial_pos = (0, 0, 0.5) # Počáteční pozice hráče
        self.model.setPos(self.initial_pos)
        self.model.setColor(0.8, 0.2, 0.2, 1)

        collision_sphere = CollisionSphere(0, 0, 0, 1.2)
        collision_node = CollisionNode("player_collision")
        collision_node.addSolid(collision_sphere)
        collision_node.setFromCollideMask(PLAYER_MASK)
        collision_node.setIntoCollideMask(BitMask32.allOff())
        self.collision_np = self.model.attachNewNode(collision_node)

        self.move_forward = False
        self.move_backward = False
        self.move_left = False
        self.move_right = False
        self.speed = 10.0

    def update_movement(self, task):
        """
        Aktualizuje pozici hráče na základě stisknutých kláves.
        """
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

        self.model.setX(self.model, x_move)
        self.model.setY(self.model, y_move)

        return task.cont

    def reset(self):
        """
        Resetuje pozici hráče na počáteční.
        """
        self.model.setPos(self.initial_pos)
        self.move_forward = False
        self.move_backward = False
        self.move_left = False
        self.move_right = False


class Coin:
    """
    Třída reprezentující minci ve hře.
    """
    def __init__(self, parent_node: ShowBase, position: tuple):
        self.parent_node = parent_node
        try:
            self.model = parent_node.loader.loadModel("box") # Zabudovaná kostka v Panda3D
        except Exception as e:
            self.model = parent_node.render.attachNewNode("coin_placeholder")

        self.model.reparentTo(parent_node.render)
        self.model.setScale(0.2)
        self.model.setPos(position[0], position[1], position[2] + 0.1)
        self.model.setColor(0.9, 0.8, 0.1, 1)

        collision_sphere = CollisionSphere(0, 0, 0, 1.5)
        collision_node = CollisionNode("coin_collision")
        collision_node.addSolid(collision_sphere)
        collision_node.setFromCollideMask(COIN_MASK)
        collision_node.setIntoCollideMask(PLAYER_MASK)
        self.collision_np = self.model.attachNewNode(collision_node)

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


class CoinCollectorGame(ShowBase):
    """
    Hlavní třída hry Coin Collector.
    Ve Fázi 4 obsahuje systém měření času a závěrečné hodnocení.
    """
    def __init__(self):
        ShowBase.__init__(self)

        self.win.setClearColor(VBase4(0.5, 0.7, 1.0, 1))
        props = WindowProperties()
        props.setTitle("Coin Collector - Fáze 4")
        self.win.requestProperties(props)

        self.disableMouse()
        self.camera.setPos(0, -20, 15)
        self.camera.lookAt(0, 0, 0)
        self.taskMgr.add(self.update_camera, "update_camera_task")

        ambient_light = AmbientLight("ambient_light")
        ambient_light.setColor(VBase4(0.6, 0.6, 0.6, 1))
        self.render.setLight(self.render.attachNewNode(ambient_light))

        directional_light = DirectionalLight("directional_light")
        directional_light.setColor(VBase4(0.8, 0.8, 0.7, 1))
        directional_light_node = self.render.attachNewNode(directional_light)
        directional_light_node.setHpr(45, -45, 0)
        self.render.setLight(directional_light_node)

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

        # UI prvky
        self.score_text = OnscreenText(text=f"Skóre: {self.score}/{self.max_coins_to_collect}",
                                       pos=(0.95, -0.95), scale=0.07,
                                       fg=(1, 1, 1, 1), align=TextNode.ARight,
                                       mayChange=True)
                                       
        self.time_text = OnscreenText(text="Čas: 0.0s",
                                       pos=(-0.95, -0.95), scale=0.07,
                                       fg=(1, 1, 1, 1), align=TextNode.ALeft,
                                       mayChange=True)
                                       
        self.game_message = OnscreenText(text="", pos=(0, 0.8), scale=0.1,
                                         fg=(1, 1, 1, 1), align=TextNode.ACenter,
                                         mayChange=True)

        self.game_state = "playing" 
        self.start_time = 0.0

        self.start_game()

    def start_game(self):
        """
        Inicializuje nebo restartuje herní komponenty.
        """
        self.score = 0
        self.score_text.setText(f"Skóre: {self.score}/{self.max_coins_to_collect}")
        self.game_message.setText("")
        self.time_text.setText("Čas: 0.0s")
        self.player.reset()
        self.clear_coins()
        self.spawn_coins(10)

        self.game_state = "playing"
        self.start_time = globalClock.getFrameTime()
        
        self.taskMgr.add(self.player.update_movement, "player_movement_task")
        self.taskMgr.add(self.check_collisions, "check_collisions_task")
        self.taskMgr.add(self.update_timer, "update_timer_task")
        
        self.accept("r", self.reset_game) 
        self.ignore("r") 

    def reset_game(self):
        self.start_game()

    def evaluate_performance(self, elapsed_time):
        """
        Ohodnotí výkon hráče na základě času.
        """
        if elapsed_time <= 15.0:
            return "A (Excelentní rychlost!)"
        elif elapsed_time <= 25.0:
            return "B (Dobrá práce!)"
        elif elapsed_time <= 40.0:
            return "C (Průměrný výkon)"
        else:
            return "D (Na tom se dá zapracovat)"

    def game_over(self):
        """
        Nastaví hru do stavu "game_over" a vypíše hodnocení.
        """
        self.game_state = "game_over"
        self.taskMgr.remove("player_movement_task")
        self.taskMgr.remove("check_collisions_task")
        self.taskMgr.remove("update_timer_task")
        
        elapsed_time = globalClock.getFrameTime() - self.start_time
        rating = self.evaluate_performance(elapsed_time)
        
        self.game_message.setText(
            f"Konec hry!\\n"
            f"Sebral jsi {self.score} mincí v čase {elapsed_time:.1f} s.\\n"
            f"Hodnocení: {rating}\\n"
            f"Stiskni 'R' pro restart."
        )
        self.accept("r", self.reset_game)

    def update_timer(self, task):
        """
        Aktualizuje časomíru na obrazovce.
        """
        if self.game_state == "playing":
            elapsed = globalClock.getFrameTime() - self.start_time
            self.time_text.setText(f"Čas: {elapsed:.1f}s")
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
        player_pos = self.player.model.getPos()
        self.camera.setPos(player_pos.getX(), player_pos.getY() - 15, player_pos.getZ() + 10)
        self.camera.lookAt(player_pos)
        return task.cont

    def clear_coins(self):
        for coin in list(self.coins):
            coin.remove()
        self.coins.clear()

    def spawn_coins(self, count: int):
        for _ in range(count):
            x = random.uniform(-45, 45)
            y = random.uniform(-45, 45)
            coin = Coin(self, (x, y, 0))
            self.coins.append(coin)

    def check_collisions(self, task):
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
                        self.score_text.setText(f"Skóre: {self.score}/{self.max_coins_to_collect}")
                        
                        if self.score >= self.max_coins_to_collect:
                            self.game_over()
                        break

        if not self.coins and self.score < self.max_coins_to_collect:
            self.spawn_coins(random.randint(5, 10))

        return task.cont

if __name__ == "__main__":
    game = CoinCollectorGame()
    game.run()
