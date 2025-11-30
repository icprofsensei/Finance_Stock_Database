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

tickers = pl.read_csv("tickers.csv", truncate_ragged_lines=True).to_dicts()
class SelectorApp:
     def __init__(self, root):
            self.root = root
            self.root.title('Path Selector')
            self.root.geometry("400x150")
            self.choice = ""
            self.create_widgets()
     def submit(self):
            try:
               self.choice = self.path.get()
               self.root.destroy()
            except Exception as e:
                messagebox.showerror(f"Error {e} occurred")
     def create_widgets(self):
            self.path = tk.StringVar(value = "Image")
            PathLabel = tk.Label(self.root, text= "API Option: ")
            PathLabel.pack(pady=4)
            SpecificStock = tk.Radiobutton(self.root, text = "Specific Stock", variable = self.path, value = 'SpecificStock')
            SpecificStock.pack(pady=4)
            Overview = tk.Radiobutton(self.root, text = "Overview", variable = self.path, value = "Overview")
            Overview.pack(pady=4)

            submit_button = tk.Button(self.root, text = "Submit", command = self.submit)
            submit_button.pack(pady=4)


starter = tk.Tk()
app = SelectorApp(starter)
starter.mainloop()



# Add specific stock date range to database

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

# Stock Browser

class LocatorApp:
    def __init__(self, root, data, datefeatures):
        self.root = root
        self.data = data
        self.datefeatures = datefeatures
        self.root.title('File Selector')
        self.root.geometry("600x750")
        self.startdate = ""
        self.enddate = ""
        self.output_dir = ""
        self.feature = ""
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
        if not self.startdate or not self.enddate  or not self.featuretext or not self.outputloc:
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
        
        if len(data['Tiingo']['CALLS-HOUR'].keys()) >=1:
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
        if len(data['AlphaVantage']['CALLS-HOUR'].keys()) >=1:
            if datefeatures['DATE'] not in data['AlphaVantage']['CALLS-DAY'].keys():
                alphastatuslab = tk.Label(self.root, text= f"""AlphaVantage Usage:
                                        Calls this day: {data['AlphaVantage']['CALLS-DAY'][datefeatures['DATE']]} /25
                                        """)
                alphastatuslab.grid(row=9, column=1, sticky="w",pady=4)
            else:
                alphastatuslab = tk.Label(self.root, text= f"""AlphaVantage Usage:
                                    Calls this hour: {data['AlphaVantage']['CALLS-HOUR'][datefeatures['HOUR']]} /50,
                                        Calls this day: {data['AlphaVantage']['CALLS-DAY'][datefeatures['DATE']]} /1000
                                        """)
                alphastatuslab.grid(row=9, column=1, sticky="w",pady=4)
        

        submit_button = tk.Button(self.root, text = "Submit", command = self.submit)
        submit_button.grid(row=11, column=1, sticky="w",pady=4)

# DATE FEATURES
nowobj = datetime.datetime.now()
date = nowobj.strftime("%x")
hour = nowobj.strftime("%H")
datefeatures = {'DATE':date, 'HOUR': hour}


if app.choice == 'SpecificStock':
        
    # Open the JSON dictionary file containing the API keys
        with open("data/apidictdata.json") as filejson:
            data = json.load(filejson)
     # LAUNCH GUI
        root = tk.Tk()
        locapp = LocatorApp(root, data, datefeatures)
        root.mainloop()

        apikey = data['Tiingo']['API-KEY']
        headersdict = {
            'Content-Type': 'application/json'
        }
        url = f"{data['Tiingo']['URL']}/{locapp.feature}/prices?startDate={locapp.startdate}&endDate={locapp.enddate}&resampleFreq=daily&token={apikey}"
        if (len(data['AlphaVantage']['CALLS-DAY'].keys()) >= 1 and date not in data['AlphaVantage']['CALLS-DAY'].keys()) or (len(data['Tiingo']['CALLS-DAY'].keys()) >= 1 and date not in data['Tiingo']['CALLS-DAY'].keys()):
            data['AlphaVantage']['CALLS-DAY'] = {}
            data['AlphaVantage']['CALLS-HOUR'] = {}
            data['Tiingo']['CALLS-DAY'] = {}
            data['Tiingo']['CALLS-HOUR'] = {}
        with open("data/apidictdata.json", "w") as f:
                    f.write(json.dumps(data, indent = 4))
        duckdb_path = f"{locapp.output_dir}/stocks.db"
        con = duckdb.connect(database=duckdb_path, read_only=False) 
        try:
            print(url)
            requestResponse = requests.get(url, headers=headersdict)
            jsonoutcome =(requestResponse.content)
            try:
                lazyframe =  pl.read_json(jsonoutcome)
                print("Reading data to dataframe")
                if len(lazyframe.columns) > 1:
                    if date not in data['Tiingo']['CALLS-DAY'].keys():
                            data['Tiingo']['CALLS-DAY'][date] = 1
                    else:
                            data['Tiingo']['CALLS-DAY'][date] += 1
                    if hour not in data['Tiingo']['CALLS-HOUR'].keys():
                            data['Tiingo']['CALLS-HOUR'][hour] = 1
                    else:
                            data['Tiingo']['CALLS-HOUR'][hour] += 1
                    print("Adjusted limits dictionary")
                    apidictdata = json.dumps(data, indent = 4)
                    with open("data/apidictdata.json", "w") as f:
                        f.write(apidictdata)
            except Exception as e:
                print(e)
            lazyframe = lazyframe.with_columns([pl.col("date").str.slice(0,10).cast(pl.Date), pl.col("close").cast(pl.Float64), pl.col("high").cast(pl.Float64), pl.col("low").cast(pl.Float64)])
            con.execute(f""" CREATE TABLE IF NOT EXISTS
                        TICKER_{locapp.feature}
                        AS 
                        SELECT *
                        FROM lazyframe;""")
            con.close()
            print("Added dataframe to database")

        except Exception as e:
            print(e)
else:
        with open("data/apidictdata.json") as filejson:
            data = json.load(filejson)
        count = 0
        for t in tickers:
            print(count)
            count += 1
            if (len(data['AlphaVantage']['CALLS-DAY'].keys()) >= 1 and date not in data['AlphaVantage']['CALLS-DAY'].keys()) or (len(data['Tiingo']['CALLS-DAY'].keys()) >= 1 and date not in data['Tiingo']['CALLS-DAY'].keys()):
                data['AlphaVantage']['CALLS-DAY'] = {}
                data['AlphaVantage']['CALLS-HOUR'] = {}
                data['Tiingo']['CALLS-DAY'] = {}
                data['Tiingo']['CALLS-HOUR'] = {}
            with open("data/apidictdata.json", "w") as f:
                        f.write(json.dumps(data, indent = 4))
            duckdb_path = f"data/mini_temp.db"
            con = duckdb.connect(database=duckdb_path, read_only=False) 
            try:
                apikey = data['AlphaVantage']['API-KEY']
                url = f"{data['AlphaVantage']['URL']}{t['Ticker']}&apikey={apikey}"
                alpharesponse = requests.get(url)
                alphadata = alpharesponse.json()['Time Series (Daily)']
                try:
                    dates= list(alphadata.keys())
                    openingprices = []
                    for d in dates:
                        openingprices.append({'date':d,'OPENING_PRICE':alphadata[d]['1. open']})
                    pricedf = pl.DataFrame(openingprices)
                    pricedf = pricedf.with_columns(
                        pl.col('date').str.strptime(pl.Date, format="%Y-%m-%d").alias("DATE"),
                        pl.col('OPENING_PRICE').cast(pl.Float64)
                    ).select('DATE','OPENING_PRICE' ).sort("DATE")
                    if len(pricedf.columns) > 1:
                        if date not in data['AlphaVantage']['CALLS-DAY'].keys():
                                data['AlphaVantage']['CALLS-DAY'][date] = 1
                        else:
                                data['AlphaVantage']['CALLS-DAY'][date] += 1
                        if hour not in data['AlphaVantage']['CALLS-HOUR'].keys():
                                data['AlphaVantage']['CALLS-HOUR'][hour] = 1
                        else:
                                data['AlphaVantage']['CALLS-HOUR'][hour] += 1
                        apidictdata = json.dumps(data, indent = 4)
                        with open("data/apidictdata.json", "w") as f:
                            f.write(apidictdata)
                except Exception as e:
                    print(e)
                con.execute(f""" CREATE TABLE IF NOT EXISTS
                            TICKER_{t['Ticker']}
                            AS 
                            SELECT *
                            FROM pricedf;""")
                con.close()

            except Exception as e:
                print(e)
            if count >= 12:
                 break
        con = duckdb.connect(database=duckdb_path, read_only=True) 
        tables = con.sql("SHOW ALL TABLES;").pl()
        tablels = list(tables['name'])
        greenstocks = {}
        for tn in tablels:
            stockname = tn.lstrip("TICKER_")
            t = con.sql(f"""SELECT *
                            FROM {tn}
                            ORDER BY DATE DESC
                            LIMIT 5
                            ;""").pl()
            latest = t.filter(pl.col("DATE") == pl.col("DATE").max()).select("OPENING_PRICE")['OPENING_PRICE'][0]
            first = t.filter(pl.col("DATE") == pl.col("DATE").min()).select("OPENING_PRICE")['OPENING_PRICE'][0]
            perc_change = ((latest - first)/first) * 100
            greenstocks[stockname] = perc_change
        top3 = dict(islice(dict(sorted(greenstocks.items(), reverse = True )).items(), 3))
        bottom3 = dict(islice(dict(sorted(greenstocks.items(), reverse = False )).items(), 3))
        greenstocks_processed = top3 | bottom3
        greenstocks_processed = dict(sorted(greenstocks_processed.items()))
        tickers = list(greenstocks_processed.keys())
        values = list(greenstocks_processed.values())
        sns.set_style("whitegrid")

        ax = sns.barplot(x=tickers, y=values, hue=tickers, palette="pastel", legend = False)
        ax.axhline(0, color="black", linewidth=1.2)
        for i, t in enumerate(tickers):
            ax.text(i, -1, t, ha = "center", va = "top")
        ax.set_title("Green Stock Performance Change - 5 day interval")
        ax.set_ylabel("Percentage Change (%)")
        ax.set_xticklabels([]) 
        ax.set_xlabel("")
        plt.savefig("barplot.png", dpi=300, bbox_inches="tight") 
        plt.close()

