from __future__ import print_function

import re
import sys
import os
import glob
import argparse

from os.path import join
from os.path import basename
from os.path import abspath
from os.path import isdir
from subprocess import call

# Define some paths and other constants up here
REF_FASTA = '/igo/work/nabors/genomes/GRCh38_100/Homo_sapiens.GRCh38.dna.primary_assembly.fa'
PICARD = 'java -Dpicard.useLegacyParser=false -jar /igo/home/igo/resources/picard2.21.8/picard.jar'
RUN_DIR = '/igo/stats/DRAGEN/MICHELLE_0250_AHHJYLDSXY_WGS/'
WORK_DIR = '/igo/work/streidd/dragen_picard_metrics'


# ###########  WGS script to run Juan Medina's container for the BAM

def submit_jobs_to_cluster(sample, project, sample_dir):
	
	# build input string for markdup
	input_bam = sample_dir + project + '__' + sample + '.bam'	
	
	# MarkDuplicates
	bsub_md = 'bsub -J MARK-DUPLICATES__' + sample + ' -o MARK-DUPLICATES__' + sample + '.log -n 36 -M 6 '
	md = PICARD + ' MarkDuplicates --INPUT ' + input_bam + ' --OUTPUT ' + sample + '___MD.bam --METRICS_FILE ' + sample + '___MD.txt'
	# print(collect_am)
	bsub_md_job = bsub_md + md
	print(bsub_md_job)
	call(bsub_md_job, shell = True)
	
	# CollectAlignmentSummaryMetrics
	bsub_wait_am = 'bsub -w \"done(MARK-DUPLICATES__' + sample + ')\" -J ALIGNMENT-SUMMARY__' + sample + ' -o ALIGNMENT-SUMMARY__' + sample + '.out -n 8 -M 6 '
	collect_am = PICARD + ' CollectAlignmentSummaryMetrics --INPUT ' + sample + '___MD.bam' + ' --OUTPUT ' + sample + '___AM.txt --REFERENCE_SEQUENCE ' + REF_FASTA + ' --METRIC_ACCUMULATION_LEVEL null --METRIC_ACCUMULATION_LEVEL SAMPLE'
	# print(collect_am)
	bsub_collect_am = bsub_wait_am + collect_am
	print(bsub_collect_am)
	call(bsub_collect_am, shell = True)

	# CollectWgsMetrics
	bsub_wait_wgs = 'bsub -w \"done(MARK-DUPLICATES__' + sample + ')\" -J WGS-METRICS__' + sample + ' -o WGS-METRICS__' + sample + '.log -n 8 -M 6 '
	collect_wgs = PICARD + ' CollectWgsMetrics --INPUT ' + sample + '___MD.bam' + ' --OUTPUT ' + sample + '___WGS.txt --REFERENCE_SEQUENCE ' + REF_FASTA
	#print(collect_wgs)
	bsub_collect_wgs = bsub_wait_wgs + collect_wgs
	print(bsub_collect_wgs)
	call(bsub_collect_wgs, shell = True)


############# MAIN ROUTINE
if __name__ == '__main__':
	# parser = argparse.ArgumentParser(description = 'Given WGS FASTQs, run Sanger/Elli PCAP-core for alignment, and generate stats for IGO-QC')
	# parser.add_argument('--request-dir', type = str, required = True, help = 'parent directory with subdirs per sample containing FASTQs')
	# parser.add_argument('--output-dir', type = str, required = False, default = '.', help = 'output folder where files will be generated')
	# args = parser.parse_args()


	# get the immediate folders within the wgs folder
	projects = next(os.walk(RUN_DIR))[1]
	print(projects)

	# for each sample, create symlinks (Juan's code), and kick off jobs
	for project in projects:
		if 'Project_' not in project:
			continue
		else:
			project_dir = RUN_DIR + project + '/'
			samples = next(os.walk(project_dir))[1]
			print(samples)
			for sample in samples:
				sample_dir = project_dir + sample + '/'
				os.chdir(WORK_DIR)
				# call jobs		
				submit_jobs_to_cluster(sample, project, sample_dir)

	print('Fin... 4 now')	
	
