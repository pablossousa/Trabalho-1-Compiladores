from tokens import TOKENS
from erro_lexico import gerar_erro_lexico
from tokenizador import Tokenizador
from numeros import AnalisadorNumeros
from token_tipo import TokenTipo

class AnalisadorLexico:
    """
    Classe principal do analisador léxico responsável por coordenar o processo
    de análise léxica e gerenciar os tokens encontrados.
    """
    
    def __init__(self, arquivo):
        """
        Inicializa o analisador léxico.
        
        Args:
            arquivo: Caminho para o arquivo a ser analisado
        """
        self.arquivo = arquivo
        self.tokens = []
        self.tokenizador = Tokenizador(TOKENS)
        self.analisador_numeros = AnalisadorNumeros()

    def fazer_analise_lexica(self):
        """
        Realiza a análise léxica completa do arquivo.
        
        Returns:
            Lista de tokens identificados
        """
        with open(self.arquivo, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
            self._processar_linhas(linhas)
        return self.tokens
    
    def _processar_linhas(self, linhas):
        """
        Processa todas as linhas do arquivo, gerenciando comentários e tokenização.
        
        Args:
            linhas: Lista de linhas do arquivo
        """
        nivel_comentario_bloco = 0
        linha_num_aberto = None
        coluna_aberto = None

        for linha_num, linha in enumerate(linhas):
            conteudo_processado = self._extrair_conteudo_sem_comentarios(
                linha, linha_num, nivel_comentario_bloco, linha_num_aberto, coluna_aberto)
            
            if conteudo_processado is None:
                nivel_comentario_bloco, linha_num_aberto, coluna_aberto = conteudo_processado
                continue
                
            nova_linha, nivel_comentario_bloco, linha_num_aberto, coluna_aberto = conteudo_processado
                
            if nova_linha.strip() and nivel_comentario_bloco == 0:
                tokens_linha = self.analise_linha(nova_linha, linha_num)
                self.tokens.extend(tokens_linha)
                
        if nivel_comentario_bloco > 0:
            gerar_erro_lexico("comentário de bloco '{...}' não fechado", 
                             linha_num_aberto, linhas[linha_num_aberto], coluna_aberto)
    
    def _extrair_conteudo_sem_comentarios(self, linha, linha_num, nivel_comentario_bloco, linha_num_aberto, coluna_aberto):
        """
        Extrai o conteúdo da linha ignorando comentários.
        """
        pos_atual = 0
        nova_linha = ''
        
        while pos_atual < len(linha):
            char = linha[pos_atual]

            if nivel_comentario_bloco > 0:
                if char == '{':
                    nivel_comentario_bloco += 1
                    if nivel_comentario_bloco == 1:
                        linha_num_aberto = linha_num
                        coluna_aberto = pos_atual
                elif char == '}':
                    nivel_comentario_bloco -= 1
                pos_atual += 1
                continue

            if char == '{':
                nivel_comentario_bloco += 1
                linha_num_aberto = linha_num
                coluna_aberto = pos_atual
                pos_atual += 1
                continue

            if linha[pos_atual:pos_atual+2] == '//':
                break

            nova_linha += char
            pos_atual += 1
            
        return nova_linha, nivel_comentario_bloco, linha_num_aberto, coluna_aberto
    
    def analise_linha(self, linha, linha_num):
        """
        Analisa uma linha e extrai todos os tokens.
        """
        tokens = []
        pos_atual = 0
        
        while pos_atual < len(linha):
            char = linha[pos_atual]
            coluna = pos_atual

            if char.isspace():
                pos_atual += 1
                continue

            if char in ['"', "'"]:
                lexema, tipo, avancar = self.tokenizador.identificar_string(linha, linha_num, pos_atual)
                tokens.append((tipo.value, lexema[1:-1], linha_num, coluna))
                pos_atual += avancar
                
            elif char.isalpha():
                lexema, avancar = self.tokenizador.identificar_identificador(linha, pos_atual, linha_num)
                tipo = TOKENS["PALAVRAS_RESERVADAS"].get(lexema.lower(), TokenTipo.IDENTIFICADOR)
                tokens.append((tipo.value, lexema, linha_num, coluna))
                pos_atual += avancar
                
            elif char in ":=<>":
                lexema, token, avancar = self.tokenizador.identificar_operador_composto(linha, linha_num, pos_atual)
                tokens.append((token.value, lexema, linha_num, coluna))
                pos_atual += avancar
                
            elif char in TOKENS["SIMBOLOS"]:
                token = TOKENS["SIMBOLOS"][char]
                tokens.append((token.value, char, linha_num, coluna))
                pos_atual += 1
                
            elif char in "+-*/" or linha[pos_atual:pos_atual+3].lower() in ["mod", "div"]:
                lexema, token, avancar = self.tokenizador.identificar_operador_aritmetico(linha, pos_atual)
                tokens.append((token.value, lexema, linha_num, coluna))
                pos_atual += avancar
                
            elif char == '&':
                lexema, tipo, avancar = self.analisador_numeros.identificar_numero_octal(linha, pos_atual, linha_num)
                tokens.append((tipo, lexema, linha_num, coluna))
                pos_atual += avancar
                
            elif char.isdigit():
                lexema, tipo, avancar = self.analisador_numeros.identificar_numero(linha, pos_atual, linha_num)
                tokens.append((tipo, lexema, linha_num, coluna))
                pos_atual += avancar
                
            elif char == '$':
                lexema, tipo, avancar = self.analisador_numeros.identificar_numero_hexadecimal(linha, pos_atual, linha_num)
                tokens.append((tipo, lexema, linha_num, coluna))
                pos_atual += avancar
                
            else:
                gerar_erro_lexico("Caractere inválido", linha_num, linha, coluna)
                pos_atual += 1

        return tokens
