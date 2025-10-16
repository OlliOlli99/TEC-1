import os
from pathlib import Path

current_dir = Path(__file__).resolve().parent
proofs_dir = current_dir.parent / "proofs"
mt_sip_path = proofs_dir / "MT-SIP.txt"

def rename_state_zero(content):
    new_lines = []

    for line in content.splitlines():
        strip_line = line.strip()
        
        if not strip_line or (strip_line.startswith(';') and strip_line != ';S'):
            new_lines.append(line)
            continue

        if strip_line == ';S':
            new_lines.append(';I')
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
    new_content = rename_state_zero(file_in_content)
    walls = create_walls(new_content)
    new_states = left_to_wall(new_content)

    with open(mt_sip_path, 'r') as sipser:
        mt_sip = sipser.read()
    
    with open(os.path.splitext(file_in.name)[0] + '.out', 'w') as file_out:
        file_out.write(mt_sip)
        file_out.write('\n; wall transitions:\n')
        for w in walls:
            file_out.write(w + '\n')
        
        file_out.write('\n; modified Sipser:\n')
        for line in new_states:
            file_out.write(line + '\n')
