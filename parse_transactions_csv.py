#!/usr/bin/python3

import csv
import argparse

def parse_csv_file(csv_file, transaction_name):
    """ Parses a CSV file of transactions for a given transaction name. """
    
    reader = csv.reader(csv_file)
    
    for row in reader:
        print(', '.join(row))
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv-filepath', help='Filepath to transactions CSV file', required=True)
    args = parser.parse_args()
    
    try:
        with open(args.csv_filepath, 'r') as csv_file:
            # TODO: update `transaction_name` arg passed here
            parse_csv_file(csv_file, None)
            
    except Exception as e:
        print(e)