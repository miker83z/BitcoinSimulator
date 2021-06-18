import networkx as nx
import matplotlib.pyplot as plt
import powerlaw
import sys
#from simulator import *

def calculateAverageDegree(G):
	sum = 0
	averageDegree = 0
	averageDegree = nx.average_degree_connectivity(G)
	for value in averageDegree:
		sum = sum + averageDegree[value]
	averageDegree = sum/len(averageDegree)
	return averageDegree

#metrix to check the coherence of values with the real Bitcoin
def calculateMetrix(DG,sequence):
	sumOut = sumIn = singleIn = singleOut = doubleIn = doubleOut = zeroIn = zeroOut = totOut = totIn = 0
	fit = powerlaw.Fit(sequence) 
	print(fit.alpha)
	print("--------------")
	if(1.75<fit.alpha and fit.alpha > 3.5):
		return False
	else:			
		for i in range(1,len(DG)):
			#out degree 
			totOut = totOut + DG.out_degree(i)
			if DG.out_degree(i) ==1 :
				singleOut = singleOut+1
			elif DG.out_degree(i) == 2:
				doubleOut = doubleOut+1
			elif DG.out_degree(i) == 0:
				zeroOut = zeroOut+1
			elif DG.out_degree(i) >2:
				sumOut = sumOut+1
			#in degree
			totIn = totIn + DG.in_degree(i)
			if DG.in_degree(i) == 1 :
				singleIn = singleIn+1
			elif DG.in_degree(i) == 2:
				doubleIn = doubleIn+1
			elif DG.in_degree(i) == 0:
				zeroIn = zeroIn+1
			elif DG.in_degree(i) >2:
				sumIn = sumIn+1 
		print("Transazioni per nodo:")
		print("OutDregree (#numtransaction, #node): zero: "+str(zeroOut)+", single: "+str(singleOut)+", double: "+str(doubleOut)+". multi: "+str(sumOut))
		print("InDegree (#numtransaction, #node): "+str(zeroIn)+", single: "+str(singleIn)+", double: "+str(doubleIn)+". multi: "+str(sumIn))
		print("InDegree medio: "+str(totIn/len(list(DG))))
		print("OutDegree medio: "+str(totOut/len(list(DG)))) 
		print("--------------")
	
		#degree medio main component
		G = nx.to_undirected(DG)
		mainComponents = sorted(nx.connected_components(G), key=len, reverse=True)
		MC = G.subgraph(mainComponents[0])
		print("Net average degree: "+str(calculateAverageDegree(DG)))
		print("MC average degree: "+str(calculateAverageDegree(MC)))
		print("--------------")

		#not implemented for multigraph 
		# #average clustering coefficient
		
		# print("ACC MC: "+str(nx.average_clustering(MC)))
		# print("--------------")
		
		print("ASPL MC: "+str(nx.average_shortest_path_length(MC)))
		S = [DG.subgraph(c).copy() for c in nx.weakly_connected_components(DG)]
		for index,value in enumerate(S):
			try: aspl
			except NameError: aspl = 0
			aspl = aspl + nx.average_shortest_path_length(value)
			if index == (len(S)-1):
				aspl = aspl/len(S)
		print("ASPL: "+str(aspl)) 
		return True


#metrix after the creation of the simulated network
def graphMetrix(DG):
	density = nx.density(DG)
	#print('Density: '+str(density))
	closeness = nx.closeness_centrality(DG)
	#print('Closeness: '+str(closeness))
	#print('--------------')
	#betweenness = nx.betweenness_centrality(DG)
	# print('Betweenness: '+str(betweenness))
	# print('--------------')
	# egoGraph = nx.ego_graph(DG, '77',5)
	# plotGraph(egoGraph)
	# G = nx.DiGraph.to_undirected(DG)
	# cliques_containing_node = nx.cliques_containing_node(G, '77')
	# print("cliques_containing_node"+str(cliques_containing_node))
	# print('----------------------')
	# node_clique_number = nx.node_clique_number(G,'77')
	# print("node_clique_number"+str(node_clique_number))
	# print('----------------------')
	# number_of_cliques = nx. number_of_cliques(G, '77')
	# print("number_of_cliques"+str(number_of_cliques))
	# print('----------------------')
	# k_clique_communiti = k_clique_communities(G, 3)
	# print("k_clique_communities"+str(list(k_clique_communiti)))
	# print('----------------------')
	in_degree = sorted(DG.in_degree(), key=lambda x: x[1], reverse=True)
	out_degree = sorted(DG.out_degree(), key=lambda x: x[1], reverse=True)
	# #it's the equivalent of an adjacency  matrix
	# adjacency_matrix = nx.to_numpy_matrix(DG)
	# df = pd.DataFrame(data=adjacency_matrix.astype(int))
	# df.to_csv('res/outfile.csv', sep=' ', header=True, index=True)
	return density, in_degree, out_degree, density, closeness#, betweenness
	
