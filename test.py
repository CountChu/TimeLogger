#
# FILENAME.
#       test.py - Test Python App.
#
# FUNCTIONAL DESCRIPTION.
#       The app run unit test.
#
# NOTICE.
#       Author: visualge@gmail.com (CountChu)
#       Created on 2024/1/27
#       Created on 2024/1/27
#

import unittest
import time_logger
import os

import pdb
br = pdb.set_trace

class TestMyModule(unittest.TestCase):

	def setUp(self):
		self.csv = 'data/report-1706351147.csv'

	def test_1(self):
		self.assertEqual(1+2, 3)

	def test_get_newest_csv(self):
		dn = 'data'
		csv = time_logger.get_newest_csv(dn)
		self.assertEqual(csv, self.csv)

	def test_parse_csv(self):
		df = time_logger.parse_csv(self.csv, op_date=None, op_verbose=False)
		item = df.loc[1]
		TagList = item['TagList']
		self.assertEqual(TagList, ['$', 'SUSE'])

	def test_get_TagSet(self):
		df = time_logger.parse_csv(self.csv, op_date=None, op_verbose=False)
		df2 = df[df['Date'] == '2024-01-26']
		TagSet = time_logger.get_TagSet(df2)
		self.assertEqual(TagSet, {'$', 'SUSE'})

	def test_2(self):
		df = time_logger.parse_csv(self.csv, op_date=None, op_verbose=False)
		df2 = df[df['Date'] == '2024-01-26']
		TagSet = set()
		for TagList in df2['TagList']:
			print(TagList)
			TagSet = TagSet.union(set(TagList))

	def test_cal_total_minutes_by_tag(self):
		df = time_logger.parse_csv(self.csv, op_date=None, op_verbose=False)
		df2 = df[df['Date'] == '2024-01-26']

		minutes = time_logger.cal_total_minutes_by_tag(df2, '$')
		self.assertEquals(minutes, 467)

		minutes = time_logger.cal_total_minutes_by_tag(df2, 'SUSE')
		self.assertEquals(minutes, 408)

	def test_handle_csv(self):
		time_logger.handle_csv(self.csv, None, True, True, False) 

def main():
	unittest.main()


if __name__ == '__main__':
    main()