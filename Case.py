import pandas as pd
import streamlit as st
import csv

def extract():
    conversion = {}
    date_sums = {}

    with open('Question_case1.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader, None)

        for row in csv_reader:

            date, clicks, impressions = row[0], row[8], row[7]
                    
            # Check if the date is already in the dictionary
            print(clicks, impressions)
            if date in date_sums:
                # If it's in the dictionary, increment the values in the tuple
                current_tuple = date_sums[date]
                updated_tuple = (current_tuple[0] + impressions, current_tuple[1] + clicks)
                date_sums[date] = updated_tuple
            else:
                # If it's not in the dictionary, add it with the current values as a tuple
                date_sums[date] = (impressions, clicks)



  

if __name__ == "__main__":
    extract()


        # row_count = 0
    
        # for row in csv_reader:
        #     print(row[0])
            
        #     row_count += 1
            
        #     if row_count >= 5:
        #         break
