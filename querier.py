import polars as pl
import json
import polars as pl
import tkinter as tk
from tkinter import filedialog, messagebox
from tkcalendar import Calendar
import tksheet
import duckdb as ddb


class QueryEngine():
    def __init__(self, root):
        self.root = root
        self.root.title('Stock Browser')
        self.root.geometry("1350x650")
        self.query = ""
        self.create_widgets()
    
    def run_query(self):
        self.query = self.query_entry_text.get(1.0, tk.END)
        con = ddb.connect("data/stocks.db")
        self.result = con.execute(self.query).pl()
        con.close()
        self.cols = self.result.columns
        self.data = self.result.to_numpy().tolist()
        self.sheet.headers(self.cols)
        self.sheet.set_sheet_data(self.data)

    def create_widgets(self):
        query_lab = tk.Label(self.root, text = "Query:")
        query_lab.pack(pady = 5)
        self.query_entry_text = tk.Text(self.root, width = 150, height = 5)
        self.query_entry_text.pack(pady = 5)
        query_submit_button = tk.Button(self.root, text = "Submit Query", command = self.run_query)
        query_submit_button.pack(pady = 5)
        self.sheet = tksheet.Sheet(self.root)
        self.sheet.pack(expand = True, fill = 'both')
        self.sheet.enable_bindings("column_width_resize")

root = tk.Tk()
app= QueryEngine(root)
root.mainloop()
