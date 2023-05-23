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



class Node1 :
    def __init__(self, alphabets):
        self.name1 = []
        self.name = ""
        self.actions = {'$' :[] ,}
        for alphabet in alphabets :
            self.actions[alphabet] = []
    def add_action(self , action , node):
        self.actions[action].append (node)
    def add_name(self, name):
        self.name1.append(name)
    def changename(self):
        self.name1.sort(key=lambda x: int(x[1]))
        for n in self.name1:
            self.name += n



def repeatd(arr):
    result = []
    for item in arr :
        if item not in result and item != [] :
            result.append(item)

    return result

def e_closure(result):
    for s in result :
        e = s.actions["$"]
        if e == [] or e in result :
            continue
        result.extend(s.actions["$"])
    return result

def Is_Equal(array1 , array2):
    if len(array1)!= len( array2):
        return False

    for item in array1 :
        if item not in array2 :
            return False
    return True

def Start(start):
    newstates = [start]
    e_c = start.actions["$"]
    if len(e_c) != 0 :
        newstates.extend(e_c)
        for s in e_c :
            newstates.extend(Start(s))
    return repeatd(newstates)


def convert( states):
    for alphabet in alphabets :
        newstate = []
        for state in states :
            newstate.extend(state.actions[alphabet])
            newstate.extend(e_closure(newstate))
        newstate = repeatd(newstate)
        rep =False
        for k in newstates:
            if Is_Equal(k , newstate) :
                rep = True
                break
        if not rep:
            d = newstate
            newstates.append(d)
            convert(newstate)



def listtonode(result):
    ListOfnode = []
    for i in range(len(result)):
        if (len(result[i])!=0):
            node2append = Node1(alphabets=alphabets)
            for j in range(len(result[i])):
                if(not result[i][j].name in node2append.name):
                    node2append.add_name(result[i][j].name)
            ListOfnode.append(node2append)
        else:
            toappend = Node1(alphabets)
            toappend.name1 = []
            toappend.name = "TRAP"
            ListOfnode.append(toappend)
    return ListOfnode




def find_node2(namelist,nodes):
    for node in nodes :
        if node.name1 == namelist :
            return node
        
def addactions(result,listofnodes):  
    for i in range(len(result)):
        names = []
        for a in alphabets:
            state2go = []
            for j in range(len(result[i])):
                if(result[i][j].name not in names): 
                    names.append(result[i][j].name)
                if (len(result[i][j].actions[a])!=0):
                    for k in range(len(result[i][j].actions[a])):
                        state2go.append(result[i][j].actions[a][k].name)
            findstate = find_node2(state2go,listofnodes)
            here_node = find_node2(names,listofnodes)
            here_node.add_action(a,findstate)




address = 'C:\git\TheoryofLanguagesAndAutomata\Project1\samples\phase1-sample\in\input1.json'
alphabets, nodes, starting_node, fs = json2code(address)
newstates = [Start(starting_node)]
convert(newstates[0])
result = newstates
listofnode = listtonode(result)
lr = addactions(result,listofnode)

for node in listofnode:
    node.name1.sort(key=lambda x: int(x[1]))


for node in listofnode:
    node.changename()

fss = []
for i in range(len(listofnode)):
    for s in listofnode[i].name1:  
        if(find_node(s,nodes) in fs):
            fss.append(listofnode[i])
            break

starting_node = listofnode[0]
json1 = convert2json_DFA(listofnode,alphabets,starting_node,fss)

with open("OutputPart1.json", "w") as outfile:
    outfile.write(json1)
