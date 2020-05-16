from copy import deepcopy

class DirGraphNode:
    """Classe dei nodi di un grafo"""

    def __init__(self, id = None, **labels):
        """Costruttore della classe"""
        self.id = id #ID del nodo
        self.labels = labels.copy() #dizionario degli attributi del nodo
        self.neighbours_out = [] #lista dei nodo out, contiene anche le info sul nodo
        self.neighbours_in = [] #lista dei nodi in



    def get_neighbours(self):
        '''Restituisce lista di vicini del nodo'''
        n_out = []
        n_in = []

        for x in self.neighbours_out:
            n_out.append(x[0])
        for x in self.neighbours_in:
            n_in.append(x)
        
        return (n_out, n_in)



    def degrees(self):
        '''Restituisce il grado OUT e IN del nodo scelto'''
        deg_out = 0 
        deg_in = 0
        for x in self.neighbours_out:
            deg_out += 1
        for x in self.neighbours_in:
            deg_in += 1
        return (deg_out, deg_in)



    def get_edge_labels(self, node_list):
        '''Restituisce una lista contenente i dizionari dei lati'''
        
        lista_out = []
        
        for node in node_list:
            for x in self.neighbours_out:
                if (node.id == x[0].id):
                    lista_out.append(x[1])
        return lista_out 



    def add_neighbours_out(self, node_list, **edge_labels):
        """Aggiunge un elenco di nodi che si collegano OUT"""

        neighbours_out, _ = self.get_neighbours()
        for node in node_list:
            if node not in neighbours_out: #viene eseguito solo se il nodo non è già presente
                self.neighbours_out.append((node, edge_labels.copy()))
            else: #uso index per trovare l'indice della posizione del nodo che cerchiamo
                ind_node = neighbours_out.index(node)
                self.neighbours_out[ind_node][1].update(edge_labels)
           
  

    def add_neighbours_in(self, node_list):
        """Aggiunge un elenco di nodi che si collegano IN"""
        for node in node_list:
            if node not in self.neighbours_in:
                self.neighbours_in.append(node)
            else :
                print('il nodo è già presente')#vedere come fare i warning



    def rmv_neighbours_out(self, node_list):
        for node in node_list:
            neighbours_out, _ = self.get_neighbours()
            if node in neighbours_out:
                ind_node = neighbours_out.index(node)
                self.neighbours_out.remove(self.neighbours_out[ind_node])



    def rmv_neighbours_in(self, node_list):
        for node in node_list:
            if node in self.neighbours_in:
                self.neighbours_in.remove(node)



    def print_nodes_info(self):
        """stampa dei valore dei nodi neighbours"""

        print('Archi in ingresso nel nodo id:', self.id)
        for x in self.neighbours_in:
            print(x.id)

        print('Archi in uscita dal nodo id:', self.id)
     
        for x in self.neighbours_out:
            print(x[0].id, ' ', x[1])

#############################################################################################

class DirectedGraph:
    """Classe del grafo orientato"""



    def __init__(self, name = 'Nuovo Grafo', default_weight = 1, Id_list = []):
        '''Costruttore classe grafo orientato'''
        self.name = name
        self.default_weight =default_weight
        self.nodes = {} #dizionario{id : oggetto}
        self.add_nodes(Id_list)



    def add_nodes(self, new_nodes_id, **labels):
        """Aggiunge nodi"""
        #controllo nodi
        for id in new_nodes_id:
            if id in self.nodes:
                self.nodes[id].labels.update(labels) #modifica dei labels già esistenti
            else:
                self.nodes[id] = DirGraphNode(id, **labels.copy()) #creazione di un nuovo nodo



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



    def add_edges(self, edge_id_list, **edge_labels):
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
            if id_edge[1] not in self.nodes: #verifica presenza secondo nodo
                self.nodes[id_edge[1]] = DirGraphNode(id_edge[1])

            #verifica esistenza edge out, così posso già cambiare il dizionario

            neighbours_out, _ = self.nodes[id_edge[0]].get_neighbours()
            if self.nodes[id_edge[1]] not in neighbours_out:
                self.nodes[id_edge[0]].add_neighbours_out([self.nodes[id_edge[1]]], **edge_labels.copy())
                self.nodes[id_edge[1]].add_neighbours_in([self.nodes[id_edge[0]]])
            else:
                ind_node = neighbours_out.index(self.nodes[id_edge[1]])
                self.nodes[id_edge[0]].neighbours_out[ind_node][1].update(edge_labels)
                    


    def rmv_nodes(self, node_id_list):
        '''Rimuove i nodi dal grafico con gli id specificati'''
        lista_edges = []
        for id in node_id_list:
            if id in self.nodes:
                for x in self.nodes[id].neighbours_out:
                    lista_edges.append((id, x[0].id))
                for x in self.nodes[id].neighbours_in:
                    lista_edges.append((x.id, id))
        self.rmv_edges(lista_edges)
        for id in node_id_list:
                del self.nodes[id]
        


    def rmv_edges(self, edge_id_list):
        '''Rimuove i lati con gli id specificati'''
        for id in edge_id_list:
            #controllo esistenza dei 2 nodi
            if id[0] in self.nodes:
                if id[1] in self.nodes:
                    self.nodes[id[0]].rmv_neighbours_out([self.nodes[id[1]]])
                    self.nodes[id[1]].rmv_neighbours_in([self.nodes[id[0]]])

    
    def get_edges(self):
        '''Restituisce tutti i lati del grafo in una lista come tuple di id'''
        edge_list = []
        for x in self.nodes:
            #creo lista di successori di x
            neighbours_out, _ = self.nodes[x].get_neighbours()
            for y in neighbours_out:
                edge_list.append((x, y.id))
        return (edge_list)        



    def get_edge_labels(self, edge_list):
        '''Restituisce i dizionari dei lati specificati '''
        labels_list = []

        for edge in edge_list:
            #controllo se il primo nodo esiste
            if (edge[0] in self.nodes) & (edge[1] in self.nodes):
                #controllo se il lato esite
                neighbours_out, _ = self.nodes[edge[0]].get_neighbours()

                if self.nodes[edge[1]] in neighbours_out:

                    index = neighbours_out.index(self.nodes[edge[1]])
                    labels_list.append(self.nodes[edge[0]].neighbours_out[index][1])
                else:
                    labels_list.append(None)
            else:
                labels_list.append(None)

        return labels_list                



    def size(self):
        '''Restituisce le dimensioni del grafo'''

        count_nodes = len(self.nodes)
        count_edges = len(self.get_edges())
            
        return (count_nodes,count_edges)   


    def copy(self):
        '''Restituisce una copia del grafo'''
        Graph_Copy = DirectedGraph(self.name, self.default_weight)
        Graph_Copy.nodes = deepcopy(self.nodes)
        return Graph_Copy




    def compute_adjacency(self):

        A = [[]]
        for node_1 in self.nodes:
            for  node_2 in self.nodes:
                if node_2 in self.nodes[node_1].neighbours_out[0]:
                    A[node_1[node_2]] = self.nodes[node_1].neighbours_out[1['weight']]
                else:
                    A[node_1[node_2]] = 0
        return (A)           


    def add_from_adjacency(self,A):
        '''Aggiunge nuovi nodi al grafo e li collega tra loro secondo la matrice A'''





    def print_info(self):
        '''Stampa informazioni sul grafo'''
        for id_node in self.nodes:
            self.nodes[id_node].print_nodes_info()

##############################################################################################