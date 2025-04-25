from AnalisadorLexico import AnalisadorLexico, ErroLexico
import sys

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python main.py <arquivo.pas>")
    else:
        try:
            analisador = AnalisadorLexico(sys.argv[1])
            for token in analisador.fazer_analise_lexica():
                print(token)
        except ErroLexico as e:
            print(e)  # imprime o erro e ENCERRA por si só