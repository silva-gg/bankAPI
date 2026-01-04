"""
Testes para as resoluções dos desafios Python.

Este módulo contém testes automatizados para validar as soluções
dos 6 desafios de programação.
"""

import pytest
from resolucoes_code.desafio1_concatenando_dados import concatenar_dados
from resolucoes_code.desafio2_repetindo_textos import repetir_texto
from resolucoes_code.desafio3_operacoes_matematicas import (
    calcular, somar, subtrair, multiplicar, dividir
)
from resolucoes_code.desafio4_par_impar import verificar_par_impar, eh_par
from resolucoes_code.desafio5_media_notas import calcular_media, calcular_media_lista
from resolucoes_code.desafio6_palindromo import eh_palindromo, eh_palindromo_simples


class TestDesafio1ConcatenandoDados:
    """Testes para o Desafio 1: Concatenando Dados."""
    
    def test_concatenar_strings_simples(self):
        """Testa concatenação de strings simples."""
        resultado = concatenar_dados("Olá", " Mundo")
        assert resultado == "Olá Mundo"
    
    def test_concatenar_numeros_como_string(self):
        """Testa concatenação de números convertidos para string."""
        resultado = concatenar_dados("123", "456")
        assert resultado == "123456"
    
    def test_concatenar_string_vazia(self):
        """Testa concatenação com string vazia."""
        resultado = concatenar_dados("Python", "")
        assert resultado == "Python"
    
    def test_concatenar_duas_strings_vazias(self):
        """Testa concatenação de duas strings vazias."""
        resultado = concatenar_dados("", "")
        assert resultado == ""
    
    def test_concatenar_com_espacos(self):
        """Testa concatenação de strings com espaços."""
        resultado = concatenar_dados("Hello ", "World!")
        assert resultado == "Hello World!"


class TestDesafio2RepetindoTextos:
    """Testes para o Desafio 2: Repetindo Textos."""
    
    def test_repetir_texto_tres_vezes(self):
        """Testa repetição de texto 3 vezes."""
        resultado = repetir_texto("Py", 3)
        assert resultado == "PyPyPy"
    
    def test_repetir_texto_uma_vez(self):
        """Testa repetição de texto 1 vez."""
        resultado = repetir_texto("Python", 1)
        assert resultado == "Python"
    
    def test_repetir_texto_zero_vezes(self):
        """Testa repetição de texto 0 vezes."""
        resultado = repetir_texto("Test", 0)
        assert resultado == ""
    
    def test_repetir_string_com_espaco(self):
        """Testa repetição de string com espaço."""
        resultado = repetir_texto("Ha ", 3)
        assert resultado == "Ha Ha Ha "
    
    def test_repetir_numero_grande(self):
        """Testa repetição com número grande."""
        resultado = repetir_texto("X", 10)
        assert resultado == "XXXXXXXXXX"


class TestDesafio3OperacoesMatematicas:
    """Testes para o Desafio 3: Operações Matemáticas Simples."""
    
    def test_somar_numeros_positivos(self):
        """Testa soma de números positivos."""
        assert somar(5, 3) == 8
        assert somar(10.5, 2.5) == 13.0
    
    def test_subtrair_numeros(self):
        """Testa subtração de números."""
        assert subtrair(10, 3) == 7
        assert subtrair(5.5, 2.5) == 3.0
    
    def test_multiplicar_numeros(self):
        """Testa multiplicação de números."""
        assert multiplicar(4, 5) == 20
        assert multiplicar(2.5, 4) == 10.0
    
    def test_dividir_numeros(self):
        """Testa divisão de números."""
        assert dividir(10, 2) == 5.0
        assert dividir(15, 3) == 5.0
    
    def test_dividir_por_zero(self):
        """Testa divisão por zero."""
        with pytest.raises(ValueError, match="Não é possível dividir por zero"):
            dividir(10, 0)
    
    def test_calcular_soma(self):
        """Testa função calcular com soma."""
        assert calcular(5, 3, '+') == 8
    
    def test_calcular_subtracao(self):
        """Testa função calcular com subtração."""
        assert calcular(10, 4, '-') == 6
    
    def test_calcular_multiplicacao(self):
        """Testa função calcular com multiplicação."""
        assert calcular(6, 7, '*') == 42
    
    def test_calcular_divisao(self):
        """Testa função calcular com divisão."""
        assert calcular(20, 4, '/') == 5.0
    
    def test_calcular_operacao_invalida(self):
        """Testa operação inválida."""
        with pytest.raises(ValueError, match="Operação inválida"):
            calcular(5, 3, '%')
    
    def test_operacoes_com_numeros_negativos(self):
        """Testa operações com números negativos."""
        assert somar(-5, -3) == -8
        assert subtrair(-10, -3) == -7
        assert multiplicar(-4, 5) == -20


class TestDesafio4ParImpar:
    """Testes para o Desafio 4: Verificando Números Pares e Ímpares."""
    
    def test_numero_par_positivo(self):
        """Testa número par positivo."""
        assert verificar_par_impar(4) == "par"
        assert eh_par(4) is True
    
    def test_numero_impar_positivo(self):
        """Testa número ímpar positivo."""
        assert verificar_par_impar(7) == "ímpar"
        assert eh_par(7) is False
    
    def test_zero_eh_par(self):
        """Testa se zero é par."""
        assert verificar_par_impar(0) == "par"
        assert eh_par(0) is True
    
    def test_numero_par_negativo(self):
        """Testa número par negativo."""
        assert verificar_par_impar(-6) == "par"
        assert eh_par(-6) is True
    
    def test_numero_impar_negativo(self):
        """Testa número ímpar negativo."""
        assert verificar_par_impar(-9) == "ímpar"
        assert eh_par(-9) is False
    
    def test_numeros_grandes(self):
        """Testa números grandes."""
        assert verificar_par_impar(1000) == "par"
        assert verificar_par_impar(9999) == "ímpar"


class TestDesafio5MediaNotas:
    """Testes para o Desafio 5: Calculando Média de Notas."""
    
    def test_calcular_media_tres_notas(self):
        """Testa cálculo de média de 3 notas."""
        media = calcular_media(8.0, 7.0, 9.0)
        assert media == pytest.approx(8.0, rel=1e-2)
    
    def test_calcular_media_notas_iguais(self):
        """Testa média de notas iguais."""
        media = calcular_media(7.5, 7.5, 7.5)
        assert media == pytest.approx(7.5, rel=1e-2)
    
    def test_calcular_media_com_zero(self):
        """Testa média incluindo zero."""
        media = calcular_media(0, 5, 10)
        assert media == pytest.approx(5.0, rel=1e-2)
    
    def test_calcular_media_lista_tres_notas(self):
        """Testa média de lista com 3 notas."""
        media = calcular_media_lista([8.0, 7.0, 9.0])
        assert media == pytest.approx(8.0, rel=1e-2)
    
    def test_calcular_media_lista_varios_elementos(self):
        """Testa média de lista com vários elementos."""
        media = calcular_media_lista([6, 7, 8, 9, 10])
        assert media == pytest.approx(8.0, rel=1e-2)
    
    def test_calcular_media_lista_um_elemento(self):
        """Testa média de lista com um elemento."""
        media = calcular_media_lista([7.5])
        assert media == pytest.approx(7.5, rel=1e-2)
    
    def test_calcular_media_lista_vazia(self):
        """Testa média de lista vazia."""
        with pytest.raises(ValueError, match="A lista de notas não pode estar vazia"):
            calcular_media_lista([])
    
    def test_calcular_media_notas_decimais(self):
        """Testa média com notas decimais."""
        media = calcular_media(7.5, 8.3, 9.2)
        assert media == pytest.approx(8.333, rel=1e-2)


class TestDesafio6Palindromo:
    """Testes para o Desafio 6: Verificando Palíndromos."""
    
    def test_palindromo_palavra_simples(self):
        """Testa palíndromo com palavra simples."""
        assert eh_palindromo("arara") is True
        assert eh_palindromo("python") is False
    
    def test_palindromo_palavra_unica_letra(self):
        """Testa palíndromo com letra única."""
        assert eh_palindromo("a") is True
    
    def test_palindromo_palavra_duas_letras_iguais(self):
        """Testa palíndromo com duas letras iguais."""
        assert eh_palindromo("aa") is True
    
    def test_palindromo_palavra_duas_letras_diferentes(self):
        """Testa não-palíndromo com duas letras diferentes."""
        assert eh_palindromo("ab") is False
    
    def test_palindromo_frase_com_espacos(self):
        """Testa palíndromo com espaços."""
        assert eh_palindromo("ovo") is True
        assert eh_palindromo("a torre da derrota") is True
    
    def test_palindromo_case_insensitive(self):
        """Testa palíndromo ignorando maiúsculas/minúsculas."""
        assert eh_palindromo("Arara") is True
        assert eh_palindromo("ABA") is True
    
    def test_palindromo_simples_case_sensitive(self):
        """Testa palíndromo simples (case-sensitive)."""
        assert eh_palindromo_simples("ovo") is True
        assert eh_palindromo_simples("Ovo") is False
        assert eh_palindromo_simples("python") is False
    
    def test_palindromo_palavras_longas(self):
        """Testa palíndromos com palavras longas."""
        assert eh_palindromo("reviver") is True
        assert eh_palindromo("socorram me subi no onibus em marrocos") is True
    
    def test_palindromo_string_vazia(self):
        """Testa palíndromo com string vazia."""
        assert eh_palindromo("") is True
        assert eh_palindromo_simples("") is True
    
    def test_nao_palindromo_palavras_comuns(self):
        """Testa palavras comuns que não são palíndromos."""
        assert eh_palindromo("banana") is False
        assert eh_palindromo("teste") is False
        assert eh_palindromo("programacao") is False


# Testes adicionais de integração
class TestIntegracao:
    """Testes de integração para validar o funcionamento conjunto."""
    
    def test_todas_funcoes_importaveis(self):
        """Verifica se todas as funções podem ser importadas."""
        from resolucoes_code import (
            concatenar_dados,
            repetir_texto,
            calcular,
            verificar_par_impar,
            calcular_media,
            eh_palindromo
        )
        # Se chegou aqui, todas as funções foram importadas com sucesso
        assert True
    
    def test_workflow_completo_exemplo(self):
        """Testa um workflow completo usando várias funções."""
        # Concatenar dados
        texto = concatenar_dados("Python", " 3.11")
        assert "Python" in texto
        
        # Repetir texto
        repetido = repetir_texto("!", 3)
        assert len(repetido) == 3
        
        # Calcular operação
        resultado = calcular(10, 5, '+')
        assert resultado == 15.0
        
        # Verificar par/ímpar
        tipo = verificar_par_impar(int(resultado))
        assert tipo == "ímpar"
        
        # Calcular média
        media = calcular_media(8.0, 9.0, 7.0)
        assert 7.0 < media < 9.0
        
        # Verificar palíndromo
        eh_pal = eh_palindromo("ana")
        assert eh_pal is True
