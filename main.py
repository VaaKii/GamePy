from ursina.prefabs.platformer_controller_2d import PlatformerController2d
from ursina.prefabs.grid_editor import GridEditor
from ursina import *

app = Ursina()

WORLD_SIZE = (100,30)
WORLD_START = -150
INVENTORY_ACTIVE = False


class Item(Entity):
    def __init__(self,pos,scale):
        super().__init__(
            model="quad",
            collider="box",
            position=pos,
            scale=scale,
        )
        self.grounded = False
        self.air_time = 0
        self.gravite = 1

    def update(self):
        ray = boxcast(
            self.world_position+Vec3(0,.1,0),
            self.down,
            distance=max(.1, self.air_time * self.gravity),
            ignore=(self, ),
            traverse_target=scene,
            thickness=self.scale_x*.9
            )

        if ray.hit:
            if not self.grounded:
                self.land()
            self.grounded = True
            self.y = ray.world_point[1]
            return
        else:
            self.grounded = False


class Invertory(Entity):
    def __init__(self):
        super().__init__(
            parent = camera.ui,
            model = "quad",
            scale = (.5, .8),                                           
            origin = (-.5, .5),                                         
            position = (.3,.4),                                        
            texture = 'white_cube',                                     
            texture_scale = (9,15),                                      
            color = color.dark_gray,
        )
        self.item = Entity(parent=self,scale=(1/9,1/15))

class UDBlock(Entity):
    def __init__(self, x, y, tex):
        super().__init__(
            parent=scene,
            world_x=x,
            model='quad',
            y=1,
            collider="box",
            scale=(3,3),
            texture=tex,
            world_y=y,
            color=color.white
            )

class Block(Button):
    def __init__(self, x, y, tex):
        super().__init__(
            parent=scene,
            world_x=x,
            model='quad',
            y=1,
            collider="box",
            scale=(3,3),
            texture=tex,
            world_y=y,
            color=color.white
            )


            

    def on_click(self):
        destroy(self)
        world.pop(world.index(self))
        
    
class Player(PlatformerController2d):
    def __init__(self):
        super().__init__(y=3,
                    z=.01,
                    scale_y=3,
                    max_jumps=1,
                    scale_x=3)

def create_world(start, size:tuple):
    world = []
    for i in range(size[1]):
        for g in range(size[0]):
            if i == 0:
                b1 = Block(start+(g*3),-(i*3),"assets/grass.png")
                world.append(b1)
            else:
                b1 = Block(start+(g*3),-(i*3),"assets/dirt.png") 
                world.append(b1)

    for i in range((size[1]//3)+15):
        world.append(UDBlock(-153,(i*3),"assets/stone.png"))
        world.append(UDBlock(153,(i*3)-size[1],"assets/stone.png"))
    for i in range(size[0]+1):
        world.append(UDBlock(-3+(start+(i*3)),(-(size[1]*3)),"assets/bedrock.png"))

    return world

player = Player()
world = create_world(-150,(101,30))

plane = Entity(model='quad', color=color.azure, z=10,collider="box", scale=5000)

def input(key):
    global INVENTORY_ACTIVE
    if key == "right mouse up":
        if mouse.hovered_entity is plane:
            world.append(Block((3*(((mouse.world_point.x-1.5)//3)+1)),(3*((((mouse.world_point.y-1.5)//3)+1))),"assets/dirt.png"))
    if key == "e":
        if not INVENTORY_ACTIVE:
            inv.enable()
            INVENTORY_ACTIVE = True
        else:
            inv.disable()
            INVENTORY_ACTIVE = False
    if key == "middle mouse up":
        print("Player:",player.position)
        print("Real:",mouse.world_point)
        print("Math:",lerp(0,window.right.x,35+((3*(player.position.x/3))+1.5)))
    

def update():
    if player.x > abs(WORLD_START) - 30 and len(camera.scripts) > 0:
        del camera.scripts[0]
    elif player.x < WORLD_START + 30 and len(camera.scripts) > 0:
        del camera.scripts[0]
    elif len(camera.scripts) < 1 and -120 < player.x < 120 :
        camera.add_script(SmoothFollow(player,offset=(0,0,-9),speed=5))




inv = Invertory()
inv.disable()

item1 = Button(parent=inv.item,origin=(-.5,.5), color=color.red, position=(0,0))
test = Entity(model="quad",collider="box",position=(0,0))
window.title = "MyGame"
window.vsync = False 
camera.add_script(SmoothFollow(player,offset=(0,0,-9),speed=5))
window.borderless = False
camera.orthographic = True
camera.fov = 35
window.borderless = False 
window.exit_button.disable()
app.run()