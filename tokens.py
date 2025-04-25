# Dicionário de tokens conforme seu PDF
TOKENS = {
    "OPERADORES_ARITMETICOS": {
        "+": "ADICAO",
        "-": "SUBTRACAO",
        "*": "MULTIPLICACAO",
        "/": "DIVISAO_REAL",
        "mod": "MODULO",
        "div": "DIVISAO_INTEIRA"
    },
    "OPERADORES_LOGICOS_RELACIONAIS_ATRIBUICAO": {
        "or": "OU_LOGICO",
        "and": "E_LOGICO",
        "not": "NAO_LOGICO",
        "==": "IGUALDADE",
        "<>": "DIFERENCA",
        ">=": "MAIOR_IGUAL",
        "<=": "MENOR_IGUAL",
        ">": "MAIOR",
        "<": "MENOR",
        ":=": "ATRIBUICAO"
    },
    "PALAVRAS_RESERVADAS": {
        "program": "PROGRAM",
        "var": "VAR",
        "integer": "INTEGER",
        "real": "REAL",
        "string": "STRING",
        "begin": "BEGIN",
        "end": "END",
        "for": "FOR",
        "to": "TO",
        "while": "WHILE",
        "do": "DO",
        "break": "BREAK",
        "continue": "CONTINUE",
        "if": "IF",
        "else": "ELSE",
        "then": "THEN",
        "write": "WRITE",
        "writeln": "WRITELN",
        "read": "READ",
        "readln": "READLN"
    },
    "SIMBOLOS": {
        ";": "PONTO_VIRGULA",
        ",": "VIRGULA",
        ".": "PONTO",
        ":": "DOIS_PONTOS",
        "(": "ABRE_PARENTESES",
        ")": "FECHA_PARENTESES"
    }
}

# Expressões regulares
REGEXES = {
    "STRING": r"(\"[^\"]*\"|'[^']*')",  
    "OCTAL": r"0[0-7]+",                
    "DECIMAL": r"[1-9][0-9]*",          
    "HEXA": r"0x[0-9A-F]+",             
    "FLUTUANTE": r"[0-9]+\.[0-9]*0",    
    "IDENTIFICADOR": r"\b[a-zA-Z_][a-zA-Z0-9_]*\b",  
    "COMENTARIO_LINHA": r"//.*",        
    "COMENTARIO_BLOCO": r"{[^}]*}"     
}

# # Expressões regulares
# REGEXES = {
#     "STRING": r"(\"[^\"]*\"|'[^']*')",  
# "DECIMAL": r"(0|[1-9][0-9]*)",      # Agora aceita '0' como decimal
# "OCTAL": r"0[0-7]*",                # Permite apenas '0' como octal válido também
          
#     "HEXA": r"0x[0-9A-F]+",             
#     "FLUTUANTE": r"[0-9]+\.[0-9]*0",    
#     "IDENTIFICADOR": r"\b[a-zA-Z_][a-zA-Z0-9_]*\b",  
#     "COMENTARIO_LINHA": r"//.*",        
#     "COMENTARIO_BLOCO": r"{[^}]*}"     
# }