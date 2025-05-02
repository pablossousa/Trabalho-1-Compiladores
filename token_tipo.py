from enum import IntEnum

class TokenTipo(IntEnum):
    # Operadores Aritméticos
    ADICAO = 1
    SUBTRACAO = 2
    MULTIPLICACAO = 3
    DIVISAO_REAL = 4
    MODULO = 5
    DIVISAO_INTEIRA = 6

    # Operadores Lógicos, Relacionais e Atribuição
    OU_LOGICO = 10
    E_LOGICO = 11
    NAO_LOGICO = 12
    IGUALDADE = 13
    IGUAL = 14
    DIFERENCA = 15
    MAIOR_IGUAL = 16
    MENOR_IGUAL = 17
    MAIOR = 18
    MENOR = 19
    ATRIBUICAO = 20

    # Palavras Reservadas
    PROGRAM = 30
    VAR = 31
    INTEGER = 32
    REAL = 33
    STRING_TYPE = 34
    BEGIN = 35
    END = 36
    FOR = 37
    TO = 38
    WHILE = 39
    DO = 40
    BREAK = 41
    CONTINUE = 42
    IF = 43
    ELSE = 44
    THEN = 45
    WRITE = 46
    WRITELN = 47
    READ = 48
    READLN = 49

    # Símbolos
    PONTO_VIRGULA = 60
    VIRGULA = 61
    PONTO = 62
    DOIS_PONTOS = 63
    ABRE_PARENTESES = 64
    FECHA_PARENTESES = 65

    # Outros
    IDENTIFICADOR = 70
    DECIMAL = 71
    FLUTUANTE = 72
    HEXADECIMAL = 73
    OCTAL = 74
    STRING = 75

    # Erro ou Desconhecido
    TOKEN_DESCONHECIDO = 99
