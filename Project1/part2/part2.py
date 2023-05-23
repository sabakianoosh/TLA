import json, sys, os
from graphviz import Digraph

class Node :
    def __init__(self , n , alphabets):
        self.name = n
        self.actions = {'$' :[] ,}
        for alphabet in alphabets :
            self.actions[alphabet] = []
    def add_action(self , action , node):
        self.actions[action].append (node)


def find_node(str,nodes):
    for node in nodes :
        if node.name == str :
            return node

def json2code(states_ad):
    nodes = []
    states_ad = open(states_ad)
    nfa = json.load(states_ad)
    states = nfa['states']
    states = states.replace("{", "").replace("}", "").replace("'", "").split(',')
    alphabets = nfa['input_symbols']
    alphabets = alphabets.replace("{", "").replace("}", "").replace("'", "").split(',')
    fs_str = nfa['final_states'].replace("{", "").replace("}", "").replace("'", "").split(',')
    
    starting_node_str = nfa['initial_state']
    tans = nfa["transitions"]

    for state in states :
        n = Node(state , alphabets)
        if( n not in nodes):
            nodes.append(n)


    landa_transitions = []
    for key,value in tans.items():
        
        start = find_node(key,nodes)
        for key1,value1 in value.items():
            ends = value1.replace("{", "").replace("}", "").replace("'", "").split(',')
            ends = [find_node(x,nodes) for x in ends]
            if(key1==""):   
                for end in ends:
                    start.add_action("$",end)
                    landa_transitions.append([start,end])
            else:
                for end in ends:
                    start.add_action(key1,end)

    for i in range(len(landa_transitions)):
        for j in range(len(nodes)):
            for key,value in nodes[j].actions.items():
                if (landa_transitions[i][0] in value):
                    nodes[j].add_action(key,landa_transitions[i][1])
    
    fs = [find_node(x,nodes) for x in fs_str]
    starting_node = find_node(starting_node_str,nodes)

    return alphabets,nodes,starting_node,fs




def convert2json_DFA(states, input_symbols, starting_node, fs):
    states_str = "{"
    input_symbols_str = "{"
    final_states_str = "{"
    for state in states:
        states_str += f"'{state.name}',"
    for input_symbol in input_symbols:
        input_symbols_str += f"'{input_symbol}',"
    for final_state in fs:
        final_states_str += f"'{final_state.name}',"
    items = [states_str, input_symbols_str, final_states_str]
    for i in range(len(items)):
        items[i] = items[i][:-1]
        items[i]+="}"
    transitions_str = {}
    for state in states:
        transitions_str[f"{state.name}"] = {}
        for input_symbol in input_symbols:
            if(len(state.actions[input_symbol])==0): 
                transitions_str[f"{state.name}"][f"{input_symbol}"] = "TRAP"
            else:
                transitions_str[f"{state.name}"][f"{input_symbol}"] = str(state.actions[input_symbol][0].name)

    dictionary = {"states":items[0], "input_symbols": items[1],
                 "transitions":transitions_str,
                 "initial_state":str(starting_node.name), "final_states":items[2]}

    jsonFile = json.dumps(dictionary,indent=4)
    return jsonFile
     


def convert2json_NFA(states, input_symbols, starting_node, fs):
    states_str = "{"
    input_symbols_str = "{"
    final_states_str = "{"
    for state in states:
        states_str += f"'{state.name}',"
    for input_symbol in input_symbols:
        input_symbols_str += f"'{input_symbol}',"
    for final_state in fs:
        final_states_str += f"'{final_state.name}',"
    items = [states_str, input_symbols_str, final_states_str]
    for i in range(len(items)):
        items[i] = items[i][:-1]
        items[i]+="}"
    transitions_str = {}
    for state in states:
        transitions_str[f"{state.name}"] = {}
        for key,value in state.actions.items():
            if(key=="$"):
                alphabet = ""
            else:
                alphabet = key
            if(len(value)!=0): 
                transitions_str[f"{state.name}"][f"{alphabet}"] = "{"
                if(len(value)==1):
                    transitions_str[f"{state.name}"][f"{alphabet}"] += f"'{value[0].name}'"
                    transitions_str[f"{state.name}"][f"{alphabet}"] += "}"
                else:
                    for i in range(len(value)):
                        transitions_str[f"{state.name}"][f"{alphabet}"] += f"'{value[i].name}',"
                    transitions_str[f"{state.name}"][f"{alphabet}"] = transitions_str[f"{state.name}"][f"{alphabet}"][:-1]
                    transitions_str[f"{state.name}"][f"{alphabet}"] += "}"




    dictionary = {"states":items[0], "input_symbols": items[1],
                 "transitions":transitions_str,
                 "initial_state":str(starting_node.name), "final_states":items[2]}

    jsonFile = json.dumps(dictionary,indent=4)
    return jsonFile



final_i = []
notfinal_i = [1]
def reachable(list , current_state):
    for alphabet in alphabets:
        next_s = current_state.actions[alphabet][0]
        if next_s != [] and next_s not in list:
            list.append(next_s)
            if next_s in fs :
                final_i.append(list.index(next_s)+1)
            else :
                notfinal_i.append(list.index(next_s)+1)
            reachable(list, next_s)
    return list

#reachable nodes from initial state
states_ad = 'C:\git\TheoryofLanguagesAndAutomata\Project1\samples\phase2-sample\in\input1copy.json'
alphabets, nodes, starting_state, fs = json2code(states_ad)

R_nodes = reachable([starting_state] , starting_state)
names = [x.name for x in R_nodes]

T1_rows = fs
T2_rows = [node for node in R_nodes if node not in fs]

#constructing tables 

def init_table(table , table_rows):
    for i in range(1 , len(table_rows)+1):
        table[i][0] = table_rows[i-1]
    for j in range(1 , len(alphabets)+1):
        table[0][j] = alphabets[j-1]


def make_table(table , table_rows):
    for i in range(1 , len(table_rows) + 1):
        for j in range(1 , len(alphabets)+1):
            table[i][j] = table[i][0].actions[table[0][j]]
            


def are_same(row1 , row2):
    sameness = True
    for j in range(1 , len(alphabets)+1):
        if row1[j][0].name != row2[j][0].name :
            sameness = False
    return sameness


def contains(list , node):
    for i in range (len(list)):
        if node in list[i]:
            return True
    return False

def are_equal(list1 , list2):
   for i in range(len(list2)):
    for j in range (len(list2[i])):
        if len(list1[i])!=len(list2[i]) or list1[i][j] != list2[i][j]:
            return False
    return True

def reduce_table(table , list , level):
    newlist = [[] for i in range(len(table))]
    index = 0
    for item in list :
        for i in range(len(item)):
            if not contains(newlist, item[i]):
                newlist[index].append(item[i])
                for k in range (i+1 , len(item)):
                    if are_same(table[item[i]], table[item[k]]):
                        newlist[index].append(item[k])
            else :
                continue
            index += 1
    
    if not are_equal(newlist , list) :
        for i in range(len(newlist)):
            for item in newlist[i] :
                table[item][0].name = f"g{level}{i}"
        return reduce_table(table, newlist , level+1)

    return newlist

T =[[0 for j in range (len(alphabets)+1) ] for i in range(len(R_nodes) +1) ]

init_table(T, R_nodes)

make_table(T, R_nodes)

for action in T1_rows :
    action.name =  "f0"
for action in T2_rows :
    action.name = "f1"
   
result = reduce_table(T, [notfinal_i, final_i], 0)

states = []
fs = []
namesofstates_l = []
namesofstates_s = []


for i in range(len(result)):
    if(len(result[i])==0):
        break
    else:
        newname = ""
        for j in range(len(result[i])):
            result[i].append(R_nodes[result[i][0]-1])
            newname+=names[result[i][0]-1]
            del result[i][0]
        for state in result[i]:
            state.name = newname
        states.append(result[i][0])
            


for final_index in final_i:#passing element in states for names changes
    fs.append(R_nodes[final_index-1])


starting_state = states[0]

json1 = convert2json_DFA(states,alphabets,starting_state,fs)

with open("OutputPart2.json", "w") as outfile:
    outfile.write(json1)
