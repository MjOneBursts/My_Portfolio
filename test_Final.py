import unittest, Jara_Michael_FinalProject, sys


#Jara_Michael_FinalProject.main()


class TestFinal(unittest.TestCase):
    def test_line_count(self):
        res = Jara_Michael_FinalProject.count_lines()
        self.assertAlmostEqual(res, 585794) #Makes sure we count the right amount of lines





if __name__ == 'main':
    unittest.main()