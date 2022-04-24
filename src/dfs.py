class Vertice:
    def __init__(self, cor, endereco, predecessor, distancia):
        self.cor = cor
        self.endereco = endereco
        self.predecessor = predecessor
        self.distancia = distancia

class Grafo:
    def __init__(self, vertices):
        self.vertices = vertices

def busca_profundidade(grafo, vertice_fonte, visitados):
    visitados.add(vertice_fonte)
    falta_visitar = [vertice_fonte]
    while falta_visitar:
        vertice = falta_visitar.pop()
        for vizinho in grafo[vertice]:
            if vizinho not in visitados:
                visitados.add(vizinho)
                falta_visitar.append(vizinho)