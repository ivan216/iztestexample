from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.structs.plant import PlantType
from rpze.flow.flow import FlowManager
from rpze.structs.zombie import ZombieType
from rpze.iztest.plant_modifier import randomize_generate_cd
from rpze.flow.utils import delay
from random import randint

## 4曾，50万次测试，受伤57次

def fun(ctler:Controller):
    iz_test = IzTest(ctler).init_by_str('''
        -1 -1
        
        .....
        .....
        .....
        .....
        .....''')
    
    hurt_count = 0
    kg = yy = None

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal kg, yy
        kg = iz_test.game_board.iz_place_zombie(2,5,ZombieType.digger)

        yy = iz_test.game_board.new_plant(2,0,PlantType.gloomshroom)
        randomize_generate_cd(yy)
        yy2 = iz_test.game_board.new_plant(2,1,PlantType.gloomshroom)
        randomize_generate_cd(yy2)
        yy3 = iz_test.game_board.new_plant(3,0,PlantType.gloomshroom)
        randomize_generate_cd(yy3)
        yy4 = iz_test.game_board.new_plant(3,1,PlantType.gloomshroom)
        randomize_generate_cd(yy4)

        await delay(randint(1,4))
        kg.x = 9.9

    @iz_test.flow_factory.add_tick_runner()
    def check_end(fm:FlowManager):
        if fm.time > 4:
            if kg.hp < 90:
                return iz_test.end(False)

    @iz_test.on_game_end()
    def count(_):
        nonlocal hurt_count
        if yy.hp < 300:
            hurt_count += 1

    @iz_test.check_tests_end()
    def show(n,_):
        if n%1000 ==0:
            print("当前有伤次数: ",hurt_count," 有伤率: %.4f"%(hurt_count/n))
        if n < 500000:
            return None
        return True
    
    iz_test.start_test(jump_frame=1, speed_rate=2, print_interval=100)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
