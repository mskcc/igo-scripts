# -*- coding: utf-8 -*-
"""
Created on Sat Sep 14 14:50:46 2019

@author: cl326
"""
import pandas as pd
import numpy as np
from collections import OrderedDict
import collections

# function that generate matching table by given file address
    # white space can influence query result, need to be removed(strip())


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
        if i[1] not in sample_list:
            sample_name = i[1].strip()
            sample_list.append(sample_name)
            
                
    #creat marker list for matching table title
    marker_list = [' AMEL',	' CSF1PO',' D2S1338', ' D3S1358', ' D5S818', ' D7S820', ' D8S1179', ' D13S317', ' D16S539', ' D18S51', ' D19S433', ' D21S11',	' FGA',' ', ' ', ' TH01', ' TPOX', ' vWA']


    # create dictionary "matching_table" contains sample and marker infor
    
    matching_table = {}
    
    for sample in sample_list:
        if sample != 'Sample Name':
            matching_table[sample] = [" "] * len(marker_list)
        
    
    for i in file_content:
        sample_name = i[1].strip()
        if sample_name in matching_table.keys():
            if i[5] == ' ':
                matching_table[sample_name][marker_list.index(i[3])] = " "
            elif i[6] == ' ':              
                matching_table[sample_name][marker_list.index(i[3])] = i[5]
            elif i[7] == ' ':    
                matching_table[sample_name][marker_list.index(i[3])] = i[5] + ',' + i[6]
            else:
                matching_table[sample_name][marker_list.index(i[3])] = i[5] + ',' + i[6] + ',' + i[7]
    
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
        
    wb.save('matching_table_for_website.xlsx')
                
# fucntion that create body list for api batch query by given matching table

def create_api_body(matching_table):
    body = []
    marker_list = ['AMEL',	'CSF1PO','D2S1338', 'D3S1358', 'D5S818', 'D7S820', 'D8S1179', 'D13S317', 'D16S539', 'D18S51', 'D19S433', 'D21S11',	'FGA',' ', ' ', 'TH01', 'TPOX', 'vWA']
    for key in matching_table.keys():
        sample_infor ={}
        sample_infor["description"] = key
        i = 0
        while i < len(marker_list):            
            sample_infor[marker_list[i]] = matching_table[key][i+1]
            i = i + 1
        sample_infor.update({"algorithm": 1,"scoringMode": 2,"scoreFilter": 75,"outputFormat": "xlsx"})   
        
        for key, values in sample_infor.items():
            if values == None:
                del sample_infor[key]
                break
                
        body.append(sample_infor)
        
    return body
  

# function to modify result_table into one excel tab and sorted by IGO ID.
# input required batch query result and sample list

def modify_result(sample_list_address, batch_query_address):
    
    #get sample list as dataframe
    file_sample_list = sample_list_address
    sample_list = pd.read_excel(file_sample_list, index_col = 1)
    
    
    workbook_location = batch_query_address
    all_dfs = pd.read_excel(workbook_location, sheet_name = None)
    
    sheet_name = all_dfs.keys()
    
    for i in sheet_name:
        all_dfs[i].replace(np.nan, str(" "), inplace=True)
    
    
    for i in sheet_name:
        all_dfs[i].at[0,"Name"] = i
        if i in sample_list.index:
            all_dfs[i].at[0,"Accession"] = sample_list.at[i,"Sample ID"]
    
    all_dfs_new = OrderedDict()
    
    for i in sheet_name:
        if i in sample_list.index:
            all_dfs_new[sample_list.at[i,"Sample ID"]] = all_dfs[i]
        else:
            all_dfs_new[i] = all_dfs[i]
            
    all_dfs_sorted = collections.OrderedDict(sorted(all_dfs_new.items()))
    
    total_df = pd.concat(all_dfs_sorted, ignore_index=False, sort=False)
    
    column_keep = ['Accession', 'Name', 'Score', 'Amel', 'CSF1PO', 'D2S1338',
           'D3S1358', 'D5S818', 'D7S820', 'D8S1179', 'D13S317', 'D16S539',
           'D18S51', 'D19S433', 'D21S11', 'FGA', 'TH01', 'TPOX', 'vWA']
    new_df = total_df[column_keep]
    
    # print(new_df.at[('B1_LN229_Sample_20191101_120142', 0),"Name"])
    
    
    new_df.to_excel("combine_for_user_report.xlsx")      