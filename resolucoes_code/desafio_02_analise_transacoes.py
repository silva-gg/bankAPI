"""
Desafio 2: Análise de Histórico de Transações

Descrição:
    Implementar funções para analisar históricos de transações bancárias,
    identificando padrões de gastos, receitas e comportamentos mensais.

Requisitos:
    - Analisar transações por tipo (depósito, saque, transferência)
    - Calcular totais por período (diário, mensal)
    - Identificar maior e menor transação
    - Calcular médias e estatísticas

Exemplo de uso:
    transacoes = [
        {'tipo': 'deposit', 'valor': 1000, 'data': '2024-01-15'},
        {'tipo': 'withdrawal', 'valor': 200, 'data': '2024-01-20'},
    ]
    analise = analisar_transacoes(transacoes)
"""

from datetime import datetime
from typing import List, Dict, Any
from collections import defaultdict


def analisar_transacoes(transacoes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Analisa uma lista de transações e retorna estatísticas.
    
    Args:
        transacoes: Lista de dicionários com transações
            Cada transação deve ter: 'tipo', 'valor', 'data'
            
    Returns:
        dict: Estatísticas das transações incluindo:
            - total_transacoes: Número total de transações
            - total_depositos: Soma de todos os depósitos
            - total_saques: Soma de todos os saques
            - total_transferencias: Soma de todas as transferências
            - num_depositos: Número de depósitos
            - num_saques: Número de saques
            - num_transferencias: Número de transferências
            - media_deposito: Média de valor dos depósitos
            - media_saque: Média de valor dos saques
            - maior_transacao: Maior transação
            - menor_transacao: Menor transação
            
    Examples:
        >>> transacoes = [
        ...     {'tipo': 'deposit', 'valor': 1000, 'data': '2024-01-15'},
        ...     {'tipo': 'withdrawal', 'valor': 200, 'data': '2024-01-20'}
        ... ]
        >>> resultado = analisar_transacoes(transacoes)
        >>> resultado['total_depositos']
        1000.0
    """
    if not transacoes:
        return {
            'total_transacoes': 0,
            'total_depositos': 0.0,
            'total_saques': 0.0,
            'total_transferencias': 0.0,
            'num_depositos': 0,
            'num_saques': 0,
            'num_transferencias': 0,
            'media_deposito': 0.0,
            'media_saque': 0.0,
            'maior_transacao': None,
            'menor_transacao': None
        }
    
    # Inicializar contadores
    depositos = []
    saques = []
    transferencias = []
    todas_transacoes = []
    
    # Processar transações
    for transacao in transacoes:
        tipo = transacao.get('tipo', '').lower()
        valor = float(transacao.get('valor', 0))
        
        todas_transacoes.append(transacao)
        
        if tipo in ['deposit', 'deposito']:
            depositos.append(valor)
        elif tipo in ['withdrawal', 'saque']:
            saques.append(valor)
        elif tipo in ['transfer', 'transferencia']:
            transferencias.append(valor)
    
    # Calcular estatísticas
    total_depositos = sum(depositos)
    total_saques = sum(saques)
    total_transferencias = sum(transferencias)
    
    media_deposito = total_depositos / len(depositos) if depositos else 0.0
    media_saque = total_saques / len(saques) if saques else 0.0
    
    # Encontrar maior e menor transação
    valores = depositos + saques + transferencias
    maior_transacao = max(valores) if valores else None
    menor_transacao = min(valores) if valores else None
    
    return {
        'total_transacoes': len(transacoes),
        'total_depositos': round(total_depositos, 2),
        'total_saques': round(total_saques, 2),
        'total_transferencias': round(total_transferencias, 2),
        'num_depositos': len(depositos),
        'num_saques': len(saques),
        'num_transferencias': len(transferencias),
        'media_deposito': round(media_deposito, 2),
        'media_saque': round(media_saque, 2),
        'maior_transacao': round(maior_transacao, 2) if maior_transacao else None,
        'menor_transacao': round(menor_transacao, 2) if menor_transacao else None
    }


def analisar_por_mes(transacoes: List[Dict[str, Any]]) -> Dict[str, Dict[str, float]]:
    """
    Agrupa e analisa transações por mês.
    
    Args:
        transacoes: Lista de transações com 'data' no formato 'YYYY-MM-DD'
        
    Returns:
        dict: Análise por mês (formato 'YYYY-MM')
            Cada mês contém: depositos, saques, transferencias, saldo_liquido
            
    Examples:
        >>> transacoes = [
        ...     {'tipo': 'deposit', 'valor': 1000, 'data': '2024-01-15'},
        ...     {'tipo': 'withdrawal', 'valor': 200, 'data': '2024-01-20'},
        ...     {'tipo': 'deposit', 'valor': 500, 'data': '2024-02-10'}
        ... ]
        >>> resultado = analisar_por_mes(transacoes)
        >>> resultado['2024-01']['depositos']
        1000.0
    """
    if not transacoes:
        return {}
    
    # Agrupar por mês
    por_mes = defaultdict(lambda: {
        'depositos': 0.0,
        'saques': 0.0,
        'transferencias': 0.0,
        'num_transacoes': 0
    })
    
    for transacao in transacoes:
        # Extrair mês da data
        data_str = transacao.get('data', '')
        try:
            data = datetime.fromisoformat(data_str.replace('Z', '+00:00'))
            mes = data.strftime('%Y-%m')
        except (ValueError, AttributeError):
            continue
        
        tipo = transacao.get('tipo', '').lower()
        valor = float(transacao.get('valor', 0))
        
        por_mes[mes]['num_transacoes'] += 1
        
        if tipo in ['deposit', 'deposito']:
            por_mes[mes]['depositos'] += valor
        elif tipo in ['withdrawal', 'saque']:
            por_mes[mes]['saques'] += valor
        elif tipo in ['transfer', 'transferencia']:
            por_mes[mes]['transferencias'] += valor
    
    # Calcular saldo líquido para cada mês
    resultado = {}
    for mes, dados in por_mes.items():
        saldo_liquido = dados['depositos'] - dados['saques'] - dados['transferencias']
        
        resultado[mes] = {
            'depositos': round(dados['depositos'], 2),
            'saques': round(dados['saques'], 2),
            'transferencias': round(dados['transferencias'], 2),
            'saldo_liquido': round(saldo_liquido, 2),
            'num_transacoes': dados['num_transacoes']
        }
    
    return resultado


def identificar_gastos_excessivos(
    transacoes: List[Dict[str, Any]],
    limite_diario: float
) -> List[Dict[str, Any]]:
    """
    Identifica dias com gastos acima do limite.
    
    Args:
        transacoes: Lista de transações
        limite_diario: Limite diário de gastos
        
    Returns:
        list: Dias com gastos excessivos com total gasto
        
    Examples:
        >>> transacoes = [
        ...     {'tipo': 'withdrawal', 'valor': 500, 'data': '2024-01-15'},
        ...     {'tipo': 'withdrawal', 'valor': 600, 'data': '2024-01-15'}
        ... ]
        >>> alertas = identificar_gastos_excessivos(transacoes, 1000)
        >>> len(alertas)
        1
    """
    if not transacoes or limite_diario <= 0:
        return []
    
    # Agrupar gastos por dia
    gastos_por_dia = defaultdict(float)
    
    for transacao in transacoes:
        tipo = transacao.get('tipo', '').lower()
        
        # Considerar apenas saques e transferências como gastos
        if tipo not in ['withdrawal', 'saque', 'transfer', 'transferencia']:
            continue
        
        data_str = transacao.get('data', '')
        try:
            data = datetime.fromisoformat(data_str.replace('Z', '+00:00'))
            dia = data.strftime('%Y-%m-%d')
        except (ValueError, AttributeError):
            continue
        
        valor = float(transacao.get('valor', 0))
        gastos_por_dia[dia] += valor
    
    # Identificar dias com gastos excessivos
    dias_excessivos = []
    for dia, total in gastos_por_dia.items():
        if total > limite_diario:
            dias_excessivos.append({
                'data': dia,
                'total_gasto': round(total, 2),
                'excesso': round(total - limite_diario, 2)
            })
    
    # Ordenar por data
    dias_excessivos.sort(key=lambda x: x['data'])
    
    return dias_excessivos


def calcular_tendencia(transacoes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calcula tendências de gastos e receitas ao longo do tempo.
    
    Args:
        transacoes: Lista de transações ordenadas por data
        
    Returns:
        dict: Informações de tendência incluindo:
            - tendencia_depositos: 'crescente', 'decrescente' ou 'estavel'
            - tendencia_saques: 'crescente', 'decrescente' ou 'estavel'
            - variacao_depositos: Variação percentual
            - variacao_saques: Variação percentual
            
    Examples:
        >>> transacoes = [...]  # transações ao longo de vários meses
        >>> tendencia = calcular_tendencia(transacoes)
        >>> tendencia['tendencia_depositos']
        'crescente'
    """
    if len(transacoes) < 2:
        return {
            'tendencia_depositos': 'estavel',
            'tendencia_saques': 'estavel',
            'variacao_depositos': 0.0,
            'variacao_saques': 0.0
        }
    
    # Analisar por mês
    por_mes = analisar_por_mes(transacoes)
    
    if not por_mes:
        return {
            'tendencia_depositos': 'estavel',
            'tendencia_saques': 'estavel',
            'variacao_depositos': 0.0,
            'variacao_saques': 0.0
        }
    
    # Ordenar meses
    meses_ordenados = sorted(por_mes.keys())
    
    if len(meses_ordenados) < 2:
        return {
            'tendencia_depositos': 'estavel',
            'tendencia_saques': 'estavel',
            'variacao_depositos': 0.0,
            'variacao_saques': 0.0
        }
    
    # Comparar primeiro e último mês
    primeiro_mes = por_mes[meses_ordenados[0]]
    ultimo_mes = por_mes[meses_ordenados[-1]]
    
    # Calcular variações
    variacao_depositos = 0.0
    if primeiro_mes['depositos'] > 0:
        variacao_depositos = ((ultimo_mes['depositos'] - primeiro_mes['depositos']) / 
                             primeiro_mes['depositos']) * 100
    
    variacao_saques = 0.0
    if primeiro_mes['saques'] > 0:
        variacao_saques = ((ultimo_mes['saques'] - primeiro_mes['saques']) / 
                          primeiro_mes['saques']) * 100
    
    # Determinar tendências
    def determinar_tendencia(variacao: float) -> str:
        if variacao > 5:
            return 'crescente'
        elif variacao < -5:
            return 'decrescente'
        else:
            return 'estavel'
    
    return {
        'tendencia_depositos': determinar_tendencia(variacao_depositos),
        'tendencia_saques': determinar_tendencia(variacao_saques),
        'variacao_depositos': round(variacao_depositos, 2),
        'variacao_saques': round(variacao_saques, 2)
    }
