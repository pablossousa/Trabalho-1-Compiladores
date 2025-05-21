from tokens import TOKENS
from erro_lexico import gerar_erro_lexico
from tokenizador import Tokenizador
from numeros import AnalisadorNumeros
from token_tipo import TokenTipo
import sys

aspas_simples_duplas = {'"', "'"}
simbolos_composto = {':', '=', '<', '>'}
simbolos_operadores = {'+', '-', '*', '/'}
conjunto_divisores = {"mod", "div"}

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
            linhas = f.readlines() # lista de strings
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
            # if conteudo_processado is not None:
            nova_linha, nivel_comentario_bloco, linha_num_aberto, coluna_aberto = self._extrair_conteudo_sem_comentarios(linha, linha_num, nivel_comentario_bloco, 
            linha_num_aberto, coluna_aberto) # removendo comentario de cada linha

            if nova_linha.strip() and nivel_comentario_bloco == 0:
                tokens_linha = self.analise_linha(nova_linha, linha_num)
                self.tokens.extend(tokens_linha)

        if nivel_comentario_bloco > 0:
            gerar_erro_lexico("comentário de bloco '{...}' não fechado", 
                            linha_num_aberto, linhas[linha_num_aberto], coluna_aberto)
    
    def _extrair_conteudo_sem_comentarios(self, linha, linha_num, nivel_comentario_bloco, linha_num_aberto, coluna_aberto):  
        """
        Extrai o conteúdo da linha ignorando comentários, mas mantendo posições de coluna corretas.
        Substitui comentários por espaços para preservar os índices.
        """
        pos_atual = 0
        nova_linha = ''

        while pos_atual < len(linha):
            char = linha[pos_atual]

            # quando ja tiver uma chave aberta({)
            if nivel_comentario_bloco > 0:
                if char == '{':
                    nivel_comentario_bloco += 1
                elif char == '}':
                    nivel_comentario_bloco -= 1
                nova_linha += ' '
                pos_atual += 1
            # primeira ocorrencia de chave entra aqui
            elif char == '{':
                nivel_comentario_bloco += 1
                linha_num_aberto = linha_num
                coluna_aberto = pos_atual
                nova_linha += ' '
                pos_atual += 1

            # apaga linha com //
            elif linha[pos_atual:pos_atual+2] == '//':
                nova_linha += ' ' * (len(linha) - pos_atual)
                pos_atual = len(linha)  # força saída do while

            else:
                nova_linha += char
                pos_atual += 1

        return nova_linha, nivel_comentario_bloco, linha_num_aberto, coluna_aberto
    
    # recebe a linha tratada dos espaços junto com o numero da linha 
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

            elif char in aspas_simples_duplas: # checa aspas simples ou duplas
                lexema, tipo, avancar = self.tokenizador.identificar_string(linha, linha_num, pos_atual)
                tokens.append((tipo.value, lexema[1:-1], linha_num, coluna))
                pos_atual += avancar
                
            elif char.isalpha(): # checa identificador, palavras reservdas, operadores que são strings etc (string em geral)
                tipo, lexema, avancar = self.tokenizador.identificar_identificador(linha, pos_atual, linha_num)
                tokens.append((tipo.value, lexema, linha_num, coluna))
                pos_atual += avancar
                
            elif char in simbolos_composto: # simbolos_composto = {':', '=', '<', '>'}
                lexema, token, avancar = self.tokenizador.identificar_operador_composto(linha, linha_num, pos_atual)
                tokens.append((token.value, lexema, linha_num, coluna))
                pos_atual += avancar
                
            elif char in TOKENS["SIMBOLOS"]:
                token = TOKENS["SIMBOLOS"][char]
                tokens.append((token.value, char, linha_num, coluna))
                pos_atual += 1
                
            elif char in simbolos_operadores: # simbolos operadores {'+', '-', '*', '/'} 
                lexema, token, avancar = self.tokenizador.identificar_operador_aritmetico(linha, pos_atual)
                tokens.append((token.value, lexema, linha_num, coluna))
                pos_atual += avancar
                
            elif char.isdigit():
                # if linha[pos_atual + 1].isdigit():

                    lexema, tipo, avancar = self.analisador_numeros.identificar_numero(linha, pos_atual, linha_num)
                    tokens.append((tipo, lexema, linha_num, coluna))
                    pos_atual += avancar
                # else:
                #     lexema = char
                #     tokens.append(( TokenTipo.DECIMAL.value, lexema, linha_num, coluna))
                #     pos_atual += avancar
                
            else:
                gerar_erro_lexico("Caractere inválido", linha_num, linha, coluna)
                pos_atual += 1
                

        return tokens
