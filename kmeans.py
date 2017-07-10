import csv
import editdistance
from random import randint
import numpy as np
import matplotlib.pyplot as plt

in_file = open("C:/Users/acedon/Desktop/hashtagnew1.csv","r")
e = ""
term = 1
maxIter = 500

def DataForm(in_file):
	reader = csv.reader(in_file,delimiter=";")
	formatData = []
	id = []
	hashtags = []

	for row in reader:
		id.append(row[0])
	in_file.close()
	in_file = open("C:/Users/acedon/Desktop/hashtagnew1.csv","r")
	reader = csv.reader(in_file,delimiter=";")
	for row in reader:
		hashtags.append(row[1])
	in_file.close()	

	idsneu = []
	hashtagsneu = []
	i = 0
	for i in range(0,len(hashtags),1):					#Aufspallten der zusammen auftretenden hashtags bei gleichbleibender id 
		temp = hashtags[i].partition(",")
		while (temp[2] != ""):
			idsneu.append(id[i])
			hashtagsneu.append(temp[0])
			temp = temp[2].partition(",")
		
		if (temp[2]== ""):
			idsneu.append(id[i])
			hashtagsneu.append(temp[0])
	
	for i in range(0,len(idsneu),1):
		formatData.append((idsneu[i],hashtagsneu[i]))
	
	return formatData

def filter(list, value):
	for x,y in list:
		if x == value:
			return x,y
	
def Init(formatData): # INIT FUNKTION AUF VARIABLE CLUSTERZAHL ANPASSEN
	c1 = formatData[(randint(0,len(formatData)))]
	c2 = formatData[(randint(0,len(formatData)))]
	c3 = formatData[(randint(0,len(formatData)))]
	c4 = formatData[(randint(0,len(formatData)))]
	
	#SafetyCheck damit nicht 2 Center gleich sind
	while( (c1[1] == c2[1]) | (c1[1] == c3[1]) | (c1[1] == c4[1]) | (c2[1] == c3[1]) | (c2[1] == c4[1]) | (c3[1] == c4[1]) ): 
		if(c1[1] == c2[1]):
			c2 = formatData[(randint(0,len(formatData)))]
		if(c1[1] == c3[1]):
			c3 = formatData[(randint(0,len(formatData)))]
		if(c1[1] == c4[1]):
			c4 = formatData[(randint(0,len(formatData)))]
		if(c2[1] == c3[1]):
			c3 = formatData[(randint(0,len(formatData)))]
		if(c2[1] == c4[1]):
			c4 = formatData[(randint(0,len(formatData)))]
		if(c3[1] == c4[1]):
			c4 = formatData[(randint(0,len(formatData)))]
		
	
	cluster1 = []
	cluster2 = []
	cluster3 = []
	cluster4 = []
	obercluster = []
	center = []
	t1 = ()
	for i in range(0,len(formatData),1):
		ecluster = []
		t1 = formatData[i]
		ecluster.append(editdistance.eval(t1[1],c1[1]))
		ecluster.append(editdistance.eval(t1[1],c2[1]))
		ecluster.append(editdistance.eval(t1[1],c3[1]))
		ecluster.append(editdistance.eval(t1[1],c4[1]))
		m = min(ecluster)
		tempind = ecluster.index(m)
		if tempind == 0:
			cluster1.append(formatData[i])
		if tempind == 1:
			cluster2.append(formatData[i])
		if tempind == 2:
			cluster3.append(formatData[i])
		if tempind == 3:
			cluster4.append(formatData[i])
	
	obercluster.append(cluster1)
	obercluster.append(cluster2)
	obercluster.append(cluster3)
	obercluster.append(cluster4)

	center.append(c1)
	center.append(c2)
	center.append(c3)
	center.append(c4)
	return (obercluster, center, formatData)
	
def NextCenter(obercluster, center, formatData):
	#print("Obercluster NCENTER START", obercluster)
	print("Center NCENTER START", center)
	iter = 0
	newCenters = []
	oldCenter = []
	t = () 
	for i in range(0,len(center),1):

		mitte = 0
		tempEdit = []
		oldCenter.append(center[i])
		cluster = obercluster[i]
		if((len(center)) == 1):
			cluster = obercluster
		found = False
		print("CLUSTER EINZELN", len(center))
		#print("Aktuelles ClusterELEMENT MITTELWERT", cluster)
	#Mittelwert des aktuellen clusters bestimmen
		for i in range(0,len(cluster),1):
			elem = cluster[i]
			#print("CLUSTER EINZELN IIIIIIII", cluster[i])
			#print("ELEM", elem)
			tempEdit.append(editdistance.eval(elem[1],e))
		for i in range(0,len(tempEdit),1):
			mitte = mitte + tempEdit[i]
		mitte = mitte//(len(cluster))
		
		
		
		#Gibt es Hashtag mit mittelwert?? falls Ja ist es das neue center
		for i in range(0,len(formatData),1):
			elem = formatData[i]
			if((editdistance.eval(elem[1],e)) == mitte):
				print("CENTER MIT MITTELWERT:", elem)
				newCenters.append(elem)
				found = True
				break
				
		#Falls Nicht suchen wir nach dem nächst größerem unde dem nächst kleineren und nehmen das bessere von beiden
		#Nächst kleinere
		if(found == False):
			j = mitte
			smallerIter = 0
			smallerC = ()
			while(j >= 0):			
				j = j-1
				for i in range(0,len(formatData),1):    # Falls fehler formatdata zu cluster ändern
					elem = formatData[i]
					if( ( editdistance.eval(elem,e) ) == j ):
						smallerC = elem
						break
				smallerIter = smallerIter -1
				if(smallerC != t):
					break
				
	#nächst größeres          !!!!!!! BIGGERC ERHÄLT NiE EINEN WERT KP WARUM
		if(found == False):
			j = mitte
			tempMaxIter = ( max(tempEdit))
			biggerIter = 0
			biggerC = ()
			while(j <= tempMaxIter ):
				j = j + 1
				for i in range(0,len(formatData),1):     # Falls fehler formatdata zu cluster ändern
					elem = formatData[i]
					if ( (editdistance.eval(elem,e) == j )):
						biggerC = elem
						break
				biggerIter = biggerIter - 1
				if(biggerC != t):
					break
	#checken welches besser ist			
		if( (found == False)):
			if( (abs(smallerIter) >= biggerIter) & (biggerC != t) & ( (len(newCenters))<4 ) ):
				print("BIGGER:", ( max(tempEdit)))
				newCenters.append(biggerC)
				print("SMALLER:", smallerC)
				newCenters.append(smallerC)
			else: 
				print("SMALLER:", smallerC)
				newCenters.append(smallerC)
		#print("NextCenter NEWCENTER1:", newCenters)

	#print("NextCenter NEWCENTER2:", newCenters)
	#verhindern,dass zwei center gleiches hashtag sind!!!!!!!!!
	print("NextCenter NEWCENTER1 ENDE:", newCenters)
	return (newCenters,oldCenter)
	
def ValidateCenter(newCenters,oldCenter):
	#print("NEWCENTERS VAL",newCenters)
	#print("oldCenters VAL", oldCenter)
	i = 0
	workingIndex = [False,False,False,False]
	for i in range(0,len(newCenters),1):
		#print("For StarT")
		elem1 = newCenters[i]
		elem2 = oldCenter[i]
		test = []
		print("TEST",test)
		print("OLDCENTER", elem2)
		print("NEWCENTER", elem1)
		test.append(editdistance.eval(elem1[1],e) )
		test.append(editdistance.eval(elem2[1],e) )
		print("TEST",test)
		if( max(test)- min(test) > term):
			workingIndex[i] = False
		else:
			workingIndex[i] = True
	print(workingIndex)
	return workingIndex

def recompute(newCenters,obercluster,formatData):
	print("recompute newCenter", newCenters)
	elem = NextCenter(obercluster,[newCenters],formatData)
	reCenter = elem[0]
	print("recompute return", reCenter)
	return reCenter

def TerminationCheck(obercluster,newCenters,oldCenter,formatData):

	workingIndex = ValidateCenter(newCenters,oldCenter)
	if(workingIndex == [True,True,True,True]):
		return(obercluster,newCenters,[True])
	else:
		for i in range(0,len(workingIndex),1):
			while(workingIndex[i] != True):
				if(workingIndex[i] == False):
					tempIndex = []
					tempCenter = recompute(newCenters[i],obercluster[i])
					tempValid = ValidateCenter(tempCenter,newCenters[i])
					if(tempValid[0] == True ):
						newCenters[i] = tempCenter
						workingIndex[i] = True
					
					
	
	return(obercluster,newCenters,[True])
	
def clustering(center,formatData):
	obercluster = [[],[],[],[]]
	for j in range(0,len(formatData),1):
		ecluster = [] 
		for i in range(0,len(center),1):
			ecluster.append(editdistance.eval(formatData[j],center[i]))
		m = min(ecluster)
		tempind = ecluster.index(m)
		obercluster[tempind].append(formatData[j])
	oberlen= len(obercluster)
	#print("oberclustertempind", obercluster[tempind] )
	for i in range(0,oberlen,1):
		if(obercluster[i] == []): #!!!!!!!!!!!!!!!!!!!!!PROBLEMpUNKT!!!!!!!!!!!
			del(obercluster[i])
	
	return obercluster

def plotten(center,obercluster):
	e2 = ""
	y =  []
	x = []
	y2 = []
	x2=[]
	print("PLOTT CLUSTER", obercluster)
	for i in range(0,len(obercluster),1):
		temp = obercluster[i]
		for j in range(0,len(obercluster[i]),1):
			#print("TEMP" , temp)
			x.append(temp[j][0])
			y.append(editdistance.eval(temp[j][1],e2))

	for i in range(0,len(center),1):
		x2.append(center[i][0])
		y2.append(editdistance.eval(center[i][1],e2))
	plt.scatter(x,y,label = "Editdistance der Hashtags zum leeren wort")
	
	plt.scatter(x2,y2, marker = "x", s=150)
	plt.xlabel("Hashtag-Id")
	plt.ylabel("Editdistance")
	plt.legend()
	plt.show()
	
	
	return 0 
	
def kmeans(in_file):
	temp = Init(DataForm(in_file))
	formatData = temp[2]
	obercluster = temp[0]
	#print("OBERCLUSTER ANFANG KMEANS", obercluster)
	firstCenters = temp[1]
	workingIndex = [False,False,False,False]
	temp2 = NextCenter(obercluster,firstCenters,formatData)
	print("TEMP2 NEW CENTER" , temp2[0])
	newCenters = temp2[0]
	oldCenter = temp2[1]
	print("NEWCENTERS VOR WHILE",newCenters)
	print("OLDCENTERS VOR WHILE",oldCenter)
	while(workingIndex != [True,True,True,True]):
		obercluster = clustering(newCenters, formatData)
		#print("OBERCLUSTER NACH CLUSTERING", obercluster)
		print("NEWCENTERS",newCenters)
		print("oldCenters", oldCenter)

		for i in range(0,len(workingIndex),1):
			if(workingIndex[i] == False):
				workingIndex = (ValidateCenter(newCenters,oldCenter))
				print("NEWCENTERS",newCenters)
				oldCenter[i] = newCenters[i]
				#print("GESAMMTES OBERCLUSTER vor RECOMPUTE KRIEGT",oberc 	luster)
				#print("OBERCLUSTER DAS RECOMPUTE KRIEGT",obercluster[i])				
				zwischen = recompute(newCenters[i],obercluster[i],formatData) #!!!!!!!!!!!!PROBLEPUNKT!!!!!!!!!!
				newCenters[i] = zwischen[0]
		print("OLDCENTER", oldCenter)
		print("NEWCENTER", newCenters)
		print(workingIndex)
	print("obercluster FINNNN", obercluster)	
	
	plotten(newCenters,obercluster)
	
	return (obercluster,newCenters)


test = kmeans(in_file)
