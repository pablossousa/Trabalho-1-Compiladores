import sys
from analisador_lexico import AnalisadorLexico
from erro_lexico import ErroLexico
from token_tipo import TokenTipo

def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <arquivo>")
        return
        
    arquivo = sys.argv[1]
    
    try:
        analisador = AnalisadorLexico(arquivo)
        tokens = analisador.fazer_analise_lexica()
        
        print("\nTokens encontrados:")
        print("-" * 60)
        print(f"{'TIPO':<20} {'LEXEMA':<20} {'LINHA':<5} {'COLUNA':<5}")
        print("-" * 60)
        
        for tipo, lexema, linha, coluna in tokens:
            tipo_nome = TokenTipo(tipo).name if tipo in TokenTipo._value2member_map_ else tipo
            print(f"{tipo_nome:<20} {lexema:<20} {linha:<5} {coluna:<5}")
            
        print("-" * 60)
        print(f"Total de tokens: {len(tokens)}")
        
    except ErroLexico as e:
        print(f"Erro: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

if __name__ == "__main__":
    main()
