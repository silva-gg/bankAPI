# 🎯 Desafios de Programação - bankAPI

Este diretório contém desafios de programação baseados na API bancária, suas soluções e testes.

## 📚 Sobre os Desafios

Os desafios foram criados para demonstrar compreensão dos conceitos de API bancária, algoritmos financeiros e manipulação de dados. Cada desafio tem sua própria solução e conjunto de testes.

## 🏆 Lista de Desafios

### Desafio 1: Calculadora de Juros Compostos
**Arquivo:** `desafio_01_juros_compostos.py`
**Descrição:** Implementar uma função que calcula juros compostos para contas poupança.
**Conceitos:** Matemática financeira, fórmulas de juros

### Desafio 2: Análise de Histórico de Transações
**Arquivo:** `desafio_02_analise_transacoes.py`
**Descrição:** Analisar o histórico de transações para identificar padrões de gastos mensais e receitas.
**Conceitos:** Análise de dados, agregações, processamento de datas

### Desafio 3: Gerador de Relatório de Saldo
**Arquivo:** `desafio_03_relatorio_saldo.py`
**Descrição:** Gerar relatório de saldo de conta com filtros de data.
**Conceitos:** Manipulação de dados, filtros, formatação de relatórios

### Desafio 4: Calculadora de Tarifas de Transação
**Arquivo:** `desafio_04_calculadora_tarifas.py`
**Descrição:** Implementar sistema de cálculo de tarifas baseado no tipo e valor da transação.
**Conceitos:** Regras de negócio, cálculos condicionais

### Desafio 5: Resumo de Atividade de Conta
**Arquivo:** `desafio_05_resumo_atividade.py`
**Descrição:** Criar resumo estatístico de atividades da conta (número e total de depósitos/saques).
**Conceitos:** Estatísticas descritivas, agregações

### Desafio 6: Rastreador de Limite de Saque Diário
**Arquivo:** `desafio_06_limite_saque.py`
**Descrição:** Implementar verificador de limite de saque diário com alertas.
**Conceitos:** Validações, limites, controle de acesso

### Desafio 7: Estatísticas de Tempo de Vida da Conta
**Arquivo:** `desafio_07_estatisticas_conta.py`
**Descrição:** Calcular idade da conta e estatísticas históricas completas.
**Conceitos:** Cálculos de data/tempo, análise histórica

## 🧪 Testes

Todos os desafios têm testes correspondentes no diretório `tests/test_resolucoes_code/`:
- `test_desafio_01.py`
- `test_desafio_02.py`
- `test_desafio_03.py`
- `test_desafio_04.py`
- `test_desafio_05.py`
- `test_desafio_06.py`
- `test_desafio_07.py`

## ▶️ Como Executar

### Executar todos os testes dos desafios:
```bash
poetry run pytest tests/test_resolucoes_code/ -v
```

### Executar teste específico:
```bash
poetry run pytest tests/test_resolucoes_code/test_desafio_01.py -v
```

### Executar com cobertura:
```bash
poetry run pytest tests/test_resolucoes_code/ --cov=resolucoes_code --cov-report=html
```

## 📝 Estrutura dos Arquivos

Cada desafio segue a estrutura:

```python
"""
Desafio X: Nome do Desafio

Descrição detalhada do problema a ser resolvido.

Requisitos:
- Requisito 1
- Requisito 2

Exemplo de uso:
    resultado = funcao_desafio(parametros)
"""

def funcao_principal(...):
    # Implementação
    pass
```

## ✅ Critérios de Avaliação

As soluções são avaliadas com base em:
1. **Correção:** A solução resolve o problema corretamente
2. **Eficiência:** O código é eficiente e otimizado
3. **Legibilidade:** O código é claro e bem documentado
4. **Testes:** Todos os testes passam com sucesso
5. **Boas Práticas:** Segue convenções Python (PEP 8)

## 🚀 Integração Contínua

Os testes são executados automaticamente no GitHub Actions em cada push/PR.
Veja `.github/workflows/ci-cd.yml` para mais detalhes.
