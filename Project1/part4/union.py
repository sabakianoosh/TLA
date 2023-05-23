import json, sys, os
from graphviz import Digraph

SCRIPT_DIR = os.path.dirname(os.path.abspath('auxiliaries.py'))
sys.path.append(os.path.dirname('C:\git\TheoryofLanguagesAndAutomata\Project1\\auxiliaries.py'))

from auxiliaries import *



states_ad1 = ('C:\git\TheoryofLanguagesAndAutomata\Project1\samples\phase4-sample\\union\in\FA1.json')

states_ad2 = ('C:\git\TheoryofLanguagesAndAutomata\Project1\samples\phase4-sample\\union\in\FA2.json')

alphabets1, nodes1, starting_node1, fs1 = json2code(states_ad1)
alphabets2, nodes2, starting_node2, fs2 = json2code(states_ad2)

alphabets1.extend(alphabets2)
alphabets = alphabets1
nodes1.extend(nodes2)
nodes = nodes1


new_starting_state = Node("q00", alphabets)
new_starting_state.add_action("$", starting_node1)
new_starting_state.add_action("$", starting_node2)
starting_node = new_starting_state



nodes1_no = len(nodes1) - len(alphabets2)


counter4name = nodes1_no-1
for i in range(len(nodes2)):
    nodes2[i].name = f"q{counter4name}"
    counter4name+=1

finalstate = Node(f"q{counter4name+1}",alphabets)
for f in fs1:
    f.add_action("$",finalstate)

for f in fs2:
    f.add_action("$",finalstate)


starting_node.name = f"q{counter4name}"
nodes.append(finalstate)
nodes.append(starting_node)



result = convert2json_NFA(nodes, alphabets, starting_node, [finalstate])
with open("OutputPart4_union.json", "w") as outfile:
    outfile.write(result)
