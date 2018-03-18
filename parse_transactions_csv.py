#!/usr/bin/python3

import csv
import argparse

def calculate_total(amounts):
    """ Iterate over an array of currency strings and return total as float. """
    
    total = 0
    
    for amount in amounts:
        total += float(amount)
        
    return total

def parse_csv_file(csv_file, transaction_name, transaction_month):
    """ Parses a CSV file of transactions for a given transaction name, and month it occured. """
    
    # TODO: parse date ranges
    
    reader = csv.reader(csv_file)
    
    amounts = []
    
    for row in reader:
        if transaction_name is not None:
            # Parse `row` for `transaction_name` value
            if transaction_name in row[1]:
                if transaction_month is not None:
                    # Parsing a `transaction_month`, only add amount if month matches
                    if transaction_month in row[0].split('/')[1]:
                        print('Matched month')
                        print('Transaction: {}'.format(row))
                        print('Amount: {}'.format(row[-2]))
                        amounts.append(row[-2])
                else:
                    # No `transaction_month` to parse
                    print('Transaction: {}'.format(row))
                    print('Amount: {}'.format(row[-2]))
                    amounts.append(row[-2])
                            
    print('Total amounts: {}'.format(amounts))
    
    total = calculate_total(amounts)
    
    print('Total: {}'.format(total))
    
if __name__ == '__main__':
    """ Script to parse bank transaction CSV files for certain transaction names/dates. """
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv-filepath', help='Filepath to transactions CSV file', required=True)
    parser.add_argument('--transaction-name', help='Name of transaction to look for in CSV file', required=False, default=None, type=str)
    parser.add_argument('--transaction-month', help='Parse a specific month that transaction occured', required=False, default=None)
    args = parser.parse_args()
    
    try:
        with open(args.csv_filepath, 'r') as csv_file:
            parse_csv_file(csv_file, args.transaction_name, args.transaction_month)
            
    except Exception as e:
        print(e)