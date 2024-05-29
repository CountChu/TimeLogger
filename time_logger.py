#
# FILENAME.
#       time_logger.py - Time Logger Python App.
#
# FUNCTIONAL DESCRIPTION.
#       The app read the latest CSV file and output time log files for all dates.
#
#       The latest CSV file is read from the data directory where files are 
#       sorted by file names.
#
#       The log files are generated in the output directory, and each file is for
#       each date.
#
# NOTICE.
#       Author: visualge@gmail.com (CountChu)
#       Created on 2023/9/16
#       Updated on 2023/12/24
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

    Usage 3: Follow Usage 2 and display time taken of each item. 
        python time_logger.py -m -t

    Usage 4: Follow Usage 3 and display non-first lines with indent. 
        python time_logger.py -m -t --indent

    Usage 5: Generate one log file for the given date from the latest CSV file.
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

    parser.add_argument(
            '-t',
            dest='time',
            action='store_true',
            help='Display time taken of each item.') 

    parser.add_argument(
            '--indent',
            dest='indent',
            action='store_true',
            help='Display non-first lines with indent.')     

    parser.add_argument(
            '-v',
            dest='verbose',
            action='store_true',
            help='Display verbose messages.')                   

    #
    # Return arguments.
    #

    args = parser.parse_args()  
    return args

def extract_date(value):
    return value[:10]

def extract_time(value):
    return value[12:]    

def get_minutes(value):
    HH = value[:2]
    MM = value[3:]
    out = int(HH) * 60 + int(MM)
    return out  

def calculate_minutes(value):
    return get_minutes(value)

def cal_total_minutes_by_tag(df, tag):
    mask = df['TagList'].apply(lambda x: tag in x)
    out = df[mask]['DurationMinutes'].sum()
    return out

def get_hh_mm_str(minutes):
    HH = minutes // 60
    MM = minutes % 60
    out = '%02d:%02d' % (HH, MM)    
    return out

def get_TagSet(df):
    out = set()
    for TagList in df['TagList']:
        out = out.union(set(TagList))
    return out

def write_daily(op_multi, op_indent, op_time, fn, verbose, df):
    if verbose:
        print('Writing %s' % fn)

    f = open(fn, 'w')

    line = ''
    minutes = cal_total_minutes_by_tag(df, '$')
    hh_mm = get_hh_mm_str(minutes)
    line += '$ = %s' % hh_mm

    TagSet = get_TagSet(df)
    for Tag in TagSet:
        if Tag == '$':
            continue

        minutes = cal_total_minutes_by_tag(df, Tag)
        hh_mm = get_hh_mm_str(minutes)
        line += ', %s = %s\n' % (Tag, hh_mm)

    f.write('%s\n' % line)
    f.write('-'*40+'\n')    

    #
    # s = 'init'
    # s = 'sep1' if 12:00 - ??:??
    # s = 'area1'
    # s = 'sep2' if 18:00 - ??:??
    # s = 'area2'
    #

    s = 'init'  
    for row in df.iterrows():
        FromTime = row[1]['FromTime']
        ToTime = row[1]['ToTime']
        Class = row[1]['Class']
        DurationMinutes = row[1]['DurationMinutes']
    
        Comment = row[1]['Comment']
        if pd.isna(Comment):
            Comment = ''

        Tags = row[1]['Tags']
        if pd.isna(Tags):
            Tags = ''
        else:
            Tags = Tags + ' '

        if s == 'init':
            if get_minutes(FromTime) >= get_minutes('12:00'):
                s = 'sep1'
            elif get_minutes(FromTime) >= get_minutes('18:00'): 
                s = 'sep2'          
        elif s == 'sep1':
            if get_minutes(FromTime) >= get_minutes('18:00'): 
                s = 'sep2'
            else:
                s = 'area1'
        elif s == 'area1':
            if get_minutes(FromTime) >= get_minutes('18:00'): 
                s = 'sep2'  
        elif s == 'sep2':
            s = 'area2'     
        elif s == 'area2':
            pass
        else:
            assert False, s

        print('%10s | %s - %s' % (s, FromTime, ToTime))

        if s in ['sep1', 'sep2']:
            f.write('-'*40+'\n')

        #f.write('===')
        if Comment == '':
            if op_multi and op_indent:
                if op_time:
                    f.write('%s - %s %3d %s\n' % (FromTime, ToTime, DurationMinutes, Tags)) 
                    f.write('    [%s]\n' % (Class))
                else:
                    f.write('%s - %s% s\n' % (FromTime, ToTime, Tags))
                    f.write('    [%s]\n' % (Class))
            else:
                if op_time:
                    f.write('%s - %s %3d | %s%s\n' % (FromTime, ToTime, DurationMinutes, Tags, Class))
                else:
                    f.write('%s - %s | %s%s\n' % (FromTime, ToTime, Tags, Class))
        else:
            if op_multi:
                if op_indent:
                    if op_time:
                        f.write('%s - %s %3d %s\n' % (FromTime, ToTime, DurationMinutes, Tags))
                        f.write('    [%s]\n' % (Class))
                        f.write('    %s\n' % Comment)                   
                    else:
                        f.write('%s - %s %s\n' % (FromTime, ToTime, Tags))
                        f.write('    [%s]\n' % (Class))
                        f.write('    %s\n' % Comment)
                else:
                    if op_time:
                        f.write('%s - %s %3d | %s%s\n' % (FromTime, ToTime, DurationMinutes, Tags, Class))
                        f.write('                  | %s\n' % Comment)                   
                    else:
                        f.write('%s - %s | %s%s\n' % (FromTime, ToTime, Tags, Class))
                        f.write('              | %s\n' % Comment)
            else:
                if op_time: 
                    f.write('%s - %s %3d | %s%s | %s\n' % (FromTime, ToTime, DurationMinutes, Tags, Class, Comment))
                else:       
                    f.write('%s - %s | %s%s | %s\n' % (FromTime, ToTime, Tags, Class, Comment))


    f.close()

def get_TagList(Tags):
    if pd.isna(Tags):
        return []
    else:
        return Tags.split(',')

def parse_csv(csv, op_date, op_verbose):

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

    if op_date!= None:
        df = df[df['Date'] == op_date]  

    columns = ['Date', 'FromTime', 'ToTime', 'DurationMinutes', 'Class', 'Comment', 'Tags']
    df2 = df[columns]
    df2 = df2.iloc[::-1]

    df2['TagList'] = df2.apply(lambda row: get_TagList(row['Tags']), axis=1)

    return df2

def dump_df(df, op_verbose):

    for row in df.iterrows():
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
            Tags = ' '
        else:
            Tags = Tags + ' '

        if op_verbose:
            if Comment == '':
                print('%s | %s - %s %4d | %s%s' % (Date, FromTime, ToTime, Duration, Tags, Class))
            else:   
                print('%s | %s - %s %4d | %s%s | %s' % (Date, FromTime, ToTime, Duration, Tags, Class, Comment))

    return df

def handle_csv(csv, op_date, op_multi, op_indent, op_time, op_verbose):

    df = parse_csv(csv, op_date, op_verbose)
    dump_df(df, op_verbose)

    Date_ls = df['Date'].unique()
    i = 0
    n = len(Date_ls)
    for Date in sorted(Date_ls):
        out_fn = os.path.join('output', '%s.txt' % Date)
        df2 = df[df['Date'] == Date]

        if op_verbose:
            verbose = True
        else:
            if i in [0, 1, n-2, n-1]:
                verbose = True
            else:
                verbose = False

        write_daily(op_multi, op_indent, op_time, out_fn, verbose, df2)
        if i == 2 and n >= 5:
            print('... ...')

        i += 1

def get_newest_csv(dn):
    csv_ls = []
    for bn in os.listdir(dn):
        if os.path.splitext(bn)[1] != '.csv':
            continue 

        csv_ls.append(os.path.join(dn, bn))

    #
    # Read the newest csv.
    #

    csv_ls.sort()
    csv = csv_ls[-1]

    return csv

def main():

    #
    # Read arguments.
    #

    args = build_args()

    #
    # Get files in the data directory.
    #

    csv = get_newest_csv('data')

    #
    # Handle the csv.
    #

    handle_csv(csv, args.date, args.multi, args.indent, args.time, args.verbose)

if __name__ == '__main__':
    main()