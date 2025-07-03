> MARTINS, Victor S.; FREITAS, Julio Cezar Gonçalves de; MENDES, Ingrid Nery; TEIXEIRA, Otávio Noura. **Algoritmos Genéticos aplicado ao mundo de Wumpus: uma comparação entre agentes baseados em regras e agentes inteligentes**. In: ESCOLA REGIONAL DE ALTO DESEMPENHO NORTE 2 (ERAD-NO2) E ESCOLA REGIONAL DE APRENDIZADO DE MÁQUINA E INTELIGÊNCIA ARTIFICIAL NORTE 2 (ERAMIA-NO2), 1. , 2021, Online. Anais [...]. Porto Alegre: Sociedade Brasileira de Computação, 2021 . p. 33-36. DOI: <https://doi.org/10.5753/erad-no2.2021.18677>

---

## Sobre o Projeto

Este projeto implementa agentes para o clássico problema do **Wumpus World**. O objetivo é explorar um ambiente perigoso, encontrar o ouro e sair vivo, evitando poços e o Wumpus. Foram desenvolvidos diferentes tipos de agentes:

- **Agente em Primeira Pessoa:** Controlado pelo usuário via teclado.
- **Agente Lógico:** Toma decisões com base em regras e lógica, utilizando percepções do ambiente.
- **Agente com Algoritmo Genético:** Utiliza técnicas de otimização para aprender sequências de ações eficientes.

---

## Simulação do Agente Lógico

### Como executar

Execute o script Python:
```bash
python Wumpus_ReativeRun.py
```

### Configurações

- Para ver os movimentos do agente no terminal, defina a variável `print_world` como `True`.
- Para alterar o tamanho do mundo, modifique o valor `WORLD_SIZE` em `WumpusReative.py` e os valores `self.max_row` e `self.max_col` nas linhas 80 e 81 do arquivo `LogicRobot.py`.
- É possível definir a quantidade de mundos, sementes e outras opções diretamente no script.

---

## Simulação do Agente baseado em Algoritmos Genéticos

### Como executar

Execute o script Python:
```bash
python Wumpus_GeneticAlgorithm.py
```

### Configurações

- Defina a quantidade de mundos, testes e sementes no próprio script.
- As configurações do Algoritmo Genético podem ser feitas em `Wumpus_GeneticAlgorithm.py`.
- Para alterar o tamanho do mundo, modifique o valor `WORLD_SIZE` em `WumpusReative.py`.

---

## Dependências

- Python 3.x
- numpy

Instale as dependências com:
```bash
pip install -r requirements.txt
```

---

## Objetivo do Projeto

O projeto **Wumpus World** simula um ambiente perigoso onde agentes inteligentes devem encontrar o ouro e sair do mundo, evitando perigos como poços e o Wumpus. Cada agente utiliza estratégias diferentes para resolver o problema, permitindo comparar abordagens baseadas em lógica, controle humano e algoritmos genéticos.

---

## Exemplos de Comandos

- Executar o agente lógico:
  ```bash
  python Wumpus_ReativeRun.py
  ```
- Executar o agente genético:
  ```bash
  python Wumpus_GeneticAlgorithm.py
  ```

---

## Observações

- Certifique-se de editar as configurações desejadas nos scripts antes de executar.
- Recomenda-se utilizar um ambiente virtual Python para evitar conflitos de dependências.

---
