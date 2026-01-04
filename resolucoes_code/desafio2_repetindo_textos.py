"""
Desafio 2: Repetindo Textos
Descrição: Solicitar uma string e um número inteiro. Retornar a string repetida N vezes.
"""


def repetir_texto(texto: str, vezes: int) -> str:
    """
    Repete um texto N vezes.
    
    Args:
        texto: Texto a ser repetido
        vezes: Número de vezes que o texto será repetido
    
    Returns:
        String com o texto repetido N vezes
    """
    return texto * vezes


def main():
    """Função principal para execução interativa."""
    print("=== Desafio 2: Repetindo Textos ===")
    texto = input("Digite o texto: ")
    vezes = int(input("Digite quantas vezes deseja repetir: "))
    resultado = repetir_texto(texto, vezes)
    print(f"Resultado: {resultado}")


if __name__ == "__main__":
    main()
