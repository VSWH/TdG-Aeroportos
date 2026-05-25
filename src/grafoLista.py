# Victor Sung Woo Hong 10425852
# Mauricio Custódio Vicentini 10426074

import heapq
import os


class Grafo:
    def _init_(self):
        self.n = 0
        self.m = 0
        self.listaAdj = []
        self.rotulos = []

    # c) Inserir vertice
    def insere_vertice(self, rotulo, peso=0):
        self.rotulos.append((rotulo, peso))
        self.listaAdj.append([])
        self.n += 1
        return self.n - 1

    # d) Inserir aresta
    def insereA(self, v, w, peso):
        if not self.vertice_valido(v) or not self.vertice_valido(w):
            return False

        for aresta in self.listaAdj[v]:
            if aresta[0] == w:
                return False

        self.listaAdj[v].append((w, peso))
        self.listaAdj[w].append((v, peso))
        self.m += 1
        return True

    # f) Remover aresta
    def removeA(self, v, w):
        if not self.vertice_valido(v) or not self.vertice_valido(w):
            return False

        removido_v = False
        removido_w = False

        for aresta in list(self.listaAdj[v]):
            if aresta[0] == w:
                self.listaAdj[v].remove(aresta)
                removido_v = True
                break

        for aresta in list(self.listaAdj[w]):
            if aresta[0] == v:
                self.listaAdj[w].remove(aresta)
                removido_w = True
                break

        if removido_v and removido_w:
            self.m -= 1
            return True
        return False

    # e) Remove vertice
    def remove_vertice(self, v):
        if not self.vertice_valido(v):
            return False

        conexoes = list(self.listaAdj[v])
        for w, peso in conexoes:
            self.removeA(v, w)

        self.rotulos[v] = None
        self.listaAdj[v] = None
        return True

    # Verifica se um vertice existe e nao foi removido
    def vertice_valido(self, v):
        return 0 <= v < self.n and self.rotulos[v] is not None and self.listaAdj[v] is not None

    # Retorna todos os vertices ativos do grafo
    def vertices_ativos(self):
        ativos = []
        for i in range(self.n):
            if self.vertice_valido(i):
                ativos.append(i)
        return ativos

    # i) Verifica conexidade do grafo nao orientado
    def verifica_conexidade(self):
        ativos = self.vertices_ativos()

        if len(ativos) == 0:
            return "VAZIO"

        inicio = ativos[0]
        visitados = set()
        fila = [inicio]
        visitados.add(inicio)

        while fila:
            v = fila.pop(0)
            for w, peso in self.listaAdj[v]:
                if self.vertice_valido(w) and w not in visitados:
                    visitados.add(w)
                    fila.append(w)

        if len(visitados) == len(ativos):
            return "CONEXO"
        return "DESCONEXO"

    # h) Mostrar grafo
    def show(self):
        print(f"\nGrafo (n: {self.n}, m: {self.m})")
        for i in range(self.n):
            if not self.vertice_valido(i):
                continue

            apelido = self.rotulos[i][0]
            print(f"[{i:2d}] {apelido:^5}: ", end="")

            if not self.listaAdj[i]:
                print("(sem conexoes)", end="")
            else:
                conexoes = [f"-> {w}({peso}km)" for w, peso in self.listaAdj[i]]
                print(", ".join(conexoes), end="")
            print()
        print("\nFim da impressao do grafo.\n")

    # k) Dijkstra - menor rota entre dois aeroportos
    def dijkstra(self, origem, destino):
        if not self.vertice_valido(origem) or not self.vertice_valido(destino):
            print("\n[Erro] Origem ou destino invalido.")
            return

        dist = [float("inf")] * self.n
        anterior = [None] * self.n
        dist[origem] = 0

        fila_prioridade = [(0, origem)]

        while fila_prioridade:
            distancia_atual, v = heapq.heappop(fila_prioridade)

            if distancia_atual > dist[v]:
                continue

            if v == destino:
                break

            for vizinho, peso in self.listaAdj[v]:
                if not self.vertice_valido(vizinho):
                    continue

                nova_distancia = distancia_atual + peso

                if nova_distancia < dist[vizinho]:
                    dist[vizinho] = nova_distancia
                    anterior[vizinho] = v
                    heapq.heappush(fila_prioridade, (nova_distancia, vizinho))

        if dist[destino] == float("inf"):
            print("\n[Analise] Nao existe rota entre os aeroportos informados.")
            return

        caminho = []
        atual = destino

        while atual is not None:
            caminho.append(atual)
            atual = anterior[atual]

        caminho.reverse()

        print("\n" + "=" * 60)
        print("MENOR ROTA ENTRE AEROPORTOS - DIJKSTRA")
        print("=" * 60)
        print(f"Origem : [{origem}] {self.rotulos[origem][0]}")
        print(f"Destino: [{destino}] {self.rotulos[destino][0]}")
        print(f"Distancia minima: {dist[destino]} km")
        print("\nCaminho encontrado:")

        caminho_formatado = []
        for v in caminho:
            caminho_formatado.append(f"[{v}] {self.rotulos[v][0]}")

        print(" -> ".join(caminho_formatado))
        print("=" * 60)

    # l) Mostrar o grau de todos os aeroportos
    def mostrar_graus(self):
        print("\n" + "=" * 60)
        print("GRAU DOS AEROPORTOS")
        print("=" * 60)

        if len(self.vertices_ativos()) == 0:
            print("[Aviso] O grafo esta vazio.")
            return

        graus = []

        for i in range(self.n):
            if self.vertice_valido(i):
                grau = len(self.listaAdj[i])
                codigo = self.rotulos[i][0]
                graus.append((grau, i, codigo))
                print(f"Aeroporto [{i}] {codigo}: grau {grau}")

        graus.sort(reverse=True)

        print("\nAeroportos mais conectados:")
        for grau, i, codigo in graus[:10]:
            print(f"[{i}] {codigo} -> grau {grau}")

        print("=" * 60)

    # m) Verificar se o grafo e Euleriano ou Semieuleriano
    def verifica_euleriano(self):
        print("\n" + "=" * 60)
        print("ANALISE EULERIANA")
        print("=" * 60)

        status_conexidade = self.verifica_conexidade()

        if status_conexidade != "CONEXO":
            print("O grafo nao e Euleriano, pois nao e conexo.")
            print("=" * 60)
            return

        impares = []

        for i in range(self.n):
            if self.vertice_valido(i):
                grau = len(self.listaAdj[i])
                if grau % 2 != 0:
                    impares.append(i)

        if len(impares) == 0:
            print("O grafo e EULERIANO.")
            print("Justificativa: e conexo e todos os vertices possuem grau par.")
        elif len(impares) == 2:
            print("O grafo e SEMIEULERIANO.")
            print("Justificativa: e conexo e possui exatamente dois vertices de grau impar.")
            print(f"Vertices impares: {impares}")
        else:
            print("O grafo NAO e Euleriano nem Semieuleriano.")
            print(f"Quantidade de vertices de grau impar: {len(impares)}")
            print(f"Vertices impares: {impares}")

        print("=" * 60)

    # n) Coloracao gulosa
    def coloracao_gulosa(self):
        print("\n" + "=" * 60)
        print("COLORACAO GULOSA DO GRAFO")
        print("=" * 60)

        if len(self.vertices_ativos()) == 0:
            print("[Aviso] O grafo esta vazio.")
            return

        cores = {}

        for v in range(self.n):
            if not self.vertice_valido(v):
                continue

            cores_vizinhos = set()

            for vizinho, peso in self.listaAdj[v]:
                if vizinho in cores:
                    cores_vizinhos.add(cores[vizinho])

            cor = 1
            while cor in cores_vizinhos:
                cor += 1

            cores[v] = cor

        qtd_cores = max(cores.values()) if cores else 0

        print(f"Quantidade de cores utilizadas: {qtd_cores}")
        print("\nResultado da coloracao:")

        for v in sorted(cores.keys()):
            codigo = self.rotulos[v][0]
            print(f"Aeroporto [{v}] {codigo}: cor {cores[v]}")

        print("=" * 60)

    # o) Kruskal - Arvore Geradora Minima
    def kruskal(self):
        print("\n" + "=" * 60)
        print("ARVORE GERADORA MINIMA - KRUSKAL")
        print("=" * 60)

        if self.verifica_conexidade() != "CONEXO":
            print("[Erro] O grafo nao e conexo. Nao e possivel gerar uma arvore geradora minima.")
            print("=" * 60)
            return

        pai = {}
        rank = {}

        for v in self.vertices_ativos():
            pai[v] = v
            rank[v] = 0

        def encontrar(v):
            if pai[v] != v:
                pai[v] = encontrar(pai[v])
            return pai[v]

        def unir(a, b):
            raiz_a = encontrar(a)
            raiz_b = encontrar(b)

            if raiz_a == raiz_b:
                return False

            if rank[raiz_a] < rank[raiz_b]:
                pai[raiz_a] = raiz_b
            elif rank[raiz_a] > rank[raiz_b]:
                pai[raiz_b] = raiz_a
            else:
                pai[raiz_b] = raiz_a
                rank[raiz_a] += 1

            return True

        arestas = []

        for u in range(self.n):
            if not self.vertice_valido(u):
                continue

            for v, peso in self.listaAdj[u]:
                if self.vertice_valido(v) and u < v:
                    arestas.append((peso, u, v))

        arestas.sort()

        arvore = []
        custo_total = 0

        for peso, u, v in arestas:
            if unir(u, v):
                arvore.append((u, v, peso))
                custo_total += peso

        print(f"Custo total da arvore geradora minima: {custo_total} km")
        print(f"Quantidade de arestas selecionadas: {len(arvore)}")
        print("\nArestas selecionadas:")

        for u, v, peso in arvore:
            codigo_u = self.rotulos[u][0]
            codigo_v = self.rotulos[v][0]
            print(f"[{u}] {codigo_u} -- [{v}] {codigo_v} : {peso} km")

        print("=" * 60)


def ler_arquivo(nome_arquivo="grafo.txt"):
    grafo = Grafo()
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            linhas = f.readlines()
            linhas = [linha.strip() for linha in linhas if linha.strip()]

            tipo_grafo = int(linhas[0])
            n = int(linhas[1])
            linha_atual = 2

            for _ in range(n):
                partes = linhas[linha_atual].split('"')
                id_vertice = int(partes[0].strip())
                rotulo = partes[1].strip()
                peso_vertice = int(partes[2].strip())

                if rotulo == "REMOVIDO":
                    grafo.rotulos.append(None)
                    grafo.listaAdj.append(None)
                    grafo.n += 1
                else:
                    grafo.insere_vertice(rotulo, peso_vertice)

                linha_atual += 1

            m = int(linhas[linha_atual])
            linha_atual += 1

            for _ in range(m):
                dados_aresta = linhas[linha_atual].split()
                u = int(dados_aresta[0])
                v = int(dados_aresta[1])
                peso_aresta = int(dados_aresta[2])

                grafo.insereA(u, v, peso_aresta)
                linha_atual += 1

        print(f"\n[SUCESSO] Arquivo '{nome_arquivo}' lido com sucesso!")
        print(f"Foram carregados {grafo.n} aeroportos e {grafo.m} rotas.")
        return grafo

    except FileNotFoundError:
        print(f"\n[ERRO] O arquivo '{nome_arquivo}' nao foi encontrado.")
        return None
    except Exception as e:
        print(f"\n[ERRO] Falha ao processar o arquivo: {e}")
        return None


def gravar_arquivo(grafo, nome_arquivo="grafo.txt"):
    try:
        with open(nome_arquivo, "w", encoding="utf-8") as f:
            f.write("2\n")
            f.write(f"{grafo.n}\n")

            for i in range(grafo.n):
                if grafo.rotulos[i] is None:
                    f.write(f'{i} "REMOVIDO" 0\n')
                else:
                    apelido = grafo.rotulos[i][0]
                    peso = grafo.rotulos[i][1]
                    f.write(f'{i} "{apelido}" {peso}\n')

            arestas_gravadas = set()
            linhas_arestas = []

            for u in range(grafo.n):
                if grafo.listaAdj[u] is not None:
                    for v, peso in grafo.listaAdj[u]:
                        aresta_unica = tuple(sorted((u, v)))
                        if aresta_unica not in arestas_gravadas:
                            linhas_arestas.append(f"{u} {v} {peso}\n")
                            arestas_gravadas.add(aresta_unica)

            f.write(f"{len(linhas_arestas)}\n")
            for linha in linhas_arestas:
                f.write(linha)

        print(f"\n[SUCESSO] Grafo salvo com sucesso no arquivo '{nome_arquivo}'.")
    except Exception as e:
        print(f"\n[ERRO] Falha ao gravar o arquivo: {e}")


def mostrar_arquivo(nome_arquivo="grafo.txt"):
    try:
        with open(nome_arquivo, "r", encoding="utf-8") as f:
            linhas = f.readlines()

        if not linhas:
            print("\n[Aviso] O arquivo esta vazio.")
            return

        linhas = [linha.strip() for linha in linhas if linha.strip()]
        tipo = int(linhas[0])
        n = int(linhas[1])

        print("\n" + "=" * 50)
        print(f"      CONTEUDO DO ARQUIVO: {nome_arquivo}      ")
        print("=" * 50)
        print(f" Tipo do Grafo : {tipo} (Nao Orientado com Peso)")
        print(f" Qtd. Vertices : {n}")
        print("-" * 50)

        linha_atual = 2
        for _ in range(n):
            print(f" Vertice -> {linhas[linha_atual]}")
            linha_atual += 1

        m = int(linhas[linha_atual])
        print("-" * 50)
        print(f" Qtd. Arestas  : {m}")
        print("-" * 50)
        linha_atual += 1

        for _ in range(m):
            print(f" Aresta  -> {linhas[linha_atual]}")
            linha_atual += 1

        print("=" * 50 + "\n")

    except FileNotFoundError:
        print(f"\n[ERRO] O arquivo '{nome_arquivo}' nao foi encontrado.")
    except Exception as e:
        print(f"\n[ERRO] Falha ao ler o arquivo: {e}")


def main():
    meu_grafo = Grafo()

    while True:
        print("\n" + "=" * 60)
        print("ANALISADOR DE ROTAS AEREAS NO BRASIL - ODS 9")
        print("=" * 60)
        print(" a) Ler dados do arquivo grafo.txt")
        print(" b) Gravar dados no arquivo grafo.txt")
        print(" c) Inserir vertice")
        print(" d) Inserir aresta")
        print(" e) Remove vertice")
        print(" f) Remove aresta")
        print(" g) Mostrar conteudo do arquivo")
        print(" h) Mostrar grafo")
        print(" i) Apresentar a conexidade do grafo")
        print(" j) Encerrar a aplicacao")
        print(" k) Encontrar menor rota entre dois aeroportos (Dijkstra)")
        print(" l) Mostrar grau dos aeroportos")
        print(" m) Verificar se o grafo e Euleriano")
        print(" n) Colorir grafo usando algoritmo guloso")
        print(" o) Gerar Arvore Geradora Minima (Kruskal)")
        print("=" * 60)

        opcao = input("Escolha uma opcao: ").lower().strip()

        if opcao == "a":
            grafo_lido = ler_arquivo("grafo.txt")
            if grafo_lido:
                meu_grafo = grafo_lido

        elif opcao == "b":
            if meu_grafo.n == 0:
                print("\n[Aviso] O grafo esta vazio. Nao ha dados para gravar.")
            else:
                gravar_arquivo(meu_grafo, "grafo.txt")

        elif opcao == "c":
            codigo = input("Digite o codigo do novo aeroporto (ex: VCP): ").upper().strip()
            novo_id = meu_grafo.insere_vertice(codigo, 0)
            print(f"\n[Sucesso] Aeroporto {codigo} inserido com o ID [{novo_id}].")

        elif opcao == "d":
            try:
                u = int(input("Digite o ID do aeroporto de origem: "))
                v = int(input("Digite o ID do aeroporto de destino: "))
                peso = int(input("Digite a distancia em km (peso): "))

                if not meu_grafo.vertice_valido(u) or not meu_grafo.vertice_valido(v):
                    print("\n[Erro] IDs de aeroportos invalidos.")
                elif u == v:
                    print("\n[Erro] Nao e permitido criar rotas para o mesmo aeroporto (laco).")
                else:
                    sucesso = meu_grafo.insereA(u, v, peso)
                    if sucesso:
                        print(f"\n[Sucesso] Rota entre [{u}] e [{v}] ({peso}km) criada!")
                    else:
                        print("\n[Aviso] Essa rota ja existe no grafo.")
            except ValueError:
                print("\n[Erro] Por favor, digite apenas numeros inteiros para IDs e distancias.")

        elif opcao == "e":
            try:
                v = int(input("Digite o ID do aeroporto que deseja remover: "))
                sucesso = meu_grafo.remove_vertice(v)
                if sucesso:
                    print(f"\n[Sucesso] Aeroporto [{v}] e todas as suas rotas foram removidos.")
                else:
                    print(f"\n[Erro] Aeroporto [{v}] nao encontrado ou ja removido.")
            except ValueError:
                print("\n[Erro] Por favor, digite um numero inteiro valido.")

        elif opcao == "f":
            try:
                u = int(input("Digite o ID do aeroporto de origem da rota: "))
                v = int(input("Digite o ID do aeroporto de destino da rota: "))

                sucesso = meu_grafo.removeA(u, v)
                if sucesso:
                    print(f"\n[Sucesso] A rota entre [{u}] e [{v}] foi removida.")
                else:
                    print("\n[Erro] Rota nao encontrada entre esses aeroportos.")
            except ValueError:
                print("\n[Erro] Por favor, digite apenas numeros inteiros.")

        elif opcao == "g":
            mostrar_arquivo("grafo.txt")

        elif opcao == "h":
            if meu_grafo.n == 0:
                print("\n[Aviso] O grafo esta vazio. Tente ler o arquivo primeiro (Opcao 'a').")
            else:
                meu_grafo.show()

        elif opcao == "i":
            if meu_grafo.n == 0:
                print("\n[Aviso] O grafo esta vazio.")
            else:
                status = meu_grafo.verifica_conexidade()
                print(f"\n[Analise] O grafo atual e: {status}")

        elif opcao == "j":
            print("\nEncerrando a aplicacao. Ate logo!")
            break

        elif opcao == "k":
            if meu_grafo.n == 0:
                print("\n[Aviso] O grafo esta vazio. Tente ler o arquivo primeiro (Opcao 'a').")
            else:
                try:
                    origem = int(input("Digite o ID do aeroporto de origem: "))
                    destino = int(input("Digite o ID do aeroporto de destino: "))
                    meu_grafo.dijkstra(origem, destino)
                except ValueError:
                    print("\n[Erro] Digite apenas numeros inteiros para os IDs.")

        elif opcao == "l":
            if meu_grafo.n == 0:
                print("\n[Aviso] O grafo esta vazio. Tente ler o arquivo primeiro (Opcao 'a').")
            else:
                meu_grafo.mostrar_graus()

        elif opcao == "m":
            if meu_grafo.n == 0:
                print("\n[Aviso] O grafo esta vazio. Tente ler o arquivo primeiro (Opcao 'a').")
            else:
                meu_grafo.verifica_euleriano()

        elif opcao == "n":
            if meu_grafo.n == 0:
                print("\n[Aviso] O grafo esta vazio. Tente ler o arquivo primeiro (Opcao 'a').")
            else:
                meu_grafo.coloracao_gulosa()

        elif opcao == "o":
            if meu_grafo.n == 0:
                print("\n[Aviso] O grafo esta vazio. Tente ler o arquivo primeiro (Opcao 'a').")
            else:
                meu_grafo.kruskal()

        else:
            print(f"\n[Aviso] A opcao '{opcao}' e invalida.")


if __name__ == "__main__":
    main()
