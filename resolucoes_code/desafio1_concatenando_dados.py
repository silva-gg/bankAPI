"""
Desafio 1: Concatenando Dados
Descrição: Receber dois dados do usuário e concatenar em uma única string.
"""


def concatenar_dados(dado1: str, dado2: str) -> str:
    """
    Concatena dois dados em uma única string.
    
    Args:
        dado1: Primeiro dado a ser concatenado
        dado2: Segundo dado a ser concatenado
    
    Returns:
        String concatenada dos dois dados
    """
    return f"{dado1}{dado2}"


def main():
    """Função principal para execução interativa."""
    print("=== Desafio 1: Concatenando Dados ===")
    dado1 = input("Digite o primeiro dado: ")
    dado2 = input("Digite o segundo dado: ")
    resultado = concatenar_dados(dado1, dado2)
    print(f"Resultado: {resultado}")


if __name__ == "__main__":
    main()
