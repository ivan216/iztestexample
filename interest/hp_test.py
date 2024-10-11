from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.iztest.operations import place

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        2-0
        .....
        .....
        .....
        .....
        .....
        lz 
        0  
        3-6''')
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        lz = iz_test.game_board.zombie_list[0]
        print("lz")
        print(lz.hp)
        print(lz.accessories_hp_1)
        print(lz.accessories_hp_2)
        print("tt")
        tt = place("tt 3-6")
        print(tt.hp)
        print(tt.accessories_hp_1)
        print(tt.accessories_hp_2)
        print("tz")
        tz = place("tz 3-6")
        print(tz.hp)
        print(tz.accessories_hp_1)
        print(tz.accessories_hp_2)
        print("kg")
        kg = place("kg 3-6")
        print(kg.hp)
        print(kg.accessories_hp_1)
        print(kg.accessories_hp_2)
        print("gl")
        gl = place("gl 3-6")
        print(gl.hp)
        print(gl.accessories_hp_1)
        print(gl.accessories_hp_2)

    iz_test.start_test(jump_frame=0, speed_rate=2)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)