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
        self.root.geometry("550x200")
        self.TiingoAPIKey = ""
        self.AlphavantageAPIKey = ""
        self.create_widgets()

    
    
    def submit(self):
        self.AlphavantageAPIKey =self.AlphavantageAPIKeytext.get("1.0", tk.END).strip()
        self.TiingoAPIKey = self.TiingoAPIKeytext.get("1.0", tk.END).strip()
        if not self.TiingoAPIKey or not self.AlphavantageAPIKey:
            messagebox.showwarning("Input Error: Complete all fields")
        else:
            try:
                self.root.destroy()
            except Exception as e:
                messagebox.showerror(f"Error {e} occurred")

    def create_widgets(self):

    
        TiingoAPIKeyLab = tk.Label(self.root, text= "Tiingo API Key: ")
        TiingoAPIKeyLab.pack(pady=4)
        self.TiingoAPIKeytext = tk.Text(self.root, width = 50, height = 1)
        self.TiingoAPIKeytext.pack(pady=4)

        AlphavantageAPIKeyLab = tk.Label(self.root, text= "Alpha Vantage API Key: ")
        AlphavantageAPIKeyLab.pack(pady=4)
        self.AlphavantageAPIKeytext = tk.Text(self.root, width = 50, height = 1)
        self.AlphavantageAPIKeytext.pack(pady=4)


        submit_button = tk.Button(self.root, text = "Submit", command = self.submit)
        submit_button.pack(pady=4)


#  LAUNCH GUI

root = tk.Tk()
app = LocatorApp(root)
root.mainloop()

apidict = {
    'Tiingo':{
        'API-KEY': app.TiingoAPIKey,
        'URL': 'https://api.tiingo.com/tiingo/daily/',
        "CALLS-DAY": {},
        "CALLS-HOUR":{}
    },
    'AlphaVantage':{
        'API-KEY': app.AlphavantageAPIKey,
        'URL': "https://www.alphavantage.co/query?function=CASH_FLOW&symbol=",
        "CALLS-DAY": {},
        "CALLS-HOUR":{}
    }
}
apidictdata = json.dumps(apidict, indent = 4)
with open("data/apidictdata.json", "a+") as f:
    f.write(apidictdata)
