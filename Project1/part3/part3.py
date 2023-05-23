import json
class Node :
    def __init__(self , n):
        self.name = n
        self.actions = []
    def add_action(self , action , node):
        a = (action , node)
        self.actions.append(a)

states_ad = open('C:\git\TheoryofLanguagesAndAutomata\Project1\samples\phase3-sample\in\input1copy.json')
nfa = json.load(states_ad)
states = nfa['states']
states = states.replace("{", "").replace("}", "").replace("'", "").split(',')
fs = nfa['final_states'].replace("{", "").replace("}", "").replace("'", "").split(',')
starting_state_str = nfa['initial_state']
tans = nfa["transitions"]
nodes = []

for state in states :
    n = Node(state)
    nodes.append(n)



def find_node(str):
    for node in nodes :
        if node.name == str :
            return node

def is_landa(actions):
    for action in actions :
        if action[0] == "$":
            return action
    return None

for key,value in tans.items():
    start = find_node(key)
    for key1,value1 in value.items():
        ends = value1.replace("{", "").replace("}", "").replace("'", "").split(',')
        ends = [find_node(x) for x in ends]
        if(key1==""): 
            for end in ends:
                start.add_action("$",end)
        else:
            for end in ends:
                start.add_action(key1,end)
    


language = input()

def check_answer(state):
    if state.name in fs :
        return True
    return False

def check_language(current_state , language , index):
    acts = [x[0] for x in current_state.actions]
    if index == len(language) :
        return check_answer(current_state)
    elif language[index] not in acts :
        return False
    
    
    for action in current_state.actions :
        if action[0] == language[index] :
            result = check_language(action[1], language, index+1)
            acts.remove(action[0])
            if not result :
                for action in current_state.actions :
                    if action[0] == "$" :
                        return check_language(action[1], language, index)
                if language[index] in acts :
                    continue
                return False
            return result
                
starting_state = find_node(starting_state_str)


if check_language(starting_state, language, 0):
    print("Accepted")
else:
    print("Rejected")
  