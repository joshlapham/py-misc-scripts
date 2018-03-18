#!/usr/bin/python3

import csv
import argparse

def calculate_total(amounts):
    """ Iterate over an array of currency strings and return total as float. """
    
    total = 0
    
    for amount in amounts:
        total += float(amount)
        
    return total

def parse_csv_file(csv_file, transaction_name):
    """ Parses a CSV file of transactions for a given transaction name. """
    
    # TODO: parse date ranges
    
    reader = csv.reader(csv_file)
    
    amounts = []
    
    for row in reader:
        if transaction_name is not None:
            # Parse `row` for `transaction_name` value
            if transaction_name in row[1]:
                print('Transaction: {}'.format(row))
                print('Amount: {}'.format(row[-2]))
                amounts.append(row[-2])
            
    print('Total amounts: {}'.format(amounts))
    
    total = calculate_total(amounts)
    
    print('Total: {}'.format(total))
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv-filepath', help='Filepath to transactions CSV file', required=True)
    parser.add_argument('--transaction-name', help='Name of transaction to look for in CSV file', required=False, default=None, type=str)
    args = parser.parse_args()
    
    try:
        with open(args.csv_filepath, 'r') as csv_file:
            parse_csv_file(csv_file, args.transaction_name)
            
    except Exception as e:
        print(e)