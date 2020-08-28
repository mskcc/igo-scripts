import re
import sys
import glob	
import os
import linecache
import getopt

def rename(run, genome):
	gap = '___'
	count = 0

	for file in glob.iglob('*txt'):
		sample = re.findall(r'^(.+?)___',file)[0]
		project = re.findall('IGO_(.+?)_\d',sample)[0]
		suffix = re.findall(r'___(.+?)$',file)[0]
		stat_file = run + gap + 'P' + project + gap + sample + gap + genome + gap + suffix
		print(file + '  --->  ' + stat_file)
		count += 1
		print(count)
		os.rename(file, stat_file)


def main(argv):
    run = None
    genome = None
    path = None
    try:
        opts, args = getopt.getopt(argv,"hp:r:g:",["path=","run=","genome="])
    except getopt.GetoptError:
        print('usage: create_correct_metrics_files.py -r <run> -g <genome> (-p path)')
        sys.exit(2)
    if(len(argv) == 0):
        print('usage: create_correct_metrics_files.py -r <run> -g <genome> (-p path)')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('usage: create_correct_metrics_files.py -r <run> -g <genome> (-p path)')
            sys.exit()
        elif opt in ("-r", "--run"):
            run = arg
        elif opt in ("-g", "--genome"):
            genome = arg
        elif opt in ("-p", "--path"):
            path = arg
        else:
            print('usage: create_correct_metrics_files.py -r <run> -g <genome> (-p path)')
            sys.exit(2)

    if not run or not genome:
        print('usage: create_correct_metrics_files.py -r <run> -g <genome> (-p path)')
        sys.exit(2)    		
    print('Run: {}'.format(run))
    print('Genome: {}'.format(genome))
    if path:
    	print('Path: {}'.format(path)) 
    	os.chdir(path)
    rename(run, genome)

if __name__ == "__main__":
    main(sys.argv[1:])
