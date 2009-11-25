import time
import math
from operator import itemgetter
import random

def dist(unit1, unit2):
    dx = float(unit1.x)-float(unit2.x)
    dy = float(unit1.y)-float(unit2.y)
    return math.sqrt(dx*dx + dy*dy)

def loop(game, command):
    while game.active:
        idle_probes = [unit for unit in game.my_units if unit.type == 'protoss_probe' and unit.order == "player_guard"]
        minerals = [unit for unit in game.units if unit.type == 'resource_mineral_field']
        if not minerals:
            continue
        for probe in idle_probes:
            #Shitty algo but one line!
            best_mineral, distance = sorted([(mineral, dist(mineral, probe)) for mineral in minerals],key=itemgetter(1))[0]
            command.right_click_unit(probe, best_mineral)
        if game.me['minerals'] >= 50:
            try:
                nexus = (unit for unit in game.my_units if unit.type == 'protoss_nexus' and unit.train_timer == "0").next()
                command.train(nexus, 'protoss_probe')
            except StopIteration:
                pass
        if game.me['minerals'] > 100 and game.me['supply']-game.me['supply_used'] <= 2:
            try:
                probe = (unit for unit in game.my_units if unit.type == 'protoss_probe').next()
                command.build(probe, 
                              int(probe.x) + random.uniform(-10,10),
                              int(probe.y) + random.uniform(-10,10),
                              "protoss_pylon")
            except StopIteration:
                pass
                
        time.sleep(.5)
    print "Agent ending"

print __file__,"loaded"

