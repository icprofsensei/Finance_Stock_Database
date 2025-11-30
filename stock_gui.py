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


tickers = pl.read_csv("tickers.csv").to_dicts()
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



# TKINTER GUI

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
        self.api = ""
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
        self.api = self.api.get()
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
        
        self.api = tk.StringVar(value = "Image")
        APIoptlab = tk.Label(self.root, text= "API Option: ")
        APIoptlab.grid(row=9, column=0, sticky="w",pady=4)
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
            if datefeatures['HOUR'] not in data['AlphaVantage']['CALLS-HOUR'].keys():
                alphastatuslab = tk.Label(self.root, text= f"""AlphaVantage Usage:
                                        Calls this day: {data['AlphaVantage']['CALLS-DAY'][datefeatures['DATE']]} /1000
                                        """)
                alphastatuslab.grid(row=9, column=1, sticky="w",pady=4)
            else:
                alphastatuslab = tk.Label(self.root, text= f"""AlphaVantage Usage:
                                    Calls this hour: {data['AlphaVantage']['CALLS-HOUR'][datefeatures['HOUR']]} /50,
                                        Calls this day: {data['AlphaVantage']['CALLS-DAY'][datefeatures['DATE']]} /1000
                                        """)
                alphastatuslab.grid(row=9, column=1, sticky="w",pady=4)
        Tiingo = tk.Radiobutton(self.root, text = "Tiingo", variable = self.api, value = 'Tiingo')
        Tiingo.grid(row = 10, column = 0, sticky = 'w')
        Alpha = tk.Radiobutton(self.root, text = "Alpha Vantage", variable = self.api, value = "Alpha")
        Alpha.grid(row = 10, column = 1, sticky = 'w')

        submit_button = tk.Button(self.root, text = "Submit", command = self.submit)
        submit_button.grid(row=11, column=1, sticky="w",pady=4)

# DATE FEATURES
nowobj = datetime.datetime.now()
date = nowobj.strftime("%x")
hour = nowobj.strftime("%H")
datefeatures = {'DATE':date, 'HOUR': hour}
# Open the JSON dictionary file containing the collected API keys
with open("data/apidictdata.json") as filejson:
    data = json.load(filejson)


if (len(data['AlphaVantage']['CALLS-DAY'].keys()) >= 1 and date not in data['AlphaVantage']['CALLS-DAY'].keys()) or (len(data['Tiingo']['CALLS-DAY'].keys()) >= 1 and date not in data['Tiingo']['CALLS-DAY'].keys()):
     data['AlphaVantage']['CALLS-DAY'] = {}
     data['AlphaVantage']['CALLS-HOUR'] = {}
     data['Tiingo']['CALLS-DAY'] = {}
     data['Tiingo']['CALLS-HOUR'] = {}
     with open("data/apidictdata.json", "w") as f:
                f.write(json.dumps(data, indent = 4))
     
#LAUNCH GUI
root = tk.Tk()
app = LocatorApp(root, data, datefeatures)
root.mainloop()

apikey = data[app.api]['API-KEY']
headersdict = {
    'Content-Type': 'application/json'
}
if app.api == 'Tiingo':
    url = f"{data[app.api]['URL']}/{app.feature}/prices?startDate={app.startdate}&endDate={app.enddate}&resampleFreq=daily&token={apikey}"
duckdb_path = f"{app.output_dir}/stocks.db"
con = duckdb.connect(database=duckdb_path, read_only=False) 

try:
    

    print(url)
    requestResponse = requests.get(url, headers=headersdict)
    jsonoutcome =(requestResponse.content)
    try:
        lazyframe =  pl.read_json(jsonoutcome)
        print("Reading data to dataframe")
        if len(lazyframe.columns) > 1:
            if date not in data[app.api]['CALLS-DAY'].keys():
                    data[app.api]['CALLS-DAY'][date] = 1
            else:
                    data[app.api]['CALLS-DAY'][date] += 1
            if hour not in data[app.api]['CALLS-HOUR'].keys():
                    data[app.api]['CALLS-HOUR'][hour] = 1
            else:
                    data[app.api]['CALLS-HOUR'][hour] += 1
            print("Adjusted limits dictionary")
            apidictdata = json.dumps(data, indent = 4)
            with open("data/apidictdata.json", "w") as f:
                f.write(apidictdata)
    except Exception as e:
         print(e)
    lazyframe = lazyframe.with_columns([pl.col("date").str.slice(0,10).cast(pl.Date), pl.col("close").cast(pl.Float64), pl.col("high").cast(pl.Float64), pl.col("low").cast(pl.Float64)])
    con.execute(f""" CREATE TABLE IF NOT EXISTS
                TICKER_{app.feature}
                AS 
                SELECT *
                FROM lazyframe;""")
    con.close()
    print("Added dataframe to database")

except Exception as e:
     print(e)