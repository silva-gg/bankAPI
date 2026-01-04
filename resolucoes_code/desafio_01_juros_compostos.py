"""
Desafio 1: Calculadora de Juros Compostos

Descrição:
    Implementar uma calculadora de juros compostos para contas poupança.
    Juros compostos são calculados sobre o capital inicial mais os juros
    acumulados de períodos anteriores.

Fórmula:
    M = C * (1 + i)^t
    
    Onde:
    - M = Montante final
    - C = Capital inicial
    - i = Taxa de juros por período (em decimal)
    - t = Número de períodos

Requisitos:
    - Calcular montante final após aplicação de juros compostos
    - Calcular juros totais ganhos
    - Suportar diferentes períodos de capitalização
    - Validar entradas (valores positivos)

Exemplo de uso:
    >>> calcular_juros_compostos(1000.0, 0.05, 12)
    {'montante_final': 1795.86, 'juros_ganhos': 795.86, 'capital_inicial': 1000.0}
"""


def calcular_juros_compostos(
    capital_inicial: float,
    taxa_juros: float,
    periodos: int
) -> dict:
    """
    Calcula juros compostos para um capital inicial.
    
    Args:
        capital_inicial: Valor inicial do investimento (deve ser positivo)
        taxa_juros: Taxa de juros por período em decimal (ex: 0.05 para 5%)
        periodos: Número de períodos de capitalização (deve ser positivo)
        
    Returns:
        dict: Dicionário contendo:
            - montante_final: Valor final após juros
            - juros_ganhos: Total de juros acumulados
            - capital_inicial: Capital inicial investido
            
    Raises:
        ValueError: Se algum parâmetro for inválido (negativo ou zero)
        
    Examples:
        >>> resultado = calcular_juros_compostos(1000.0, 0.05, 12)
        >>> resultado['montante_final']
        1795.86
        
        >>> resultado = calcular_juros_compostos(5000.0, 0.02, 24)
        >>> resultado['juros_ganhos']
        3081.63
    """
    # Validação de entradas
    if capital_inicial <= 0:
        raise ValueError("Capital inicial deve ser maior que zero")
    
    if taxa_juros < 0:
        raise ValueError("Taxa de juros não pode ser negativa")
    
    if periodos < 0:
        raise ValueError("Número de períodos não pode ser negativo")
    
    # Caso especial: zero períodos
    if periodos == 0:
        return {
            'montante_final': capital_inicial,
            'juros_ganhos': 0.0,
            'capital_inicial': capital_inicial
        }
    
    # Cálculo de juros compostos: M = C * (1 + i)^t
    montante_final = capital_inicial * ((1 + taxa_juros) ** periodos)
    juros_ganhos = montante_final - capital_inicial
    
    # Arredondar para 2 casas decimais
    montante_final = round(montante_final, 2)
    juros_ganhos = round(juros_ganhos, 2)
    
    return {
        'montante_final': montante_final,
        'juros_ganhos': juros_ganhos,
        'capital_inicial': capital_inicial
    }


def calcular_juros_compostos_com_aportes(
    capital_inicial: float,
    taxa_juros: float,
    periodos: int,
    aporte_mensal: float
) -> dict:
    """
    Calcula juros compostos considerando aportes mensais regulares.
    
    Args:
        capital_inicial: Valor inicial do investimento
        taxa_juros: Taxa de juros por período em decimal
        periodos: Número de períodos
        aporte_mensal: Valor do aporte mensal
        
    Returns:
        dict: Dicionário com montante final, juros ganhos e total investido
        
    Examples:
        >>> resultado = calcular_juros_compostos_com_aportes(1000.0, 0.01, 12, 100.0)
        >>> resultado['montante_final'] > resultado['total_investido']
        True
    """
    # Validações
    if capital_inicial < 0:
        raise ValueError("Capital inicial não pode ser negativo")
    
    if taxa_juros < 0:
        raise ValueError("Taxa de juros não pode ser negativa")
    
    if periodos < 0:
        raise ValueError("Número de períodos não pode ser negativo")
    
    if aporte_mensal < 0:
        raise ValueError("Aporte mensal não pode ser negativo")
    
    # Inicializar valores
    montante = capital_inicial
    
    # Calcular montante com aportes mensais
    for _ in range(periodos):
        montante = (montante + aporte_mensal) * (1 + taxa_juros)
    
    total_investido = capital_inicial + (aporte_mensal * periodos)
    juros_ganhos = montante - total_investido
    
    # Arredondar
    montante = round(montante, 2)
    juros_ganhos = round(juros_ganhos, 2)
    total_investido = round(total_investido, 2)
    
    return {
        'montante_final': montante,
        'juros_ganhos': juros_ganhos,
        'total_investido': total_investido,
        'capital_inicial': capital_inicial
    }


def taxa_equivalente(
    taxa_atual: float,
    periodos_atual: int,
    periodos_desejado: int
) -> float:
    """
    Calcula a taxa equivalente para diferentes períodos de capitalização.
    
    Útil para converter taxas (ex: anual para mensal).
    
    Args:
        taxa_atual: Taxa de juros no período atual
        periodos_atual: Número de períodos da taxa atual em um ano
        periodos_desejado: Número de períodos desejados em um ano
        
    Returns:
        float: Taxa equivalente no novo período
        
    Examples:
        >>> # Converter taxa anual de 12% para mensal
        >>> taxa_mensal = taxa_equivalente(0.12, 1, 12)
        >>> round(taxa_mensal, 4)
        0.0095
    """
    if taxa_atual < 0:
        raise ValueError("Taxa não pode ser negativa")
    
    if periodos_atual <= 0 or periodos_desejado <= 0:
        raise ValueError("Períodos devem ser maiores que zero")
    
    # Fórmula: (1 + i_ano)^(1/n) - 1
    taxa_equivalente = ((1 + taxa_atual) ** (periodos_atual / periodos_desejado)) - 1
    
    return round(taxa_equivalente, 6)
