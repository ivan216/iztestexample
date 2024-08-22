from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.rp_extend import Controller
from rpze.structs.griditem import GriditemType
from rpze.iztest.cond_funcs import until_plant_last_shoot
from rpze.iztest.operations import delay,place
from rpze.flow.flow import FlowManager

def fun(ctler: Controller):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        
        .....
        .....
        dyloz
        .....
        .....
        xg
        0  
        3-7 ''')
    
    def has_ladder(row : int,col : int):
        for item in ~iz_test.game_board.griditem_list :
            if (item.type_ == GriditemType.ladder) \
            and (item.row == row) and (item.col == col):
                return True
        return False
    
    @iz_test.flow_factory.add_flow()
    async def place_zombie(_):
        y = iz_test.ground["3-2"]
        await (until_plant_last_shoot(y) | delay(600))
        place("tz 3-6")

    @iz_test.flow_factory.add_tick_runner()
    def check_end(fm : FlowManager):
        if fm.time > 1000:
            if iz_test.game_board.zombie_list.obj_num == 0:
                if has_ladder(2,3):
                    return iz_test.end(True)
                else:
                    return iz_test.end(False)

    iz_test.start_test(jump_frame=1, speed_rate=1)

with InjectedGame(r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe") as game:
    fun(game.controller)
    