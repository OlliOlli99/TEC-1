import os

def rename_state_zero(content):
    new_lines = []

    for line in content.splitlines():
        strip_line = line.strip()
        
        if not strip_line or (strip_line.startswith(';') and strip_line != ';S'):
            new_lines.append(line)
            continue

        if strip_line == ';S':
            continue
        
        transition = strip_line.split()
        if len(transition) >= 5:
            current_state, current_symbol, new_symbol, direction, new_state = transition
            
            if current_state == "0":
                current_state = "0o"
            if new_state == "0":
                new_state = "0o"

            new_line = f"{current_state} {current_symbol} {new_symbol} {direction} {new_state}"
            new_lines.append(new_line)
        else:
            new_lines.append(line)
    
    return new_lines

def left_to_wall(content):
    new_lines = []

    for line in content:
        strip_line = line.strip()
        if not strip_line:
            new_lines.append(line)
            continue

        if strip_line.startswith(';'):
            new_lines.append(line)
            continue
        
        transition = strip_line.split()
        if len(transition) < 5:
            new_lines.append(line)
            continue

        current_state, current_symbol, new_symbol, direction, new_state = transition

        if direction == 'l' and len(new_state) == 1:
            new_state = f"wall{new_state}"
        
        new_line = f"{current_state} {current_symbol} {new_symbol} {direction} {new_state}"
        new_lines.append(new_line)
    
    return new_lines


def create_walls(content):
    walls = []
    wall_sates = set()

    for line in content:
        strip_line = line.strip()
        if not strip_line or strip_line.startswith(';'):
            continue
        
        transition = strip_line.split()
        if len(transition) < 5:
            continue
        
        current_state, current_symbol, new_symbol, direction, new_state = transition

        if direction == 'l' and len(new_state) == 1:
            if new_state not in wall_sates:
                wall_name = f"wall{new_state}"
                walls.append(f"{wall_name} # * r {new_state}")
                walls.append(f"{wall_name} * * * {new_state}")
                wall_sates.add(new_state)
    
    return walls
    

def translate_sipser(file_in):

    file_in_content = file_in.read()
    file_int_state_zero = rename_state_zero(file_in_content)
    walls = create_walls(file_int_state_zero)
    file_in_new_states = left_to_wall(file_int_state_zero)

    with open('MT-DI.txt', 'r') as sipser:
        mt_di = sipser.read()
    
    with open(os.path.splitext(file_in.name)[0] + '.out', 'w') as file_out:
        file_out.write(mt_di)
        file_out.write('\n; wall transitions:\n')
        for w in walls:
            file_out.write(w + '\n')

        walls = create_walls(file_in_new_states)
        for w in walls:
            file_out.write(w + '\n')
        
        file_out.write('\n; original MT::\n')
        for line in file_in_new_states:
            file_out.write(line + '\n')


#def translate_infinite(file):    
#    return print("true")

def translator():
    with open('MT.in', 'r') as file_in:
        content = file_in.read()
        file_in.seek(0)
        if ';S' in content:
            translate_sipser(file_in)
    

translator()
