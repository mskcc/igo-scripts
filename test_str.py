# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 21:34:46 2019

@author: cl326
"""
import STR_analysis
import sys

file_location = str(sys.argv[1])

match_table = STR_analysis.get_matching_table(file_location)
header = ['Sample Name', ' AMEL',	' CSF1PO',' D2S1338', ' D3S1358', ' D5S818', ' D7S820', ' D8S1179', ' D13S317', ' D16S539', ' D18S51', ' D19S433', ' D21S11',	' FGA',' ', ' ', ' TH01', ' TPOX', ' vWA']
STR_analysis.write_excel(header, match_table)
