import graphs


Grafo_1 = graphs.DirectedGraph('nome', 2, [1, 2, 4])
Grafo_1.add_nodes([3, 4], **{'color' : 'green'})
Grafo_1.auto_add_nodes(2, **{'color' : 'orange'})

#Test funzionamento Grafi_1
Grafo_1 = graphs.DirectedGraph('mappa_ipad_1', 1)
Grafo_1.auto_add_nodes(3)
Grafo_1.add_edges([(1, 6)])

Grafo_1.add_edges([(1, 6), (2, 1), (3, 5), (1, 4), (3, 6), (4, 5)])
Grafo_1.add_edges([(2, 4)],**{'weight' : 16})
Grafo_1.add_edges([(2, 4)],**{'weight' : 2})
Grafo_1.add_edges([(4, 3)], **{'weight' : 3})
Grafo_1.add_edges([(6, 2)], **{'weight' : 4})
Grafo_1.add_edges([(2, 6)], **{'weight' : 4})

Grafo_1.add_edges([(1, 7), (7, 1)])
Grafo_2 = Grafo_1.copy()

Grafo_1.rmv_nodes([7])
Grafo_1.rmv_edges([(3, 5), (4, 3)])
Grafo_1.print_info()

print(Grafo_1.size())
print(Grafo_1.get_edges())
a =Grafo_1.get_edges()
a.append((1, 7))
print(Grafo_1.get_edge_labels(a))

print(Grafo_2.size())
print(Grafo_2.get_edges())
print(Grafo_2.get_edge_labels(Grafo_2.get_edges()))

print(Grafo_1.compute_adjacency())
