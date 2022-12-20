import sys
import pathlib
import numpy as np

run_mode = sys.argv[1:2][0]

if run_mode not in ['--lightshows', '--brightness']:
    print('In order to run, please add --lightshows or --brightness argument.')
    exit()

ROOT_PATH = pathlib.Path().resolve()
INPUT_FILE = ROOT_PATH.joinpath('input_verif_test.txt')

if not INPUT_FILE.is_file():
    print('We could not find any input.txt file. Please create one then run again.')
    exit()

events = ['turn on', 'toggle', 'turn off'] #turn on, toggle, turn off - Keep the order if you want to change the words key.
coords_separation = 'through'
coords_axis_separation = ','

actions = []
input_error = False

input_file = open(INPUT_FILE , "r")
lines = input_file.readlines()
for line in lines:

    mission = {}
    for event in events:
        if line.startswith(event):
            mission = {'event': event}
            line = line.replace(event, '').strip()
            break

    if "event" not in mission:
        print('Lines must start with events like: turn off, turn on, toggle.')
        input_error = True
        break

    if coords_separation not in line:
        print('Lines must have coordonates like X,Y separed by word "' + coords_separation + '".')
        input_error = True
        break

    line = line.split(coords_separation)

    if coords_axis_separation not in line[0] or coords_axis_separation not in line[1]:
        print('Coordonates X and Y must be separated by "' + coords_axis_separation + '".')
        input_error = True
        break
    
    get_from = line[0].strip().split(',')
    mission['from'] = {
        'X': int(get_from[0]),
        'Y': int(get_from[1])
    }

    get_to = line[1].strip().split(',')
    mission['to'] = {
        'X': int(get_to[0]),
        'Y': int(get_to[1])
    }

    actions.append(mission)
input_file.close()

if input_error:
    print('Sorry, the process stopped because your input file don\'t meet the required standardization.')
else:
    bulbs = np.zeros((1000, 1000), dtype=int)

    for mission in actions:
        for ix in range(mission['from']['X'], mission['to']['X']+1):
            for iy in range(mission['from']['Y'], mission['to']['Y']+1):

                if run_mode == '--lightshows':
                    if mission['event'] == events[0]:
                        bulbs[ix, iy] = 1
                    elif mission['event'] == events[1]:
                        bulbs[ix, iy] = not bulbs[ix, iy]
                    elif mission['event'] == events[2]:
                        bulbs[ix, iy] = 0
                elif run_mode == '--brightness':
                    if mission['event'] == events[0]:
                        bulbs[ix, iy] += 1
                    elif mission['event'] == events[1]:
                        bulbs[ix, iy] += 2
                    elif mission['event'] == events[2]:
                        if bulbs[ix, iy] > 0:
                            bulbs[ix, iy] -= 1

        if run_mode == '--lightshows':
            print('(Lightshows) Mission: ' + mission['event'] + ' -> From: (' + str(mission['from']['X']) + ',' + str(mission['from']['Y']) + ') To: (' + str(mission['to']['X']) + ',' + str(mission['to']['Y']) + '). Count of lights (ON): ' + str(np.count_nonzero(bulbs == 1)))
        elif run_mode == '--brightness':
            print('(Brightness) Mission: ' + mission['event'] + ' -> From: (' + str(mission['from']['X']) + ',' + str(mission['from']['Y']) + ') To: (' + str(mission['to']['X']) + ',' + str(mission['to']['Y']) + '). Sum of Brightness: ' + str(np.sum(bulbs)))