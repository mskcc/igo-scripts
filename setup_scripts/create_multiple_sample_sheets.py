import csv
import argparse
import pandas as pd
import os


def txg(sample_data, header):
	# create empty data frame
	txg_data = pd.DataFrame(columns = header)
	# check for 10X samples in index2 of the sample sheet
	for x in range(0, len(sample_data['index2']), 1):
		if ('SI-' in sample_data['index2'].loc[x]):
			txg_data.loc[x] = sample_data.loc[x]  
			sample_data.drop([x], inplace = True, axis = 0)   	
	# drop index2 column for 10X sample data
	txg_data.drop(['index2'], inplace = True, axis = 1)   #this works
	# move regular sample sheet to the last element of the list	
	txg_data.index = range(len(txg_data))
	sample_data.index = range(len(sample_data))
	data_sheets[4] = sample_data
	if not txg_data.empty:
		data_sheets[0] = txg_data

		
def dlp(sample_data, header):
	# create empty data frame
	dlp_data = pd.DataFrame(columns = header)
	# test for DLP data
	for x in range(0, len(sample_data['Sample_Well']), 1):
		if (sample_data['Sample_Well'].loc[x] == 'DLP'):
			dlp_data.loc[x] = sample_data.loc[x]
			sample_data.drop([x], inplace = True, axis = 0)
	# clean up index and  move regular sample sheet to the last element of the list
	dlp_data.index = range(len(dlp_data))
	sample_data.index = range(len(sample_data))
	data_sheets[4] = sample_data
	if not dlp_data.empty:
		data_sheets[1] = dlp_data
		
		
def hwg(sample_data, header):
	# create empty data frame
	hwg_data = pd.DataFrame(columns = header)
	# test for HWG data
	for x in range(0, len(sample_data['Sample_Well']), 1):
		if (sample_data['Sample_Well'].loc[x] == 'HumanWholeGenome'):
			hwg_data.loc[x] = sample_data.loc[x]
			sample_data.drop([x], inplace = True, axis = 0)
	# clean up index and move regular sample sheet to the last element of the list
	hwg_data.index = range(len(hwg_data))
	sample_data.index = range(len(sample_data))
	data_sheets[4] = sample_data
	if not hwg_data.empty:
		data_sheets[3] = hwg_data
			
		
def padded(sample_data, header):
	# create empty data frame for padded requests
	i7_data = pd.DataFrame(columns = header)
	# get a list of individual requests
	requests = set(sample_data['Sample_Project'])
	# use for testing thew length of 'index2'
	len_req_samples = 0
	len_index2 = 0
	for req in requests:
		# check index2 to see if the same index, this would indicate padding
		#  put the groupby step here to avoid random errors from an earlier experience
		requests_group = sample_data.groupby(['Sample_Project'], as_index = False)
		req_group = requests_group['Sample_Name'].get_group(req)
		req_samples = set(req_group)
		len_req_samples = len(req_samples)
		len_index2 = len(set(requests_group['index2'].get_group(req)))
		if (len_req_samples > 1) and (len_index2 == 1):
			# move the padded project to another data frame
			i7_data = i7_data.append(requests_group.get_group(req))
			sample_data.drop(sample_data[sample_data['Sample_Project'] == req].index, inplace = True)
	# move regular sample sheet to the last element of the list	
	i7_data.index = range(len(i7_data))
	sample_data.index = range(len(sample_data))
	data_sheets[4] = sample_data
	if not i7_data.empty:
		data_sheets[2] = i7_data


def create_csv(top_of_sheet, sample_sheet):
	# check to see if sample sheet has been manipulated in any way
	if (data_sheets[0].equals(no_data)) and (data_sheets[1].equals(no_data)) and (data_sheets[2].equals(no_data)) and (data_sheets[3].equals(no_data)):
		print('NO CHANGES MADE TO THE ORIGINAL SAMPLE SHEET')
		return
	else:
		print('NEW SAMPLE SHEETS LOCATED HERE = /igo/home/igo/DividedSampleSheets')
	# list for sample sheet extensions
	extensions = ['_10X.csv', '_DLP.csv', '_PAD.csv', '_WGS.csv', '.csv']
	
	# go to new DividedSampleSheets directory
	os.chdir('/igo/home/igo/DividedSampleSheets')
	
	# create a csv sheet for all valid data sheets
	for y in range(0, len(data_sheets), 1):
		# break the loop in there were no changes in regular sample sheet or all of the samples were 10X, DLP or PADDED
		if data_sheets[y].empty:
			continue
		else:
			data_sheets[y].sort_values('Lane')
			# print(data_element['Lane'])
			data_element_list = data_sheets[y].T.reset_index().values.T.tolist()
			# print(data_element_list)
			data_element_sample_sheet = top_of_sheet + data_element_list
			# ext = extensions[data_sheets.index(data_element)]
			data_element_sample_sheet_name = sample_sheet[:-4] + extensions[y]
			data_element_csv_file = open(data_element_sample_sheet_name, 'w')
			with data_element_csv_file:
				writer = csv.writer(data_element_csv_file)
				writer.writerows(data_element_sample_sheet)
	

def main():
	parser = argparse.ArgumentParser(description = 'This script takes a dual indexed sample sheet and splits it if there are DLP, PADDED or 10X indices')
	parser.add_argument('--sample-sheet', type = str, required = True, help = 'The name and path of the sample sheet to be split')
	args = parser.parse_args()
	
	# grab sample sheet
	sample_sheet = args.sample_sheet
	
	print('SAMPLE SHEET = ' + sample_sheet)
	
	# grab sample sheet - alternate way
	# sample_sheet = args.sample_sheet.split('/')[5]
	# sample_sheet_dir = args.sample_sheet[:-len(sample_sheet)]
	# print('LOCATION OF SAMPLE SHEET = ' + sample_sheet_dir)
	# print('SAMPLE SHEET = ' + sample_sheet)
	
	# switch to the SampleSheetCopies directory
        WRITE_TO='/home/streidd/work/igo-scripts/setup_scripts/sample_sheets'
	os.chdir(WRITE_TO)
	
	# print for sanity check - where are we?
	print('LOCATION OF SAMPLE SHEET = ' + os.getcwd())
	
	# hold area for the sample sheet created
	# index listing
	# 0 = 10X, 1 = DLP, 2 = padded, 3 = HumanWholeGenome, 4 = rest of sample sheet
	global data_sheets, no_data, dual_index
	dual_index = True  
	# empty data set for comparison
	no_data = pd.DataFrame()
	data_sheets = [no_data, no_data, no_data, no_data, no_data]
		
	# this will hold the top of the sample sheet
	top_of_sheet = list()
	# this will hold the sample data portion of the sheet
	csv_sample_data = list()
	barcode_types = list()

	with open(sample_sheet) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter = ',')
		got_data = False
		for row in csv_reader:
			if (row[0] != 'Lane') and (got_data is False):
				# got_data is False
				top_of_sheet.append(row)
			elif (row[0] == 'Lane'):
				got_data = True
				header = row
			# elif (got_data is True):
			elif got_data:
				csv_sample_data.append(row)	
	# this is the data part of the sheet
	sample_data = pd.DataFrame(csv_sample_data, columns = header)
	
	# check to see if 'index2'  in header, if not set dual_index = False
	if 'index2' not in header:
		dual_index = False


	# testing to see if we have dual barcodes, if not, we just quit.
	# first check for 10X samples
	if dual_index:
		# check for 10X samples
		txg(sample_data, header)	   
	
		# call the DLP routine
		dlp(data_sheets[4], header)
		
		# routine for taking out HumanWholeGenome
		hwg(data_sheets[4], header)
		
		# check for padding
		padded(data_sheets[4], header)
	
		# did we have to split sample sheets?
		create_csv(top_of_sheet, sample_sheet)
	
if __name__ == '__main__':
	main()
