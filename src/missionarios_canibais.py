import copy

class Margem():
    def __init__(self, lado: str, n_missionarios=0, n_canibais=0):
        self.n_missionarios = n_missionarios
        self.n_canibais = n_canibais
        self.lado = lado


class Estado():
    def __init__(self, margem_esquerda: Margem, margem_direita: Margem):
        self.margem_esquerda = margem_esquerda
        self.margem_direita = margem_direita


class Barco():
    def __init__(self, margem: str):
        self.margem = margem

    def deslocar(self, estado: Estado, nm=0, nc=0):

        # só pode levar 2 sujeitos no barquinho
        if nm + nc > 2:
            return
        # já transportou o pessoal, não tem mais o que fazer tio
        if estado.margem_esquerda.n_missionarios == 0 and estado.margem_esquerda.n_canibais == 0:
            return

        novo_estado = copy.deepcopy(estado)
        # movimentando o barquinho
        if self.margem == 'esquerda':
            self.margem = 'direita'
            novo_estado.margem_esquerda.n_canibais -= nc
            novo_estado.margem_esquerda.n_missionarios -= nm
            novo_estado.margem_direita.n_canibais += nc
            novo_estado.margem_direita.n_missionarios += nm
            # print(f'movimentou da esquerda pra direita com {nm} missionários e {nc} canibais')
        else:
            self.margem = 'esquerda'
            novo_estado.margem_direita.n_canibais -= nc
            novo_estado.margem_direita.n_missionarios -= nm
            novo_estado.margem_esquerda.n_canibais += nc
            novo_estado.margem_esquerda.n_missionarios += nm
            # print(f'movimentou da direita pra esquerda com {nm} missionários e {nc} canibais')
        return novo_estado


# par ordenado => primeira posição número de missionários, segunda posição número de canibais
# (1 , 0) - um missionário no barco
# (2 , 0) - dois missionários no barco
# (1 , 1) - um missionário e um canibal no barco
# (0 , 1) - um canibal no barco
# (0 , 2) - dois canibais no barco

possibilidades_barco = [(1, 0), (0, 1), (1, 1), (2, 0), (0, 2)]
visitados = []
borda = []

barco = Barco('esquerda')


def sucessores(estado: Estado):
    sucessores = []
    for (i, j) in possibilidades_barco:
        novo_estado = barco.deslocar(estado, i, j)
        if novo_estado is None: continue
        # não pode haver menos missionários do canibais em qualquer uma  das margens
        if (
                novo_estado.margem_esquerda.n_missionarios < novo_estado.margem_esquerda.n_canibais and novo_estado.margem_esquerda.n_missionarios > 0) or (
                novo_estado.margem_direita.n_missionarios < novo_estado.margem_direita.n_canibais and novo_estado.margem_direita.n_missionarios > 0):
            continue
        if novo_estado in visitados: continue
        sucessores.append(novo_estado)
    return sucessores


def adjacenteNaoVisitado(estado: Estado):
    l = sucessores(estado)
    if len(l) > 0:
        return l[0]
    else:
        return -1

# Verifica se o objetivo foi atingido
def testeObjetivo(estado: Estado, n_missionarios, n_canibais):
    return estado.margem_direita.n_missionarios == n_missionarios and estado.margem_direita.n_canibais == n_canibais


def dfs(estadoInicial : Estado):
    borda.append(estadoInicial)
    while len(borda) != 0:
        estado = borda[len(borda) - 1]
        # se atingiu o objetivo, blz, pode parar
        if testeObjetivo(estado, estadoInicial.margem_esquerda.n_missionarios, estadoInicial.margem_esquerda.n_canibais): break
        v = adjacenteNaoVisitado(estado)
        if v == -1:
            borda.pop()
        else:
            visitados.append(v)
            borda.append(v)
    else:
        print("Não encontrei.")
    return borda


def main():
    margem_esquerda = Margem('esquerda', 3, 3)
    margem_direita = Margem('direita', 0, 0)
    estadoInicial = Estado(margem_esquerda, margem_direita)
    solucao = dfs(estadoInicial)
    print(solucao)



if __name__ == '__main__':
    main()