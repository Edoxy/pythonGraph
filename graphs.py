class DirGraphNode:
    """Classe dei nodi di un grafo"""

    def __init__(self, id = None, **labels):
        """Costruttore della classe"""
        self.id = id #ID del nodo
        self.labels = labels.copy() #dizionario degli attributi del nodo
        self.neighbours_out = [] #lista dei nodo out, contiene anche le info sul nodo
        self.neighbours_in = [] #lista dei nodi in

  

    def degrees(self):
        '''Restituisce il grado OUT e IN del nodo scelto'''
        deg_out = 0 
        deg_in = 0
        for x in self.neighbours_out:
            deg_out += 1
        for x in self.neighbours_in:
            deg_out += 1
        return (deg_out, deg_in)



    def get_edge_labels(self, *nodelist):
        '''Restituisce una lista contenente i dizionari dei lati'''
        
        lista_out = []
        
        for new_node in nodelist:
            for x in self.neighbours_out:
                if (new_node.id == x[0].id):
                    lista_out.append(x[1])
        return lista_out 



    def add_neighbours_out(self, *node_list, **edge_labels):
        """Aggiunge un elenco di nodi che si collegano OUT"""

    #Controllo presenza del nodo
        for new_node in node_list:
            found = 0
            for x in self.neighbours_out:
                if (x[0].id == new_node.id):  #se il nodo è già presente controllo sugli id
                    x[1] = edge_labels.copy()
                    found = 1
            if (found == 0): #se il nodo non è presente in tutta la lista
                new_edge_labels = edge_labels.copy()
                self.neighbours_out.append((new_node, new_edge_labels)) #aggiunta della tupla alla lista
            
  

    def add_neighbours_in(self, *node_list):
        """Aggiunge un elenco di nodi che si collegano IN"""
        for new_node in node_list:
            found = 0
            for x in self.neighbours_out:
                if (x[0].id == new_node.id):  #se il nodo è già presente controllo sugli id
                    found = 1
            if (found == 0): #se il nodo non è presente in tutta la lista allora si aggiunge
                self.neighbours_in.append(new_node)



    def rmv_neighbours_out(self, *node_list):
        for node in node_list:
            for x in self.neighbours_out:
                if (x[0].id == node.id):
                    self.neighbours_out.remove(x)
                


    def rmv_neighbours_in(self, *node_list):
        for node in node_list:
            for x in self.neighbours_in:
                if (x.id == node.id):
                    self.neighbours_in.remove(x)



    def print_nodes_info(self):
        """stampa dei valore dei nodi neighbours"""

        print('NODI IN nel nodo id:', self.id)
        for x in self.neighbours_in:
            print(x.id)

        print('NODI OUT nel nodo id:', self.id)
     
        for x in self.neighbours_out:
            print(x[0].id, ' ', x[1])

#############################################################################################

class DirectedGraph:
    """Classe del grafo orientato"""



    def __init__(self, name, default_weight):
        '''Costruttore classe grafo orientato'''
        self.name = name
        self.default_weight =default_weight
        self.nodes = {} #dizionario{id : oggetto}



    def add_nodes(self, *new_nodes_id, **labels):
        """Aggiunge nodi"""
        #controllo nodi
        for id in new_nodes_id:
            if id in self.nodes:
                self.nodes[id].labels = labels.copy() #modifica dei labels già esistenti
            else:
                self.nodes[id] = DirGraphNode(id, labels.copy()) #creazione di un nuovo nodo


    def auto_add_nodes(self, N, **labels):
        '''Aggiunge automaticamente N nodi generando gli id'''
        #ricerca del max id
        max_id = 0
        for id in set(self.nodes): #crea insieme delle chiavi di self.nodes
            if id > max_id:
                max_id = id #memorizza il max
        for i in range(N): #crea nuovi oggetti con id sequenziale partendo dal max
            max_id += 1
            self.nodes[max_id] = DirGraphNode(max_id)
            self.nodes[max_id].labels = labels.copy()



    def add_edges(self, *edge_id_list, **edge_labels):
        '''Aggiunge lati ai nodi presenti nell'elenco o se necessario ne crea di nuovi
        *edge_list = lista di tuple di id dei nodi
        '''
        #controllo che il peso sia presente tra le etichette
        if 'weight' not in edge_labels:
            edge_labels['weight'] = self.default_weight
       
        for id_edge in edge_id_list:
             #verifica esistenza nodi
            if id_edge[0] not in self.nodes:   #verifica presenza del primo   
                self.nodes[id_edge[0]] = DirGraphNode(id_edge[0])
            elif id_edge[1] not in self.nodes: #verifica presenza secondo nodo
                self.nodes[id_edge[1]] = DirGraphNode(id_edge[1])

            #verifica esistenza edge out, così posso già cambiare il dizionario

            found = False
            for n_out in self.nodes[id_edge[0]].neighbours_out:
                #contollo se edge1 compare nella lista out di edge0
                if n_out[0].id == id_edge[1]:
                    found = True
                    #n_out[1] = edge_labels.copy()
            #chiama i costruttori del lato in ambo i sensi
            if not found:
                self.nodes[id_edge[0]].add_neighbours_out(*[self.nodes[id_edge[1]]], **edge_labels.copy())
                self.nodes[id_edge[1]].add_neighbours_in(*[self.nodes[id_edge[0]]])
                    


    def rmv_nodes(self, *node_id_list):
        '''Rimuove i nodi dal grafico con gli id specificati'''

    def print_info(self):
        '''Stampa informazioni sul grafo'''
        for id_node in self.nodes:
            self.nodes[id_node].print_nodes_info()


'''
#prova dei nodi
#step 1
labels = {'colore' : 'giallo'}
nodo_1 = DirGraphNode(1, **labels)
nodo_2 = DirGraphNode(2)
nodo_3 = DirGraphNode(3, **{'colore' : 'blu'})

nodo_1.add_neighbours_in(*[nodo_2, nodo_3])
nodo_1.add_neighbours_out(*[nodo_2], **{'weight' : 4})
nodo_2.add_neighbours_in(*[nodo_3, nodo_1])
nodo_2.add_neighbours_out(*[nodo_1], **{'weight' : 4})
nodo_3.add_neighbours_out(*[nodo_1], **{'weight' : 2})
nodo_3.add_neighbours_out(*[nodo_2], **{'weight' : 3})

#verifica dei nodi in
nodo_1.print_nodes_info()
nodo_2.print_nodes_info()
nodo_3.print_nodes_info()

#step2
print('\nFase 2')
nodo_3.rmv_neighbours_out(*[nodo_2])
nodo_2.rmv_neighbours_in(*[nodo_3])
nodo_3.add_neighbours_in(*[nodo_2])
nodo_2.add_neighbours_out(*[nodo_3], **{'weight' : 1})

#verifica dei nodi in
nodo_1.print_nodes_info()
nodo_2.print_nodes_info()
nodo_3.print_nodes_info()
'''
#Test funzionamento Grafi
Grafo_1 = DirectedGraph('mappa_ipad_1', 1)
Grafo_1.auto_add_nodes(3)
Grafo_1.add_edges(*[(1, 6)])

Grafo_1.add_edges(*[(1, 6), (2, 1), (3, 5), (1, 4), (3, 6), (4, 5)])
Grafo_1.add_edges(*[(2, 4)],**{'weight' : 2})
Grafo_1.add_edges(*[(4, 3)], **{'weight' : 3})
Grafo_1.add_edges(*[(6, 2), (2, 6)], **{'weight' : 4})
Grafo_1.print_info()