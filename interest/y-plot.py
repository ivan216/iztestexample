from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
import matplotlib.pyplot as plt

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-0
        .....
        .....
        yssss
        .....
        .....
        tt
        0  
        3-6 ''')
    
    hp_count = [0 for x in range(0,70)]
    hp_count2 = [0 for x in range(0,70)]
    x = [x for x in range(0,70)]
    zb = None
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal zb
        zlist = iz_test.game_board.zombie_list
        zb = zlist[0]
        zb.accessories_hp_1 = 2000
    
    @iz_test.on_game_end()
    def end_callback(result: bool):
        nonlocal hp_count,hp_count2
        plist = iz_test.ground
        if plist["3-1"] is None:
            i = (2000 - zb.accessories_hp_1) // 20
            if i%2 == 0:
                hp_count[i] += 1
            else:
                hp_count2[i] += 1
            

    iz_test.start_test(jump_frame=1, speed_rate=5)

    plt.figure(1)
    plt.bar(x,hp_count,color='blue')
    plt.bar(x,hp_count2,color= 'red')

    plt.show()

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
