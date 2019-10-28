# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 14:50:46 2019

@author: cl326
"""
# function that generate matching table by given file address

def get_matching_table(file_address):
    #read csv file by line
    import csv
    
    file_content = []
    with open(file_address) as f:
        f_csv = csv.reader(f)
        for row in f_csv:
            file_content.append(row)
            
    # get sample list 
    sample_list = []    
    for i in file_content:        
        if i[0] not in sample_list:
            sample_list.append(i[0])
                
    #creat marker list for matching table title
    marker_list = [' AMEL',	' CSF1PO',' D2S1338', ' D3S1358', ' D5S818', ' D7S820', ' D8S1179', ' D13S317', ' D16S539', ' D18S51', ' D19S433', ' D21S11',	' FGA',' ', ' ', ' TH01', ' TPOX', ' vWA']


    # create dictionary "matching_table" contains sample and marker infor
    
    matching_table = {}
    
    for sample in sample_list:
        if sample != 'Sample File':
            matching_table[sample] = [None] * len(marker_list)
        
    
    for i in file_content:
        if i[0] in matching_table.keys():
            matching_table[i[0]][marker_list.index(i[3])] = i[5] + ',' + i[6] + ',' + i[7]
    
    for key in matching_table.keys():
        matching_table[key].insert(0,key)
        
    return matching_table
                
    
# function write matching table in excel file by given matching_table dictionary and file header

def write_excel(header, matching_table): 
    from openpyxl import Workbook
    wb = Workbook()
    ws = wb.active
    ws.append(header)
    for key in matching_table.keys():
        ws.append(matching_table[key])
        
    wb.save('matching_table_test.xlsx')
                


