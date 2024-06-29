from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.iztest.plant_modifier import set_puff_x_offset
from random import randint
from rpze.rp_extend import Controller

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-1
        .....
        .....
        pblh2
        .....
        .....
        gl 
        0  
        3-6''')
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        plist = iz_test.ground
        xp = plist["3-1"]
        set_puff_x_offset(xp,range(-5,-2))
        #xp.x = randint(35,37)   #这是1列左偏的小喷，40是不偏移的坐标。37一定打不到橄榄，38-39概率打到橄榄。

    iz_test.start_test(jump_frame=0, speed_rate=2)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
    