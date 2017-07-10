import csv
from random import randint
import numpy as np
import matplotlib.pyplot as plt
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import datetime

in_file = open("C:/Users/acedon/Desktop/hashtagnew1.csv","r");  
reader = csv.reader(in_file,delimiter=";");                     #csv datei wird eingelesen und im platzhalter reader getan

x = input("Geben sie den Namen des Hashtags ein, dessen Vorkommen sie zeitlich visualisieren möchten:")

timestamps = []; #initialisiere leere liste fuer alle zeitstempel des bestimmten hashtags
for row in reader:
	if (x == row[1]):
		timestamps.append(row[2]);  #fülle liste mit zeitstempel
		
counter = {};   #initialisiere dictionary mit zeitstempel als schlüssel und zähler als wert
for i in timestamps:
	if i not in counter:
		counter[i] = 0;
		for j in timestamps:
			if (i == j):
				counter[i] += 1; #counter eindeutig gefüllt

date = [];
counters = [];

for i in counter:     #übertrage zeitstempel von counter in liste
	date.append(i);
	
for j in counter:          #übertrage die zähler in eigene liste
	counters.append(counter[j]);
	
data2 = [go.Bar(            #plotte die beiden listen als y und x achse
            x=date,
            y=counters
    )]

py.iplot(data2, filename='basic-bar2')
				
				
