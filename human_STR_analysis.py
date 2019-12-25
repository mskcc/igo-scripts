# -*- coding: utf-8 -*-
"""
Spyder Editor

"""
# http method test


import requests, STR_analysis_function

match_table = STR_analysis_function.get_matching_table("./Genotypes Table.csv")
header = ['Sample Name', ' AMEL',	' CSF1PO',' D2S1338', ' D3S1358', ' D5S818', ' D7S820', ' D8S1179', ' D13S317', ' D16S539', ' D18S51', ' D19S433', ' D21S11',	' FGA',' ', ' ', ' TH01', ' TPOX', ' vWA']
STR_analysis_function.write_excel(header, match_table)

body = STR_analysis_function.create_api_body(match_table)

# print (body)

url_batch = "https://web.expasy.org/cellosaurus-str-search/api/batch"

headers = {'content-type' : 'application/json', 'Accept': 'application/json'}

result = requests.post(url_batch, json = body, headers = headers)

with open('comparison_result_from_database.xlsx', 'wb') as output:
    output.write(result.content)

output.close()

STR_analysis_function.modify_result("./Sample_list.xlsx", "./comparison_result_from_database.xlsx")