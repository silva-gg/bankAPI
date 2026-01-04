"""
Testes para Desafio 1: Calculadora de Juros Compostos
"""

import pytest
from resolucoes_code.desafio_01_juros_compostos import (
    calcular_juros_compostos,
    calcular_juros_compostos_com_aportes,
    taxa_equivalente
)


class TestCalcularJurosCompostos:
    """Testes para a função calcular_juros_compostos"""
    
    def test_juros_basico(self):
        """Testa cálculo básico de juros compostos"""
        resultado = calcular_juros_compostos(1000.0, 0.05, 12)
        
        assert resultado['capital_inicial'] == 1000.0
        assert resultado['montante_final'] == 1795.86
        assert resultado['juros_ganhos'] == 795.86
    
    def test_sem_juros(self):
        """Testa com taxa de juros zero"""
        resultado = calcular_juros_compostos(1000.0, 0.0, 12)
        
        assert resultado['montante_final'] == 1000.0
        assert resultado['juros_ganhos'] == 0.0
    
    def test_zero_periodos(self):
        """Testa com zero períodos"""
        resultado = calcular_juros_compostos(1000.0, 0.05, 0)
        
        assert resultado['montante_final'] == 1000.0
        assert resultado['juros_ganhos'] == 0.0
    
    def test_um_periodo(self):
        """Testa com um período apenas"""
        resultado = calcular_juros_compostos(1000.0, 0.10, 1)
        
        assert resultado['montante_final'] == 1100.0
        assert resultado['juros_ganhos'] == 100.0
    
    def test_valores_grandes(self):
        """Testa com valores maiores"""
        resultado = calcular_juros_compostos(50000.0, 0.08, 24)
        
        assert resultado['capital_inicial'] == 50000.0
        assert resultado['montante_final'] > 50000.0
        assert resultado['juros_ganhos'] > 0
    
    def test_capital_negativo_erro(self):
        """Testa erro com capital negativo"""
        with pytest.raises(ValueError, match="Capital inicial deve ser maior que zero"):
            calcular_juros_compostos(-1000.0, 0.05, 12)
    
    def test_capital_zero_erro(self):
        """Testa erro com capital zero"""
        with pytest.raises(ValueError, match="Capital inicial deve ser maior que zero"):
            calcular_juros_compostos(0.0, 0.05, 12)
    
    def test_taxa_negativa_erro(self):
        """Testa erro com taxa negativa"""
        with pytest.raises(ValueError, match="Taxa de juros não pode ser negativa"):
            calcular_juros_compostos(1000.0, -0.05, 12)
    
    def test_periodos_negativos_erro(self):
        """Testa erro com períodos negativos"""
        with pytest.raises(ValueError, match="Número de períodos não pode ser negativo"):
            calcular_juros_compostos(1000.0, 0.05, -12)
    
    def test_arredondamento(self):
        """Testa se os valores são arredondados corretamente"""
        resultado = calcular_juros_compostos(1234.56, 0.0345, 7)
        
        # Verifica que tem no máximo 2 casas decimais
        assert len(str(resultado['montante_final']).split('.')[-1]) <= 2
        assert len(str(resultado['juros_ganhos']).split('.')[-1]) <= 2
    
    def test_taxa_alta_longo_prazo(self):
        """Testa com taxa alta e muitos períodos"""
        resultado = calcular_juros_compostos(1000.0, 0.10, 36)
        
        # Com 10% ao mês por 36 meses, o montante deve ser muito maior
        assert resultado['montante_final'] > 10000.0
        assert resultado['juros_ganhos'] > 9000.0


class TestCalcularJurosCompostosComAportes:
    """Testes para cálculo com aportes mensais"""
    
    def test_com_aportes_basico(self):
        """Testa cálculo com aportes mensais"""
        resultado = calcular_juros_compostos_com_aportes(1000.0, 0.01, 12, 100.0)
        
        assert resultado['capital_inicial'] == 1000.0
        assert resultado['total_investido'] == 2200.0  # 1000 + (100 * 12)
        assert resultado['montante_final'] > resultado['total_investido']
        assert resultado['juros_ganhos'] > 0
    
    def test_sem_capital_inicial(self):
        """Testa apenas com aportes mensais"""
        resultado = calcular_juros_compostos_com_aportes(0.0, 0.01, 12, 100.0)
        
        assert resultado['capital_inicial'] == 0.0
        assert resultado['total_investido'] == 1200.0
        assert resultado['montante_final'] > 1200.0
    
    def test_sem_aportes(self):
        """Testa sem aportes mensais (apenas capital inicial)"""
        resultado = calcular_juros_compostos_com_aportes(1000.0, 0.01, 12, 0.0)
        
        # Deve ser igual ao cálculo simples
        resultado_simples = calcular_juros_compostos(1000.0, 0.01, 12)
        
        assert abs(resultado['montante_final'] - resultado_simples['montante_final']) < 0.01
    
    def test_aporte_negativo_erro(self):
        """Testa erro com aporte negativo"""
        with pytest.raises(ValueError, match="Aporte mensal não pode ser negativo"):
            calcular_juros_compostos_com_aportes(1000.0, 0.01, 12, -100.0)
    
    def test_capital_negativo_erro(self):
        """Testa erro com capital negativo"""
        with pytest.raises(ValueError, match="Capital inicial não pode ser negativo"):
            calcular_juros_compostos_com_aportes(-1000.0, 0.01, 12, 100.0)
    
    def test_valores_realisticos(self):
        """Testa com valores realistas de investimento"""
        # Investir R$ 5000 inicial + R$ 500/mês por 2 anos a 0.8% a.m.
        resultado = calcular_juros_compostos_com_aportes(5000.0, 0.008, 24, 500.0)
        
        assert resultado['capital_inicial'] == 5000.0
        assert resultado['total_investido'] == 17000.0  # 5000 + (500 * 24)
        assert resultado['montante_final'] > 17000.0
        assert resultado['juros_ganhos'] > 1000.0


class TestTaxaEquivalente:
    """Testes para conversão de taxas equivalentes"""
    
    def test_anual_para_mensal(self):
        """Testa conversão de taxa anual para mensal"""
        # Taxa anual de 12% para mensal
        taxa_mensal = taxa_equivalente(0.12, 1, 12)
        
        # A taxa mensal deve ser aproximadamente 0.95%
        assert 0.009 < taxa_mensal < 0.010
    
    def test_mensal_para_anual(self):
        """Testa conversão de taxa mensal para anual"""
        # Taxa mensal de 1% para anual
        taxa_anual = taxa_equivalente(0.01, 12, 1)
        
        # A taxa anual deve ser aproximadamente 12.68%
        assert 0.12 < taxa_anual < 0.13
    
    def test_mesma_taxa(self):
        """Testa quando períodos são iguais"""
        taxa = taxa_equivalente(0.10, 12, 12)
        
        assert abs(taxa - 0.10) < 0.0001
    
    def test_taxa_zero(self):
        """Testa com taxa zero"""
        taxa = taxa_equivalente(0.0, 12, 1)
        
        assert taxa == 0.0
    
    def test_taxa_negativa_erro(self):
        """Testa erro com taxa negativa"""
        with pytest.raises(ValueError, match="Taxa não pode ser negativa"):
            taxa_equivalente(-0.10, 12, 1)
    
    def test_periodos_invalidos_erro(self):
        """Testa erro com períodos inválidos"""
        with pytest.raises(ValueError, match="Períodos devem ser maiores que zero"):
            taxa_equivalente(0.10, 0, 12)
        
        with pytest.raises(ValueError, match="Períodos devem ser maiores que zero"):
            taxa_equivalente(0.10, 12, -1)
    
    def test_semestral_para_mensal(self):
        """Testa conversão de taxa semestral para mensal"""
        # Taxa semestral de 6% para mensal
        taxa_mensal = taxa_equivalente(0.06, 2, 12)
        
        # Deve ser aproximadamente 1% ao mês
        assert 0.009 < taxa_mensal < 0.011
