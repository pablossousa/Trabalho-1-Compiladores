from erro_lexico import gerar_erro_lexico
from token_tipo import TokenTipo

class AnalisadorNumeros:
    """Classe responsável por analisar números em diferentes formatos."""
    
    def identificar_numero(self, linha, pos_inicio, linha_num):
        pos_atual = pos_inicio
        tamanho_linha = len(linha)
        
        while pos_atual < tamanho_linha and linha[pos_atual].isdigit():
            pos_atual += 1
            
        if pos_atual < tamanho_linha and linha[pos_atual] == '.':
            return self._processar_numero_flutuante(linha, pos_inicio, pos_atual, linha_num)
        else:
            return self._verificar_numero_valido(linha, pos_inicio, pos_atual, TokenTipo.DECIMAL.value, linha_num)
    
    def _processar_numero_flutuante(self, linha, pos_inicio, pos_atual, linha_num):
        tamanho_linha = len(linha)
        pos_atual += 1
        
        if pos_atual == tamanho_linha or not linha[pos_atual].isdigit():
            gerar_erro_lexico("ponto decimal sem dígitos após o ponto", linha_num, linha, pos_atual-1)
            
        while pos_atual < tamanho_linha and linha[pos_atual].isdigit():
            pos_atual += 1
            
        if pos_atual < tamanho_linha and linha[pos_atual] in 'eE':
            pos_atual = self._processar_exponencial(linha, pos_atual, linha_num)
                
        return self._verificar_numero_valido(linha, pos_inicio, pos_atual, TokenTipo.FLUTUANTE.value, linha_num)
    
    def _processar_exponencial(self, linha, pos_atual, linha_num):
        tamanho_linha = len(linha)
        pos_atual += 1
        
        if pos_atual < tamanho_linha and linha[pos_atual] in '+-':
            pos_atual += 1
            
        if pos_atual >= tamanho_linha or not linha[pos_atual].isdigit():
            gerar_erro_lexico("esperado dígito após o expoente", linha_num, linha, pos_atual)
        
        while pos_atual < tamanho_linha and linha[pos_atual].isdigit():
            pos_atual += 1
            
        return pos_atual
    
    def _verificar_numero_valido(self, linha, pos_inicio, pos_atual, tipo, linha_num):
        tamanho_linha = len(linha)
        
        if pos_atual < tamanho_linha and (linha[pos_atual].isalpha() or linha[pos_atual] in '_$'):
            gerar_erro_lexico(f"caractere inválido '{linha[pos_atual]}' após número", linha_num, linha, pos_atual)
            
        if pos_atual < tamanho_linha and linha[pos_atual] == '.':
            gerar_erro_lexico("ponto extra não permitido em número", linha_num, linha, pos_atual)
            
        return linha[pos_inicio:pos_atual], tipo, pos_atual - pos_inicio
    
    def identificar_numero_hexadecimal(self, linha, pos_inicio, linha_num):
        if linha[pos_inicio] != '$':
            gerar_erro_lexico("esperado '$' para hexadecimal", linha_num, linha, pos_inicio)
            
        pos_atual = pos_inicio + 1
        tamanho_linha = len(linha)
        
        if pos_atual >= tamanho_linha or not (linha[pos_atual].isdigit() or linha[pos_atual].lower() in 'abcdef'):
            gerar_erro_lexico("esperado dígito hexadecimal após '$'", linha_num, linha, pos_atual)
            
        while pos_atual < tamanho_linha and (linha[pos_atual].isdigit() or linha[pos_atual].lower() in 'abcdef'):
            pos_atual += 1
            
        if pos_atual < tamanho_linha and (linha[pos_atual].isalpha() or linha[pos_atual] in '_$'):
            gerar_erro_lexico(f"caractere inválido '{linha[pos_atual]}' após número hexadecimal", linha_num, linha, pos_atual)
            
        return linha[pos_inicio:pos_atual], TokenTipo.HEXADECIMAL.value, pos_atual - pos_inicio
    
    def identificar_numero_octal(self, linha, pos_inicio, linha_num):
        if linha[pos_inicio] != '&':
            gerar_erro_lexico("esperado '&' para início de número octal", linha_num, linha, pos_inicio)
            
        pos_atual = pos_inicio + 1
        tamanho_linha = len(linha)
        
        if pos_atual >= tamanho_linha or linha[pos_atual].lower() != 'o':
            gerar_erro_lexico("esperado 'O' após '&' para número octal", linha_num, linha, pos_atual)
            
        pos_atual += 1
        
        if pos_atual >= tamanho_linha or linha[pos_atual] not in '01234567':
            gerar_erro_lexico("esperado dígito octal após '&O'", linha_num, linha, pos_atual)
            
        while pos_atual < tamanho_linha and linha[pos_atual] in '01234567':
            pos_atual += 1
            
        if pos_atual < tamanho_linha and (linha[pos_atual].isalpha() or linha[pos_atual] in '_$'):
            gerar_erro_lexico(f"caractere inválido '{linha[pos_atual]}' após número octal", linha_num, linha, pos_atual)
            
        return linha[pos_inicio:pos_atual], TokenTipo.OCTAL.value, pos_atual - pos_inicio
