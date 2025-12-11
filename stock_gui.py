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
from specific import BrowserApp, LocatorApp
import yfinance as yf

tickers = pl.read_csv("tickers.csv", truncate_ragged_lines=True).to_dicts()
class SelectorApp:
     def __init__(self, root):
            self.root = root
            self.root.title('Path Selector')
            self.root.geometry("450x200")
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
            SpecificStock = tk.Radiobutton(self.root, text = "Specific Stock value", variable = self.path, value = 'SpecificStock')
            SpecificStock.pack(pady=4)
            CASHHistRep = tk.Radiobutton(self.root, text = "Specific Stock CASH", variable = self.path, value = 'CASHHIST')
            CASHHistRep.pack(pady=4)
            BALANCEHistRep = tk.Radiobutton(self.root, text = "Specific Stock BALANCE", variable = self.path, value = 'BALANCEHIST')
            BALANCEHistRep.pack(pady=4)
            Overview = tk.Radiobutton(self.root, text = "Overview", variable = self.path, value = "Overview")
            Overview.pack(pady=4)

            submit_button = tk.Button(self.root, text = "Submit", command = self.submit)
            submit_button.pack(pady=4)


starter = tk.Tk()
app = SelectorApp(starter)
starter.mainloop()



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
        locapp = LocatorApp(root, data, datefeatures, 'dates')
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
elif app.choice =='CASHHIST':
      print('Using AlphaVantage')
      with open("data/apidictdata.json") as filejson:
            data = json.load(filejson)
      count = 0
      root = tk.Tk()
      locapp = LocatorApp(root, data, datefeatures, 'nodates')
      root.mainloop()
      if (date not in data['AlphaVantage']['CALLS-DAY'].keys()) and (date not in data['Tiingo']['CALLS-DAY'].keys()):
        data['AlphaVantage']['CALLS-DAY'] = {}
        data['AlphaVantage']['CALLS-HOUR'] = {}
        data['Tiingo']['CALLS-DAY'] = {}
        data['Tiingo']['CALLS-HOUR'] = {}
        with open("data/apidictdata.json", "w") as f:
                    f.write(json.dumps(data, indent = 4))
      duckdb_path = f"{locapp.output_dir}/stocks.db"
      con = duckdb.connect(database=duckdb_path, read_only=False) 
      try:
        apikey = data['AlphaVantage']['API-KEY']
        url = f"{data['AlphaVantage']['URLCASHFLOW']}{locapp.feature}&apikey={apikey}"
        alpharesponse = requests.get(url)
        alphadata = alpharesponse.json()['quarterlyReports']
        try:
            cashflowdata = pl.from_dicts(alphadata)
            cashflowdata = cashflowdata.with_columns(
                pl.col("fiscalDateEnding").str.strptime(pl.Date, format="%Y-%m-%d").alias("DATE")
            ).sort("DATE").drop("fiscalDateEnding")
            if len(cashflowdata.columns) > 1:
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

        con.execute(f"DROP TABLE IF EXISTS CASHFLOW_{locapp.feature}")
        con.execute(f""" CREATE TABLE IF NOT EXISTS
                    CASHFLOW_{locapp.feature}
                    AS 
                    SELECT *
                    FROM cashflowdata;""")
        con.close()
      except Exception as e:
        print(e)
elif app.choice =='BALANCEHIST':
      print('Using AlphaVantage')
      with open("data/apidictdata.json") as filejson:
            data = json.load(filejson)
      count = 0
      root = tk.Tk()
      locapp = LocatorApp(root, data, datefeatures, 'nodates')
      root.mainloop()
      if (date not in data['AlphaVantage']['CALLS-DAY'].keys()) and (date not in data['Tiingo']['CALLS-DAY'].keys()):
        data['AlphaVantage']['CALLS-DAY'] = {}
        data['AlphaVantage']['CALLS-HOUR'] = {}
        data['Tiingo']['CALLS-DAY'] = {}
        data['Tiingo']['CALLS-HOUR'] = {}
        with open("data/apidictdata.json", "w") as f:
                    f.write(json.dumps(data, indent = 4))
      duckdb_path = f"{locapp.output_dir}/stocks.db"
      con = duckdb.connect(database=duckdb_path, read_only=False) 
      try:
        apikey = data['AlphaVantage']['API-KEY']
        url = f"{data['AlphaVantage']['URLBALANCESHEET']}{locapp.feature}&apikey={apikey}"
        alpharesponse = requests.get(url)
        alphadata = alpharesponse.json()['quarterlyReports']
        try:
            cashflowdata = pl.from_dicts(alphadata)
            cashflowdata = cashflowdata.with_columns(
                pl.col("fiscalDateEnding").str.strptime(pl.Date, format="%Y-%m-%d").alias("DATE")
            ).sort("DATE").drop("fiscalDateEnding")
            if len(cashflowdata.columns) > 1:
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

        con.execute(f"DROP TABLE IF EXISTS CASHFLOW_{locapp.feature}")
        con.execute(f""" CREATE TABLE IF NOT EXISTS
                    BALANCESHEET_{locapp.feature}
                    AS 
                    SELECT *
                    FROM cashflowdata;""")
        con.close()
      except Exception as e:
        print(e)
else:
        with open("data/apidictdata.json") as filejson:
            data = json.load(filejson)
        count = 0
        for t in tickers:
            ticker = t['Ticker']
            if ticker == '688223':
                  ticker = 'ZJS1.BE'
            elif ticker == '301278':
                  ticker = '301278.SZ'
            elif ticker == 'NEEPRS':
                  ticker = '0K80.L'
            else:
                  ticker = ticker
                    
            tablename = ticker.split('.')[0]
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
                stock = yf.Ticker(ticker)
                end_date = nowobj.strftime("%Y-%m-%d")
                start_date = (nowobj - datetime.timedelta(days=10)).strftime("%Y-%m-%d")
                historical_data = stock.history(start=start_date, end=end_date).to_dict(orient = 'index')
                dates= list(historical_data.keys())
                openingprices = []
                for d in dates:
                        openingprices.append({'date':d,'OPENING_PRICE':historical_data[d]['Open']})
                pricedf = pl.DataFrame(openingprices)
                pricedf = pricedf.with_columns(
                        pl.col('date').dt.to_string().str.strptime(pl.Datetime,"%Y-%m-%d %H:%M:%S%.f%z").alias("DATE"),
                        pl.col('OPENING_PRICE').cast(pl.Float64)
                    ).select('DATE','OPENING_PRICE' ).sort("DATE")
                try:
                    
                    con.execute(f"DROP TABLE IF EXISTS TICKER_{tablename}")
                    con.execute(f""" CREATE TABLE IF NOT EXISTS
                                TICKER_{tablename}
                                AS 
                                SELECT *
                                FROM pricedf;""")
                    con.close()
                except Exception as e:
                      print(e)

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
        plt.savefig("data/barplotnew.png", dpi=300, bbox_inches="tight") 
        plt.close()

