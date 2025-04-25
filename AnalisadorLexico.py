import re
import sys
from tokens import TOKENS, REGEXES

class ErroLexico(Exception):
    """Exceção para erros léxicos."""
    pass

def erro_lexico(msg, linha_num, linha, coluna):
    raise ErroLexico(f'Erro léxico na linha {linha_num}, coluna {coluna}: {msg}\n \033[91m"{linha.replace("\n","").strip()}"\033[0m')

class AnalisadorLexico:
    def __init__(self, arquivo):
        self.arquivo = arquivo
        self.tokens = []

    def fazer_analise_lexica(self):
        with open(self.arquivo, 'r', encoding='utf-8') as f:
            dentro_comentario_bloco = False
            for linha_num, linha in enumerate(f):
                if dentro_comentario_bloco:
                    if "}" in linha:
                        dentro_comentario_bloco = False
                    continue
                if "{" in linha and "}" not in linha:
                    dentro_comentario_bloco = True
                    continue
                if re.search(REGEXES["COMENTARIO_LINHA"], linha):
                    linha = re.sub(REGEXES["COMENTARIO_LINHA"], "", linha)

                tokens_linha = self.analise_linha(linha, linha_num)
                self.tokens += tokens_linha
        return self.tokens
    
    def analise_linha(self, linha, linha_num):
        tokens = []
        i = 0
        coluna = 0
        while i < len(linha):
            char = linha[i]

            # Ignorar espaços e tabulações
            if char.isspace():
                i += 1
                coluna += 1
                continue

            # Identificar string (entre aspas)
            if char in ['"', "'"]:
                lexema, tipo, avancar = self.identificar_string(linha, linha_num, i)
                if isinstance(avancar, int):
                    tokens.append((tipo, lexema, linha_num, coluna))
                else:
                    tokens.append((avancar, lexema, linha_num, coluna))
                i += avancar
                coluna += avancar
                continue

            # Símbolos compostos e simples (AFD)
            if char in ":=<>":
                lexema, token, avancar = self.identificar_operador_composto(linha, i)
                tokens.append((token, lexema, linha_num, coluna))
                i += avancar
                coluna += avancar
                continue

            if char in TOKENS["SIMBOLOS"]:
                token = TOKENS["SIMBOLOS"][char]
                tokens.append((token, char, linha_num, coluna))
                i += 1
                coluna += 1
                continue

            if char in "+-*/" or linha[i:i+3] in ["mod", "div"]:
                lexema, token, avancar = self.identificar_operador_aritmetico(linha, i)
                tokens.append((token, lexema, linha_num, coluna))
                i += avancar
                coluna += avancar
                continue

            # Número
            if char.isdigit():
                lexema, tipo, avancar = self.identificar_numero(linha, i, linha_num)
                tokens.append((tipo, lexema, linha_num, coluna))
                i += avancar
                coluna += avancar
                continue

            # Identificador ou palavra reservada
            if char.isalpha() or char == "_":
                lexema, avancar = self.identificar_identificador(linha, i)
                tipo = TOKENS["PALAVRAS_RESERVADAS"].get(lexema, "IDENTIFICADOR")
                tokens.append((tipo, lexema, linha_num, coluna))
                i += avancar
                coluna += avancar
                continue

            # Se não casou com nada, é desconhecido
            tokens.append(("TOKEN_DESCONHECIDO", char, linha_num, coluna))
            i += 1
            coluna += 1

        return tokens

    def identificar_operador_composto(self, linha, i):
        dois_chars = linha[i:i+2]
        if dois_chars in TOKENS["OPERADORES_LOGICOS_RELACIONAIS_ATRIBUICAO"]:
            return dois_chars, TOKENS["OPERADORES_LOGICOS_RELACIONAIS_ATRIBUICAO"][dois_chars], 2
        if linha[i] in TOKENS["OPERADORES_LOGICOS_RELACIONAIS_ATRIBUICAO"]:
            return linha[i], TOKENS["OPERADORES_LOGICOS_RELACIONAIS_ATRIBUICAO"][linha[i]], 1
        if linha[i] in TOKENS["SIMBOLOS"]:
            return linha[i], TOKENS["SIMBOLOS"][linha[i]], 1
        return linha[i], "ERRO: TOKEN_DESCONHECIDO", 1

    def identificar_numero(self, linha, i, linha_num):
        j = i
        while j < len(linha) and linha[j].isdigit():
            j += 1

        # Possível número flutuante
        if j < len(linha) and linha[j] == ".":
            j += 1
            while j < len(linha) and linha[j].isdigit():
                j += 1
            lexema = linha[i:j]
            if re.fullmatch(REGEXES["FLUTUANTE"], lexema):
                return lexema, "FLUTUANTE", j - i
            else:
                erro_lexico(f"número malformado: '{lexema}'", linha_num, linha, i)

        # Não tem ponto: pode ser decimal, octal ou hexa
        else:
            lexema = linha[i:j]
            if re.fullmatch(REGEXES["HEXA"], lexema):
                return lexema, "HEXADECIMAL", j - i
            if re.fullmatch(REGEXES["OCTAL"], lexema):
                return lexema, "OCTAL", j - i
            if re.fullmatch(REGEXES["DECIMAL"], lexema):
                return lexema, "DECIMAL", j - i
            else:
                erro_lexico(f"número malformado: '{lexema}'", linha_num, linha, i)

    def identificar_identificador(self, linha, i):
        j = i
        while j < len(linha) and (linha[j].isalnum() or linha[j] == "_"):
            j += 1
        return linha[i:j], j - i
    
    def identificar_operador_aritmetico(self, linha, i):
        if linha[i] in TOKENS["OPERADORES_ARITMETICOS"]:
            return linha[i], TOKENS["OPERADORES_ARITMETICOS"][linha[i]], 1

        for palavra in ["mod", "div"]:
            if linha[i:i+len(palavra)] == palavra:
                fim = i + len(palavra)
                if fim == len(linha) or not linha[fim].isalnum():
                    return palavra, TOKENS["OPERADORES_ARITMETICOS"][palavra], len(palavra)

        return linha[i], "TOKEN_DESCONHECIDO", 1
    
    def identificar_string(self, linha, linha_num, i):
        if linha[i] != '"':
            erro_lexico("uso de aspas simples não permitido", linha_num, linha, i)

        delimitador = linha[i]
        coluna_inicio = i  # salva a posição inicial do "
        lexema = delimitador
        i += 1

        while i < len(linha):
            char = linha[i]
            lexema += char
            if char == delimitador:
                i += 1
                return lexema, "STRING", len(lexema)
            i += 1

        erro_lexico("string não fechada corretamente", linha_num, linha, coluna_inicio)