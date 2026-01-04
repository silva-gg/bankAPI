"""
Desafio 5: Calculando Média de Notas
Descrição: Calcular a média de três notas recebidas por entrada.
"""


def calcular_media(nota1: float, nota2: float, nota3: float) -> float:
    """
    Calcula a média aritmética de três notas.
    
    Args:
        nota1: Primeira nota
        nota2: Segunda nota
        nota3: Terceira nota
    
    Returns:
        Média das três notas
    """
    return (nota1 + nota2 + nota3) / 3


def calcular_media_lista(notas: list[float]) -> float:
    """
    Calcula a média aritmética de uma lista de notas.
    
    Args:
        notas: Lista de notas
    
    Returns:
        Média das notas
    
    Raises:
        ValueError: Se a lista estiver vazia
    """
    if not notas:
        raise ValueError("A lista de notas não pode estar vazia")
    return sum(notas) / len(notas)


def main():
    """Função principal para execução interativa."""
    print("=== Desafio 5: Calculando Média de Notas ===")
    nota1 = float(input("Digite a primeira nota: "))
    nota2 = float(input("Digite a segunda nota: "))
    nota3 = float(input("Digite a terceira nota: "))
    media = calcular_media(nota1, nota2, nota3)
    print(f"Média: {media:.2f}")


if __name__ == "__main__":
    main()
