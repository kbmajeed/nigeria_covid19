

#Kabir Abdulmajeed
#(c) 2020
#kbmajeed@yahoo.com


import os
import requests
import unicodedata
import time as ti
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from prettytable import PrettyTable


def mineData(save_to_disk=True, verbose=True):
    """
    DESCRIPTION:
        This function extracts data on COVID-19 cases in Nigeria from the web.
        You have the option to save the data (save_to_disk), and see its properties (verbose)
    INPUTS:
        save_to_dist: set to True to save dataset, if False, returns data to caller
        verbose: set to True to print statistics and visualize data
    OUTPUTS:
        If save_to_disk=True, data is saved in Excel file named nigera_covid19.csv
    """

    # url link to case tables
    url = "https://en.wikipedia.org/wiki/Template:2019%E2%80%9320_coronavirus_pandemic_data/Nigeria_medical_cases_chart"
    date = ti.ctime()

    # define web extractors
    web = requests.get(url)
    soup = BeautifulSoup(web.text, 'lxml')
    dat = soup.find('tbody')
    tds = dat.findAll('tr')

    # extract data 
    # **Note, if table format changes, you will have missing or no data!
    records = []
    for id, item in enumerate(tds[2:-1]):
        try:
            tmp = str(item.text).split('\n')
            date = tmp[1]
            num_cases = int(tmp[9].split('(')[0])
            tmp2 = tmp[9].split('(')[1]
            new_cases = int(tmp2.split(')')[0])
            pct_change = tmp[11]
            records.append([id, date, num_cases, new_cases, pct_change])
        except:
            pass
    
    # pandas dataframing
    cols = ['record_id', 'record_date', 'num_cases', 'new_cases', 'pct_change']    
    data = pd.DataFrame(records, columns=cols)
    data['index'] = np.arange(0,len(data))

    if verbose:
        #present data
        data.tail()
        table = PrettyTable()
        table.field_names = ["Property", "Value"]
        table.add_row(['Start Dates', data["record_date"].iloc[0]])
        table.add_row(['End Date', data["record_date"].iloc[-1]])
        table.add_row(['Samples', len(data)])
        table.add_row(['Min/Max Cases', [data["num_cases"].min(),data["num_cases"].max()]])
        table.add_row(['Records', data["record_id"].values])
        print(table)
        
        #visualize data
        fig = plt.figure(1, figsize=(12,6))
        plt.plot(data["record_date"], data["num_cases"], 'b-', linewidth=4)
        plt.grid(True)
        plt.xlabel("Days")
        plt.ylabel("Number of Cases")
        fig.autofmt_xdate()
        plt.title("Nigeria COVID-19 Cases")      
    
    if save_to_disk:
        # save data to current directory
        cwd = os.getcwd()
        data.to_csv("nigeria_covid19.csv")
        print("Data saved to {} on {}".format(cwd, date))

    return data




