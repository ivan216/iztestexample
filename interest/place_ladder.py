from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.iztest.operations import place,delay
from rpze.structs.griditem import GriditemType

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-0
        ooooo
        ooooo
        ooooo
        ooooo
        ooooo
        tt
        0  
        3-9 ''')
    
    def place_ladder( row:int , col:int ):
        ret = iz_test.game_board.griditem_list.alloc_item()
        ret.type_ = GriditemType.ladder
        ret.col = col
        ret.row = row
        ret.layer = 303000 + 10000 * row
        return ret
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        place_ladder(4,0)
        place_ladder(4,1)
        place_ladder(4,2)
        place_ladder(4,3)
        place_ladder(4,4)
        place("xg 5-6")
    
    iz_test.start_test(jump_frame=0, speed_rate=1)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)