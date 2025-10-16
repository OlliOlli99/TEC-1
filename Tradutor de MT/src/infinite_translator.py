import os
from pathlib import Path

current_dir = Path(__file__).resolve().parent
proofs_dir = current_dir.parent / "proofs"
mt_di_path = proofs_dir / "MT-DI.txt"

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

def direction_to_wall(content):
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

        if direction == 'r' and len(new_state) == 1:
            new_state = f"&{new_state}"
        elif direction == 'l' and len(new_state) == 1:
            new_state = f"#{new_state}"
        
        new_line = f"{current_state} {current_symbol} {new_symbol} {direction} {new_state}"
        new_lines.append(new_line)
    
    return new_lines


def create_walls(content):
    right_walls = []
    right_wall_sates = set()

    left_walls = []
    left_wall_states = set()

    

    for line in content:
        strip_line = line.strip()
        if not strip_line or strip_line.startswith(';'):
            continue
        
        transition = strip_line.split()
        if len(transition) < 5:
            continue
        
        current_state, current_symbol, new_symbol, direction, new_state = transition

        if direction == 'r' and len(new_state) == 1:
            if new_state not in right_wall_sates:
                wall_name = f"&{new_state}"
                right_walls.append(f"\n{wall_name} * * * {new_state}")
                right_walls.append(f"{wall_name} & _ r {wall_name}")
                right_walls.append(f"{wall_name} _ & l {new_state}")
                right_wall_sates.add(new_state)
        
        elif direction == 'l' and len(new_state) == 1:
            if new_state not in left_wall_states:
                wall_name = f"#{new_state}"
                init = f"{wall_name}-0"
                move0 = f"{wall_name}-move0"
                move1 = f"{wall_name}-move1"
                rwall = f"{wall_name}-wall&"
                lwall = f"{wall_name}-wall#"

                left_walls.append(f"\n{wall_name} * * * {new_state}")
                left_walls.append(f"{wall_name} # * r {init}")
                left_walls.append(f"{init} 0 _ r {move0}")                
                left_walls.append(f"{init} 1 _ r {move1}")
                left_walls.append(f"{move0} 0 * r {move0}")
                left_walls.append(f"{move0} 1 0 r {move1}")
                left_walls.append(f"{move0} & 0 r {rwall}")
                left_walls.append(f"{move1} 1 * r {move1}")
                left_walls.append(f"{move1} 0 1 r {move0}")
                left_walls.append(f"{move1} & 1 r {rwall}")
                left_walls.append(f"{rwall} _ & l {lwall}")
                left_walls.append(f"{lwall} * * l {lwall}")
                left_walls.append(f"{lwall} _ * * {new_state}")
                left_wall_states.add(new_state)
                
    

    walls = right_walls + left_walls
    
    return walls
    

def translate_infinite(file_in):

    file_in_content = file_in.read()
    new_content = rename_state_zero(file_in_content)
    walls = create_walls(new_content)
    new_states = direction_to_wall(new_content)

    with open(mt_di_path, 'r') as doubly_infinite:
        mt_di = doubly_infinite.read()
    
    with open(os.path.splitext(file_in.name)[0] + '.out', 'w') as file_out:
        file_out.write(mt_di)
        for w in walls:
            file_out.write(w + '\n')

        walls = create_walls(new_states)
        for w in walls:
            file_out.write(w + '\n')
        
        file_out.write('\n; modified DI:\n')
        for line in new_states:
            file_out.write(line + '\n')
