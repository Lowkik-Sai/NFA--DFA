from graphviz import Digraph

def get_user_input():
    Q = input("Enter NFA states (comma-separated): ").split(',')
    q0 = input("Enter initial state: ")
    alphabet = input("Enter alphabet symbols (comma-separated): ").split(',')
    delta = []
    print("Enter transitions (enter 'done' to finish): ")
    while True:
        transition = input("Enter transition (e.g., A 0 BCD): ")
        if transition.lower() == 'done':
            break
        delta.append(transition.split(' '))

    F = input("Enter final states (comma-separated): ").split(',')

    return Q, q0, alphabet, delta, F

def epsilonClosure(deltaDict,state,string=""):
    
    closureStack=[state]
    epsString=string #Default epsString=""
    
    while len(closureStack)>0:
        currState=closureStack.pop(0)
        if "e" in deltaDict[currState]:
            eps=deltaDict[currState]['e']
            for ele in eps:
                if ele in epsString:
                    continue
                closureStack.append(ele)
                epsString+=str(ele)
    epsString=[x for x in epsString]
    epsString.sort()
    return epsString


def buildDfa(Q, q0, alphabet, deltaDict, epsilonClosureDict):

    dfaStates = [q0]
    dfaDelta = {}
    newDfaStates = [q0]

    trapState = 'ϕ'  # Trap state
    dfaDelta[trapState] = {}
    for alpha in alphabet:
        dfaDelta[trapState][alpha] = trapState

    while len(newDfaStates) > 0:
        currState = newDfaStates.pop(0)
        dfaDelta[currState] = {}
        for alpha in alphabet:
            newState = set()  # Alpha and Epsilon Transition states

            # 1. Transitions from current state
            for state in currState:
                if state in deltaDict and alpha in deltaDict[state]:
                    newState.update(set(deltaDict[state][alpha]))
                # Checking for epsilon transitions to states
                for epsState in epsilonClosureDict[state]:
                    if epsState in deltaDict and alpha in deltaDict[epsState]:
                        newState.update(set(deltaDict[epsState][alpha]))

            # 2. Repeated epsilon closure
            nextStates = set(newState)
            while True:
                newEpsilonClosure = set()
                for state in nextStates:
                    newEpsilonClosure.update(set(epsilonClosureDict[state]))
                if newEpsilonClosure.issubset(nextStates):
                    break
                nextStates.update(newEpsilonClosure)

            newState.update(nextStates)  # Updating newState after loop exits

            newStateStr = "".join(sorted(list(newState)))
            if newStateStr not in dfaStates:
                dfaStates.append(newStateStr)
                newDfaStates.append(newStateStr)
            if not newStateStr:  # If newStateStr is empty, transition to trap state
                newStateStr = trapState
            dfaDelta[currState][alpha] = newStateStr
            
    if '' in dfaDelta:
        del dfaDelta['']
    return dfaDelta


def getFinalStates(dfaDelta,F):
    finalStates=[]
    
    for state in dfaDelta:
        for final in F:
            if str(final) in state:
                finalStates.append(state)
    
    return finalStates   
    

def draw_dfa(dfa_delta, initial_state, final_states):
    dot = Digraph()
    dot.graph_attr['rankdir'] = 'LR'
    dot.node_attr['shape'] = 'circle'

    # Adding start state arrow to start state in DFA
    dot.attr('node', shape='none')
    dot.node('')
    dot.edge('', initial_state)

    for state, transitions in dfa_delta.items():
        state_str = ''.join(state)
        if state_str in final_states:
            dot.node(state_str, state_str, shape='doublecircle')  # Final state
        else:
            dot.node(state_str, state_str, shape='circle')  # Non-final state

    for state, transitions in dfa_delta.items():
        state_str = ''.join(state)
        for symbol, next_state in transitions.items():
            next_state_str = ''.join(next_state)
            dot.edge(state_str, next_state_str, label=symbol)

    dot.render('dfa_diagram', format='png', view=True)

def draw_nfa(nfa_delta, initial_state, final_states):
    dot = Digraph()
    dot.graph_attr['rankdir'] = 'LR'
    dot.node_attr['shape'] = 'circle'

    # Adding start state arrow to start state in DFA
    dot.attr('node', shape='none')
    dot.node('')
    dot.edge('', initial_state)

    # Track visited states to avoid infinite loops during epsilon transitions
    visited = set()

    def draw_state(state, state_str):
        if state in final_states:
            dot.node(state_str, state_str, shape='doublecircle')  # Final state
        else:
            dot.node(state_str, state_str, shape='circle')  # Non-final state

        if state not in visited:
            visited.add(state)
            for symbol, next_states in nfa_delta.get(state, {}).items():
                for next_state in next_states:
                    next_state_str = ''.join(next_state)
                    dot.edge(state_str, next_state_str, label=symbol)
                    draw_state(next_state, next_state_str)  # Recursive call for next states

    draw_state(initial_state, ''.join(initial_state))

    dot.render('nfa_diagram', format='png', view=True)




if __name__ == "__main__":
    Q, q0, alphabet, delta, F = get_user_input()
    
    #dict for deltaTransitions
    deltaDict={}
    for state in Q:
        deltaDict[state]={}
    
    for trans in delta:
        if trans[0] not in deltaDict:
            deltaDict[trans[0]] = {}
        # Getting already existing transitions and appending/adding them to list
        existing_transitions = deltaDict[trans[0]].get(str(trans[1]), [])
        deltaDict[trans[0]][str(trans[1])] = existing_transitions + [str(x) for x in trans[2]]

    epsilonClosureDict={}
    for state in Q:
        epsilonClosureDict[state]=epsilonClosure(deltaDict,state)
        
    print("Delta Transitions ",deltaDict)
    print("Epsilon Closure Dict", epsilonClosureDict)
        
    dfaDelta=buildDfa(Q,q0,alphabet,deltaDict,epsilonClosureDict)
    print("DFA Answer ",dfaDelta)
    
    finalStates=getFinalStates(dfaDelta,F)
    print("Final States ",finalStates)
    
    draw_nfa(deltaDict,q0,finalStates)
    draw_dfa(dfaDelta,q0,finalStates)