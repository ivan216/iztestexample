from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.iztest.operations import place, repeat
from rpze.flow.utils import until, delay
from rpze.flow.utils import AwaitableCondFunc, VariablePool
from rpze.flow.flow import FlowManager
from rpze.structs.plant import Plant, PlantType

def until_spike_n_attack(spike: Plant, n: int = 1) -> AwaitableCondFunc[None]:

    def _await_func(_,v=VariablePool(i=0)):
        if spike.status_cd == 100:
            v.i += 1
        if v.i == n:
            return True
        return False
    
    return AwaitableCondFunc(_await_func)

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        
        .....
        .....
        ..s..
        .....
        .....
        ''')
    
    pl = zb = None
    print("\n")

    @iz_test.flow_factory.add_flow()
    async def place_zombie(fm:FlowManager):
        nonlocal pl,zb
        pl = iz_test.game_board.new_plant(2,4,PlantType.spikerock)
        zb = place("lz 3-6")
        await until_spike_n_attack(pl,2).after(93)  #刺50-96  #钢93-101
        place("xg 3-6")

        # await until(lambda _:pl.status_cd == 99)
        # zb.die_no_loot()

    @iz_test.flow_factory.add_tick_runner()
    def output(fm:FlowManager):
        if pl is not None:
            print("\033[2A\033[K",pl.status_cd)
            print("\033[K",zb.accessories_hp_1)

        if iz_test.ground["3-3"] is None:
            return iz_test.end(False)

    iz_test.start_test(jump_frame=0, speed_rate=2)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)