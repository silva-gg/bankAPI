"""
Desafio 3: Operações Matemáticas Simples
Descrição: Receber dois números do usuário e realizar uma operação matemática entre eles.
"""


def somar(num1: float, num2: float) -> float:
    """Retorna a soma de dois números."""
    return num1 + num2


def subtrair(num1: float, num2: float) -> float:
    """Retorna a subtração de dois números."""
    return num1 - num2


def multiplicar(num1: float, num2: float) -> float:
    """Retorna a multiplicação de dois números."""
    return num1 * num2


def dividir(num1: float, num2: float) -> float:
    """
    Retorna a divisão de dois números.
    
    Raises:
        ValueError: Se o divisor for zero
    """
    if num2 == 0:
        raise ValueError("Não é possível dividir por zero")
    return num1 / num2


def calcular(num1: float, num2: float, operacao: str) -> float:
    """
    Realiza uma operação matemática entre dois números.
    
    Args:
        num1: Primeiro número
        num2: Segundo número
        operacao: Operação a ser realizada (+, -, *, /)
    
    Returns:
        Resultado da operação
    
    Raises:
        ValueError: Se a operação for inválida
    """
    operacoes = {
        '+': somar,
        '-': subtrair,
        '*': multiplicar,
        '/': dividir
    }
    
    if operacao not in operacoes:
        raise ValueError(f"Operação inválida: {operacao}. Use +, -, * ou /")
    
    return operacoes[operacao](num1, num2)


def main():
    """Função principal para execução interativa."""
    print("=== Desafio 3: Operações Matemáticas Simples ===")
    num1 = float(input("Digite o primeiro número: "))
    num2 = float(input("Digite o segundo número: "))
    operacao = input("Digite a operação (+, -, *, /): ")
    
    try:
        resultado = calcular(num1, num2, operacao)
        print(f"Resultado: {num1} {operacao} {num2} = {resultado}")
    except ValueError as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    main()
