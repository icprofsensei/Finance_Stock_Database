import duckdb as ddb
import polars as pl


def executer(sql):
    con = ddb.connect("data/stocks.db")
    result = con.execute(sql).pl()
    con.close()
    return result

tables = executer("SHOW ALL TABLES;")
print(tables)

FSLR = executer("SELECT * FROM CASHFLOW_FSLR;")
print(FSLR)

