import unittest
import get_git_log_info


class TestGetLogInfo(unittest.TestCase):
    def setUp(self):
        print('setup\n')
        self.name_list = ['hoca', 'Hoca', 'Hoca Chen', 'Jeff', 'Derrick']
        with open('testfile.txt') as f:
            self.test_data = f.read()


    def tearDown(self):
        print('tearDown\n')
        pass

    def test_get_name(self):
        print('test_get_name')
        expected_ret = ['hoca', 'Hoca', 'Hoca Chen']
        ret = get_git_log_info.get_author_name('hoca', self.name_list)
        self.assertEqual(ret, expected_ret)

    def test_separate_add_delete(self):
        ret = get_git_log_info.get_total_add_delete_line(self.test_data)
        #---Add line--
        self.assertEqual(ret[0], 4121)
        #---Delete line--
        self.assertEqual(ret[1], 3004)

if __name__ == '__main__':
    unittest.main()
