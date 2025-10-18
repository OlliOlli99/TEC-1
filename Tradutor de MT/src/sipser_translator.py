import os
from pathlib import Path

current_dir = Path(__file__).resolve().parent
proofs_dir = current_dir.parent / "proofs"
mt_sip_path = proofs_dir / "MT-SIP.txt"

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
        if strip_line == ';S':
            new_lines.append(';I')
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
def left_to_wall(content):
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
        if direction == 'l' and not new_state.startswith("halt"):
            new_state = f"wall{new_state}"
        
        new_line = f"{current_state} {current_symbol} {new_symbol} {direction} {new_state}"
        new_lines.append(new_line)
    
    return new_lines

# Criar os estados auxiliares para movimentar a fita
def create_walls(content):
    walls = []
    wall_sates = set()

    for line in content:
        has_comment, trans_content, comment = inline_comment(line)
        strip_line = trans_content.strip()

        if not strip_line or strip_line.startswith(';'):
            continue
        
        transition = strip_line.split()
        if len(transition) < 5:
            continue
        
        current_state, current_symbol, new_symbol, direction, new_state = transition
        
        # Movimentos para a esquerda
        if direction == 'l' and not new_state.startswith("halt"):
            if new_state not in wall_sates:
                wall_name = f"wall{new_state}"
                # Estado para verificar se o símbolo atual é "#"
                walls.append(f"\n;new wall state {new_state}")                
                walls.append(f"{wall_name} # * r {new_state}")
                walls.append(f"{wall_name} * * * {new_state}")
                wall_sates.add(new_state)
    
    return walls
    
# Processar um arquivo de MT de entrada, gerar os estados auxiliares
# e escrever o arquivo traduzido de saída
def translate_sipser(file_in):

    # Lê conteúdo da MT de entrada
    file_in_content = file_in.read()
    # Renomeia estado inicial
    new_content = rename_state_zero(file_in_content)
    # Cria estados auxiliares para "movimento de parede"
    walls = create_walls(new_content)
    # Prefixa novos estados de acordo com a direção
    new_states = left_to_wall(new_content)

    # Lê a MT duplamente infinita original
    with open(mt_sip_path, 'r') as sipser:
        mt_sip = sipser.read()
    
    # Escreve arquivo de saída
    with open(os.path.splitext(file_in.name)[0] + '.out', 'w') as file_out:
        file_out.write(mt_sip + '\n')

        file_out.write('\n;translator transitions:')
        for w in walls:
            file_out.write(w + '\n')
        
        file_out.write('\n;modified Sipser:\n')
        for line in new_states:
            file_out.write(line + '\n')
