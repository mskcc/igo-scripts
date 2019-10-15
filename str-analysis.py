# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 14:50:46 2019

@author: cl326
"""

#read csv file by line 

import csv

file_content = []

with open('D:\STR analysis\STR Genotypes Table.csv') as f:
	f_csv = csv.reader(f)
	for row in f_csv:
		file_content.append(row)
        
#creat marker list for matching table title
marker_list = [' AMEL',	' CSF1PO',' D2S1338', ' D3S1358', ' D5S818', ' D7S820', ' D8S1179', ' D13S317', ' D16S539', ' D18S51', ' D19S433', ' D21S11',	' FGA',' ', ' ', ' TH01', ' TPOX', ' vWA']

#print len(marker_list)

# get sample list 

sample_list = []
pos_sample_name = file_content[0].index(' Sample Name')

for i in file_content:
    
    if i[pos_sample_name] not in sample_list:
        sample_list.append(i[pos_sample_name])
        
#print sample_list
      

# create dictionary "matching_table" contains sample and marker infor

matching_table = {}

for sample in sample_list:
    if sample != ' Sample Name':
        matching_table[sample] = [None] * len(marker_list)
    

for i in file_content:
    if i[1] in matching_table.keys():
        matching_table[i[1]][marker_list.index(i[3])] = i[5] + ',' + i[6] + ',' + i[7]

for key in matching_table.keys():
    matching_table[key].insert(0,key)
    
# print matching_table
        
marker_list.insert(0,'Sample Name')

# write in matching table excel file

from openpyxl import Workbook
wb = Workbook()
ws = wb.active
ws.append(marker_list)
for key in matching_table.keys():
    ws.append(matching_table[key])


wb.save('matching_table_test.xlsx')
                    