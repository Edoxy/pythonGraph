from copy import deepcopy
import numpy
from scipy.sparse import dok_matrix
from math import sqrt, sin, cos
import pickle as pkl
from matplotlib.pyplot import scatter, plot, text, show, figure, arrow
import os
import heapq
import random

class DirGraphNode:
    """Classe dei nodi di un grafo"""

    def __init__(self, id = None, **labels):
        """Costruttore della classe"""
        self.id = id #ID del nodo
        self.labels = labels.copy() #dizionario degli attributi del nodo
        self.neighbours_out = [] #lista dei nodo out, contiene anche le info sul nodo
        self.neighbours_in = [] #lista dei nodi in



    def get_neighbours(self):
        '''Restituisce lista nodi (oggetti) di vicini del nodo'''
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



    def __init__(self, name = 'Nuovo Grafo', default_weight = 1, Id_list = [], Edge_list = [], Node_diz = {}, Edge_diz = {}):
        '''Costruttore classe grafo orientato'''
        self.name = name
        self.default_weight = default_weight
        self.nodes = {} #dizionario{id : oggetto}
        self.add_nodes(Id_list, **Node_diz)
        self.add_edges(Edge_list, **Edge_diz)



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



    def add_from_adjacency(self, A_s):
        '''Aggiunge nuovi nodi al grafo e li collega tra loro secondo la matrice A'''
        A = dok_matrix(A_s)#sparsizza
        A = A_s
        N, _ = A.get_shape()
        id = self.auto_add_nodes(N)
        for edge in A.keys():
            self.add_edges([(edge[0] + id, edge[1] + id)], **{'weight' : A[edge]})



    def add_graph(self, graph):
        '''Dato un nuovo Grafo, lo connette a quello attuale; se i nodi sono già esistenti si aggirnano solo le connessioni'''
        max_id = self.auto_add_nodes(0) 
        new_graph = graph.copy()
        #aggiungo nodi al grafo
        for node_id in new_graph.nodes:
            new_graph.nodes[node_id].id = max_id + node_id
            self.nodes.update({max_id + node_id : new_graph.nodes[node_id]})



    def save(self, percorso_file, folder_name = None):
        '''Genera una cartella all' interno del percorso_file contenente info sul grafo'''
        if folder_name == None:
            folder_name = self.name
        
        lista_id_nodi=[]
        node_labels = {}
        for node in self.nodes.keys():
            lista_id_nodi.append(node)
            node_labels.update({node : self.nodes[node].labels})


        A = self.compute_adjacency(True)

        ### Creazione Cartella nel percorso
        path = os.path.join(percorso_file, folder_name)
        if not os.path.exists(path):
            os.mkdir(path)

        ### Primo file: lista dei nodi
        id_list = open(path + '\\' + 'id_list.pkl', 'wb')
        pkl.dump(lista_id_nodi, id_list)
        id_list.close()

        ### Secondo file: matrice di adiacenza salvata come dictionary of keys
        adjacency = open(path + '\\' + 'adjacency.pkl', 'wb')
        pkl.dump(dict(A), adjacency)
        adjacency.close()

        ### Terzo file: dizionario a 3 chiavi(nome,peso di default,dizionario etichette dei nodi{ik:vk.labels})

            
        diz_attributi = {'name' : self.name, 'default_weight' : self.default_weight, 'node_labels' : node_labels}
        attributes = open(path + '\\' + 'attributes.pkl', 'wb')
        pkl.dump(diz_attributi, attributes)
        attributes.close()

        ### Quarto file: dizionario delle etichette dei lati (tranne il peso)
            
        diz_edge_labels = {}
        for edge in self.get_edges():
                
            label = self.get_edge_labels([edge])
            del label[0]['weight']
            diz_edge_labels.update({edge : label[0]})
            
        edge_labels = open(path + '\\' + 'edge_labels.pkl', 'wb')
        pkl.dump(diz_edge_labels, edge_labels)
        edge_labels.close()

        
        #### MANCA SECONDA PARTE DEL SUGGERIMENTO



    def add_from_files(self, percorso_file):
        '''Aggiunge al grafo G il grafo G' primo dalla cartella'''
        ###Memorizzo le info dal file

        id_list = open(percorso_file + '\\' + 'id_list.pkl', 'rb')
        node_list = pkl.load(id_list)
        id_list.close()

        adjacency = open(percorso_file + '\\' + 'adjacency.pkl', 'rb')
        A_diz = pkl.load(adjacency)
        adjacency.close()

        attributes = open(percorso_file + '\\' + 'attributes.pkl', 'rb')
        G_prime_attributes = pkl.load(attributes)
        attributes.close()

        edge_labels = open(percorso_file + '\\' + 'edge_labels.pkl', 'rb')
        diz_edge_labels = pkl.load(edge_labels)
        edge_labels.close()

        new_graph = DirectedGraph()

        for node in node_list:
            new_graph.add_nodes([node],**G_prime_attributes['node_labels'][node])

        for edge in diz_edge_labels:
            ind1 = node_list.index(edge[0])
            ind2 = node_list.index(edge[1])
            diz_edge_labels[edge].update({'weight' : A_diz[(ind1, ind2)]})
            new_graph.add_edges([edge], **diz_edge_labels[edge])

        self.add_graph(new_graph)



    def minpath_dijkstra(self, start, finish):
        '''Restituisce 2 tuple: una rappresentante gli ID del cammino minimo e l'altra contenente i pesi'''
        ###Controllo peso
        for labels in self.get_edge_labels(self.get_edges()):
            if labels['weight'] <= 0:
                print('Errore: non tutti i lati hanno peso positivo')
                return None, None
        queue = []
        for x in self.nodes[start].neighbours_out:
            #heappush(h, (5, 'write code'))
            heapq.heappush(queue, (x[1]['weight'], [start, x[0].id], [x[1]['weight']]))
        if len(queue) == 0:
                print('Errore: non esiste nessun cammino tra i due nodi')
                return None, None
        found = False
        while found == False:
            current = heapq.heappop(queue)
            for y in self.nodes[current[1][-1]].neighbours_out:
                if y[0].id not in current[1]:
                    new_weight = current[0] + y[1]['weight']
                    path = current[1].copy()
                    path.append(y[0].id)
                    weights = current[2].copy()
                    weights.append(y[1]['weight'])
                    heapq.heappush(queue, (new_weight, path, weights))
            if len(queue) == 0:
                print('Errore: non esiste nessun cammino tra i due nodi')
                return None, None
            if finish == queue[0][1][-1]:
                found = True
            
        print(queue[0][0])
        return queue[0][1], queue[0][2]
               


    def plot(self):
        '''rappresentazione grafica del grafo'''
        #distribuzione sui punti di una circonferenza
        n_nodi = len(self.nodes)
        step = 1 / n_nodi
        x = []
        y = []
        pos_node_plot = {}

        fig = figure()
        ax = fig.add_subplot(111)

        '''for i in range(n_nodi):
            x.append(cos(step * i * 2 * numpy.pi))
            y.append(sin(step * i * 2 * numpy.pi))'''
        #disegno su cerchi concenrici
        k = 0
        a = 5
        while n_nodi > a:
            k += 1
            a += (5*pow(2, k))
        
        j = 0
        while j < (a - (5*pow(2, k))):
            for z in range(k):
                step = 1 / (5*pow(2, z))
                for i in range(5*pow(2, z)):
                    x.append(0.5 * (z+1) * cos(step * i * 2 * numpy.pi))
                    y.append(0.5 * (z+1) * sin(step * i * 2 * numpy.pi))
                    j += 1
        rimanenti = n_nodi - j
        step = 1 / rimanenti
        for i in range(rimanenti):
            x.append(0.5 * (z+2) * cos(step * i * 2 * numpy.pi))
            y.append(0.5 * (z+2) * sin(step * i * 2 * numpy.pi))


        i = 0
        for id in self.nodes:
            pos_node_plot.update({id : i})
            ax.text(x[i], y[i], str(id), fontsize = 15, bbox=dict(facecolor='white', alpha=0.75))
            i += 1
             
        ax.scatter(x, y, color='darkgreen', marker= "h")

        for edge in self.get_edges():
            x_i = [x[pos_node_plot[edge[0]]], x[pos_node_plot[edge[1]]] - x[pos_node_plot[edge[0]]]]
            y_i = [y[pos_node_plot[edge[0]]], y[pos_node_plot[edge[1]]] - y[pos_node_plot[edge[0]]]]

            ax.arrow(x_i[0], y_i[0], x_i[1], y_i[1], length_includes_head = True, head_width = 0.045, head_length = 0.075)

        show()



    def print_info(self):
        '''Stampa informazioni sul grafo'''
        for id_node in self.nodes:
            self.nodes[id_node].print_nodes_info()



    def plotpath(self, list_id):
        '''rappresentazione grafica del grafo'''
        #distribuzione sui punti di una circonferenza
        n_nodi = len(self.nodes)
        step = 1 / n_nodi
        x = []
        y = []
        pos_node_plot = {}

        fig = figure()
        ax = fig.add_subplot(111)

        #disegno su cerchi concenrici
        k = 0
        a = 5
        while n_nodi > a:
            k += 1
            a += (5*pow(2, k))
        
        j = 0
        while j < (a - (5*pow(2, k))):
            for z in range(k):
                step = 1 / (5*pow(2, z))
                for i in range(5*pow(2, z)):
                    x.append(0.5 * (z+1) * cos(step * i * 2 * numpy.pi))
                    y.append(0.5 * (z+1) * sin(step * i * 2 * numpy.pi))
                    j += 1
        rimanenti = n_nodi - j
        step = 1 / rimanenti
        for i in range(rimanenti):
            x.append(0.5 * (z+2) * cos(step * i * 2 * numpy.pi))
            y.append(0.5 * (z+2) * sin(step * i * 2 * numpy.pi))



        i = 0
        for id in self.nodes:
            pos_node_plot.update({id : i})
            ax.text(x[i], y[i], str(id), fontsize = 15, bbox=dict(facecolor='white', alpha=0.75))
            i += 1
             
        ax.scatter(x, y, color='darkgreen', marker= "h")

        for i in range(len(list_id) - 1):
            x_i = [x[pos_node_plot[list_id[i]]], x[pos_node_plot[list_id[i + 1]]] - x[pos_node_plot[list_id[i]]]]
            y_i = [y[pos_node_plot[list_id[i]]], y[pos_node_plot[list_id[i + 1]]] - y[pos_node_plot[list_id[i]]]]

            ax.arrow(x_i[0], y_i[0], x_i[1], y_i[1], length_includes_head = True, head_width = 0.045, head_length = 0.075)

        show()

##############################################################################################