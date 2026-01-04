"""
Pacote de resoluções dos desafios Python.

Este pacote contém as soluções para os 6 desafios de programação básica em Python.
"""

__version__ = "1.0.0"
__author__ = "silva-gg"

# Importações para facilitar o uso do pacote
from .desafio1_concatenando_dados import concatenar_dados
from .desafio2_repetindo_textos import repetir_texto
from .desafio3_operacoes_matematicas import calcular, somar, subtrair, multiplicar, dividir
from .desafio4_par_impar import verificar_par_impar, eh_par
from .desafio5_media_notas import calcular_media, calcular_media_lista
from .desafio6_palindromo import eh_palindromo, eh_palindromo_simples

__all__ = [
    "concatenar_dados",
    "repetir_texto",
    "calcular",
    "somar",
    "subtrair",
    "multiplicar",
    "dividir",
    "verificar_par_impar",
    "eh_par",
    "calcular_media",
    "calcular_media_lista",
    "eh_palindromo",
    "eh_palindromo_simples",
]
