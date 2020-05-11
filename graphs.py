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
        
        return((n_out, n_in))            



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
            for x in self.neighbours_in:
                if (x.id == new_node.id):  #se il nodo è già presente controllo sugli id
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

        print('Archi in ingresso nel nodo id:', self.id)
        for x in self.neighbours_in:
            print(x.id)

        print('Archi in uscita dal nodo id:', self.id)
     
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
            if id_edge[1] not in self.nodes: #verifica presenza secondo nodo
                self.nodes[id_edge[1]] = DirGraphNode(id_edge[1])

            #verifica esistenza edge out, così posso già cambiare il dizionario

            found = False
            for n_out in self.nodes[id_edge[0]].neighbours_out:
                #contollo se edge1 compare nella lista out di edge0
                if n_out[0].id == id_edge[1]:
                    found = True
                    self.nodes[id_edge[0]].rmv_neighbours_out(n_out[0])
                    self.nodes[id_edge[0]].add_neighbours_out(*[self.nodes[id_edge[1]]], **edge_labels.copy())
                                    

            #chiama i costruttori del lato in ambo i sensi
            if not found:
                self.nodes[id_edge[0]].add_neighbours_out(*[self.nodes[id_edge[1]]], **edge_labels.copy())
                self.nodes[id_edge[1]].add_neighbours_in(*[self.nodes[id_edge[0]]])
                    


    def rmv_nodes(self, *node_id_list):
        '''Rimuove i nodi dal grafico con gli id specificati'''
        for id in node_id_list:
             if id in self.nodes:
                 #elimino i lati collegati a id poi elimino id
                 for x in self.nodes[id].neighbours_out:
                     self.nodes[x].rmv_neighbours_in(*[self.nodes[id]])
                 for x in self.nodes[id].neighbours_in:
                     self.nodes[x].rmv_neighbours_out(*[self.nodes[id]])    
                 self.nodes.pop(id)


    def rmv_edges(self, *edge_id_list):
        '''Rimuove i lati con gli id specificati'''
        for id in edge_id_list:
            #controllo esistenza dei 2 nodi
            if id[0] in self.nodes:
                if id[1] in self.nodes:
                    self.nodes[id[0]].rmv_neighbours_out(*[self.nodes[id]])
                    self.nodes[id[1]].rmv_neighbours_in(*[self.nodes[id]])

    
    def get_edges(self):
        '''Restituisce tutti i lati del grafo'''
        edge_list = []
        for x in self.nodes:
            for y in self.nodes[x].neighbours_out:
                edge_list.append((self.nodes[x],self.nodes[y]))
        return (edge_list)        

    def get_edge_labels(self, *edge_list):
        '''Restituisce i dizionari dei lati specificati '''
        labels_list = []

        for new_edge in edge_list:
            if new_edge[0] in self.nodes:
                #controllo se il lato esiste
                found = False
                for x in self.nodes[new_edge[0]].neighbours_out:
                    if x[0].id == new_edge[1]:
                        found = True
                        labels_list.append(x[1])
                    if not found:
                        #se il lato non esiste aggiungo none
                        labels_list.append(None)
        return (labels_list)                


    def size(self):
        '''Restituisce le dimensioni del grafo'''
        count_nodes = 0
        count_edges = 0
        for node in self.nodes:
            count_nodes += 1
            for edge in self.nodes[node].neighbours_out:
                count_edges += 1
        return ((count_nodes,count_edges))   


    def copy(self):
        '''Restituisce una copia del grafo'''
              

    def print_info(self):
        '''Stampa informazioni sul grafo'''
        for id_node in self.nodes:
            self.nodes[id_node].print_nodes_info()

##############################################################################################