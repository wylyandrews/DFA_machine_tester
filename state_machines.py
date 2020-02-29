import itertools

class State():
    # success shows that if the machine ends here, it's a success
    # connections is a dictionary where keys are inputs and values are other states to connect to
    # connection_req is the definition of which keys are necessary for all DFA states
    def __init__(self, success, connections=None, connection_req=None):
        self.success = success
        
        if connections:
            self.connections = connections
        else:
            self.connections = dict()
            
        if connection_req:
            self.connection_req = connection_req
        else:
            self.connection_req = list(self.connections.keys())
            
        for inp, next_state in self.connections.items():
            if inp not in connection_req:
                raise Exception("Connection key is not in the requirements.")
            if not isinstance(next_state, State):
                raise Exception("Connection does not lead to another state.")
    
    def validate_connections(self):
        for inp, next_state in self.connections.items():
            if inp not in self.connection_req:
                raise Exception("Connection key is not in the requirements.")
            if not isinstance(next_state, State):
                raise Exception("Connection does not lead to another state.")
        
        for req in self.connection_req:
            if req not in self.connections.keys():
                raise Exception("Not all requirements are solved.")

        
class StateMachine():
    # start is the starting State
    # states is all the states in the machine
    # connection_req is the possible input for the machine (as a list of values)
    def __init__(self, start, states, connection_req=None):
        self.states = states
        self.start = start

        if self.start not in states:
            raise Exception("Start state not in given states.")

        if connection_req:
            self.connection_req = connection_req
        else:
            self.connection_req = self.start
            
        success_exists = False
        for state in states:
            if state.success:
                success_exists = True
            if state.connection_req != self.connection_req:
                raise Exception("State connection_reqs do not match up")

        if not success_exists:
            raise Exception("State machine has no success state")
        self.map = dict()
        for state in states:
            state.validate_connections()
            if state in self.map.keys():
                raise Exception("start was added to the map twice")
            self.map[state] = state.connections

def run_tests(machine, input_choices, length_of_strings):
    runs = list()
    runs.append("")
    for i in range(1, length_of_strings+1):
        for generated_tuple in itertools.product(input_choices, repeat=i):
            runs.append(''.join(generated_tuple))
    print(f"my_runs: {runs}")
    # runs = ['', 'a', 'b', 'aa', 'ab', 'ba', 'bb', 'aaa', 'aab', 'aba', 'abb', 'baa', 'bab', 'bba', 'bbb']
    success_inputs = list()
    fail_inputs = list()
    for run in runs:
        if run_machine(machine, run):
            success_inputs.append(run)
        else:
            fail_inputs.append(run)
    return (success_inputs, fail_inputs)

def run_machine(machine, run):
    current_state = machine.start
    for c in run:
        current_state = current_state.connections[c]
    return current_state.success

my_input_possibilities = ['0', '1']

q_early_1 = State(success=True, connections=None, connection_req=my_input_possibilities)
q_early_2 = State(success=True, connections=None, connection_req=my_input_possibilities)
q_early_3 = State(success=True, connections=None, connection_req=my_input_possibilities)
q_early_4 = State(success=True, connections=None, connection_req=my_input_possibilities)

q1 = State(success=True, connections=None, connection_req=my_input_possibilities)
q2 = State(success=True, connections=None, connection_req=my_input_possibilities)
q3 = State(success=True, connections=None, connection_req=my_input_possibilities)
q4 = State(success=True, connections=None, connection_req=my_input_possibilities)
q5 = State(success=True, connections=None, connection_req=my_input_possibilities)
q6 = State(success=True, connections=None, connection_req=my_input_possibilities)
q7 = State(success=False, connections=None, connection_req=my_input_possibilities)


q_early_1.connections['0'] = q1
q_early_1.connections['1'] = q_early_2
q_early_2.connections['0'] = q5
q_early_2.connections['1'] = q_early_3
q_early_3.connections['0'] = q4
q_early_3.connections['1'] = q_early_4
q_early_4.connections['0'] = q7
q_early_4.connections['1'] = q7
q1.connections['0'] = q1
q1.connections['1'] = q2
q2.connections['0'] = q5
q2.connections['1'] = q3
q3.connections['0'] = q4
q3.connections['1'] = q7
q4.connections['0'] = q1
q4.connections['1'] = q7
q5.connections['0'] = q1
q5.connections['1'] = q6
q6.connections['0'] = q5
q6.connections['1'] = q7
q7.connections['0'] = q7
q7.connections['1'] = q7

my_states = [q_early_1, q_early_2, q_early_3, q_early_4, q1, q2, q3, q4, q5, q6, q7]
my_machine = StateMachine(q_early_1, my_states, my_input_possibilities)

my_results = run_tests(my_machine, my_input_possibilities, 4)

"""
my_input_possibilities = ['a', 'b']

q1 = State(success=False, connections=None, connection_req=my_input_possibilities)
q2 = State(success=True, connections=None, connection_req=my_input_possibilities)
q3 = State(success=True, connections=None, connection_req=my_input_possibilities)
q4 = State(success=False, connections=None, connection_req=my_input_possibilities)

q1.connections['a'] = q2
q1.connections['b'] = q4
q2.connections['a'] = q2
q2.connections['b'] = q3
q3.connections['a'] = q3
q3.connections['b'] = q4
q4.connections['a'] = q4
q4.connections['b'] = q4

my_states = [q1, q2, q3, q4]
my_machine = StateMachine(q1, my_states, my_input_possibilities)
"""
