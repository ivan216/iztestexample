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
    kg = yy = None
    hp_r = [0] * 4

    @iz_test.flow_factory.add_flow()
    async def _(_):
        nonlocal kg, yy
        kg = iz_test.game_board.iz_place_zombie(2,5,ZombieType.digger)
        yy = randomize_generate_cd(iz_test.game_board.new_plant(2,0,PlantType.gloomshroom))
        randomize_generate_cd(iz_test.game_board.new_plant(2,1,PlantType.gloomshroom))
        randomize_generate_cd(iz_test.game_board.new_plant(3,0,PlantType.gloomshroom))
        randomize_generate_cd(iz_test.game_board.new_plant(3,1,PlantType.gloomshroom))

        await delay(randint(1,4))
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

    @iz_test.check_tests_end()
    def _(n,_):
        if n % 1e4 == 0:
            rate = hurt_count/n
            print(f"当前受伤次数: {hurt_count} ,受伤率{rate:.3%}")
        if n < 2e4:
            return None
        return hurt_count/n
    
    iz_test.start_test(jump_frame=1, speed_rate=2, print_interval=1e3)
    print("受伤情况(从0开始, 间隔4): ",hp_r)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
