from rpze.basic.inject import InjectedGame
from rpze.rp_extend import Controller
from rpze.iztest.iztest import IzTest
from rpze.flow.flow import FlowManager
from rpze.structs.plant import PlantType
from rpze.structs.zombie import ZombieType
from rpze.iztest.plant_modifier import randomize_generate_cd
from rpze.flow.utils import delay
from random import randint

def fun(ctler:Controller):
    test_count = int(1e4)
    inter = int(1e3)

    iz_test = IzTest(ctler).init_by_str(f'''
        {test_count} -1
        
        .o...
        .....
        .....
        .....
        .....
        tt
        0
        1-2''')
    
    hurt_count = 0
    kg = yy = None
    hp_r = [0] * 8

    @iz_test.flow_factory.add_flow()
    async def _(_):
        nonlocal kg, yy

        kg = iz_test.game_board.iz_place_zombie(2,5,ZombieType.digger)

        yy = iz_test.game_board.new_plant(2,0,PlantType.gloomshroom)
        randomize_generate_cd(yy)
        yy2 = iz_test.game_board.new_plant(1,0,PlantType.gloomshroom)
        randomize_generate_cd(yy2)
        yy3 = iz_test.game_board.new_plant(3,0,PlantType.gloomshroom)
        randomize_generate_cd(yy3)

        await delay(randint(201,204))
        kg.x = 9.9

    @iz_test.flow_factory.add_tick_runner()
    def _(fm:FlowManager):
        if fm.time > 0:
            if kg.hp < 90:
                return iz_test.end(False)
    
    @iz_test.on_game_end()
    def _(_):
        nonlocal hurt_count
        if yy.hp < 300:
            hurt_count += 1
            i = (300 - yy.hp) // 4
            hp_r[i] += 1
        if iz_test._test_time % inter == inter - 1 :
            n = iz_test._test_time + 1
            print(f"当前次数：{n}, 受伤次数: {hurt_count}, 受伤率: {hurt_count/n:.3%}")
    
    iz_test.start_test(jump_frame=1, speed_rate=2, print_interval=0)
    print("受伤情况(从0开始, 间隔4): ",hp_r)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
