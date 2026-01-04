# Resoluções dos Desafios Python

Este diretório contém as soluções para os 6 desafios de programação Python do projeto "resolvendo-codigos-py-copilot".

## 📋 Desafios Implementados

### 1. Concatenando Dados (`desafio1_concatenando_dados.py`)
**Objetivo:** Receber dois dados do usuário e concatenar em uma única string.

**Funções:**
- `concatenar_dados(dado1, dado2)` - Concatena dois dados

**Exemplo:**
```python
from resolucoes_code.desafio1_concatenando_dados import concatenar_dados

resultado = concatenar_dados("Olá", " Mundo")
print(resultado)  # Output: Olá Mundo
```

### 2. Repetindo Textos (`desafio2_repetindo_textos.py`)
**Objetivo:** Solicitar uma string e um número inteiro. Retornar a string repetida N vezes.

**Funções:**
- `repetir_texto(texto, vezes)` - Repete um texto N vezes

**Exemplo:**
```python
from resolucoes_code.desafio2_repetindo_textos import repetir_texto

resultado = repetir_texto("Python ", 3)
print(resultado)  # Output: Python Python Python 
```

### 3. Operações Matemáticas Simples (`desafio3_operacoes_matematicas.py`)
**Objetivo:** Receber dois números do usuário e realizar uma operação matemática entre eles.

**Funções:**
- `somar(num1, num2)` - Soma dois números
- `subtrair(num1, num2)` - Subtrai dois números
- `multiplicar(num1, num2)` - Multiplica dois números
- `dividir(num1, num2)` - Divide dois números
- `calcular(num1, num2, operacao)` - Realiza operação especificada

**Exemplo:**
```python
from resolucoes_code.desafio3_operacoes_matematicas import calcular

resultado = calcular(10, 5, '+')
print(resultado)  # Output: 15.0
```

### 4. Verificando Números Pares e Ímpares (`desafio4_par_impar.py`)
**Objetivo:** Receber um número inteiro e verificar se é par ou ímpar.

**Funções:**
- `verificar_par_impar(numero)` - Retorna "par" ou "ímpar"
- `eh_par(numero)` - Retorna True se par, False se ímpar

**Exemplo:**
```python
from resolucoes_code.desafio4_par_impar import verificar_par_impar, eh_par

print(verificar_par_impar(4))  # Output: par
print(eh_par(7))  # Output: False
```

### 5. Calculando Média de Notas (`desafio5_media_notas.py`)
**Objetivo:** Calcular a média de três notas recebidas por entrada.

**Funções:**
- `calcular_media(nota1, nota2, nota3)` - Calcula média de 3 notas
- `calcular_media_lista(notas)` - Calcula média de uma lista de notas

**Exemplo:**
```python
from resolucoes_code.desafio5_media_notas import calcular_media

media = calcular_media(8.0, 7.5, 9.0)
print(f"Média: {media:.2f}")  # Output: Média: 8.17
```

### 6. Verificando Palíndromos (`desafio6_palindromo.py`)
**Objetivo:** Testar se uma palavra é palíndroma (igual de trás para frente).

**Funções:**
- `eh_palindromo(texto)` - Verifica se é palíndromo (ignora espaços e case)
- `eh_palindromo_simples(palavra)` - Verifica se é palíndromo (case-sensitive)

**Exemplo:**
```python
from resolucoes_code.desafio6_palindromo import eh_palindromo

print(eh_palindromo("arara"))  # Output: True
print(eh_palindromo("python"))  # Output: False
```

## 🧪 Testes

Todos os desafios possuem testes automatizados localizados em `tests/test_desafios.py`.

Para executar os testes:
```bash
poetry run pytest tests/test_desafios.py -v
```

## 🚀 Executando os Desafios

Cada desafio pode ser executado de forma interativa:

```bash
# Desafio 1
python resolucoes_code/desafio1_concatenando_dados.py

# Desafio 2
python resolucoes_code/desafio2_repetindo_textos.py

# E assim por diante...
```

## 📚 Aprendizados

Estes desafios cobrem conceitos fundamentais de Python:
- Manipulação de strings
- Operações matemáticas
- Estruturas condicionais (if/else)
- Funções e parâmetros
- Type hints
- Docstrings
- Tratamento de erros
