import sys
import os
import unittest
sys.path.append('../src')
from igo_transfer import transfer_to_igo_dir, extract_well_index, get_pos_info


class TestIgoTransfer(unittest.TestCase):
    @staticmethod
    def setup_nikon_igo(nikon, igo):
        if not os.path.exists(igo):
            print('Creating igo dir at %s' % igo)
            os.mkdir(igo)
        if not os.path.exists(nikon):
            print('Creating nikon dir at %s' % nikon)
            os.mkdir(nikon)
        print('Finished setup')
        return

    @staticmethod
    def create_files(directory):
        print('Creating mock nikon files')
        for char_code in range(65, 89):  # 'A': 65, 'X': 88
            row_idx = chr(char_code)
            for col_idx in range(1, 25):
                for run in ['c1', 'c2']:
                    for row in range(1, 4):
                        for col in range(1, 4):
                            file_name = '%s/%s%02d%s_00%d_00%d.tif' % (directory, row_idx, col_idx, run, col, row)
                            f = open(file_name, 'w')
                            f.write(file_name)
                            f.close()
        # Create bad files
        file_name = '%s/P05c2.tif' % directory
        f = open(file_name, 'w')
        f.write(file_name)
        f.close()
        print('Finished creating mock nikon files')
        return

    def verify_file_contents(self, directory):
        print('Verifying file contents of dir: %s' % directory)
        test_dic = {
            'R01_C01_0000_00_c1.tif': 'A01c1_001_001.tif',
            'R01_C69_0000_00_c1.tif': 'A23c1_003_001.tif',
            'R02_C68_0000_00_c1.tif': 'A23c1_002_002.tif',
            'R03_C69_0000_00_c1.tif': 'A23c1_003_003.tif',
            'R03_C68_0000_00_c1.tif': 'A23c1_002_003.tif',
            'R30_C26_0000_00_c1.tif': 'J09c1_002_003.tif',
            'R46_C59_0000_00_c2.tif': 'P20c2_002_001.tif',
            'R70_C03_0000_00_c1.tif': 'X01c1_003_001.tif',
            'R71_C01_0000_00_c2.tif': 'X01c2_001_002.tif',
            'R71_C72_0000_00_c1.tif': 'X24c1_003_002.tif',
            'R40_C45_0000_00_c1.tif': 'N15c1_003_001.tif',
            'R46_C15_0000_00_c2.tif': 'P05c2_003_001.tif'
        }
        expected_file_ct = 10368  # 72*72*2
        actual_file_ct = 0
        try:
            for root, dirs, files in os.walk(directory):
                for name in files:
                    actual_file_ct += 1
                    if name in test_dic:
                        f = open(os.path.join(root, name), "r")
                        contents = f.read()
                        contents_path = contents.split('/')
                        f.close()
                        self.assertEqual(contents_path[-1], test_dic[name])
                        del test_dic[name]
        except IOError as err:
            print("Error reading file: %s" % err)
        self.assertEqual(len(test_dic), 0)
        self.assertEqual(actual_file_ct, expected_file_ct)
        return

    def test_igo_directory_creation(self):
        target_dir = '%s/igo_dir_test' % os.getcwd()
        src_dir = '%s/Transfer_test' % os.getcwd()

        self.setup_nikon_igo(target_dir, src_dir)
        self.create_files(src_dir)
        transfer_to_igo_dir(target_dir, src_dir)
        self.verify_file_contents(target_dir)

    def test_extract_well_index(self):
        [col_idx, row_idx] = extract_well_index('A01')
        self.assertEqual(row_idx, 0)
        self.assertEqual(col_idx, 0)

        [col_idx, row_idx] = extract_well_index('B03')
        self.assertEqual(row_idx, 1)
        self.assertEqual(col_idx, 2)

    def test_get_pos_info(self):
        [row, col, run] = get_pos_info('A15c2_002_003.tif')
        self.assertEqual(row, 3)
        self.assertEqual(col, 44)
        self.assertEqual(run, 'c2')

        [row, col, run] = get_pos_info('P22c1_003_001.tif')
        self.assertEqual(row, 46)
        self.assertEqual(col, 66)
        self.assertEqual(run, 'c1')

        [row, col, run] = get_pos_info('X24c2_003_002.tif')
        self.assertEqual(row, 71)
        self.assertEqual(col, 72)
        self.assertEqual(run, 'c2')

        [row, col, run] = get_pos_info('X01c1_002_002.tif')
        self.assertEqual(row, 71)
        self.assertEqual(col, 2)
        self.assertEqual(run, 'c1')

        [row, col, run] = get_pos_info('E05c1_003_001.tif')
        self.assertEqual(row, 13)
        self.assertEqual(col, 15)
        self.assertEqual(run, 'c1')

        [row, col, run] = get_pos_info('E05c2_002_003.tif')
        self.assertEqual(row, 15)
        self.assertEqual(col, 14)
        self.assertEqual(run, 'c2')


if __name__ == '__main__':
    unittest.main()
