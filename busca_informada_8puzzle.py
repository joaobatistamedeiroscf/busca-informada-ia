

import heapq
import itertools
import sys
import time

OBJETIVO = (1, 2, 3, 4, 5, 6, 7, 8, 0)

# Posição (linha, coluna) de cada peça no objetivo
POS_OBJ = {v: divmod(i, 3) for i, v in enumerate(OBJETIVO)}

# Ações: deslocamento do espaço vazio (dlinha, dcoluna)
ACOES = {
    "CIMA": (-1, 0),
    "BAIXO": (1, 0),
    "ESQUERDA": (0, -1),
    "DIREITA": (0, 1),
}

INSTANCIAS = {
    "A (fácil)": (1, 5, 2,
                  4, 8, 3,
                  0, 7, 6),
    "B (intermediária)": (5, 8, 2,
                          1, 7, 3,
                          0, 4, 6),
    "C (difícil)": (8, 7, 2,
                    5, 4, 3,
                    0, 1, 6),
}


# --------------------------------------------------------------------------
# Heurísticas
# --------------------------------------------------------------------------
def h1(estado):
    """Peças fora do lugar (sem contar o vazio)."""
    return sum(1 for i, v in enumerate(estado) if v != 0 and v != OBJETIVO[i])


def h2(estado):
    """Soma das distâncias de Manhattan (sem contar o vazio)."""
    total = 0
    for i, v in enumerate(estado):
        if v == 0:
            continue
        x, y = divmod(i, 3)
        xo, yo = POS_OBJ[v]
        total += abs(x - xo) + abs(y - yo)
    return total


HEURISTICAS = {"h1": h1, "h2": h2}


# --------------------------------------------------------------------------
# Problema
# --------------------------------------------------------------------------
def tem_solucao(estado):
    """Paridade das inversões: com largura 3 (ímpar), solúvel se par."""
    pecas = [v for v in estado if v != 0]
    inv = sum(1 for i in range(len(pecas)) for j in range(i + 1, len(pecas))
              if pecas[i] > pecas[j])
    return inv % 2 == 0


def sucessores(estado):
    """Gera (acao, novo_estado); custo de cada ação = 1."""
    pos = estado.index(0)
    x, y = divmod(pos, 3)
    for nome, (dx, dy) in ACOES.items():
        nx, ny = x + dx, y + dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            npos = nx * 3 + ny
            lista = list(estado)
            lista[pos], lista[npos] = lista[npos], lista[pos]
            yield nome, tuple(lista)


def formatar(estado):
    return "\n".join(
        " ".join("_" if v == 0 else str(v) for v in estado[r * 3:r * 3 + 3])
        for r in range(3)
    )


# --------------------------------------------------------------------------
# Busca (Greedy e A* compartilham a mesma estrutura; muda só f(n))
# --------------------------------------------------------------------------
def busca_informada(inicial, heuristica, algoritmo):
    """
    algoritmo: "greedy" -> f = h      |   "astar" -> f = g + h

    Retorna um dicionário com o caminho e as métricas pedidas.

    Definições das métricas:
      - expandidos: nós retirados da fronteira e efetivamente expandidos
      - gerados: total de sucessores produzidos (inclui os descartados
        por repetição)
      - fronteira máxima: maior nº de estados distintos na fila de prioridade
    """
    inicio = time.perf_counter()

    def f(g, h):
        return h if algoritmo == "greedy" else g + h

    desempate = itertools.count()  # desempate estável (FIFO) na heap
    h0 = heuristica(inicial)
    heap = [(f(0, h0), next(desempate), 0, inicial)]
    # melhor g conhecido de cada estado que está na fronteira
    na_fronteira = {inicial: 0}
    pai = {inicial: (None, None)}   # estado -> (estado_pai, acao)
    g_de = {inicial: 0}
    expandidos_set = set()          # "lista fechada"

    expandidos = gerados = 0
    fronteira_max = 1
    resultado = {"encontrada": False}

    while heap:
        _, _, g, estado = heapq.heappop(heap)

        # entrada obsoleta (estado já expandido ou achado caminho melhor)
        if estado in expandidos_set or na_fronteira.get(estado) != g:
            continue
        del na_fronteira[estado]

        if estado == OBJETIVO:
            caminho, acoes = [], []
            atual = estado
            while atual is not None:
                caminho.append(atual)
                p, a = pai[atual]
                if a:
                    acoes.append(a)
                atual = p
            caminho.reverse()
            acoes.reverse()
            resultado = {
                "encontrada": True,
                "caminho": caminho,
                "acoes": acoes,
                "custo": g,
                "profundidade": len(acoes),
            }
            break

        expandidos_set.add(estado)
        expandidos += 1

        for acao, filho in sucessores(estado):
            gerados += 1
            if filho in expandidos_set:
                continue
            g_filho = g + 1

            if algoritmo == "greedy":
                # Greedy ignora g: mantém o primeiro caminho encontrado
                if filho in na_fronteira:
                    continue
            else:
                # A*: só aceita se melhora o melhor g conhecido (reabertura)
                if filho in na_fronteira and na_fronteira[filho] <= g_filho:
                    continue

            na_fronteira[filho] = g_filho
            pai[filho] = (estado, acao)
            g_de[filho] = g_filho
            heapq.heappush(
                heap, (f(g_filho, heuristica(filho)), next(desempate),
                       g_filho, filho))

        fronteira_max = max(fronteira_max, len(na_fronteira))

    resultado.update({
        "expandidos": expandidos,
        "gerados": gerados,
        "fronteira_max": fronteira_max,
        "tempo": time.perf_counter() - inicio,
    })
    return resultado


def greedy(inicial, heuristica):
    return busca_informada(inicial, heuristica, "greedy")


def astar(inicial, heuristica):
    return busca_informada(inicial, heuristica, "astar")


# --------------------------------------------------------------------------
# Saída
# --------------------------------------------------------------------------
def imprimir_caminho(res):
    for i, est in enumerate(res["caminho"]):
        print(f"Estado {i}")
        print(formatar(est))
        print()


def main():
    quiet = "--quiet" in sys.argv
    tabelas = {}

    for nome_inst, inicial in INSTANCIAS.items():
        assert tem_solucao(inicial), f"Instância {nome_inst} sem solução!"
        print("=" * 60)
        print(f"INSTÂNCIA {nome_inst}")
        print(formatar(inicial))
        print("=" * 60)

        linhas = []
        for alg_nome, alg in (("Greedy", greedy), ("A*", astar)):
            for h_nome, h in HEURISTICAS.items():
                res = alg(inicial, h)
                if not res["encontrada"]:
                    print(f"\n--- {alg_nome} + {h_nome}: sem solução ---")
                    continue
                if not quiet:
                    print(f"\n--- {alg_nome} + {h_nome} "
                          f"(custo = {res['custo']}) ---\n")
                    imprimir_caminho(res)
                linhas.append((alg_nome, h_nome, res))
        tabelas[nome_inst] = linhas

    print("\n" + "#" * 60)
    print("RESULTADOS")
    print("#" * 60)
    for nome_inst, linhas in tabelas.items():
        print(f"\nInstância {nome_inst}\n")
        print("| Algoritmo | Heurística | Custo | Prof. | Exp. | Gerados "
              "| Front.Max | Tempo (s) |")
        print("|---|---|---|---|---|---|---|---|")
        for alg_nome, h_nome, r in linhas:
            print(f"| {alg_nome} | {h_nome} | {r['custo']} | "
                  f"{r['profundidade']} | {r['expandidos']} | "
                  f"{r['gerados']} | {r['fronteira_max']} | "
                  f"{r['tempo']:.4f} |")


if __name__ == "__main__":
    main()
