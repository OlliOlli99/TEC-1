import os
from pathlib import Path

current_dir = Path(__file__).resolve().parent
proofs_dir = current_dir.parent / "proofs"
mt_di_path = proofs_dir / "MT-DI.txt"

# Separar comentários após transição
def inline_comment(line: str):
    stripped = line.strip()

    if not stripped or stripped.startswith(';'):
        return (False, line, "")
    
    if ';' in stripped:
        before, after = stripped.split(';', 1)

        if before.strip():
            return (True, before.strip(), after.strip())
    
    return (False, stripped, "")

# Renomear estado inicial da MT original para "0o" para evitar conflitos internos do tradutor
def rename_state_zero(content):
    new_lines = []

    for line in content.splitlines():
        has_comment, trans_content, comment = inline_comment(line)
        strip_line = trans_content.strip()
        
        # Cabeçalho da máquina: converte MT de entrada duplamente infinita para Sipser
        if strip_line == ';I':
            new_lines.append(';S')
            continue
        # Linha vazia ou comentário
        elif not strip_line or strip_line.startswith(';'):
            new_lines.append(line)
            continue
        
        # Processa transições da MT
        transition = strip_line.split()
        if len(transition) >= 5:
            current_state, current_symbol, new_symbol, direction, new_state = transition
            
            # Renomeia o estado inicial
            if current_state == "0":
                current_state = "0o"
            if new_state == "0":
                new_state = "0o"

            new_line = f"{current_state} {current_symbol} {new_symbol} {direction} {new_state}"
            new_lines.append(new_line)
        else:
            new_lines.append(line)
    
    return new_lines

# Prefixar os novos estados criados para movimentação da fita com '&' (direita) e '#' (esquerda)
def direction_to_wall(content):
    new_lines = []

    for line in content:
        has_comment, trans_content, comment = inline_comment(line)
        strip_line = trans_content.strip()
        
        # Linha vazia
        if not strip_line:
            new_lines.append(line)
            continue
        
        # Comentário
        if strip_line.startswith(';'):
            new_lines.append(line)
            continue
        
        # Transição inválida
        transition = strip_line.split()
        if len(transition) < 5:
            new_lines.append(line)
            continue

        current_state, current_symbol, new_symbol, direction, new_state = transition

        # Prefixa novos estados conforme a direção
        if direction == 'r' and not new_state.startswith("halt"):
            new_state = f"&{new_state}"
        elif direction == 'l' and not new_state.startswith("halt"):
            new_state = f"#{new_state}"
        
        new_line = f"{current_state} {current_symbol} {new_symbol} {direction} {new_state}"
        new_lines.append(new_line)
    
    return new_lines

# Criar os estados auxiliares para movimentar a fita
def create_walls(content):
    right_walls = []
    right_wall_sates = set()

    left_walls = []
    left_wall_states = set()

    for line in content:
        has_comment, trans_content, comment = inline_comment(line)
        strip_line = trans_content.strip()
        if not strip_line or strip_line.startswith(';'):
            continue
        
        transition = strip_line.split()
        if len(transition) < 5:
            continue
        
        current_state, current_symbol, new_symbol, direction, new_state = transition

        # Movimentos para a direita
        if direction == 'r' and not new_state.startswith("halt"):
            if new_state not in right_wall_sates:
                wall_name = f"&{new_state}"
                moveB = f"{wall_name}-moveB"
                right_walls.append(f"\n;right movement transitions state {new_state}")
                # Estado para verificar se o símbolo atual é "&"
                right_walls.append(f"{wall_name} * * * {new_state}")
                right_walls.append(f"{wall_name} & _ r {moveB}")
                right_walls.append(f"{moveB} _ & l {new_state}")
                right_wall_sates.add(new_state)
        
        # Movimentos para a esquerda
        elif direction == 'l' and not new_state.startswith("halt"):
            if new_state not in left_wall_states:
                wall_name = f"#{new_state}"
                init = f"{wall_name}-0"
                move0 = f"{wall_name}-move0"
                move1 = f"{wall_name}-move1"
                moveB = f"{wall_name}-moveB"
                rwall = f"{wall_name}-wall&"
                lwall = f"{wall_name}-wall#"

                left_walls.append(f"\n;left movement transitions state {new_state}")
                # Estado para verificar se o símbolo atual é #
                left_walls.append(f"{wall_name} * * * {new_state}")
                left_walls.append(f"{wall_name} # * r {init}")
                # Estado para iniciar a movimentação da fita
                left_walls.append(f"{init} 0 _ r {move0}")                
                left_walls.append(f"{init} 1 _ r {move1}")
                left_walls.append(f"{init} _ _ r {moveB}")
                # Estado complementar para mover os 0's
                left_walls.append(f";new move0 state {new_state}")
                left_walls.append(f"{move0} 0 * r {move0}")
                left_walls.append(f"{move0} 1 0 r {move1}")
                left_walls.append(f"{move0} _ 0 r {moveB}")
                left_walls.append(f"{move0} & 0 r {rwall}")
                # Estado complementar para mover os 1's
                left_walls.append(f";new move1 state {new_state}")
                left_walls.append(f"{move1} 1 * r {move1}")
                left_walls.append(f"{move1} 0 1 r {move0}")
                left_walls.append(f"{move1} _ 1 r {moveB}")
                left_walls.append(f"{move1} & 1 r {rwall}")
                # Estado complementar para mover os brancos (_)
                left_walls.append(f";new moveB state {new_state}")
                left_walls.append(f"{moveB} _ * r {moveB}")
                left_walls.append(f"{moveB} 0 _ r {move0}")
                left_walls.append(f"{moveB} 1 _ r {move1}")
                left_walls.append(f"{moveB} & _ r {rwall}")
                # Estado complementar para mover a parede à direita
                left_walls.append(f";new wall& state {new_state}")
                left_walls.append(f"{rwall} _ & l {lwall}")
                # Estado para retornar o cabeçote ao novo branco no início da fita
                left_walls.append(f";new wall# state {new_state}")
                left_walls.append(f"{lwall} * * l {lwall}")
                left_walls.append(f"{lwall} _ * * {new_state}")
                left_wall_states.add(new_state)
                
    

    walls = right_walls + left_walls
    
    return walls
    
# Processar um arquivo de MT de entrada, gerar os estados auxiliares
# e escrever o arquivo traduzido de saída
def translate_infinite(file_in):

    # Lê conteúdo da MT de entrada
    file_in_content = file_in.read()
    # Renomeia estado inicial
    new_content = rename_state_zero(file_in_content)
    # Cria estados auxiliares para "movimento de parede"
    walls = create_walls(new_content)
    # Prefixa novos estados de acordo com a direção
    new_states = direction_to_wall(new_content)

    # Lê a MT duplamente infinita original
    with open(mt_di_path, 'r') as doubly_infinite:
        mt_di = doubly_infinite.read()
    
    # Escreve arquivo de saída
    with open(os.path.splitext(file_in.name)[0] + '.out', 'w') as file_out:
        file_out.write(mt_di + '\n')

        file_out.write('\n;translator transitions:')
        for w in walls:
            file_out.write(w + '\n')
        
        file_out.write('\n;modified DI:\n')
        for line in new_states:
            file_out.write(line + '\n')
