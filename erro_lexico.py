class ErroLexico(Exception):
    """Exceção para erros léxicos."""
    pass

def gerar_erro_lexico(msg, linha_num, linha, coluna):
    """Gera um erro léxico formatado com indicador de posição."""
    ponteiro = " " * (coluna+1) + "^"
    raise ErroLexico(
        f'Erro léxico na linha {linha_num}, coluna {coluna}: {msg}\n'
        f' \033[91m"{linha.strip()}"\n {ponteiro}\033[0m'
    )