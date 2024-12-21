from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.flow.utils import until
from random import randint

def fun(ctler: Controller):
    n = 1000
    iz_test = IzTest(ctler).init_by_str(f'''
        {n} -1
        1-0 2-0 3-0 4-0 5-0
        y....
        y....
        y....
        y....
        y....
        tt tt tt tt tt
        0 0 0 0 0
        1-6 2-6 3-6 4-6 5-6''')
    iz_test.controller.write_bool(False, 0x6a66f4)
    
    fail_count = 0
    y_fail_count = 0

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        i = 1
        nonlocal fail_count, y_fail_count
        zb = iz_test.ground.zombie(i-1)
        zb.x = 780.0 + randint(0,40)
        await until(lambda _: zb.x < 10 or zb.hp < 90)
        if zb.hp < 90:
            fail_count += 1
            if iz_test.ground[f"{i}-1"] is not None:
                y_fail_count += 1
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        i = 2
        nonlocal fail_count, y_fail_count
        zb = iz_test.ground.zombie(i-1)
        zb.x = 780.0 + randint(0,40)
        await until(lambda _: zb.x < 10 or zb.hp < 90)
        if zb.hp < 90:
            fail_count += 1
            if iz_test.ground[f"{i}-1"] is not None:
                y_fail_count += 1

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        i = 3
        nonlocal fail_count, y_fail_count
        zb = iz_test.ground.zombie(i-1)
        zb.x = 780.0 + randint(0,40)
        await until(lambda _: zb.x < 10 or zb.hp < 90)
        if zb.hp < 90:
            fail_count += 1
            if iz_test.ground[f"{i}-1"] is not None:
                y_fail_count += 1

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        i = 4
        nonlocal fail_count, y_fail_count
        zb = iz_test.ground.zombie(i-1)
        zb.x = 780.0 + randint(0,40)
        await until(lambda _: zb.x < 10 or zb.hp < 90)
        if zb.hp < 90:
            fail_count += 1
            if iz_test.ground[f"{i}-1"] is not None:
                y_fail_count += 1

    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        i = 5
        nonlocal fail_count, y_fail_count
        zb = iz_test.ground.zombie(i-1)
        zb.x = 780.0 + randint(0,40)
        await until(lambda _: zb.x < 10 or zb.hp < 90)
        if zb.hp < 90:
            fail_count += 1
            if iz_test.ground[f"{i}-1"] is not None:
                y_fail_count += 1

    iz_test.start_test(jump_frame=1, speed_rate=10)
    print("总次数: ", n*5)
    print("僵尸死亡次数: ", fail_count)
    print("玉米存活次数: ", y_fail_count)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
