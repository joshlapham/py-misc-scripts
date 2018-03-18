#!/usr/bin/python3

import csv
import argparse

def parse_csv_file(csv_file, transaction_name):
    """ Parses a CSV file of transactions for a given transaction name. """
    
    reader = csv.reader(csv_file)
    
    amounts = []
    
    for row in reader:
        # print(', '.join(row))
        # print(row[0]) # date
        # print(row[1]) # transaction name
        
        if transaction_name is not None:
            # print(transaction_name)
            # print(row[1])
            # print('Transaction name: {}; row: {}'.format(transaction_name, row[1]))
            # TODO: parse `row` for `transaction_name` value
            # print(transaction_name in row)
            # if str(transaction_name) in str(row[1]) is True:
            if transaction_name in row[1]:
                print('Transaction: {}'.format(row))
                print('Amount: {}'.format(row[-2]))
                amounts.append(row[-2])
            
    print('Total amounts: {}'.format(amounts))
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv-filepath', help='Filepath to transactions CSV file', required=True)
    parser.add_argument('--transaction-name', help='Name of transaction to look for in CSV file', required=False, default=None, type=str)
    args = parser.parse_args()
    
    try:
        with open(args.csv_filepath, 'r') as csv_file:
            # TODO: update `transaction_name` arg passed here
            parse_csv_file(csv_file, args.transaction_name)
            
    except Exception as e:
        print(e)