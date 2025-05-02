from token_tipo import TokenTipo

TOKENS = {
    "OPERADORES_ARITMETICOS": {
        "+": TokenTipo.ADICAO,
        "-": TokenTipo.SUBTRACAO,
        "*": TokenTipo.MULTIPLICACAO,
        "/": TokenTipo.DIVISAO_REAL,
        "mod": TokenTipo.MODULO,
        "div": TokenTipo.DIVISAO_INTEIRA
    },
    "OPERADORES_LOGICOS_RELACIONAIS_ATRIBUICAO": {
        "or": TokenTipo.OU_LOGICO,
        "and": TokenTipo.E_LOGICO,
        "not": TokenTipo.NAO_LOGICO,
        "==": TokenTipo.IGUALDADE,
        "=": TokenTipo.IGUAL,
        "<>": TokenTipo.DIFERENCA,
        ">=": TokenTipo.MAIOR_IGUAL,
        "<=": TokenTipo.MENOR_IGUAL,
        ">": TokenTipo.MAIOR,
        "<": TokenTipo.MENOR,
        ":=": TokenTipo.ATRIBUICAO
    },
    "PALAVRAS_RESERVADAS": {
        "program": TokenTipo.PROGRAM,
        "var": TokenTipo.VAR,
        "integer": TokenTipo.INTEGER,
        "real": TokenTipo.REAL,
        "string": TokenTipo.STRING_TYPE,
        "begin": TokenTipo.BEGIN,
        "end": TokenTipo.END,
        "for": TokenTipo.FOR,
        "to": TokenTipo.TO,
        "while": TokenTipo.WHILE,
        "do": TokenTipo.DO,
        "break": TokenTipo.BREAK,
        "continue": TokenTipo.CONTINUE,
        "if": TokenTipo.IF,
        "else": TokenTipo.ELSE,
        "then": TokenTipo.THEN,
        "write": TokenTipo.WRITE,
        "writeln": TokenTipo.WRITELN,
        "read": TokenTipo.READ,
        "readln": TokenTipo.READLN
    },
    "SIMBOLOS": {
        ";": TokenTipo.PONTO_VIRGULA,
        ",": TokenTipo.VIRGULA,
        ".": TokenTipo.PONTO,
        ":": TokenTipo.DOIS_PONTOS,
        "(": TokenTipo.ABRE_PARENTESES,
        ")": TokenTipo.FECHA_PARENTESES
    }
}
