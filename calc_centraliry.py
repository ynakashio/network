#coding:utf-8

import string
import sys
import csv
import os
import re
import numpy as np
import matplotlib
import math
import networkx as nx
import pylab
import matplotlib.pyplot as plt
from itertools import chain


def csv_loader():
	fileList = os.listdir('/Users/yuko/Desktop/sot/data/col/calc/centrality_calc')
	ptn = re.compile("(\d+)\_keyword_pairList.csv")

	csvNames=[]
	for csvName in fileList:
		result = ptn.search(csvName)
		if result:
			csvNames.append(csvName)

	print csvNames,"\n"
	return csvNames


def csv_adj_convert(csvNames):

	for csvName in csvNames:
		f = open(csvName,'rb')
		reader=csv.reader(f)
		
		g = open(csvName[0:4]+'.adjlist','wb')
		writer = csv.writer(g, delimiter='\t')
		for data in reader:
			writer.writerow(data)
		g.close
		f.close

	fileList = os.listdir('/Users/yuko/Desktop/sot/data/col/calc/centrality_calc')
	ptn = re.compile("(\d+)\.adjlist")

	adjNames=[]
	for fileName in fileList:
		result = ptn.search(fileName)
		if result:
			adjNames.append(fileName)

	print adjNames,"\n"
	return adjNames


def draw_picture(adjNames):

	for adjName in adjNames:

		print adjName[0:4],"の描画を始める"
		f = open(adjName, 'rb')
		G = nx.read_adjlist(f)
		f.close
	
		pylab.figure(figsize=(10, 15))  # 横3inch 縦4inchのサイズにする
		pos = nx.spring_layout(G)

		nx.draw_networkx_nodes(G, pos, node_size = 10, node_color = 'w')
		nx.draw_networkx_edges(G, pos, width = 1)
		nx.draw_networkx_labels(G, pos, font_size = 10, font_family = 'sans-serif', font_color = 'black')

		#nx.draw(G)	
		#plt.draw()
		#pylab.savefig(adjName[0:4]+'.png')

	return

def calc_centrality(adjNames):

	for adjName in adjNames:
	
		print adjName[0:4],"年の中心性の計算中...."
		f = open(adjName, 'rb')
		G = nx.read_adjlist(f)
		f.close

		degreeDic = nx.degree_centrality(G)
		closenessDic = nx.closeness_centrality(G)
		betweennessDic = nx.betweenness_centrality(G)
		pagerankDic = nx.pagerank(G)

		yearDic = {}
		for keyword in degreeDic.keys():				
			centralitiesList=[degreeDic[keyword]]
			centralitiesList.extend([closenessDic[keyword]])
			centralitiesList.extend([betweennessDic[keyword]])
			centralitiesList.extend([pagerankDic[keyword]])
			yearDic.update({keyword:centralitiesList})


		g = open(adjName[0:4]+'_centralitiesList.csv','wb')
		writer = csv.writer(g)

		keywordList=[]
		for keyword in yearDic.keys():
			keywordList.append(keyword)
			tmp=[keyword]
			tmp.extend(yearDic[keyword])
			writer.writerow(tmp)
		g.close
	
	fileList = os.listdir('/Users/yuko/Desktop/sot/data/col/calc/centrality_calc')
	ptn = re.compile("(\d+)\_centralitiesList.csv")

	centralitiesNames=[]
	for centralitiesName in fileList:
		result = ptn.search(centralitiesName)
		if result:
			centralitiesNames.append(centralitiesName)

	return centralitiesNames,keywordList


def sort_by_keyword(centralitiesNames,keywordList):

	for keyword in keywordList:
		print keyword,"のファイルを作成中...."

		sort_by_keywordList=[]
		for centralitiesName in centralitiesNames:
			f = open(centralitiesName,'rb')
			reader = csv.reader(f)
		
			for row in reader:
				if row[0] == keyword:
					sort_by_keywordList.append(row[1:])
		

		centrality_matrix = np.matrix(sort_by_keywordList)
		T_centrality_matrix = centrality_matrix.T

		n_row, n_col = T_centrality_matrix.shape
		centList=[]
		for i in range(n_row):
			row = T_centrality_matrix[i,:]
			result=np.array(row).flatten()
			centList.append(result)
	#	print centList

		os.chdir(r"/Users/yuko/Desktop/sot/data/col/calc/centrality_calc/sorted_by_keyword_CENTRALITIES")

		if keyword.find('/') > -1:
			print "/を含む"
			g = open(keyword.replace('/','-')+'_time_series_centrality.csv','wb')
			writer = csv.writer(g)
			for data in centList:
				writer.writerow(data)
			g.close

		elif keyword.find(' ') > -1:
			print "(半角)を含む"
			g = open(keyword.replace(' ','-')+'_time_series_centrality.csv','wb')
			writer = csv.writer(g)
			for data in centList:
				writer.writerow(data)
			g.close

		else:
			print keyword,"何も含まない"
			g= open(keyword+'_time_series_centrality.csv','wb')
			writer = csv.writer(g)
			for data in centList:
				writer.writerow(data)
			g.close

		os.chdir(r"/Users/yuko/Desktop/sot/data/col/calc/centrality_calc")
		f.close

	return


def sort_by_DEGREE(centralitiesNames,keywordList):

	degreeDic={}
		
	for centralitiesName in centralitiesNames:
		f = open(centralitiesName,'rb')
		reader = csv.reader(f)

		if centralitiesName[0:4] == '1990':
			for row in reader:
				tmp=[row[1]]
				degreeDic.update({row[0]:tmp})
		else:
			for row in reader:
				tmp=[row[1]]
				degreeDic[row[0]].extend(tmp)

		f.close
	print degreeDic 

	os.chdir(r'/Users/yuko/Desktop/sot/data/col/calc/centrality_calc/sorted_by_centralities')

	d = open('degree_time_series.csv','wb')
	writer = csv.writer(d)
	for keyword in degreeDic.keys():
		tmp=[keyword]
		tmp.extend(degreeDic[keyword])
		writer.writerow(tmp)
	d.close

	os.chdir(r'/Users/yuko/Desktop/sot/data/col/calc/centrality_calc')
	return


def sort_by_CLOSENESS(centralitiesNames,keywordList):
	
	closenessDic={}

	for centralitiesName in centralitiesNames:
		f = open(centralitiesName,'rb')
		reader = csv.reader(f)

		if centralitiesName[0:4] == '1990':
			for row in reader:
				tmp=[row[1]]
				closenessDic.update({row[0]:tmp})
		else:
			for row in reader:
				tmp=[row[1]]
				closenessDic[row[0]].extend(tmp)

		f.close
	print closenessDic 

	os.chdir(r'/Users/yuko/Desktop/sot/data/col/calc/centrality_calc/sorted_by_centralities')

	c = open('closeness_time_series.csv','wb')
	writer = csv.writer(c)
	for keyword in closenessDic.keys():
		tmp=[keyword]
		tmp.extend(closenessDic[keyword])
		writer.writerow(tmp)
	c.close
	os.chdir(r'/Users/yuko/Desktop/sot/data/col/calc/centrality_calc')

	return


def sort_by_BETWEENNESS(centralitiesNames,keywordList):
	betweennessDic={}

	for centralitiesName in centralitiesNames:
		f = open(centralitiesName,'rb')
		reader = csv.reader(f)

		if centralitiesName[0:4] == '1990':
			for row in reader:
				tmp=[row[1]]
				betweennessDic.update({row[0]:tmp})
		else:
			for row in reader:
				tmp=[row[1]]
				betweennessDic[row[0]].extend(tmp)

		f.close
	print betweennessDic 

	os.chdir(r'/Users/yuko/Desktop/sot/data/col/calc/centrality_calc/sorted_by_centralities')

	b = open('betweenness_time_series.csv','wb')
	writer = csv.writer(b)
	for keyword in betweennessDic.keys():
		tmp=[keyword]
		tmp.extend(betweennessDic[keyword])
		writer.writerow(tmp)
	b.close
	os.chdir(r'/Users/yuko/Desktop/sot/data/col/calc/centrality_calc')

	return


def sort_by_PAGERANK(centralitiesNames,keywordList):
	pagerankDic={}

	for centralitiesName in centralitiesNames:
		f = open(centralitiesName,'rb')
		reader = csv.reader(f)

		if centralitiesName[0:4] == '1990':
			for row in reader:
				tmp=[row[1]]
				pagerankDic.update({row[0]:tmp})
		else:
			for row in reader:
				tmp=[row[1]]
				pagerankDic[row[0]].extend(tmp)

		f.close
	print pagerankDic 

	os.chdir(r'/Users/yuko/Desktop/sot/data/col/calc/centrality_calc/sorted_by_centralities')

	p = open('pagerank_time_series.csv','wb')
	writer = csv.writer(p)
	for keyword in pagerankDic.keys():
		tmp=[keyword]
		tmp.extend(pagerankDic[keyword])
		writer.writerow(tmp)
	p.close
	os.chdir(r'/Users/yuko/Desktop/sot/data/col/calc/centrality_calc')

	return


if __name__ == '__main__':
	csvNames = csv_loader()
	adjNames = csv_adj_convert(csvNames)
	#draw_picture(adjNames)
	centralitiesNames, keywordList = calc_centrality(adjNames)
	sort_by_keyword(centralitiesNames, keywordList)
	sort_by_DEGREE(centralitiesNames, keywordList)
	sort_by_CLOSENESS(centralitiesNames,keywordList)
	sort_by_BETWEENNESS(centralitiesNames,keywordList)
	sort_by_PAGERANK(centralitiesNames,keywordList)