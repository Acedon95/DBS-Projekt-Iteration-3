import csv
import editdistance
from random import randint
import numpy as np
import matplotlib.pyplot as plt
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import datetime


plotly.tools.set_credentials_file(username='Acedon', api_key='YWlKkOZ9nn6jOQUhDxcq')


in_file = open("C:/Users/acedon/Desktop/tweetmitdatum;.csv","r") 
reader = csv.reader(in_file,delimiter=";")

x = []
anzahl = []
tempDatums = []
Datum = []
i = 0
for row in reader:
	tempDatums.append(row[2])
in_file.close()

	
for i in range(1,len(tempDatums),1):
	if(tempDatums[i] not in Datum):
		Datum.append(tempDatums[i])
		
DatumTripel = []

for i in range(0,len(Datum),1):
	splited = Datum[i].partition(".")
	while (splited[2] != ""):
		DatumTripel.append(splited[0])
		splited = splited[2].partition(".")
		
	if (splited[2]== ""):
		DatumTripel.append(splited[0])

realTripel = []
tag = []
monat = []
jahr = []		

i = 0

while(i in range(0,len(DatumTripel),1)):
	tag.append(DatumTripel[i])
	i = i + 1;
	monat.append(DatumTripel[i])
	i = i + 1
	jahr.append(DatumTripel[i])
	i = i + 1


for i in range(0,len(Datum),1):
	temp = 0
	in_file = open("C:/Users/acedon/Desktop/tweetmitdatum;.csv","r") 
	reader = csv.reader(in_file,delimiter=";")
	for row in reader:
		if(Datum[i] == row[2]):
			temp = temp + 1
	anzahl.append(temp)
	in_file.close()
	

xAchse = []
for i in range(0,len(tag),1):
	xAchse.append(datetime.datetime(year = (int(float(jahr[i]))), month  = (int(float(monat[i]))), day = (int(float(tag[i])))))

data = [go.Bar(
            x=xAchse,
            y=anzahl
    )]

py.iplot(data, filename='basic-bar')
