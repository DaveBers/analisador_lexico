import re

# Dicionário de tokens
TOKEN_DICT = {
    "program": 8,
    "var": 2,
    "to": 3,
    "then": 4,
    "string": 5,
    "real": 6,
    "read": 7,
    "procedure": 9,
    "print": 10,
    "literal": 13,
    "integer": 14,
    "if": 15,
    "ident": 16,
    "for": 17,
    "end": 18,
    "else": 19,
    "do": 20,
    "const": 21,
    "begin": 22,
    "vstring": 23,
    ">=": 24,
    ">": 25,
    "=": 26,
    "<>": 27,
    "<=": 28,
    "<": 29,
    "+": 30,
    ";": 31,
    ":=": 32,
    ":": 33,
    "/": 34,
    ".": 35,
    ",": 36,
    "*": 37,
    ")": 38,
    "(": 39,
    "{": 40,
    "}": 41,
    "-": 42,
    "*-*": 43,
    "(": 44,  # abre comentário bloco
    ")": 45,  # fecha comentário bloco
    '"': 46
}

# Expressões regulares para reconhecimento de tokens
TOKEN_REGEX = [
    (r'\*-\*.*', None),             # Comentário de uma linha
    (r'\(;.*?;\)', None),           # Comentário de bloco
    (r'"[^"]*"', 'literal'),        # Literais
    (r"'[^']*'", 'vstring'),        # Strings
    (r'[a-zA-Z]{1,10}', 'ident'),   # Identificadores (máx. 10 caracteres)
    (r'\d+\.\d{1,2}', 'real'),      # Reais com até 2 casas decimais
    (r'\d+', 'integer'),            # Inteiros
    (r'>=|<=|<>|:=|[+\-*/=<>;:.,(){}]', None),  # Operadores e pontuação
    (r'\s+', None)                  # Espaços em branco
]

def validar_token(tipo, valor, linha):
    if tipo == TOKEN_DICT['integer']:
        if not valor.isdigit():
            return
        if int(valor) < 0 or int(valor) > 20000:
            print(f"[Erro] Inteiro fora do intervalo (0-20000) na linha {linha}.")
    elif tipo == TOKEN_DICT['real']:
        if not re.match(r'^\d+\.\d{1,2}$', valor):
            print(f"[Erro] Real com formato inválido na linha {linha}.")
        elif float(valor) < 0 or float(valor) > 20000:
            print(f"[Erro] Real fora do intervalo (0-20000) na linha {linha}.")
    elif tipo == TOKEN_DICT['vstring']:
        if len(valor.strip("'")) > 50:
            print(f"[Erro] String com mais de 50 caracteres na linha {linha}.")
    elif tipo == TOKEN_DICT['literal']:
        if not (valor.startswith('"') and valor.endswith('"')):
            print(f"[Erro] Literal mal formado na linha {linha}.")
    elif tipo == TOKEN_DICT['ident']:
        if not re.match(r'^[a-zA-Z]{1,10}$', valor):
            print(f"[Erro] Identificador inválido na linha {linha}.")

def tokenize(code):
    tokens = []
    linhas = code.splitlines()
    for numero_linha, linha in enumerate(linhas, start=1):
        pos = 0
        while pos < len(linha):
            match = None
            for pattern, tipo_hint in TOKEN_REGEX:
                regex = re.compile(pattern)
                match = regex.match(linha, pos)
                if match:
                    valor = match.group(0)
                    if tipo_hint:
                        token_tipo = TOKEN_DICT.get(valor, TOKEN_DICT.get(tipo_hint))
                        if tipo_hint not in ['real', 'integer', 'string', 'literal', 'ident']:
                            validar_token(token_tipo, valor, numero_linha)
                            tokens.append((valor, token_tipo, numero_linha))
                    else:
                        token_tipo = TOKEN_DICT.get(valor)
                        if token_tipo:
                            tokens.append((valor, token_tipo, numero_linha))
                    break
            if not match:
                print(f"[Erro] Token desconhecido na linha {numero_linha}: {linha[pos]}")
                pos += 1  # evita loop infinito em erro
            else:
                pos = match.end()
    return tokens

if __name__ == "__main__":
    with open('code.txt', 'r') as f:
        codigo_fonte = f.read()
    resultado = tokenize(codigo_fonte)
    for token in resultado:
        print(f"Token: {token[1]:<2} Lexema: {token[0]:<15} Linha: {token[2]}")