import networkx as nx
import matplotlib.pyplot as plt
import random
from metrix import *


def diff(list1, list2):
	for i in range(len(list2)):
		if list2[i] in list1:
			list1.remove(list2[i])		
	return list1
        

def addTransaction(DG,sender, receiver):
	#one to one transaction
	if isinstance(sender, int):
		if isinstance(receiver, int):
			DG.add_edge(sender,receiver)
		else:
			#batched transaction
			for j in range(len(receiver)):
				DG.add_edge(sender,receiver[j])
	else:
		#multi input transaction
		for i in range(len(sender)):
			if isinstance(receiver, int):
				DG.add_edge(sender[i],receiver)
			else:
				#multi input and multi output transaction
				for j in range(len(receiver)):
					DG.add_edge(sender[i],receiver[j])


def init(DG):
	node = []
	for i in range(len(list(DG))):
		node.append([])
		node[i].append(list(DG)[i])
		node[i].append(0)
		
	outDegreeNode = node[:]
	inDegreeNode = node[:]
	singleOutputNode = []
	doubleOutputNode = []
	singleInputNode = []
	doubleInputNode = []
	
	ghostInputNode = random.sample(inDegreeNode, (int(0.26*len(node))))
	inDegreeNode = diff(inDegreeNode, ghostInputNode)
	singleInputNode = random.sample(inDegreeNode, (int(0.63*len(node))))
	inDegreeNode = diff(inDegreeNode, singleInputNode)
	doubleInputNode = random.sample(inDegreeNode, (int(0.05*len(node))))
	inDegreeNode = diff(inDegreeNode, doubleInputNode)
	for i in range(len(inDegreeNode)):
		inDegreeNode[i][1] = 3

	ghostOutputNode = random.sample(outDegreeNode, (int(0.22*len(node))))
	outDegreeNode = diff(outDegreeNode, ghostOutputNode)
	singleOutputNode = random.sample(outDegreeNode, (int(0.25*len(node))))
	outDegreeNode = diff(outDegreeNode, singleOutputNode) 
	doubleOutputNode = random.sample(outDegreeNode, (int(0.5*len(node))))
	outDegreeNode = diff(outDegreeNode, doubleOutputNode)

	return ghostInputNode,singleInputNode,doubleInputNode,inDegreeNode,ghostOutputNode,singleOutputNode,doubleOutputNode,outDegreeNode

def chooseReceiver(singleInputNode, doubleInputNode, multiInputNode):
	rnd = random.randrange(1,4)
	node = 0
	if rnd == 1 and len(singleInputNode) != 0:
		node = random.choice(singleInputNode)
	elif rnd == 2 and len(doubleInputNode) != 0:
		node = random.choice(doubleInputNode)
	elif rnd == 3 and len(multiInputNode) != 0:
		node = random.choice(multiInputNode)
	return node
	
def chooseSender(singleOutputNode, doubleOutputNode, multiOutputNode):
	sender = None
	index = None
	currentList = None
	randomOutput = random.randrange(1,4)	
	if(randomOutput == 1 and len(singleOutputNode) !=0):
		currentList = singleOutputNode
		sender = random.choice(currentList)
		index = 1	
	elif(randomOutput == 2 and len(doubleOutputNode) !=0):
		currentList = doubleOutputNode
		sender = random.choice(currentList)
		index = 2
	elif(randomOutput == 3 and len(multiOutputNode) !=0):
		currentList = multiOutputNode
		sender = random.choice(currentList)
		index = random.randrange(3,8)
	else:
		chooseSender(singleOutputNode, doubleOutputNode, multiOutputNode )
	return sender, index, currentList

def fillGraph(DG):
	x = init(DG)
	#ghostInputNode = x[0]
	singleInputNode = x[1]
	doubleInputNode = x[2]
	multiInputNode = x[3]
	#ghostOutputNode = x[4]
	singleOutputNode = x[5]
	doubleOutputNode = x[6]
	multiOutputNode = x[7]

	while(True):
		while(True):
			data = chooseSender(singleOutputNode, doubleOutputNode, multiOutputNode)
			if(data[0] != None and data[1] != None and data[2] != None):
				break
		sender = data[0]
		index = data[1]
		currentList = data[2]
		for i in range(index):
			while(True):
				receiver = chooseReceiver(singleInputNode, doubleInputNode, multiInputNode)
				if(receiver != 0 and receiver != sender):
					break
			addTransaction(DG, sender[0],receiver[0])
			receiver[1] = receiver[1]+ 1
			if(receiver in singleInputNode and receiver[1] == 1):
				singleInputNode.remove(receiver)
			elif(receiver in doubleInputNode and receiver[1] == 2):
				doubleInputNode.remove(receiver)
		currentList.remove(sender)
		if(len(singleOutputNode) == 0 and len(doubleOutputNode) == 0 and len(multiOutputNode) == 0) :
			break




DG = nx.DiGraph()
for i in range(100):
	DG.add_node(i)
fillGraph(DG)
calculateMetrix(DG)
#nx.draw_networkx(MC)
#nx.write_gml(DG, "bitcoin.gml")
#plt.show()
