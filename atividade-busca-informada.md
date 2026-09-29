# INSTITUTO FEDERAL DO MARANHÃO

**Campus Caxias**
Rodovia MA-349 – do Km 1,524/1,525 ao Km 3,424/3,425
Teso Duro - Caxias - MA
Ministério da Educação

| | | |
|---|---|---|
| **Curso:** Computação | **Turno:** Matutino | **Semestre:** 2º |
| **Disciplina:** Inteligência Artificial | **Professor:** Rafael T. Anchiêta | **Data:** 28/09/26 |
| **Nome:**  João Batista Medeiros Conceição Filho| | |

---

## Atividade Busca Informada

> **Objetivo.** Implementar e comparar os algoritmos Greedy Best-First Search e A* no problema do quebra-cabeça de 8 peças. A atividade deve enfatizar não apenas a obtenção de uma solução, mas também a análise da qualidade das heurísticas e do comportamento computacional dos algoritmos.

Em todas as execuções, registre pelo menos as seguintes métricas:

| Métrica | Descrição |
|---|---|
| **Solução encontrada** | Indicar se uma solução foi encontrada. |
| **Custo da solução** | Valor de $g(G)$. |
| **Profundidade** | Número de ações do estado inicial até a solução. |
| **Nós expandidos** | Nós retirados da fronteira e efetivamente expandidos. |
| **Nós gerados** | Total de sucessores produzidos. |
| **Fronteira máxima** | Maior tamanho atingido pela fila de prioridade. |
| **Tempo** | Tempo total de execução. |

---

## Questão 1

Considere o quebra-cabeça de 8 peças. O estado objetivo será:

| | | |
|:-:|:-:|:-:|
| 1 | 2 | 3 |
| 4 | 5 | 6 |
| 7 | 8 | _ |

Cada movimento da posição vazia possui custo unitário: $c(s, a, s') = 1$

Uma representação possível de estado é:

```
(1, 2, 3,
 4, 5, 6,
 7, 8, 0)
```

em que `0` representa a posição vazia.

As ações possíveis são: {CIMA, BAIXO, ESQUERDA, DIREITA}, desde que o movimento seja válido.

**(a)** Implemente Greedy Best-First Search utilizando: $f(n) = h(n)$

**(b)** Implemente A* utilizando: $f(n) = g(n) + h(n)$

*Obs.: Implemente as duas heurísticas abaixo.*

- **i.** Peças fora do lugar: $h_1(n)$ = número de peças fora do lugar. O espaço vazio não é contado.
- **ii.** Distância de Manhattan. O espaço vazio não é contado.

$$h_2(n) = \sum_{i=1}^{8} \left( |x_i - x_i^*| + |y_i - y_i^*| \right),$$

em que $(x_i, y_i)$ representa a posição atual da peça $i$ e $(x_i^*, y_i^*)$ sua posição no objetivo.

---

Execute: **Greedy + h1**, **Greedy + h2**, **A\* + h1**, **A\* + h2**.

Utilize as três instâncias abaixo.

### Instância A — fácil

| | | |
|:-:|:-:|:-:|
| 1 | 5 | 2 |
| 4 | 8 | 3 |
| 7 | 6 | _ |

### Instância B — intermediária

| | | |
|:-:|:-:|:-:|
| 5 | 8 | 2 |
| 1 | 7 | 3 |
| 4 | 6 | _ |

### Instância C — difícil

| | | |
|:-:|:-:|:-:|
| 8 | 7 | 2 |
| 5 | 4 | 3 |
| 1 | 6 | _ |

---

O programa deve imprimir o caminho completo da solução.

**Exemplo de formato:**

```
Estado 0
1 2 3
4 _ 6
7 5 8

Estado 1
1 2 3
4 5 6
7 _ 8

Estado 2
1 2 3
4 5 6
7 8 _
```

Para cada instância, preencha uma tabela semelhante à seguinte:

| Algoritmo | Heurística | Custo | Exp. | Gerados | Front.Max | Tempo |
|---|---|---|---|---|---|---|
| Greedy | h1 | | | | | |
| Greedy | h2 | | | | | |
| A* | h1 | | | | | |
| A* | h2 | | | | | |
