import graphs

#Test funzionamento Grafi_1
Grafo_1 = graphs.DirectedGraph('mappa_ipad_1', 1)
Grafo_1.auto_add_nodes(3)
Grafo_1.add_edges(*[(1, 6)])

Grafo_1.add_edges(*[(1, 6), (2, 1), (3, 5), (1, 4), (3, 6), (4, 5)])
Grafo_1.add_edges(*[(2, 4)],**{'weight' : 16})
Grafo_1.add_edges(*[(2, 4)],**{'weight' : 2})
Grafo_1.add_edges(*[(4, 3)], **{'weight' : 3})
Grafo_1.add_edges(*[(6, 2)], **{'weight' : 4})
Grafo_1.add_edges(*[(2, 6)], **{'weight' : 4})
Grafo_1.print_info()