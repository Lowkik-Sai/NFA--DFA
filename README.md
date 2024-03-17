# NFA-->DFA

# ABOUT PROJECT:
We have chosen to implement an NFA (Non-deterministic Finite Automata) to DFA
(Deterministic Finite Automata).
NFA’s are widely chosen because they are flexible in design, simplistic in construction of
language, they are concise when chosen to represent a language and they are compatible
with other models such as Push Down Automata (PDA).
But, sometimes, NFA’s efficiency can be put to test. So, we convert the NFA to an
equivalent DFA to simplify the situation we are given, and design solutions based on the
DFA that is derived from the NFA.
The reason we choose to implement an equivalent DFA for the NFA is because they are
Deterministic while having the exact same language set as the NFA. Thus, making it easier
for analysis of the situation compared to the similar one in NFA.

# EXPLAINATION:
• The above code is a Python script that converts a Non-deterministic Finite
Automata (NFA) to a Deterministic Finite Automata (DFA). The script first prompts
the user to input NFA states, initial state, alphabet symbols, transitions, and final
states. It then defines several functions to process the user input, construct the
DFA, and draw the DFA diagram using Graphviz.
• The main steps of the algorithm are:
• Parse user input: The get_user_input function reads the NFA information from the
user.
• Create a dictionary for transitions: The script converts the transitions list to a
dictionary with states as keys and transitions as values.
• Calculate epsilon closure: The epsilonClosure function calculates the epsilon
closure for a given state.
• Build DFA: The buildDfa function creates the DFA using the epsilon closure and
transitions.
• Get final states: The getFinalStates function identifies the final states in the DFA.
• Draw DFA diagram: The draw_dfa function visualizes the DFA diagram using
Graphviz.
• The script uses the graphviz library to draw the DFA diagram. The digraph object is
used to create a directed graph, and nodes and edges are added with appropriate
labels.

Install graphviz (pip install graphviz) 
Link : https://www2.graphviz.org/Packages/development/windows/10/cmake/Release/x64/ (WINDOWS)

To Run : python nfa2dfa.py
