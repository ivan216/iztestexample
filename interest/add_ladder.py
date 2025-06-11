from rpze.basic.inject import InjectedGame
from rpze.iztest.iztest import IzTest
from rpze.structs.plant import PlantType
game_path = r"D:\pvz\Plants vs. Zombies 1.0.0.1051 EN\PlantsVsZombies.exe"

def fun(ctler):
    iz_test = IzTest(ctler).init_by_str('''
        1000 -1
        3-0
        .....
        .....
        .....
        .t.s.
        .....
        tt
        0  
        1-9 ''')
    
    @iz_test.flow_factory.add_flow()
    async def _(_):
        plist = []
        plist.append(iz_test.game_board.new_plant(2,2,PlantType.pumpkin))
        plist.append(iz_test.game_board.new_plant(2,2,PlantType.gloomshroom))
        plist.append(iz_test.game_board.new_plant(2,6,PlantType.spikerock))
        plist.append(iz_test.game_board.new_plant(3,6,PlantType.cob_cannon))

        for pl in plist:
            iz_test.game_board.iz_setup_plant(pl)
        
        coord = [[2,2,3,3,3,3],[2,6,1,2,3,6]] # 代表梯子坐标
        for row,col in zip(*coord):
            iz_test.game_board.add_ladder(row,col)
    
    iz_test.start_test(jump_frame=0, speed_rate=1)

with InjectedGame(game_path) as game:
    fun(game.controller)