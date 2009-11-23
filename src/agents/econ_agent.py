import time
import math
from operator import itemgetter

def dist(unit1, unit2):
    dx = float(unit1.x)-float(unit2.x)
    dy = float(unit1.y)-float(unit2.y)
    return math.sqrt(dx*dx + dy*dy)

def loop(game, command):
    while True:
        idle_probes = [unit for unit in game.my_units if unit.type == 'protoss_probe' and unit.order == "3"]
        minerals = [unit for unit in game.units if unit.type == 'resource_mineral_field']
        if not minerals:
            continue
        for probe in idle_probes:
            #Shitty algo but one line!
            best_mineral, distance = sorted([(mineral, dist(mineral, probe)) for mineral in minerals],key=itemgetter(1))[0]
            command.right_click_unit(probe, best_mineral)
        time.sleep(1)
