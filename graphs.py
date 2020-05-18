from copy import deepcopy
import numpy
from scipy.sparse import dok_matrix
from math import sqrt
import pickle as pkl

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
        self.default_weight = default_weight
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
        return (max_id - N + 1)



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



    def compute_adjacency(self, typeSparsa = True):
        '''costruisce la matrice di adiacenza sparsa(se non viene specificato nulla o True), densa se settata False'''
        N, _ = self.size()
        if typeSparsa:
            A = dok_matrix((N,N))
        else:
            A = numpy.identity(N)
        edge_list = self.get_edges()
        labels_list = self.get_edge_labels(edge_list)
        i = 0
        for node_1 in self.nodes:
            j = 0
            for  node_2 in self.nodes:
                if (node_1, node_2) in edge_list:
                    index = edge_list.index((node_1,node_2))
                    A[i, j] = labels_list[index]['weight']
                else:
                    A[i, j] = 0
                j += 1
            i += 1    
        return A           



    def add_from_adjacency(self,A_s):
        '''Aggiunge nuovi nodi al grafo e li collega tra loro secondo la matrice A'''
        A = dok_matrix(A_s)#sparsizza
        A = A_s
        N, _ = A.get_shape()
        id = self.auto_add_nodes(N)
        for edge in A.keys():
            self.add_edges([(edge[0] + id, edge[1] + id)], **{'weight' : A[edge]})



    def add_graph(self, new_graph):
        '''Dato un nuovo Grafo, lo connette a quello attuale; se i nodi sono già esistenti si aggirnano solo le connessioni'''
        new_edges = new_graph.get_edges()
        new_edges_lables = new_graph.get_edge_labels(new_edges)#idea di implementare un default?    
        for i in range(len(new_edges)):

            self.add_edges([new_edges[i]], **new_edges_lables[i])



    def save(self, percorso_file, folder_name = self.name):
        '''Genera una cartella all' interno del percorso_file contenente info sul grafo'''
        lista_id_nodi=[]
        for node in self.nodes.keys():
            lista_id_nodi.append(node)

        A = self.compute_adjacency(True)

        ### Cartella = file contenente altri file (?)
        with open(percorso_file, 'wb') as folder_name:
            ### Primo file: lista dei nodi
            id_list_pkl = open(percorso_file, 'wb')
            pkl.dump(lista_id_nodi, id_list_pkl)
            id_list_pkl.close()

            ### Secondo file: matrice di adiacenza salvata come dictionary of keys
            adjacency_pkl = open(percorso_file, 'wb')
            pkl.dump(dict(A), adjacency_pkl)
            adjacency_pkl.close()

            ### Terzo file: dizionario a 3 chiavi(nome,peso di default,dizionario etichette dei nodi{ik:vk.labels})
            node_labels = {self.nodes.keys() : self.nodes.labels}
            diz_attributi = {'name' : self.name, 'default_weight' : self.default_weight, 'node_labels' : node_labels}
            attributes_pkl = open(percorso_file, 'wb')
            pkl.dump(diz_attributi, attributes_pkl)
            attributes_pkl.close()

            ### Quarto file: dizionario delle etichette dei lati (tranne il peso)
            keys = []
            values = []
            for edge in self.get_edges():
                keys.append(edge)
                label = self.get_edge_labels(edge)
                label.pop('weight')
                values.append(label)
            diz_edge_labels = {keys : values}
            edge_labels_pkl = open(percorso_file, 'wb')
            pkl.dump(diz_edge_labels, edge_labels_pkl)
            edge_labels_pkl.close()

        ####### I NOMI DEI 4 FILE LI HO MESSI COME "NOME_PKL INVECE CHE NOME.PKL SE NO MI DA ERRORE"
        #### MANCA SECONDA PARTE DEL SUGGERIMENTO



    def add_from_files(self, percorso_file):
        '''Aggiunge al grafo G il grafo G' dalla cartella'''
        ###Memorizzo le info dal file
        with open(percorso_file, 'rb') as file:
            id_list_pkl = open('id_list_pkl', 'rb')
            node_list = pkl.load(id_list_pkl)
            id_list_pkl.close()

            adjacency_pkl = open('adjacency_pkl', 'rb')
            A_diz = pkl.load('adjacency_pkl')
            adjacency_pkl.close()

            attributes_pkl = open('attributes_pkl', 'rb')
            G_prime_attributes = pkl.load('attributes_pkl')
            attributes_pkl.close()

            edge_labels_pkl = open('adjacency_pkl', 'rb')
            G_prime_edge_labels = pkl.load('edge_labels_pkl')
            edge_labels_pkl.close()

        for node in node_list:
            self.add_nodes(node,G_prime_attributes['node_labels'][node])
        for edge in G_prime_edge_labels:
            self.add_edges(edge, G_prime_edge_labels['edge'])
            self.add_edges(edge,A_diz[edge])  ### c' e' di sicuro un modo piu furbo con update del dizionario edge labels



    def print_info(self):
        '''Stampa informazioni sul grafo'''
        for id_node in self.nodes:
            self.nodes[id_node].print_nodes_info()

##############################################################################################