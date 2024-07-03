import copy

import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self._grafo = nx.Graph()
        self._nodi = None
        self._retailers = DAO.getAllRetailers()
        self._idMap = {}
        for r in self._retailers:
            self._idMap[r.Retailer_code] = r

        self._solBest = []
        self._costoBest = 0

    def bestPath(self, N):
        self._solBest = []
        self._costoBest = 0

        parziale = []

        for nodo in self._grafo.nodes:
            parziale.append(nodo)
            self.ricorsione(parziale, N)
            parziale.pop()

        return self._solBest, self._costoBest

    def ricorsione(self, parziale, N):
        #print(f"ricorsione chiamata per nodo {nodo}")
        #print(parziale)

        if len(parziale) == N:
            if parziale[0] in self._grafo.neighbors(parziale[-1]):
                parziale.append(parziale[0])

                if self.calcolaCosto(parziale) > self._costoBest:
                    print("SOLUZIONE TROVATA")
                    self._solBest = copy.deepcopy(parziale)
                    self._costoBest = self.calcolaCosto(parziale)
                parziale.pop() # per poter fare backtracking e non dare alla ricorsione un parziale modificato

            return

        # posso aggiungere altri nodi: ciclo sui vicini del nodo passato alla ricorsione
        for vicino in self._grafo.neighbors(parziale[-1]):
            if vicino not in parziale:
                parziale.append(vicino)
                self.ricorsione(parziale, N)
                parziale.pop()

    def calcolaCosto(self, parziale):
        costo = 0
        for i in range(0, len(parziale) - 1):
            costo += self._grafo[parziale[i]][parziale[i+1]]["weight"]
        print(f"costo = {costo}")
        return costo


    def getAllCountries(self):
        return DAO.getAllCountries()

    def getAllYears(self):
        return DAO.getAllYears()

    def buildGraph(self, country, year):
        self._grafo.clear()

        self._nodi = DAO.getRetailersCountry(country)

        self._grafo.add_nodes_from(self._nodi)

        connessioni = DAO.getConnessioni(country, year, self._idMap)

        for c in connessioni:
            self._grafo.add_edge(c.r1, c.r2, weight=c.peso)


    def getVolumeNodo(self, retailer):
        peso = 0
        vicini = nx.neighbors(self._grafo, retailer)

        for v in vicini:
            peso += self._grafo[retailer][v]["weight"]

        return peso

    def getNodiGrafo(self):
        return list(self._grafo.nodes)

    def getNumNodi(self):
        return len(self._grafo.nodes)

    def getNumArchi(self):
        return len(self._grafo.edges)

