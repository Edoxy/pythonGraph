import graphs
Grafo = graphs.DirectedGraph('grafo_lore', 1)
Grafo.add_edges([(1, 2), (2, 3), (4, 5)])
Grafo.add_edges([(3, 4), (5, 6), (6, 7)], **{'weight': 2})
Grafo.add_edges([(4, 1), (6, 3), (6, 2), (2, 6)], **{'weight': 3})
Grafo.add_edges([(1, 7)], **{'weight': 10})
Grafo.add_edges([(3, 7), (7, 3)], **{'weight': 5})
a, b = Grafo.minpath_dijkstra(1, 7)

print(Grafo.depthtree(7))
Grafo.plot()

# Grafo.plotpath(a)
# print(b)