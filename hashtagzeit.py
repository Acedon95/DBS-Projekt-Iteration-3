import csv
from random import randint
import numpy as np
import matplotlib.pyplot as plt
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import datetime

in_file = open("C:/Users/acedon/Desktop/tweetmitdatum;.csv","r");
reader = csv.reader(in_file,delimiter=";");

x = input("Geben sie den Namen des Hashtags ein, dessen Vorkommen sie zeitlich visualisieren möchten:")

timestamps = [];
for row in reader:
	if (x == row[1]):
		timestamps.append(row[2]);
print(timestamps)	
counter = {};
for i in timestamps:
	if i not in counter:
		counter[i] = 0;
		for j in timestamps:
			if (i == j):
				counter[i] += 1;

date = [];
counters = [];

for i in counter:
	date.append(i);
	
for j in counter:
	counters.append(counter[j]);
	
data2 = [go.Bar(
            x=date,
            y=counters
    )]

py.iplot(data2, filename='basic-bar2')
				
				
