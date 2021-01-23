import networkx as nx
import random
import matplotlib.pyplot as plt
import sys
import operator
import copy
import os.path
from networkx.drawing import nx_agraph
from numpy import log as ln
from scipy.special import zeta
import collections
import numpy as np
import time
import math

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""" CREATE ERDOS RENY MODEL                                     """
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def createGraph(G):
	#Adiciona os vertices
	for i in range(0, V):
		G.add_node(int(i), state='inactive')

	#Adiciona arestas
	for i in range(0, V):
		for j in range(0, V):
			p = random.random()
			#Cria aresta i -> j
			if (i != j and p > limit):
				edgePositive = random.random()
				edgeNegative = random.random()
				G.add_edge(i,j, weightPositive=edgePositive, weightNegative=edgeNegative, state="null")
			#Cria aresta j -> i
			p = random.random()
			if (i != j and p > limit):
				edgePositive = random.random()
				edgeNegative = random.random()
				G.add_edge(j, i, weightPositive=edgePositive, weightNegative=edgeNegative, state="null")


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""" CREATE POWER LAW BARABASI MODEL                              """
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def createPowerLawGraph():
	G = nx.barabasi_albert_graph(V,m)
	G = G.to_directed()

	#seta state dos vertices
	for i in range(0, V):
		nx.set_node_attributes(G, {i:'inactive'}, 'state')

	#Seta atributo das arestas
	for i in range(0, V):
		for neighbor in G.neighbors(i):
			#Cria aresta i -> j
			edgePositive = random.random()
			edgeNegative = random.random()
			nx.set_edge_attributes(G, {(i,neighbor): 'null'}, 'state')
			nx.set_edge_attributes(G, {(i,neighbor): edgePositive}, 'weightPositive')
			nx.set_edge_attributes(G, {(i,neighbor): edgeNegative }, 'weightNegative')
	return G

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""" CHUNG LU MODEL BY AIELLO WEIGHT                              """
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
def getComponent(G):
	giant = sorted(nx.connected_components(G), key = len, reverse=True)
	return giant[0]

def Aiello(n,b):
	s = []
	if (b > 1):
		z = zeta(b,1)
		eAlpha = (n/z*1.0)
	elif (b == 1):
		eAlpha = math.log(n,2)
	else:
		eAlpha = (n - n*b)**b

	for i in range(1,n+1):
		denominador = i**b
		r = eAlpha/denominador*1.0
		s.append(r)
	print(s)
	return s

def transformWeight(v):
	w = []
	for i in range(len(v)):
		count = 0
		while (count < int(v[i])):
			w.append(i+1)
			count = count + 1
	return w

def sumVector(v):
	sum = 0
	for i in v:
		sum += i
	return sum

def chungLuModel(v):
	G = nx.Graph()
	l_n = sumVector(v)
	for i in range(0,len(v)):
		G.add_node(int(i), w=v[i], state="inactive", percolation=0.001)
	for i in range(0,len(v)):
		for j in range(0,len(v)):
			if (i != j):
				p = random.random()
				p_ij = (G.nodes[i]['w']*G.nodes[j]['w'])/(l_n + G.nodes[i]['w']*G.nodes[j]['w'])
				if (p_ij > p):
					#Adiciona aresta no grafo
					edgePositive = random.random()
					edgeNegative = random.random()
					G.add_edge(i,j)
					nx.set_edge_attributes(G, {(i,j): 'null'}, 'state')
					nx.set_edge_attributes(G, {(i,j): edgePositive}, 'weightPositive')
					nx.set_edge_attributes(G, {(i,j): edgeNegative }, 'weightNegative')
					print("Criou aresta " + str(i) + " " + str(j))
	return G

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""" MAIN                                                         """
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
if __name__ == "__main__":

	#le argumentos
	V = int(sys.argv[1])
	b = float(sys.argv[2])

	#Cria Chung Lu
	s = Aiello(V,b)
	w = transformWeight(s)
	G = chungLuModel(w)
	V = len(w)
	print("Grafo Gerado")

	#get component
	bigComponent = getComponent(G)
	print("PEGOU A MAIOR COMPONENTE")
	for i in range (0,V):
		if i not in bigComponent:
			G.remove_node(i)

	#renomeia os ids, apos os ids
	V = len(bigComponent)
	start = 0
	G = nx.convert_node_labels_to_integers(G,first_label=start)
	print("GEROU O GRAFO FINAL")

	print("Escrevendo Grafo")
	nx.write_edgelist(G, sys.argv[3], data=True)
