"""
Desafio 6: Verificando Palíndromos
Descrição: Testar se uma palavra é palíndroma (igual de trás para frente).
"""


def eh_palindromo(texto: str) -> bool:
    """
    Verifica se um texto é um palíndromo.
    
    Um palíndromo é uma palavra ou frase que pode ser lida da mesma forma
    de trás para frente, ignorando espaços, pontuação e maiúsculas/minúsculas.
    
    Args:
        texto: Texto a ser verificado
    
    Returns:
        True se o texto for um palíndromo, False caso contrário
    """
    # Remove espaços e converte para minúsculas
    texto_limpo = texto.replace(" ", "").lower()
    # Compara o texto com sua versão invertida
    return texto_limpo == texto_limpo[::-1]


def eh_palindromo_simples(palavra: str) -> bool:
    """
    Verifica se uma palavra é um palíndromo (versão simples, case-sensitive).
    
    Args:
        palavra: Palavra a ser verificada
    
    Returns:
        True se a palavra for um palíndromo, False caso contrário
    """
    return palavra == palavra[::-1]


def main():
    """Função principal para execução interativa."""
    print("=== Desafio 6: Verificando Palíndromos ===")
    texto = input("Digite uma palavra ou frase: ")
    
    if eh_palindromo(texto):
        print(f'"{texto}" é um palíndromo!')
    else:
        print(f'"{texto}" não é um palíndromo.')


if __name__ == "__main__":
    main()
