import requests
from io import StringIO
import polars as pl
import json
import polars as pl
import tkinter as tk
from tkinter import filedialog, messagebox
from tkcalendar import Calendar
from tqdm import tqdm
import datetime
import duckdb

# TKINTER GUI

class LocatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title('File Selector')
        self.root.geometry("550x750")
        self.startdate = ""
        self.enddate = ""
        self.output_dir = ""
        self.feature = ""
        self.APIkey = ""
        self.create_widgets()

    
    def select_output_dir(self):
        self.output_dir = filedialog.askdirectory(title = "Select the folder where the database will be created: ")
        if self.output_dir:
            self.outputloc.delete(0, tk.END)
            self.outputloc.insert(0, self.output_dir)
    
    def submit(self):
        self.feature =self.featuretext.get("1.0", tk.END).strip()
        self.APIkey = self.APIkeytext.get("1.0", tk.END).strip()
        if not self.startdate or not self.enddate or not self.APIkeytext or not self.featuretext or not self.outputloc:
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
        self.featuretext = tk.Text(self.root, width = 50, height = 1)
        self.featuretext.grid(row=0, column=1, sticky="w",pady=5)

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
        
        APIkeylab = tk.Label(self.root, text= "API Key: ")
        APIkeylab.grid(row=9, column=0, sticky="w",pady=4)
        self.APIkeytext = tk.Text(self.root, width = 50, height = 1)
        self.APIkeytext.grid(row=9, column=1, sticky="w",pady=4)

        submit_button = tk.Button(self.root, text = "Submit", command = self.submit)
        submit_button.grid(row=10, column=1, sticky="w",pady=4)


#  LAUNCH GUI

root = tk.Tk()
app = LocatorApp(root)
root.mainloop()

headersdict = {
    'Content-Type': 'application/json'
}
url = f"https://api.tiingo.com/tiingo/daily/{app.feature}/prices?startDate={app.startdate}&endDate={app.enddate}&resampleFreq=daily&token={app.APIkey}"
duckdb_path = f"{app.output_dir}/stocks.db"
con = duckdb.connect(database=duckdb_path, read_only=False) 

try:
    requestResponse = requests.get(url, headers=headersdict)
    jsonoutcome =(requestResponse.content)
    lazyframe =  pl.read_json(jsonoutcome)
    print(lazyframe.columns)
    lazyframe = lazyframe.with_columns([pl.col("date").str.slice(0,10).cast(pl.Date), pl.col("close").cast(pl.Float64), pl.col("high").cast(pl.Float64), pl.col("low").cast(pl.Float64)])
    con.execute(f""" CREATE TABLE IF NOT EXISTS
                {app.feature}
                AS 
                SELECT *
                FROM lazyframe;""")
    con.close()

except Exception as e:
     print(e)