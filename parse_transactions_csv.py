#!/usr/bin/python3

import csv
import argparse

def parse_csv_file(csv_file, transaction_name):
    """ Parses a CSV file of transactions for a given transaction name. """
    
    reader = csv.reader(csv_file, delimiter=' ', quotechar='|')
    
    for row in reader:
        print(', '.join(row))
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv-filepath', help='Filepath to transactions CSV file', required=True)
    args = parser.parse_args()
    
    try:
        with open(args.csv_filepath, newline='') as csv_file:
            parse_csv_file(csv_file)
            
    except Exception as e:
        print(e)