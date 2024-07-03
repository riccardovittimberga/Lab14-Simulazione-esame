
import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self.graph = nx.DiGraph()
        self._nodes = []
        self._edges = []

        self.idMap = {}
        self.solBest=[]

        self._listChromosome = []
        self._listGenes = []
        self._listConnectedGenes = []

        self.loadGenes()
        self.loadChromosome()
        self.loadConnectedGenes()

    def loadChromosome(self):
        self._listChromosome = DAO.getAllChromosomes()

    def loadGenes(self):
        self._listGenes = DAO.getAllGenes()
        self.idMap = {}
        for g in self._listGenes:
            self.idMap[g.GeneID] = g.Chromosome

    def loadConnectedGenes(self):
        self._listConnectedGenes = DAO.getAllConnectedGenes()

    def build_graph(self):
        self.graph.clear()

        for c in self._listChromosome:
            self._nodes.append(c)
        self.graph.add_nodes_from(self._nodes)

        edges = {}
        for g1, g2, corr in self._listConnectedGenes:
            if (self.idMap[g1], self.idMap[g2]) not in edges:
                edges[(self.idMap[g1], self.idMap[g2])] = float(corr)
            else:
                edges[(self.idMap[g1], self.idMap[g2])] += float(corr)
        for k, v in edges.items():
            self._edges.append((k[0], k[1], v))
        self.graph.add_weighted_edges_from(self._edges)

    def searchPath(self, t):

        for n in self.get_nodes():
            partial = []
            partial_edges = []

            partial.append(n)
            self.ricorsione(partial, partial_edges, t)

        print("final", len(self.solBest), [i[2]["weight"] for i in self.solBest])

    def ricorsione(self, partial, partial_edges, t):
        n_last = partial[-1]
        neigh = self.getAdmissibleNeighbs(n_last, partial_edges, t)

        # stop
        if len(neigh) == 0:
            weight_path = self.computeWeightPath(partial_edges)
            weight_path_best = self.computeWeightPath(self.solBest)
            if weight_path > weight_path_best:
                self.solBest = partial_edges[:]
            return

        for n in neigh:
            partial.append(n)
            partial_edges.append((n_last, n, self.graph.get_edge_data(n_last, n)))
            self.ricorsione(partial, partial_edges, t)
            partial.pop()
            partial_edges.pop()

    def getAdmissibleNeighbs(self, n_last, partial_edges, t):
        all_neigh = self.graph.edges(n_last, data=True)
        result = []
        for e in all_neigh:
            if e[2]["weight"] > t:
                e_inv = (e[1], e[0], e[2])
                if (e_inv not in partial_edges) and (e not in partial_edges):
                    result.append(e[1])
        return result

    def computeWeightPath(self, mylist):
        weight = 0
        for e in mylist:
            weight += e[2]['weight']
        return weight
    def count_edges(self, t):
        count_bigger = 0
        count_smaller = 0
        for x in self.get_edges():
            if x[2]['weight'] > t:
                count_bigger += 1
            elif x[2]['weight'] < t:
                count_smaller += 1
        return count_bigger, count_smaller

    def get_nodes(self):
        return self.graph.nodes()

    def get_edges(self):
        return list(self.graph.edges(data=True))

    def get_num_of_nodes(self):
        return self.graph.number_of_nodes()

    def get_num_of_edges(self):
        return self.graph.number_of_edges()

    def get_min_weight(self):
        return min([x[2]['weight'] for x in self.get_edges()])

    def get_max_weight(self):
        return max([x[2]['weight'] for x in self.get_edges()])
