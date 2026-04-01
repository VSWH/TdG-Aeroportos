# Victor Sung Woo Hong 10425852
# Mauricio Custódio Vicentini 10426074

import os

class Grafo:
    def __init__(self):
        self.n = 0 
        self.m = 0 
        self.listaAdj = [] 
        self.rotulos = []  

    # c) Inserir vértice
    def insere_vertice(self, rotulo, peso=0):
        self.rotulos.append((rotulo, peso))
        self.listaAdj.append([]) 
        self.n += 1
        return self.n - 1 

    # d) Inserir aresta 
    def insereA(self, v, w, peso):
        for aresta in self.listaAdj[v]:
            if aresta[0] == w:
                return False 
                
        self.listaAdj[v].append((w, peso))
        self.listaAdj[w].append((v, peso))
        self.m += 1 
        return True

    def removeA(self, v, w):
        removido_v = False
        removido_w = False
        
        # Remove w da lista de v
        for aresta in self.listaAdj[v]:
            if aresta[0] == w:
                self.listaAdj[v].remove(aresta)
                removido_v = True
                break
                
        # Remove v da lista de w
        for aresta in self.listaAdj[w]:
            if aresta[0] == v:
                self.listaAdj[w].remove(aresta)
                removido_w = True
                break
                
        if removido_v and removido_w:
            self.m -= 1
            return True
        return False
        
    # e) Remove vértice
    def remove_vertice(self, v):
        if v < 0 or v >= self.n or self.rotulos[v] is None:
            return False
            
        # Remove todas as conexões (como é não orientado, removemos a via de mão dupla)
        # Usamos uma cópia da lista para não dar erro ao iterar e remover ao mesmo tempo
        conexoes = list(self.listaAdj[v])
        for w, peso in conexoes:
            self.removeA(v, w)
                
        # Anula o vértice
        self.rotulos[v] = None
        self.listaAdj[v] = None
        return True
    # i) Verifica Conexidade (Grafo não orientado)
    def verifica_conexidade(self):
        inicio = -1
        ativos = 0
        
        # Encontra o primeiro aeroporto válido para iniciar a verificação
        for i in range(self.n):
            if self.rotulos[i] is not None:
                ativos += 1
                if inicio == -1:
                    inicio = i
                    
        if ativos == 0:
            return "Vazio"
            
        # Busca em Largura (BFS) para contar quantos aeroportos conseguimos visitar
        visitados = set()
        fila = [inicio]
        visitados.add(inicio)
        
        while fila:
            v = fila.pop(0)
            for w, peso in self.listaAdj[v]:
                if w not in visitados:
                    visitados.add(w)
                    fila.append(w)
                    
        # Se visitamos todos os ativos, o grafo é conexo!
        if len(visitados) == ativos:
            return "CONEXO"
        else:
            return "DESCONEXO"
    # h) Mostrar grafo
    def show(self):
        print(f"\nGrafo (n: {self.n}, m: {self.m})")
        for i in range(self.n):
            if self.rotulos[i] is None:
                continue # Pula vértices removidos
                
            apelido = self.rotulos[i][0]
            print(f"[{i:2d}] {apelido:^5}: ", end="")
            
            if not self.listaAdj[i]:
                print("(sem conexões)", end="")
            else:
                conexoes = [f"-> {w}({peso}km)" for w, peso in self.listaAdj[i]]
                print(", ".join(conexoes), end="")
            print()
        print("\nFim da impressao do grafo.\n")


def ler_arquivo(nome_arquivo="grafo.txt"):
    grafo = Grafo() 
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
            linhas = [linha.strip() for linha in linhas if linha.strip()]
            
            tipo_grafo = int(linhas[0]) 
            n = int(linhas[1]) 
            linha_atual = 2
            
            # Lendo Vértices
            for _ in range(n):
                partes = linhas[linha_atual].split('"') 
                id_vertice = int(partes[0].strip())
                rotulo = partes[1].strip()
                peso_vertice = int(partes[2].strip())
                
                grafo.insere_vertice(rotulo, peso_vertice)
                linha_atual += 1
                
            m = int(linhas[linha_atual]) 
            linha_atual += 1
            
            # Lendo Arestas
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
        print(f"\n[ERRO] O arquivo '{nome_arquivo}' não foi encontrado.")
        return None
    except Exception as e:
        print(f"\n[ERRO] Falha ao processar o arquivo: {e}")
        return None

def gravar_arquivo(grafo, nome_arquivo="grafo.txt"):
    try:
        with open(nome_arquivo, 'w', encoding='utf-8') as f:
            f.write("2\n") # Tipo 2: Grafo não orientado
            
            # Grava os vértices (mantendo os removidos como placeholders para não quebrar IDs)
            f.write(f"{grafo.n}\n")
            for i in range(grafo.n):
                if grafo.rotulos[i] is None:
                    f.write(f'{i} "REMOVIDO" 0\n')
                else:
                    apelido = grafo.rotulos[i][0]
                    peso = grafo.rotulos[i][1]
                    f.write(f'{i} "{apelido}" {peso}\n')
                    
            # Grava as arestas
            arestas_gravadas = set()
            f.write(f"{grafo.m}\n")
            
            for u in range(grafo.n):
                if grafo.listaAdj[u] is not None:
                    for v, peso in grafo.listaAdj[u]:
                        # Como é não orientado, ordenamos (u, v) para evitar gravar ida e volta
                        aresta_unica = tuple(sorted((u, v)))
                        if aresta_unica not in arestas_gravadas:
                            f.write(f"{u} {v} {peso}\n")
                            arestas_gravadas.add(aresta_unica)
                            
        print(f"\n[SUCESSO] Grafo salvo com sucesso no arquivo '{nome_arquivo}'.")
    except Exception as e:
        print(f"\n[ERRO] Falha ao gravar o arquivo: {e}")


def mostrar_arquivo(nome_arquivo="grafo.txt"):
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as f:
            linhas = f.readlines()
            
        if not linhas:
            print("\n[Aviso] O arquivo está vazio.")
            return
            
        linhas = [linha.strip() for linha in linhas if linha.strip()]
        tipo = int(linhas[0])
        n = int(linhas[1])
        
        print("\n" + "="*50)
        print(f"      CONTEÚDO DO ARQUIVO: {nome_arquivo}      ")
        print("="*50)
        print(f" Tipo do Grafo : {tipo} (Não Orientado com Peso)")
        print(f" Qtd. Vértices : {n}")
        print("-" * 50)
        
        linha_atual = 2
        for _ in range(n):
            print(f" Vértice -> {linhas[linha_atual]}")
            linha_atual += 1
            
        m = int(linhas[linha_atual])
        print("-" * 50)
        print(f" Qtd. Arestas  : {m}")
        print("-" * 50)
        linha_atual += 1
        
        for _ in range(m):
            print(f" Aresta  -> {linhas[linha_atual]}")
            linha_atual += 1
            
        print("="*50 + "\n")
        
    except FileNotFoundError:
        print(f"\n[ERRO] O arquivo '{nome_arquivo}' não foi encontrado.")
    except Exception as e:
        print(f"\n[ERRO] Falha ao ler o arquivo: {e}")

def main():
    meu_grafo = Grafo()
    
    while True:
        print("\n" + "="*60)
        print("ANALISADOR DO SCENÁRIO DE AVIAÇÃO NO BRASIL(ODS 9)")
        print("="*60)
        print(" a) Ler dados do arquivo grafo.txt")
        print(" b) Gravar dados no arquivo grafo.txt")
        print(" c) Inserir vértice")
        print(" d) Inserir aresta")
        print(" e) Remove vértice")
        print(" f) Remove aresta")
        print(" g) Mostrar conteúdo do arquivo")
        print(" h) Mostrar grafo")
        print(" i) Apresentar a conexidade do grafo")
        print(" j) Encerrar a aplicação")
        print("="*60)
        
        opcao = input("Escolha uma opção: ").lower().strip()
        
        if opcao == 'a':
            grafo_lido = ler_arquivo("grafo.txt")
            if grafo_lido:
                meu_grafo = grafo_lido 
                
        elif opcao == 'b':
            if meu_grafo.n == 0:
                print("\n[Aviso] O grafo está vazio. Não há dados para gravar.")
            else:
                gravar_arquivo(meu_grafo, "grafo.txt")
            
        elif opcao == 'c':
            if meu_grafo is None:
                print("\n[Erro] O grafo não foi inicializado.")
                continue
            codigo = input("Digite o código do novo aeroporto (ex: VCP): ").upper().strip()
            # O peso do vértice é 0 por padrão no nosso modelo
            novo_id = meu_grafo.insere_vertice(codigo, 0)
            print(f"\n[Sucesso] Aeroporto {codigo} inserido com o ID [{novo_id}].")
            
        elif opcao == 'd':
            try:
                u = int(input("Digite o ID do aeroporto de origem: "))
                v = int(input("Digite o ID do aeroporto de destino: "))
                peso = int(input("Digite a distância em km (peso): "))
                
                if u < 0 or u >= meu_grafo.n or v < 0 or v >= meu_grafo.n:
                    print("\n[Erro] IDs de aeroportos inválidos.")
                elif u == v:
                    print("\n[Erro] Não é permitido criar rotas para o mesmo aeroporto (laço).")
                else:
                    sucesso = meu_grafo.insereA(u, v, peso)
                    if sucesso:
                        print(f"\n[Sucesso] Rota entre [{u}] e [{v}] ({peso}km) criada!")
                    else:
                        print(f"\n[Aviso] Essa rota já existe no grafo.")
            except ValueError:
                print("\n[Erro] Por favor, digite apenas números inteiros para IDs e distâncias.")

        elif opcao == 'e':
            try:
                v = int(input("Digite o ID do aeroporto que deseja remover: "))
                sucesso = meu_grafo.remove_vertice(v)
                if sucesso:
                    print(f"\n[Sucesso] Aeroporto [{v}] e todas as suas rotas foram removidos.")
                else:
                    print(f"\n[Erro] Aeroporto [{v}] não encontrado ou já removido.")
            except ValueError:
                print("\n[Erro] Por favor, digite um número inteiro válido.")
                
        elif opcao == 'f':
            try:
                u = int(input("Digite o ID do aeroporto de origem da rota: "))
                v = int(input("Digite o ID do aeroporto de destino da rota: "))
                
                sucesso = meu_grafo.removeA(u, v)
                if sucesso:
                    print(f"\n[Sucesso] A rota entre [{u}] e [{v}] foi removida.")
                else:
                    print(f"\n[Erro] Rota não encontrada entre esses aeroportos.")
            except ValueError:
                print("\n[Erro] Por favor, digite apenas números inteiros.")

        elif opcao == 'g':
            mostrar_arquivo("grafo.txt")
                
        elif opcao == 'h':
            if meu_grafo.n == 0:
                print("\n[Aviso] O grafo está vazio. Tente ler o arquivo primeiro (Opção 'a').")
            else:
                meu_grafo.show()
                
        elif opcao == 'i':
            if meu_grafo.n == 0:
                print("\n[Aviso] O grafo está vazio.")
            else:
                status = meu_grafo.verifica_conexidade()
                print(f"\n[Análise] O grafo atual é: {status}")
                
        elif opcao == 'j':
            print("\nEncerrando a aplicação. Até logo!")
            break
            
        else:
            print(f"\n[Aviso] A opção '{opcao}' é inválida.")


if __name__ == "__main__":
    main()
