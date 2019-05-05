import unittest
import csv
import geocoder


class CompareWithExample(unittest.TestCase):
    def test_all(self):
        file = open('example.csv', newline='')
        examples = csv.DictReader(file, dialect=csv.excel)
        for i in examples:
            with self.subTest(i=i):
                result = geocoder.parse_addr(i['source'])
                for field in {'zip', 'region', 'district', 'city', 'street', 'house', 'building', 'office', 'note'}:
                    self.assertEqual(i[field], result[field])
        file.close()


if __name__ == '__main__':
    unittest.main()
