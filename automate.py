L = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
N = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
S = ['{', '}', '[', ']', ',', '.', '(', ')', '&', ':', ';', '<', '>', '=', '+', '-', '_', '*', '/', '%', '|', '^', '~', '!', '?', '@', '#', '$']

VAR = L + N + ['-', '_']
VAR2 = L + N + ['_']
VAL = L + N + S + [' ']

STATES = [i for i in range(1, 11)]
START = 1
ENDS = [1]

automate = {
    1: {**{char: 4 for char in VAR2}, '-': 2, ' ': 9, '.': 10, '\t': 1, 'eof': 1, '\n': 1},
    2: {**{char: 3 for char in VAR}, ' ': 4},
    3: {**{char: 4 for char in VAR2}, '-': 1},
    4: {**{char: 4 for char in VAR}, ':': 5, 'eof': 1, '\n': 1},
    5: {**{char: 5 for char in VAL}, '\'': 6, '"': 7, 'eof': 1, '\n': 1},
    6: {**{char: 6 for char in VAL}, '\'': 8},
    7: {**{char: 7 for char in VAL}, '"': 8},
    8: {'eof': 1, '\n': 1},
    9: {' ': 1},
    10: {'.': 11},
    11: {'.': 1}
}

def transition(current_state, t):
    if t in automate[current_state]:
        return automate[current_state][t]
    return None

def is_yaml(input_string: str) -> bool:
    current_state = START
    lines = input_string.split('\n')
    for index in range(len(lines)):
        line = lines[index]
        for c in line:
            old_state = current_state
            current_state = transition(current_state, c)
            print(f'{line} : {old_state} - {c} -> {current_state}')
            if not current_state:
                return False

        if index < len(lines) - 1:
            old_state = current_state
            current_state = transition(current_state, '\n')
            print(f'{lines[index]} : {old_state} - \\n -> {current_state}\n')
            if not current_state:
                return False
            
    current_state = transition(current_state, 'eof')

    return current_state in ENDS

yaml_content = """
name: John Doe
age: 30
hobbies:
  - Reading
  - Travelling
"""

def is_yaml_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return is_yaml(file.read())
   
    except FileNotFoundError:
        return is_yaml(yaml_content)

print(is_yaml_file('./values.yaml'))