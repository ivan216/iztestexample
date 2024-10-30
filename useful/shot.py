from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.flow import FlowManager
from rpze.structs.plant import PlantType
from rpze.iztest.operations import place ,repeat
from rpze.flow.utils import until, delay
from rpze.iztest.plant_modifier import randomize_generate_cd,set_puff_x_offset

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        
        .....
        .....
        .....
        .....
        .....
        xg
        0
        3-6
        ''')
    
    pl = zb = None
    print("\n\n")

    @iz_test.flow_factory.add_flow()
    async def place_zombie(fm:FlowManager):
        nonlocal pl,zb
        pl = iz_test.game_board.new_plant(2,4,PlantType.puffshroom)
        set_puff_x_offset(pl,3)
        zb = iz_test.game_board.zombie_list[0]
        zb.hp = 300

    @iz_test.flow_factory.add_tick_runner()
    def output(fm:FlowManager):
        if fm.time > 410:
            return iz_test.end(True)

    @iz_test.flow_factory.add_tick_runner()
    def output(fm:FlowManager):
        if fm.time > 0:
            print("\033[4A\r\033[K"+"time: ",fm.time)
            print("\033[K"+"gcd: ",pl.generate_cd)
            print("\033[K"+"lcd: ",pl.launch_cd)
            print("\033[K"+"pl_hp: ",pl.hp)
            if zb is not None:
                print("\033[K"+"zb_hp: ",zb.hp)
                print("\033[2A")

    iz_test.start_test(jump_frame=0, speed_rate=0.1)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
    