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
    iz_test = IzTest(ctler)
    iz_test.controller.write_bool(False, 0x6a66f4)

    hurt_count = 0
    kg1 = kg2 =  None
    pl1 = pl2 =  None
    hp_r = [0] * 4
    test_count = int(4e5)

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal kg1,kg2, pl1,pl2
        kg1 = iz_test.game_board.iz_place_zombie(0,5,ZombieType.digger)
        kg2 = iz_test.game_board.iz_place_zombie(3,5,ZombieType.digger)
        pl1 = randomize_generate_cd(iz_test.game_board.new_plant(0,0,PlantType.gloomshroom))
        pl2 = randomize_generate_cd(iz_test.game_board.new_plant(3,0,PlantType.gloomshroom))
        randomize_generate_cd(iz_test.game_board.new_plant(0,1,PlantType.gloomshroom))
        randomize_generate_cd(iz_test.game_board.new_plant(1,0,PlantType.gloomshroom))
        randomize_generate_cd(iz_test.game_board.new_plant(1,1,PlantType.gloomshroom))
        randomize_generate_cd(iz_test.game_board.new_plant(3,1,PlantType.gloomshroom))
        randomize_generate_cd(iz_test.game_board.new_plant(4,0,PlantType.gloomshroom))
        randomize_generate_cd(iz_test.game_board.new_plant(4,1,PlantType.gloomshroom))

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal kg1
        await delay(randint(1,4))
        kg1.x = 9.9
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        nonlocal kg2
        await delay(randint(1,4))
        kg2.x = 9.9
    
    @iz_test.flow_factory.add_tick_runner()
    def check_end(fm:FlowManager):
        if fm.time > 0:
            if kg1.hp < 90 and kg2.hp < 90 :
                return iz_test.end(False)
    
    @iz_test.on_game_end()
    def count(_):
        nonlocal hurt_count
        if pl1.hp < 300:
            hurt_count += 1
            i = (300 - pl1.hp) // 4
            hp_r[i] += 1
        if pl2.hp < 300:
            hurt_count += 1
            i = (300 - pl2.hp) // 4
            hp_r[i] += 1
    
    @iz_test.check_tests_end()
    def show(n,_):
        if n % 1e4 == 0:
            rate = hurt_count/n/2
            print(f"测试次数: {2*n}, 受伤次数: {hurt_count}, 受伤率: {rate}")
        if n < test_count:
            return None
        return hurt_count/n/2
    
    iz_test.start_test(jump_frame=0, speed_rate=2, print_interval=1e3)
    print("总测试次数: ", 2*test_count)
    print("受伤情况(从0开始, 间隔4): ",hp_r)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)