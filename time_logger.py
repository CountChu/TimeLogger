#
# FILENAME.
#       time_logger.py - Time Logger Python App.
#
# FUNCTIONAL DESCRIPTION.
#       The app read the latest CSV file and output time log files for all dates.
#
#		The latest CSV file is read from the data directory where files are 
#		sorted by file names.
#
#		The log files are generated in the output directory, and each file is for
#		each date.
#
# NOTICE.
#       Author: visualge@gmail.com (CountChu)
#       Created on 2023/9/16
#       Updated on 2023/11/9
#

import argparse
import os
import pandas as pd

import pdb 
br = pdb.set_trace

def build_args():
    desc = '''
    Usage 1: Generate all log files for all dates read from the latest CSV file. 
    	python time_logger.py

    Usage 2: Follow Usage 1 and display contents as multiple lines. 
    	python time_logger.py -m

    Usage 3: Generate one log file for the given date from the latest CSV file.
    	python time_logger.py -d 2023-09-15
'''

    #
    # Build an ArgumentParser object to parse arguments.
    #

    parser = argparse.ArgumentParser(
                formatter_class=argparse.RawTextHelpFormatter,
                description=desc)

    parser.add_argument(
            '-d',
            dest='date',
            help='E.g., 2023-09-15')  	

    parser.add_argument(
            '-m',
            dest='multi',
            action='store_true',
            help='Display comment in multiple lines.')    

    #
    # Check arguments.
    #

    args = parser.parse_args()	

    return args


def extract_date(value):
	return value[:10]

def extract_time(value):
	return value[12:]    

def calculate_minutes(value):
	HH = value[:2]
	MM = value[3:]
	minutes = int(HH) * 60 + int(MM)
	return minutes

def write_daily(args, fn, df):
	print('Writing %s' % fn)

	minutes_0 = df[df['Tags'] == '$']['DurationMinutes'].sum()
	minutes_1 = df[df['Tags'] != '$']['DurationMinutes'].sum()

	f = open(fn, 'w')

	HH = minutes_0 // 60
	MM = minutes_0 % 60
	f.write('$ = %02d:%02d\n' % (HH, MM))
	f.write('\n')

	for row in df.iterrows():
		FromTime = row[1]['FromTime']
		ToTime = row[1]['ToTime']
		Class = row[1]['Class']
		
		Comment = row[1]['Comment']
		if pd.isna(Comment):
			Comment = ''

		Tags = row[1]['Tags']
		if pd.isna(Tags):
			Tags = ''
		else:
			Tags = Tags + ' '

		if Comment == '':
			f.write('%s - %s | %s%s\n' % (FromTime, ToTime, Tags, Class))
		else:
			if args.multi:
				f.write('%s - %s | %s%s\n' % (FromTime, ToTime, Tags, Class))
				f.write('              | %s\n' % Comment)
			else:			
				f.write('%s - %s | %s%s | %s\n' % (FromTime, ToTime, Tags, Class, Comment))

	f.close()

def main():

	#
	# Read arguments.
	#

	args = build_args()

	#
	# Get files in the data directory.
	#

	csv_ls = []
	for dn in os.listdir('data'):
		if os.path.splitext(dn)[1] != '.csv':
			continue 

		csv_ls.append(os.path.join('data', dn))

	#
	# Read the newest csv.
	#

	csv_ls.sort()
	csv = csv_ls[-1]

	#
	# Parse csv.
	#

	df = pd.read_csv(csv)

	Class_ls = []
	count = 0
	for row in df.iterrows():
		if pd.isna(row[1]['Activity type']):
			break

		count += 1

		Class = '' 
		
		if not pd.isna(row[1]['Group']):
			Class += row[1]['Group'] + '.'
		if not pd.isna(row[1]['Group.1']):
			Class += row[1]['Group.1'] + '.'

		Class += row[1]['Activity type']

		Class_ls.append(Class)

	df = df.loc[:(count-1)]
	df['Class'] = Class_ls
	df['Date'] = df['From'].apply(extract_date)
	df['FromTime'] = df['From'].apply(extract_time)
	df['ToTime'] = df['To'].apply(extract_time)
	df['DurationMinutes'] = df['Duration'].apply(calculate_minutes)


	#
	# If -d 
	#

	if args.date != None:
		df = df[df['Date'] == args.date]	

	columns = ['Date', 'FromTime', 'ToTime', 'DurationMinutes', 'Class', 'Comment', 'Tags']
	df2 = df[columns]
	df2 = df2.iloc[::-1]

	for row in df2.iterrows():
		Date = row[1]['Date']
		FromTime = row[1]['FromTime']
		ToTime = row[1]['ToTime']
		Duration = row[1]['DurationMinutes']
		Class = row[1]['Class']
		
		Comment = row[1]['Comment']
		if pd.isna(Comment):
			Comment = ''

		Tags = row[1]['Tags']
		if pd.isna(Tags):
			Tags = ''
		else:
			Tags = Tags + ' '

		if Comment == '':
			print('%s | %s - %s %4d | %s%s' % (Date, FromTime, ToTime, Duration, Tags, Class))
		else:	
			print('%s | %s - %s %4d | %s%s | %s' % (Date, FromTime, ToTime, Duration, Tags, Class, Comment))

	Date_ls = df2['Date'].unique()
	for Date in Date_ls:
		out_fn = os.path.join('output', '%s.txt' % Date)
		df3 = df2[df2['Date'] == Date]

		write_daily(args, out_fn, df3)


if __name__ == '__main__':
	main()