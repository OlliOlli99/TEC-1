from pathlib import Path
import sipser_translator as trans_s
import infinite_translator as trans_i

def translator(file):
    with open(file, 'r') as file_in:
        content = file_in.read()
        file_in.seek(0)
        if ';S' in content:
            trans_s.translate_sipser(file_in)
        elif ';I' in content:
            trans_i.translate_infinite(file_in)

# Tradutor de MT / src
current_dir = Path(__file__).resolve().parent
project_root = current_dir.parent
input_file = project_root / "MT.in"

# Entrada do arquivo de input "MT.in"
translator(input_file)