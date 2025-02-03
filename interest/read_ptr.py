from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.iztest.operations import place, repeat
from rpze.flow.flow import FlowManager
from rpze.structs.plant import Plant, PlantType
from rpze.iztest.plant_modifier import randomize_generate_cd
from rpze.iztest.cond_funcs import until_plant_last_shoot

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        
        .....
        .....
        ...o.
        .....
        .....
        xt 
        0  
        3-4''')
    
    i = 0   # 没有  <0x14c=332

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal i
        plant = randomize_generate_cd(iz_test.game_board.new_plant(2,2,PlantType.pea_shooter))

        if iz_test.controller.read_i32(plant.base_ptr + 4*i) == 35:
            print("i= ",i)
            print(iz_test.controller.read_i32(plant.base_ptr + 4*i))
        
        await until_plant_last_shoot(plant)
        place("xg 3-4")

        i += 1

    @iz_test.flow_factory.add_tick_runner()
    def check(fm:FlowManager):
        if fm.time > 1100:
            if iz_test.ground["3-0"] is None:
                return iz_test.end(True)
            if iz_test.game_board.zombie_list.obj_num == 0:
                return iz_test.end(False)

    iz_test.start_test(jump_frame=0, speed_rate=2,print_interval=1e2)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
