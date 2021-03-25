import pickle
from collections import Counter
import math

def hash(sequence):
    wheels = [0, 0, 0, 0]
    for s in sequence:
        s = {"U": 0, "R": 1, "D": 2, "L": 3}[s]
        towards = s
        left = (s - 1) % 4
        right = (s + 1) % 4
        wheels[towards] = 3 * ((wheels[towards] + 3) // 3) 
        wheels[left] = 3 * ((wheels[left] + 1) // 3) + 2
        wheels[right] = 3 * ((wheels[right] + 2) // 3) + 1
    wheels = [w % 15 for w in wheels]
    return tuple(wheels)

def generate_inverse_hash(max_sequence_length=11):
    print("Generate inverse hash table")

    def add_to_sequence(seq):
        return tuple(s + addendum for s in seq for addendum in "URDL")

    def gen_sequences(length):
        seq = [""]
        for i in range(length):
            seq = add_to_sequence(seq)
        return seq

    inverse_hash_table = {}
    for length in range(max_sequence_length + 1):
        print(length)
        for seq in gen_sequences(length):
            hashed = hash(seq)
            if hashed not in inverse_hash_table or len(seq) < len(inverse_hash_table[hashed]):
                inverse_hash_table[hashed] = seq

    return inverse_hash_table


def find_ups(max_sequence_length=11):
    print("Generate inverse hash table")

    def add_to_sequence(seq):
        return tuple(s + addendum for s in seq for addendum in "URDL")

    def gen_sequences(length):
        seq = [""]
        for i in range(length):
            seq = add_to_sequence(seq)
        return seq

    target = hash("UDDR")

    inverse_hash_table = {}
    for length in range(max_sequence_length + 1):
        print(length)
        for seq in gen_sequences(length):
            hashed = hash(seq)
            if hashed == target:
                print(pretty(seq))
            #if hashed not in inverse_hash_table or len(seq) < len(inverse_hash_table[hashed]):
            #    inverse_hash_table[hashed] = seq

    return inverse_hash_table

def pretty(combo):
    combo = "(reset) " + " ".join(combo)
    for repeats in reversed(range(4, 12)):
        for direction in "URDL":
            combo = combo.replace((" " + direction) * repeats, " " + direction + "x" + str(repeats))
    return combo.strip()

print(find_ups())

import sys
sys.exit(0)

def probe_open(state, solution):
    if all(st == sl for (st, sl) in zip(state, solution)):
        return True

def probe_binding(state, solution, bind_order, direction):
    if all(st == sl for (st, sl) in zip(state, solution)):
        return True

def maybe_cached(fn, filename):
    try:
        with open(filename, "rb") as f:
            obj = pickle.load(f)
    except FileNotFoundError:
        obj = fn()

        with open(filename, "wb") as f:
            pickle.dump(obj, f)
    return obj

iht = maybe_cached(generate_inverse_hash, "iht.pkl")

valid_states = sorted(iht.keys())

def generate_probing_matrix():
    print("Generate probing matrix")
    return {solution: [probe(state, solution) for state in valid_states] for solution in valid_states}

probing_matrix = maybe_cached(generate_probing_matrix, "probe.pkl")

def entropy(col):
    l = len(col)
    probabilities = [v / l for v in Counter(col).values()]
    # Shannon entropy calculation
    return -sum(p * math.log2(p) for p in probabilities)

def entropies(table):
    print("Computing entropies...")
    return [entropy([row[i] for row in table.values()]) for i in range(len(valid_states))]

def argmax(l):
    return max(enumerate(l), key=lambda x: x[1])[0]

def get_trial_state(table):
    es = entropies(table)
    max_entropy = argmax(es)
    trial_state = valid_states[max_entropy]

    print("Trial sequence:", pretty(iht[trial_state]))
    col = {s: row[max_entropy] for (s, row) in table.items()}
    print("Possible outcomes:", dict(Counter(col.values())))
    return trial_state

def apply_trial_result(table, trial_state, probe_result):
    col_index = {s: i for (i, s) in enumerate(valid_states)}[trial_state]
    col = {s: row[col_index] for (s, row) in table.items()}
    if probe_result not in col.values():
        raise ValueError("Invalid probe result")
    return {s: table[s] for s in table if col[s] == probe_result}

simulated_solution_state = hash("UDDR")
simulate = True

#table = probing_matrix
#i = 0
#while True:
#    print("Step", i)
#    trial_state = get_trial_state(table)
#    while True:
#        if simulate:
#            probe_result = probe(trial_state, simulated_solution_state)
#            print("Simulated result:", probe_result)
#        else:
#            probe_result = input("What was it: ")
#        try:
#            table = apply_trial_result(table, trial_state, probe_result)
#        except ValueError as e:
#            print(e)
#        else:
#            break
#    print()
#
#    if len(table) == 1:
#        print("Solution found!")
#        solution_state = list(table.keys())[0]
#        solution_combo = iht[solution_state]
#        print("state:", solution_state)
#        print("combo:", pretty(solution_combo))
#        break
#    i += 1
