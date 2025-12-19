import hashlib
import glob
from pathlib import Path
import os
from typing import List, Dict, Tuple

def generate_line_range_hash(filepath: Path, start_line: int, end_line: int, hash_algorithm: str = 'sha256') -> str:
    """
    Gera um hash (checksum) do conteúdo de um arquivo, lendo APENAS as
    linhas entre start_line (inclusiva) e end_line (inclusiva).
    """
    hash_func = hashlib.new(hash_algorithm)
    
    # Lista para armazenar o conteúdo do intervalo
    content_lines = []
    
    try:
        # 1. Abrir o arquivo no modo texto para leitura de linhas
        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
            
            # 2. Iterar linha por linha com um contador
            for i, line in enumerate(f, start=1):
                
                # Se o contador atingiu a linha final + 1, pare a leitura imediatamente
                if i > end_line:
                    break
                    
                # Se o contador estiver no intervalo desejado (12 a 30)
                if i >= start_line and i <= end_line:
                    content_lines.append(line)
        
        # 3. Concatenar o conteúdo lido e fazer o hash
        # O join garante que o conteúdo do intervalo seja exatamente o que você deseja
        target_content = "".join(content_lines)
        
        # Codifica a string lida para bytes antes de fazer o hash
        hash_func.update(target_content.encode('utf-8'))
        
        return hash_func.hexdigest()
            
    except OSError as e:
        # Trata erros como permissão negada ou arquivo inexistente
        print(f"Erro ao ler arquivo {filepath}: {e}")
        return "" 

def check_line_range_differences(folder_path: str, pattern: str, start: int, end: int) -> Tuple[bool, Dict[str, List[str]]]:
    """
    Verifica a diferença de conteúdo (no intervalo de linhas especificado) 
    em arquivos que correspondem ao padrão na pasta.
    """
    full_pattern = os.path.join(folder_path, pattern)
    file_paths: List[Path] = [Path(p) for p in glob.glob(full_pattern)]

    if not file_paths:
        print(f"Nenhum arquivo encontrado com o padrão '{full_pattern}'.")
        return True, {}

    print(f"Encontrados {len(file_paths)} arquivos. Processando o conteúdo das Linhas {start} a {end}...")

    # Mapeia {hash_do_conteúdo_parcial: [lista_de_nomes_de_arquivos]}
    hash_map: Dict[str, List[str]] = {}
    
    for filepath in file_paths:
        # Usa a função modificada para o intervalo de linhas (12 a 30)
        file_hash = generate_line_range_hash(filepath, start_line=start, end_line=end)
        
        if file_hash:
            filename = filepath.name
            if file_hash not in hash_map:
                hash_map[file_hash] = []
            
            hash_map[file_hash].append(filename)

    is_identical = len(hash_map) <= 1
    
    return is_identical, hash_map

# --- Configuração ---
TARGET_FOLDER = 'C:\\Users\\JoaoPedroPetersBarbo\\Documents\\github\\PyANA\\sistemas\\cdu2udc' 
FILE_PATTERN = 'CDU_AVR_*.cdu' 
START_LINE = 12 # Começa na Linha 12 (inclusiva)
END_LINE = 30   # Termina na Linha 30 (inclusiva)
# --- Execução ---

are_all_identical, difference_map = check_line_range_differences(TARGET_FOLDER, FILE_PATTERN, START_LINE, END_LINE)

print("\n--- Resultados ---")
if are_all_identical:
    num_files = sum(len(files) for files in difference_map.values())
    print(f"✅ Sucesso! O conteúdo (das linhas {START_LINE} a {END_LINE}) de todos os {num_files} arquivos é **IDÊNTICO**.")
else:
    print(f"❌ Diferenças Encontradas no Conteúdo (das linhas {START_LINE} a {END_LINE})!")
    print("Os arquivos NÃO são idênticos nesse intervalo. Agrupamento por conteúdo único (hash):")
    
    for hash_val, file_list in difference_map.items():
        print(f"\nGrupo de Conteúdo Único (Hash: {hash_val[:10]}...):")
        for filename in file_list:
            print(f"  - {filename}")