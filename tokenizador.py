from erro_lexico import gerar_erro_lexico
from token_tipo import TokenTipo

class Tokenizador:
    """Classe responsável por identificar tokens específicos no código."""
    
    def __init__(self, tokens_config):
        self.tokens_config = tokens_config
    
    def identificar_operador_composto(self, linha, linha_num, pos_inicio):
        """
        Identifica operadores compostos como ==, :=, etc.
        """
        char = linha[pos_inicio]
        proximo = linha[pos_inicio+1] if pos_inicio + 1 < len(linha) else ""
        dois_chars = char + proximo

        if dois_chars == "==":
            return "==", TokenTipo.IGUALDADE, 2
        elif char == "=":
            return "=", TokenTipo.IGUAL, 1
        elif dois_chars in self.tokens_config["OPERADORES_LOGICOS_RELACIONAIS_ATRIBUICAO"]:
            return dois_chars, self.tokens_config["OPERADORES_LOGICOS_RELACIONAIS_ATRIBUICAO"][dois_chars], 2
        elif char in self.tokens_config["OPERADORES_LOGICOS_RELACIONAIS_ATRIBUICAO"]:
            return char, self.tokens_config["OPERADORES_LOGICOS_RELACIONAIS_ATRIBUICAO"][char], 1
        elif char == ":":
            if proximo == "=":
                return ":=", TokenTipo.ATRIBUICAO, 2
            return ":", TokenTipo.DOIS_PONTOS, 1

        gerar_erro_lexico(f"operador desconhecido: '{char}'", linha_num, linha, pos_inicio)

    def identificar_identificador(self, linha, pos_inicio, linha_num):
        """
        Identifica identificadores (variáveis, funções, etc.).
        """
        if not linha[pos_inicio].isalpha():
            gerar_erro_lexico("Identificador deve começar com letra", linha_num, linha, pos_inicio)

        pos_atual = pos_inicio + 1
        tamanho_linha = len(linha)

        while pos_atual < tamanho_linha:
            char = linha[pos_atual]
            if char.isalnum() or char == "_":
                if not char.isascii():
                    gerar_erro_lexico(f"Caractere não-ASCII '{char}' inválido em identificador", linha_num, linha, pos_atual)
                pos_atual += 1
            elif char in " +-*/=<>():;,.{}[]\t\n":
                break
            else:
                gerar_erro_lexico(f"Caractere inválido '{char}' no meio do identificador", linha_num, linha, pos_atual)

        return linha[pos_inicio:pos_atual], pos_atual - pos_inicio

    def identificar_operador_aritmetico(self, linha, pos_inicio):
        """
        Identifica operadores aritméticos (+, -, *, /, mod, div).
        """
        char = linha[pos_inicio]
        
        if char in self.tokens_config["OPERADORES_ARITMETICOS"]:
            return char, self.tokens_config["OPERADORES_ARITMETICOS"][char], 1

        for operador in ["mod", "div"]:
            operador_lower = operador.lower()
            if linha[pos_inicio:pos_inicio+len(operador)].lower() == operador_lower:
                pos_fim = pos_inicio + len(operador)
                if pos_fim == len(linha) or not (linha[pos_fim].isalnum() or linha[pos_fim] == "_"):
                    return operador_lower, self.tokens_config["OPERADORES_ARITMETICOS"][operador_lower], len(operador)

        return char, TokenTipo.TOKEN_DESCONHECIDO, 1
    
    def identificar_string(self, linha, linha_num, pos_inicio):
        """
        Identifica strings (texto entre aspas).
        """
        delimitador = linha[pos_inicio]
        coluna_inicio = pos_inicio
        pos_atual = pos_inicio + 1
        
        while pos_atual < len(linha):
            if linha[pos_atual] == delimitador:
                return linha[pos_inicio:pos_atual+1], TokenTipo.STRING, pos_atual+1-pos_inicio
            pos_atual += 1
            
        gerar_erro_lexico("string não fechada corretamente", linha_num, linha, coluna_inicio)
