import os
import sys
import time
import stat
from shutil import copyfile, rmtree
from datetime import datetime
import logging
import transfer_cfg as cfg

# This tracks the files successfully transfered. The full 72 x 72 row should be filled
CELL_GRID_TRACKER = []
for i in range(72):
    GRID_ROW = [0 for i in range(72)]
    CELL_GRID_TRACKER.append(GRID_ROW)

def setup_logger(directory,run):
    """
    Sets up file program will log to. Kept at [ROOT]/logs/[RUN].log

    :param (directory) string: Name of directory to place log file
    :param (run) string: timestamp name of file, e.g. '08052019.141626.log'
    """    
    log_dir='%s/logs' % directory
    log_file='%s/%s.log' % (log_dir,run)
    if not os.path.isdir(log_dir):
        os.makedirs(log_dir)       
    logging.basicConfig(filename=log_file, level=logging.DEBUG)
    print('logging to %s' % log_file)

def extract_well_index(well):
    """
    Extracts the upper-right (row, column) position of a WELL_SIZExWELL_SIZE well on the plate

    :param (str) well: Well ('X##', 'X' indicates set of 3-rows and '##' indicates the set of 3-columns. e.g. 'A01')
    :return: int[]
    """
    if len(well) != 3:
        logging.error('Well should be of format X##, e.g. \'AO1\': %s' % well)
    if not well[0].isalpha():
        logging.error('First character of well should be a letter: %s' % well)
    if not well[1:].isdigit():
        logging.error('Last characters of well should be digits: %s' % well)

    well_char = well[0].lower()  # a: 97, z: 122
    well_pos = int(well[1:])
    row_idx = ord(well_char) - 97
    col_idx = well_pos - 1
    return [col_idx, row_idx]


def get_pos_info(file, well_size):
    """
    Parses out the position and run attributes from the name of the input file. Images are currently taken of
    3x3 positions at a time on a flipped over plate. Due to the flip, left-to-right orientation is reversed, which
    is why there's logic to take the difference when calculating the column's index.
        e.g. 'P05c2_002_001.tif' -> [46, 58, 'c2']

    :param (str) file: Name of file, e.g. 'A01c1_002_003.tif'
    :return str[]: array of row, column, and run
    """
    file_extension = '.tif'
    striped_file = file.rstrip(file_extension)
    attr = striped_file.split('_')
    if len(attr) != 3:
        raise ValueError('Created file should have format [POS][RUN]_[COL]_[ROW]: %s' % file)

    run = attr[0][-2:]                              # 'A01c1_002_003' -> 'c1'
    well = attr[0][-5:-2]                           # 'A01c1_002_003' -> 'A01'
    [col_idx, row_idx] = extract_well_index(well)   # 'A01c1_002_003' -> [0,0]
    rel_col = int(attr[1])                          # 'A01c1_002_003' -> 2
    rel_row = int(attr[2])                          # 'A01c1_002_003' -> 3

    row = (row_idx * well_size) + rel_row
    col = (col_idx * well_size) + rel_col
    
    return [row, col, run]


def put_directory_if_absent(path, rsc):
    """
    Adds directory if absent in destination directory

    :param (str) path: target directory
    :param (str) rsc: directory resource (e.g. 'c1', 'S0000', 'C27') to be written to target directory
    :return: str
    """
    files = os.listdir(path)
    next_path = '%s/%s' % (path, rsc)
    if rsc not in files:
        os.mkdir(next_path)
    return next_path


def copy_file_to_igo_dir(nikon_file, igo_dir, row, col, run):
    """
    Renames and copies nikon files to igo directory

    :param (str) nikon_file: Name of Nikon file w/ absolute path
    :param (str) igo_dir: Name of igo directory
    :param (int) row: igo row
    :param (int) col: igo column
    :param (str) run: run, e.g. 'c1' or 'c2'
    """
    CELL_GRID_TRACKER[row-1][col-1] = 1
    
    row = 'R%02d' % row
    col = 'C%02d' % col
    name = '%s_%s_0000_00_%s.tif' % (row, col, run)



    dir_path = igo_dir
    dir_path = put_directory_if_absent(dir_path, run)
    dir_path = put_directory_if_absent(dir_path, 'S0000')  # Set sample to 0-index
    dir_path = put_directory_if_absent(dir_path, col)

    file_path = '%s/%s' % (dir_path, name)
    copy_file = copyfile(nikon_file, file_path)


def transfer_to_igo_dir(well_size, igo_dir='.', nikon_dir='.'):
    """
    Transfers nikon files to directory of igo

    :param (str) igo_dir: Directory renamed files should be moved to
    :param (str) nikon_dir: Directory nikon images will be created in
    :return:
    """
    logging.info('Starting transfer from %s to %s' % (nikon_dir, igo_dir))
    files = os.listdir(nikon_dir)
    ct = 0
    for file in files:
        try:
            [row, column, run] = get_pos_info(file, well_size)
        except ValueError as err:
            logging.error('Did not copy file %s - %s' % (file, err))
            continue
        try:
            nikon_file = '%s/%s' % (nikon_dir, file)
            copy_file_to_igo_dir(nikon_file, igo_dir, row, column, run)
            ct += 1
        except OSError as err:
            logging.error('Error copying %s to %s' % (nikon_dir, dir))
    logging.info('Transferred %d files to %s' % (ct, igo_dir))
    return

"""
Removes the latest k directories in the file
@param k, int - Number of directories to remove
"""
def rm_latest(target_dir, k):
    listOfFile = os.listdir(target_dir)
    if(len(listOfFile) < 150):
        logging.info("Detected less than 15 directories, not removing any")
        return

    creation_times = []
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        full_path = os.path.join(target_dir, entry)
        # get the the stat_result object
        fileStatsObj = os.stat ( full_path )
        # Get the file creation time
        creation_times.append([entry, fileStatsObj [ stat.ST_CTIME ]])

    sorted_times = sorted(creation_times, key=lambda file_time: (file_time[1] - file_time[1]))

    logging.info("Found the following files in directory: %s" % target_dir)
    for file_time in sorted_times:
        logging.info( "File: %s, Time: %s" % (file_time[0], time.ctime ( file_time[1] ) ) )

    entries_to_delete = sorted_times[:k]

    for entry in entries_to_delete:
        file_to_remove = os.path.join(target_dir, entry[0])
        
        logging.info("Removing %s" % file_to_remove)
        rmtree(file_to_remove)

if __name__ == '__main__':
    """
    If called w/o arguments, src & dest directory locations are relative to path script is executed at. Clone repo
    at level of 'Transfer' (Location of nikon images). This will create renamed directories named by their
    timestamp in a 'renamed' directory
     
    > python igo-scripts/src/igo_transfer.py
    
    Otherwise, call with arguments that specify dest (location renamed nikon images should be moved to) and source
    (location of nikon images)
    
    > python igo-scripts/src/igo_transfer.py {dest_dir} {src_dir}
    """
    try:
        root = cfg.root
        run = datetime.now().strftime('%m%d%Y.%H%M%S')

        renamed_dir = '%s\/renamed' % root
        target_dir = '%s\/%s' % (renamed_dir, run)
        src_dir = '%s\/Transfer' % root
        
        setup_logger(root,run)
        if len(sys.argv) >= 2:
            well_size = int(sys.argv[1])
        if len(sys.argv) == 4:
            target_dir = sys.argv[2]
            src_dir = sys.argv[3]
        elif len(sys.argv) != 2:
            logging.error('Improper args %s' % str(sys.argv))
            print('Usage: \'python3 igo_transfer.py\' or \'python3 igo_transfer.py {well_size} {dest_dir} {src_dir}\'')
            sys.exit()
        if not os.path.isdir(src_dir):
            logging.error('Invalid Source Dir: %s' % src_dir)
            print('Could not find source directory - %s. Use \'python3 igo_transfer.py {well_size} {dest_dir} {src_dir}\'' % src_dir)
            sys.exit()
        if not os.path.isdir(target_dir):
            logging.info('Creating %s' % target_dir)
            os.makedirs(target_dir)          
        if well_size != 3 and well_size != 8:
            logging.error('Invalid well size: %d. Must be 3 or 8' % well_size)
            print('Well size needs to be either 3 or 8')
            sys.exit()

        print("Running. Well Size: %d" % well_size)
        logging.info("Running. Well Size: %d" % well_size)
        transfer_to_igo_dir(well_size, target_dir, src_dir)
        for i in range(len(CELL_GRID_TRACKER)):
            GRID_ROW = CELL_GRID_TRACKER[i]
            if 0 in GRID_ROW:
                logging.error("Row %d did not receive an image" % i)
                logging.info(GRID_ROW)
        rm_latest(renamed_dir,1)
    except Exception as e:
        logging.error(e)
