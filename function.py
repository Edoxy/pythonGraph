import graphs

def load(percorso_file):
    '''Aggiunge il grafo G dalla cartella'''

    graph = graphs.DirectedGraph()
    graph.add_from_files(percorso_file)
    
    return graph