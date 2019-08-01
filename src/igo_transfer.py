import os
import sys
from shutil import copyfile
from datetime import datetime

LOG = False


def log(msg):
    if LOG:
        print(msg)


def extract_well_index(well):
    """
    Extracts the upper-right (row, column) position of a 3x3 well on the plate

    :param (str) well: Well ('X##', 'X' indicates set of 3-rows and '##' indicates the set of 3-columns. e.g. 'A01')
    :return: int[]
    """
    if len(well) != 3:
        log('Well should be of format X##, e.g. \'AO1\': %s' % well)
    if not well[0].isalpha():
        log('First character of well should be a letter: %s' % well)
    if not well[1:].isdigit():
        log('Last characters of well should be digits: %s' % well)

    well_char = well[0].lower()  # a: 97, z: 122
    well_pos = int(well[1:])
    row_idx = ord(well_char) - 97
    col_idx = well_pos - 1
    return [col_idx, row_idx]


def get_pos_info(file):
    """
    Parses out the position and run attributes from the name of the input file. Images are currently taken of
    3x3 positions at a time on a flipped over plate. Due to the flip, left-to-right orientation is reversed, which
    is why there's logic to take the difference when calculating the column's index.
        e.g. 'P05c2_002_001.tif' -> [46, 58, 'c2']

    :param (str) file: Name of file, e.g. "A01c1_002_003.tif"
    :return str[]: array of row, column, and run
    """
    file_extension = '.tif'
    file = file.strip(file_extension)
    attr = file.split('_')
    if len(attr) != 3:
        raise ValueError('Created file should have format [POS][RUN]_[COL]_[ROW]: %s' % file)

    run = attr[0][-2:]  # "A01c1_002_003" -> "c1"
    well = attr[0][-5:-2]  # "A01c1_002_003" -> "A01"
    [col_idx, row_idx] = extract_well_index(well)  # "A01c1_002_003" -> [0,0]
    rel_col = int(attr[1])  # "A01c1_002_003" -> 2
    rel_row = int(attr[2])  # "A01c1_002_003" -> 3

    # Wells are 3x3
    row = (row_idx * 3) + rel_row
    col = 73 - ((col_idx * 3) + rel_col)

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
    :param (str) run: run, e.g. "c1" or "c2"
    """
    row = 'R%02d' % row
    col = 'C%02d' % col
    name = '%s_%s_0000_00_%s.tif' % (row, col, run)

    dir_path = igo_dir
    dir_path = put_directory_if_absent(dir_path, run)
    dir_path = put_directory_if_absent(dir_path, 'S0000')  # Set sample to 0-index
    dir_path = put_directory_if_absent(dir_path, col)

    file_path = '%s/%s' % (dir_path, name)
    copy_file = copyfile(nikon_file, file_path)
    log('Copied %s to %s' % (nikon_file, copy_file))


def transfer_to_igo_dir(igo_dir='.', nikon_dir='.'):
    """
    Transfers nikon files to directory of igo

    :param (str) igo_dir: Directory renamed files should be moved to
    :param (str) nikon_dir: Directory nikon images will be created in
    :return:
    """
    print('Starting transfer from %s to %s' % (nikon_dir, igo_dir))
    files = os.listdir(nikon_dir)
    ct = 0
    for file in files:
        try:
            [row, column, run] = get_pos_info(file)
        except ValueError as err:
            print('Did not copy file %s - %s' % (file, err))
            continue
        try:
            nikon_file = '%s/%s' % (nikon_dir, file)
            copy_file_to_igo_dir(nikon_file, igo_dir, row, column, run)
            ct += 1
        except OSError as err:
            print('Error copying %s to %s' % (nikon_dir, dir))
    print('Transferred %d files to %s' % (ct, igo_dir))
    return


if __name__ == '__main__':
    """
    If called w/o arguments, src & dest directory locations are relative to path script is executed at. Clone repo
    at level of "Transfer" (Location of nikon images). This will create renamed directories named by their
    timestamp in a "renamed" directory
     
    > python igo-scripts/src/igo_transfer.py
    
    Otherwise, call with arguments that specify dest (location renamed nikon images should be moved to) and source
    (location of nikon images)
    
    > python igo-scripts/src/igo_transfer.py {dest_dir} {src_dir}
    """
    target_dir = '%s/renamed/%s' % (os.getcwd(), datetime.now().strftime("%m%d%Y_%H:%M:%S"))
    src_dir = '%s/Transfer' % os.getcwd()
    if len(sys.argv) == 3:
        target_dir = sys.argv[1]
        src_dir = sys.argv[2]
    elif len(sys.argv) != 1:
        print('Usage: "python3 igo_transfer.py" or "python3 igo_transfer.py {dest_dir} {src_dir}"')
        sys.exit()

    if not os.path.isdir(src_dir):
        print('Could not find source directory - %s. Use "python3 igo_transfer.py {dest_dir} {src_dir}"' % src_dir)
        sys.exit()
    if not os.path.isdir(target_dir):
        print("Creating %s" % target_dir)
        os.makedirs(target_dir)

    transfer_to_igo_dir(target_dir, src_dir)
