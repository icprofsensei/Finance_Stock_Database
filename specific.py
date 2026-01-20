import requests
from io import StringIO
import polars as pl
import json
import polars as pl
import tkinter as tk
from tkinter import filedialog, messagebox
from tkcalendar import Calendar
import tksheet
from tqdm import tqdm
import datetime
import duckdb
import time
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import islice


#JSON data

with open("Finance_Stock_Database/data/apidictdata.json") as filejson:
            data = json.load(filejson)


# DATE FEATURES
nowobj = datetime.datetime.now()
date = nowobj.strftime("%x")
hour = nowobj.strftime("%H")
datefeatures = {'DATE':date, 'HOUR': hour}


tickers = pl.read_csv("Finance_Stock_Database/tickers.csv", truncate_ragged_lines=True).to_dicts()

class BrowserApp:
    def __init__(self, stock_browser_root, tickers):
        self.stock_browser_root = stock_browser_root
        self.tickers = tickers
        self.stock_browser_root.title('Stock Browser')
        self.stock_browser_root.geometry("550x350")
        self.curr_row = ""
        self.curr_col = ""
        self.finalticker = ""
        self.create_widgets()
    
    def submit(self):
                rowdata = self.tickers[self.curr_row]
                try:
                    self.finalticker = rowdata['Ticker']
                    self.stock_browser_root.destroy()
                    
                except Exception as e:
                    messagebox.showerror(f"Error {e} occurred")
    def on_cell_select(self, event):
        row = event['selected'][0]
        col = event['selected'][1]
        self.curr_row = row
        self.curr_col = col
    def create_widgets(self):
        cols = list(self.tickers[0].keys())
        rows = [list(row.values()) for row in self.tickers]
        self.sheet = tksheet.Sheet(self.stock_browser_root)
        self.sheet.pack(expand = True, fill = 'both')
        self.sheet.headers(cols)
        self.sheet.set_sheet_data(rows)
        self.sheet.enable_bindings("single_select", "row_select", "arrowkeys", "right_click_popup_menu")
        self.sheet.extra_bindings("cell_select", self.on_cell_select)
        submitrow = tk.Button(self.stock_browser_root, text = "Submit", command = self.submit)
        submitrow.pack(pady = 10)    


class YFBrowserApp:
    def __init__(self, stock_browser_root, tickers):
        self.stock_browser_root = stock_browser_root
        self.tickers = tickers
        self.stock_browser_root.title('Stock Browser')
        self.stock_browser_root.geometry("550x350")
        self.curr_row = ""
        self.curr_col = ""
        self.finalticker = ""
        self.create_widgets()
    
    def submit(self):
                rowdata = self.tickers[self.curr_row]
                try:
                    self.finalticker = rowdata['yfticker']
                    self.stock_browser_root.destroy()
                    
                except Exception as e:
                    messagebox.showerror(f"Error {e} occurred")
    def on_cell_select(self, event):
        row = event['selected'][0]
        col = event['selected'][1]
        self.curr_row = row
        self.curr_col = col
    def create_widgets(self):
        cols = list(self.tickers[0].keys())
        rows = [list(row.values()) for row in self.tickers]
        self.sheet = tksheet.Sheet(self.stock_browser_root)
        self.sheet.pack(expand = True, fill = 'both')
        self.sheet.headers(cols)
        self.sheet.set_sheet_data(rows)
        self.sheet.enable_bindings("single_select", "row_select", "arrowkeys", "right_click_popup_menu")
        self.sheet.extra_bindings("cell_select", self.on_cell_select)
        submitrow = tk.Button(self.stock_browser_root, text = "Submit", command = self.submit)
        submitrow.pack(pady = 10)   



# Stock Browser

class LocatorApp:
    def __init__(self, root, data, datefeatures, datepicker):
        self.root = root
        self.data = data
        self.datefeatures = datefeatures
        self.root.title('File Selector')
        self.root.geometry("600x750")
        self.startdate = ""
        self.enddate = ""
        self.output_dir = ""
        self.feature = ""
        self.datepicker = datepicker
        self.create_widgets()

    def launch_browser(self):
            stock_browser_root = tk.Toplevel(self.root)
            tickerapp = BrowserApp(stock_browser_root, tickers)
            stock_browser_root.wait_window(stock_browser_root)
            self.featuretext.delete(0, tk.END)
            self.featuretext.insert(0, tickerapp.finalticker)


    def select_output_dir(self):
        self.output_dir = filedialog.askdirectory(title = "Select the folder where the database will be created: ")
        if self.output_dir:
            self.outputloc.delete(0, tk.END)
            self.outputloc.insert(0, self.output_dir)
    
    def submit(self):
        if type(self.featuretext) == str:
            self.feature =self.featuretext.get("1.0", tk.END).strip()
        else:
            self.feature =self.featuretext.get().strip()
        if self.datepicker == 'date':
            if not self.startdate or not self.enddate  or not self.featuretext or not self.outputloc:
                messagebox.showwarning("Input Error: Complete all fields")
            else:
                try:
                    self.root.destroy()
                except Exception as e:
                    messagebox.showerror(f"Error {e} occurred")
        else:
             if not self.featuretext or not self.outputloc:
                messagebox.showwarning("Input Error: Complete all fields")
             else:
                try:
                    self.root.destroy()
                except Exception as e:
                    messagebox.showerror(f"Error {e} occurred")
    def select_start_date(self):
            self.startdate = self.calstart.get_date()
            if self.startdate:
                    self.startdatetext.delete(0, tk.END)
                    self.startdatetext.insert(0, self.startdate)
            
    
    def select_end_date(self):
            self.enddate = self.calend.get_date()
            if self.enddate:
                    self.enddatetext.delete(0, tk.END)
                    self.enddatetext.insert(0, self.enddate)

    def create_widgets(self):
        
        featurelab = tk.Label(self.root, text= "Ticker: ")
        featurelab.grid(row=0, column=0, sticky="w",pady=5)
        self.featuretext = tk.Entry(self.root, width = 50)
        self.featuretext.grid(row=0, column=1, sticky="w",pady=5)
        featurebutton = tk.Button(self.root, text = "Browse available green tickers:", command = self.launch_browser)
        featurebutton.grid(row=0, column=2, sticky="w",pady=5)

        if self.datepicker == 'dates':
            startlab = tk.Label(self.root, text= "Start Date")
            startlab.grid(row=1, column=0, sticky="w",pady=5)
            self.calstart = Calendar(self.root, selectmode = 'day',
                year = 2025, month = 5,
                day = 1, date_pattern='yyyy-mm-dd')
            self.calstart.grid(row=1, column=1, sticky="w",pady=5)
            self.startdatetext = tk.Entry(self.root, width = 50)
            self.startdatetext.grid(row=2, column=1, sticky="w",pady=5)
            startdatebutton = tk.Button(self.root, text = "Choose start date", command = self.select_start_date)
            startdatebutton.grid(row=3, column=1, sticky="w",pady=5)

            endlab = tk.Label(self.root, text= "End Date")
            endlab.grid(row=4, column=0, sticky="w",pady=5)
            self.calend = Calendar(self.root, selectmode = 'day',
                year = 2025, month = 9,
                day = 30, date_pattern='yyyy-mm-dd')
            self.calend.grid(row=4, column=1, sticky="w",pady=5)
            self.enddatetext = tk.Entry(self.root, width = 50)
            self.enddatetext.grid(row=5, column=1, sticky="w",pady=5)
            enddatebutton = tk.Button(self.root, text = "Choose end date", command = self.select_end_date)
            enddatebutton.grid(row=6, column=1, sticky="w",pady=5)

            outputlab = tk.Label(self.root, text= "Directory of database")
            outputlab.grid(row=7, column=0, sticky="w",pady=4)
            self.outputloc = tk.Entry(self.root, width = 50)
            self.outputloc.grid(row=7, column=1, sticky="w",pady=4)
            outputbutton = tk.Button(self.root, text = "Browse", command = self.select_output_dir)
            outputbutton.grid(row=8, column=1, sticky="w",pady=4)
        else:
            outputlab = tk.Label(self.root, text= "Directory of database")
            outputlab.grid(row=1, column=1, sticky="w",pady=5)
            self.outputloc = tk.Entry(self.root, width = 50)
            self.outputloc.grid(row=4, column=1, sticky="w",pady=5)
            outputbutton = tk.Button(self.root, text = "Browse", command = self.select_output_dir)
            outputbutton.grid(row=7, column=1, sticky="w",pady=4)
        
        if len(data['Tiingo']['CALLS-HOUR'].keys()) >=1 and datefeatures['DATE'] in data['Tiingo']['CALLS-DAY'].keys():
            if datefeatures['HOUR'] not in data['Tiingo']['CALLS-HOUR'].keys():
                tiingostatuslab = tk.Label(self.root, text= f"""Tiingo Usage:
                                        Calls this day: {data['Tiingo']['CALLS-DAY'][datefeatures['DATE']]} /1000
                                        """)
                tiingostatuslab.grid(row=9, column=1, sticky="w",pady=4)
            else:
                tiingostatuslab = tk.Label(self.root, text= f"""Tiingo Usage:
                                    Calls this hour: {data['Tiingo']['CALLS-HOUR'][datefeatures['HOUR']]} /50,
                                        Calls this day: {data['Tiingo']['CALLS-DAY'][datefeatures['DATE']]} /1000
                                        """)
                tiingostatuslab.grid(row=9, column=1, sticky="w",pady=4)
        if len(data['AlphaVantage']['CALLS-HOUR'].keys()) >=1 and datefeatures['DATE'] in data['AlphaVantage']['CALLS-DAY'].keys():
            if datefeatures['DATE'] not in data['AlphaVantage']['CALLS-DAY'].keys():
                alphastatuslab = tk.Label(self.root, text= f"""AlphaVantage Usage:
                                        Calls this day: {data['AlphaVantage']['CALLS-DAY'][datefeatures['DATE']]} /25
                                        """)
                alphastatuslab.grid(row=9, column=1, sticky="w",pady=4)
            else:
                alphastatuslab = tk.Label(self.root, text= f"""AlphaVantage Usage:
                                    Calls this hour: {data['AlphaVantage']['CALLS-HOUR'][datefeatures['HOUR']]},
                                        Calls this day: {data['AlphaVantage']['CALLS-DAY'][datefeatures['DATE']]} /25
                                        """)
                alphastatuslab.grid(row=9, column=1, sticky="w",pady=4)
        

        submit_button = tk.Button(self.root, text = "Submit", command = self.submit)
        submit_button.grid(row=11, column=1, sticky="w",pady=4)


class YFLocatorApp:
    def __init__(self, root, data, datefeatures):
        self.root = root
        self.data = data
        self.datefeatures = datefeatures
        self.root.title('File Selector')
        self.root.geometry("600x250")
        self.feature = ""
        self.output_dir = ""
        self.create_widgets()

    def launch_browser(self):
            stock_browser_root = tk.Toplevel(self.root)
            tickerapp = YFBrowserApp(stock_browser_root, tickers)
            stock_browser_root.wait_window(stock_browser_root)
            self.featuretext.delete(0, tk.END)
            self.featuretext.insert(0, tickerapp.finalticker)

    def select_output_dir(self):
        self.output_dir = filedialog.askdirectory(title = "Select the folder where the database will be created: ")
        if self.output_dir:
            self.outputloc.delete(0, tk.END)
            self.outputloc.insert(0, self.output_dir)

    def submit(self):
        if type(self.featuretext) == str:
            self.feature =self.featuretext.get("1.0", tk.END).strip()
        else:
            self.feature =self.featuretext.get().strip()
        if not self.featuretext:
            messagebox.showwarning("Input Error: Complete all fields")
        else:
            try:
                self.root.destroy()
            except Exception as e:
                messagebox.showerror(f"Error {e} occurred")
        

    def create_widgets(self):
        
        featurelab = tk.Label(self.root, text= "Ticker: ")
        featurelab.grid(row=0, column=0, sticky="w",pady=5)
        self.featuretext = tk.Entry(self.root, width = 50)
        self.featuretext.grid(row=0, column=1, sticky="w",pady=5)
        featurebutton = tk.Button(self.root, text = "Browse available green tickers:", command = self.launch_browser)
        featurebutton.grid(row=0, column=2, sticky="w",pady=5)
        outputlab = tk.Label(self.root, text= "Directory of database")
        outputlab.grid(row=1, column=0, sticky="w",pady=4)
        self.outputloc = tk.Entry(self.root, width = 50)
        self.outputloc.grid(row=2, column=1, sticky="w",pady=4)
        outputbutton = tk.Button(self.root, text = "Browse", command = self.select_output_dir)
        outputbutton.grid(row=3, column=1, sticky="w",pady=4)
        if len(data['Tiingo']['CALLS-HOUR'].keys()) >=1 and datefeatures['DATE'] in data['Tiingo']['CALLS-DAY'].keys():
            if datefeatures['HOUR'] not in data['Tiingo']['CALLS-HOUR'].keys():
                tiingostatuslab = tk.Label(self.root, text= f"""Tiingo Usage:
                                        Calls this day: {data['Tiingo']['CALLS-DAY'][datefeatures['DATE']]} /1000;/p
                                        """)
                tiingostatuslab.grid(row=4, column=1, sticky="w",pady=4)
            else:
                tiingostatuslab = tk.Label(self.root, text= f"""Tiingo Usage:
                                    Calls this hour: {data['Tiingo']['CALLS-HOUR'][datefeatures['HOUR']]} /50,
                                        Calls this day: {data['Tiingo']['CALLS-DAY'][datefeatures['DATE']]} /1000
                                        """)
                tiingostatuslab.grid(row=4, column=1, sticky="w",pady=4)
        if len(data['AlphaVantage']['CALLS-HOUR'].keys()) >=1 and datefeatures['DATE'] in data['AlphaVantage']['CALLS-DAY'].keys():
            if datefeatures['DATE'] not in data['AlphaVantage']['CALLS-DAY'].keys():
                alphastatuslab = tk.Label(self.root, text= f"""AlphaVantage Usage:
                                        Calls this day: {data['AlphaVantage']['CALLS-DAY'][datefeatures['DATE']]} /25
                                        """)
                alphastatuslab.grid(row=5, column=1, sticky="w",pady=4)
            else:
                alphastatuslab = tk.Label(self.root, text= f"""AlphaVantage Usage:
                                    Calls this hour: {data['AlphaVantage']['CALLS-HOUR'][datefeatures['HOUR']]},
                                        Calls this day: {data['AlphaVantage']['CALLS-DAY'][datefeatures['DATE']]} /25
                                        """)
                alphastatuslab.grid(row=5, column=1, sticky="w",pady=4)
        if len(data['Yfinance']['CALLS-HOUR'].keys()) >=1 and datefeatures['DATE'] in data['Yfinance']['CALLS-DAY'].keys():
            if datefeatures['DATE'] not in data['Yfinance']['CALLS-DAY'].keys():
                yfinlab = tk.Label(self.root, text= f"""Yfinance Usage:
                                        Calls this day: {data['Yfinance']['CALLS-DAY'][datefeatures['DATE']]} 
                                        """)
                yfinlab.grid(row=6, column=1, sticky="w",pady=4)
            else:
                yfinlab = tk.Label(self.root, text= f"""Yfinance Usage:
                                    Calls this hour: {data['Yfinance']['CALLS-HOUR'][datefeatures['HOUR']]} / 2000,
                                        Calls this day: {data['Yfinance']['CALLS-DAY'][datefeatures['DATE']]} 
                                        """)
                yfinlab.grid(row=6, column=1, sticky="w",pady=4)

        submit_button = tk.Button(self.root, text = "Submit", command = self.submit)
        submit_button.grid(row=7, column=1, sticky="w",pady=4)


