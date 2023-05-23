import json, sys, os
from graphviz import Digraph
SCRIPT_DIR = os.path.dirname(os.path.abspath('auxiliaries.py'))
sys.path.append(os.path.dirname('C:\git\TheoryofLanguagesAndAutomata\Project1\\auxiliaries.py'))

from auxiliaries import *

states_ad = 'C:\git\TheoryofLanguagesAndAutomata\Project1\samples\phase4-sample\star\in\FA.json'
alphabets, nodes, starting_state, fs = json2code(states_ad)

for s in fs:
    s.add_action("$", starting_state)

starting_state.add_action("$",fs[0])


result = convert2json_NFA(nodes, alphabets, starting_state, fs)
with open("OutputPart4_star.json", "w") as outfile:
    outfile.write(result)
