"""
Testes para Desafio 2: Análise de Histórico de Transações
"""

import pytest
from resolucoes_code.desafio_02_analise_transacoes import (
    analisar_transacoes,
    analisar_por_mes,
    identificar_gastos_excessivos,
    calcular_tendencia
)


class TestAnalisarTransacoes:
    """Testes para análise básica de transações"""
    
    def test_analise_basica(self):
        """Testa análise básica com diferentes tipos de transações"""
        transacoes = [
            {'tipo': 'deposit', 'valor': 1000, 'data': '2024-01-15'},
            {'tipo': 'withdrawal', 'valor': 200, 'data': '2024-01-20'},
            {'tipo': 'deposit', 'valor': 500, 'data': '2024-01-25'}
        ]
        
        resultado = analisar_transacoes(transacoes)
        
        assert resultado['total_transacoes'] == 3
        assert resultado['total_depositos'] == 1500.0
        assert resultado['total_saques'] == 200.0
        assert resultado['num_depositos'] == 2
        assert resultado['num_saques'] == 1
    
    def test_lista_vazia(self):
        """Testa com lista vazia"""
        resultado = analisar_transacoes([])
        
        assert resultado['total_transacoes'] == 0
        assert resultado['total_depositos'] == 0.0
        assert resultado['maior_transacao'] is None
    
    def test_apenas_depositos(self):
        """Testa apenas com depósitos"""
        transacoes = [
            {'tipo': 'deposit', 'valor': 1000, 'data': '2024-01-15'},
            {'tipo': 'deposit', 'valor': 2000, 'data': '2024-01-20'}
        ]
        
        resultado = analisar_transacoes(transacoes)
        
        assert resultado['total_depositos'] == 3000.0
        assert resultado['total_saques'] == 0.0
        assert resultado['num_saques'] == 0
        assert resultado['media_deposito'] == 1500.0
    
    def test_apenas_saques(self):
        """Testa apenas com saques"""
        transacoes = [
            {'tipo': 'withdrawal', 'valor': 100, 'data': '2024-01-15'},
            {'tipo': 'withdrawal', 'valor': 200, 'data': '2024-01-20'},
            {'tipo': 'withdrawal', 'valor': 300, 'data': '2024-01-25'}
        ]
        
        resultado = analisar_transacoes(transacoes)
        
        assert resultado['total_saques'] == 600.0
        assert resultado['num_saques'] == 3
        assert resultado['media_saque'] == 200.0
        assert resultado['total_depositos'] == 0.0
    
    def test_maior_menor_transacao(self):
        """Testa identificação de maior e menor transação"""
        transacoes = [
            {'tipo': 'deposit', 'valor': 1000, 'data': '2024-01-15'},
            {'tipo': 'withdrawal', 'valor': 50, 'data': '2024-01-20'},
            {'tipo': 'deposit', 'valor': 5000, 'data': '2024-01-25'}
        ]
        
        resultado = analisar_transacoes(transacoes)
        
        assert resultado['maior_transacao'] == 5000.0
        assert resultado['menor_transacao'] == 50.0
    
    def test_tipos_portugues(self):
        """Testa com tipos em português"""
        transacoes = [
            {'tipo': 'deposito', 'valor': 1000, 'data': '2024-01-15'},
            {'tipo': 'saque', 'valor': 200, 'data': '2024-01-20'}
        ]
        
        resultado = analisar_transacoes(transacoes)
        
        assert resultado['total_depositos'] == 1000.0
        assert resultado['total_saques'] == 200.0
    
    def test_transferencias(self):
        """Testa contabilização de transferências"""
        transacoes = [
            {'tipo': 'transfer', 'valor': 500, 'data': '2024-01-15'},
            {'tipo': 'transferencia', 'valor': 300, 'data': '2024-01-20'}
        ]
        
        resultado = analisar_transacoes(transacoes)
        
        assert resultado['total_transferencias'] == 800.0
        assert resultado['num_transferencias'] == 2


class TestAnalisarPorMes:
    """Testes para análise mensal de transações"""
    
    def test_um_mes(self):
        """Testa análise de um único mês"""
        transacoes = [
            {'tipo': 'deposit', 'valor': 1000, 'data': '2024-01-15'},
            {'tipo': 'withdrawal', 'valor': 200, 'data': '2024-01-20'}
        ]
        
        resultado = analisar_por_mes(transacoes)
        
        assert '2024-01' in resultado
        assert resultado['2024-01']['depositos'] == 1000.0
        assert resultado['2024-01']['saques'] == 200.0
        assert resultado['2024-01']['saldo_liquido'] == 800.0
        assert resultado['2024-01']['num_transacoes'] == 2
    
    def test_multiplos_meses(self):
        """Testa análise de múltiplos meses"""
        transacoes = [
            {'tipo': 'deposit', 'valor': 1000, 'data': '2024-01-15'},
            {'tipo': 'withdrawal', 'valor': 200, 'data': '2024-01-20'},
            {'tipo': 'deposit', 'valor': 1500, 'data': '2024-02-10'},
            {'tipo': 'withdrawal', 'valor': 300, 'data': '2024-02-15'}
        ]
        
        resultado = analisar_por_mes(transacoes)
        
        assert len(resultado) == 2
        assert '2024-01' in resultado
        assert '2024-02' in resultado
        assert resultado['2024-02']['depositos'] == 1500.0
    
    def test_lista_vazia(self):
        """Testa com lista vazia"""
        resultado = analisar_por_mes([])
        
        assert resultado == {}
    
    def test_saldo_negativo(self):
        """Testa mês com saldo negativo"""
        transacoes = [
            {'tipo': 'deposit', 'valor': 100, 'data': '2024-01-15'},
            {'tipo': 'withdrawal', 'valor': 500, 'data': '2024-01-20'}
        ]
        
        resultado = analisar_por_mes(transacoes)
        
        assert resultado['2024-01']['saldo_liquido'] == -400.0
    
    def test_data_com_timezone(self):
        """Testa data com timezone"""
        transacoes = [
            {'tipo': 'deposit', 'valor': 1000, 'data': '2024-01-15T10:00:00Z'}
        ]
        
        resultado = analisar_por_mes(transacoes)
        
        assert '2024-01' in resultado


class TestIdentificarGastosExcessivos:
    """Testes para identificação de gastos excessivos"""
    
    def test_sem_gastos_excessivos(self):
        """Testa quando não há gastos excessivos"""
        transacoes = [
            {'tipo': 'withdrawal', 'valor': 100, 'data': '2024-01-15'},
            {'tipo': 'withdrawal', 'valor': 200, 'data': '2024-01-16'}
        ]
        
        resultado = identificar_gastos_excessivos(transacoes, 500)
        
        assert len(resultado) == 0
    
    def test_com_gastos_excessivos(self):
        """Testa identificação de gastos excessivos"""
        transacoes = [
            {'tipo': 'withdrawal', 'valor': 300, 'data': '2024-01-15'},
            {'tipo': 'withdrawal', 'valor': 400, 'data': '2024-01-15'},
            {'tipo': 'withdrawal', 'valor': 100, 'data': '2024-01-16'}
        ]
        
        resultado = identificar_gastos_excessivos(transacoes, 500)
        
        assert len(resultado) == 1
        assert resultado[0]['data'] == '2024-01-15'
        assert resultado[0]['total_gasto'] == 700.0
        assert resultado[0]['excesso'] == 200.0
    
    def test_multiplos_dias_excessivos(self):
        """Testa múltiplos dias com gastos excessivos"""
        transacoes = [
            {'tipo': 'withdrawal', 'valor': 600, 'data': '2024-01-15'},
            {'tipo': 'withdrawal', 'valor': 700, 'data': '2024-01-16'}
        ]
        
        resultado = identificar_gastos_excessivos(transacoes, 500)
        
        assert len(resultado) == 2
    
    def test_apenas_depositos_ignorados(self):
        """Testa que depósitos são ignorados"""
        transacoes = [
            {'tipo': 'deposit', 'valor': 10000, 'data': '2024-01-15'}
        ]
        
        resultado = identificar_gastos_excessivos(transacoes, 500)
        
        assert len(resultado) == 0
    
    def test_transferencias_contadas(self):
        """Testa que transferências são contadas como gastos"""
        transacoes = [
            {'tipo': 'transfer', 'valor': 600, 'data': '2024-01-15'}
        ]
        
        resultado = identificar_gastos_excessivos(transacoes, 500)
        
        assert len(resultado) == 1
        assert resultado[0]['total_gasto'] == 600.0
    
    def test_lista_vazia(self):
        """Testa com lista vazia"""
        resultado = identificar_gastos_excessivos([], 500)
        
        assert len(resultado) == 0
    
    def test_limite_zero(self):
        """Testa com limite zero"""
        transacoes = [
            {'tipo': 'withdrawal', 'valor': 100, 'data': '2024-01-15'}
        ]
        
        resultado = identificar_gastos_excessivos(transacoes, 0)
        
        assert len(resultado) == 0


class TestCalcularTendencia:
    """Testes para cálculo de tendências"""
    
    def test_tendencia_crescente(self):
        """Testa identificação de tendência crescente"""
        transacoes = [
            {'tipo': 'deposit', 'valor': 1000, 'data': '2024-01-15'},
            {'tipo': 'deposit', 'valor': 1500, 'data': '2024-02-15'},
            {'tipo': 'deposit', 'valor': 2000, 'data': '2024-03-15'}
        ]
        
        resultado = calcular_tendencia(transacoes)
        
        assert resultado['tendencia_depositos'] == 'crescente'
        assert resultado['variacao_depositos'] > 0
    
    def test_tendencia_decrescente(self):
        """Testa identificação de tendência decrescente"""
        transacoes = [
            {'tipo': 'withdrawal', 'valor': 1000, 'data': '2024-01-15'},
            {'tipo': 'withdrawal', 'valor': 500, 'data': '2024-02-15'}
        ]
        
        resultado = calcular_tendencia(transacoes)
        
        assert resultado['tendencia_saques'] == 'decrescente'
        assert resultado['variacao_saques'] < 0
    
    def test_tendencia_estavel(self):
        """Testa identificação de tendência estável"""
        transacoes = [
            {'tipo': 'deposit', 'valor': 1000, 'data': '2024-01-15'},
            {'tipo': 'deposit', 'valor': 1020, 'data': '2024-02-15'}
        ]
        
        resultado = calcular_tendencia(transacoes)
        
        # Variação de 2% é considerada estável
        assert resultado['tendencia_depositos'] == 'estavel'
    
    def test_poucas_transacoes(self):
        """Testa com poucas transações"""
        transacoes = [
            {'tipo': 'deposit', 'valor': 1000, 'data': '2024-01-15'}
        ]
        
        resultado = calcular_tendencia(transacoes)
        
        assert resultado['tendencia_depositos'] == 'estavel'
        assert resultado['variacao_depositos'] == 0.0
    
    def test_lista_vazia(self):
        """Testa com lista vazia"""
        resultado = calcular_tendencia([])
        
        assert resultado['tendencia_depositos'] == 'estavel'
        assert resultado['tendencia_saques'] == 'estavel'
