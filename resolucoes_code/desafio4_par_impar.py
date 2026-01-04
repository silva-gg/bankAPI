"""
Desafio 4: Verificando Números Pares e Ímpares
Descrição: Receber um número inteiro e verificar se é par ou ímpar usando condicionais.
"""


def verificar_par_impar(numero: int) -> str:
    """
    Verifica se um número é par ou ímpar.
    
    Args:
        numero: Número inteiro a ser verificado
    
    Returns:
        "par" se o número for par, "ímpar" se for ímpar
    """
    if numero % 2 == 0:
        return "par"
    else:
        return "ímpar"


def eh_par(numero: int) -> bool:
    """
    Verifica se um número é par.
    
    Args:
        numero: Número inteiro a ser verificado
    
    Returns:
        True se o número for par, False caso contrário
    """
    return numero % 2 == 0


def main():
    """Função principal para execução interativa."""
    print("=== Desafio 4: Verificando Números Pares e Ímpares ===")
    numero = int(input("Digite um número inteiro: "))
    resultado = verificar_par_impar(numero)
    print(f"O número {numero} é {resultado}")


if __name__ == "__main__":
    main()
