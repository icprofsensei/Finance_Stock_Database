import polars as pl
import duckdb 
import matplotlib.pyplot as plt
path = "data/stocks.db"
con = duckdb.connect(path)
stockname = 'FSLR'
OVERALL  = con.execute(f"""
                            SELECT 
                                TRY_CAST(BS.DATE AS DATE) DATE,
                                TRY_CAST(BS.TOTALASSETS AS FLOAT) TOTALASSETS, 
                                TRY_CAST(BS.TOTALCURRENTASSETS AS FLOAT) TOTALCURRENTASSETS, 
                                TRY_CAST(BS.TOTALNONCURRENTASSETS AS FLOAT) TOTALNONCURRENTASSETS, 
                                TRY_CAST(BS.TOTALLIABILITIES AS FLOAT) TOTALLIABILITIES, 
                                TRY_CAST(BS.TOTALCURRENTLIABILITIES AS FLOAT) TOTALCURRENTLIABILITIES, 
                                TRY_CAST(BS.TOTALSHAREHOLDEREQUITY AS FLOAT) TOTALSHAREHOLDEREQUITY,
                                TRY_CAST(BS.CASHANDCASHEQUIVALENTSATCARRYINGVALUE AS FLOAT) CASHANDCASHEQUIVALENTSATCARRYINGVALUE, 
                                TRY_CAST(BS.CASHANDSHORTTERMINVESTMENTS AS FLOAT) CASHANDSHORTTERMINVESTMENTS,
                                TRY_CAST(BS.SHORTTERMINVESTMENTS AS FLOAT) SHORTTERMINVESTMENTS,
                                TRY_CAST(BS.INVENTORY AS FLOAT) INVENTORY, 
                                TRY_CAST(BS.CURRENTNETRECEIVABLES AS FLOAT) CURRENTNETRECEIVABLES, 
                                TRY_CAST(BS.OTHERCURRENTASSETS AS FLOAT) OTHERCURRENTASSETS,
                                TRY_CAST(BS.PROPERTYPLANTEQUIPMENT AS FLOAT) PROPERTYPLANTEQUIPMENT, 
                                TRY_CAST(BS.ACCUMULATEDDEPRECIATIONAMORTIZATIONPPE AS FLOAT) ACCUMULATEDDEPRECIATIONAMORTIZATIONPPE, 
                                TRY_CAST(BS.INTANGIBLEASSETS AS FLOAT) INTANGIBLEASSETS, 
                                TRY_CAST(BS.OTHERNONCURRENTASSETS AS FLOAT) OTHERNONCURRENTASSETS, 
                                TRY_CAST(BS.LONGTERMINVESTMENTS AS FLOAT) LONGTERMINVESTMENTS, 
                                TRY_CAST(BS.CURRENTACCOUNTSPAYABLE AS FLOAT) CURRENTACCOUNTSPAYABLE, 
                                TRY_CAST(BS.DEFERREDREVENUE AS FLOAT) DEFERREDREVENUE,
                                TRY_CAST(BS.SHORTTERMDEBT AS FLOAT) SHORTTERMDEBT, 
                                TRY_CAST(BS.CURRENTDEBT AS FLOAT) CURRENTDEBT, 
                                TRY_CAST(BS.OTHERCURRENTLIABILITIES AS FLOAT) OTHERCURRENTLIABILITIES, 
                                TRY_CAST(BS.LONGTERMDEBT AS FLOAT) LONGTERMDEBT, 
                                TRY_CAST(BS.OTHERNONCURRENTLIABILITIES AS FLOAT) OTHERNONCURRENTLIABILITIES
                            FROM BALANCESHEET_{stockname} BS
                            """).pl()
OVERALL = OVERALL.fill_null(0)
totalassets = OVERALL.filter(
    (pl.col("TOTALASSETS") == pl.col("TOTALCURRENTASSETS") + pl.col("TOTALNONCURRENTASSETS"))
    &
    (pl.col("TOTALASSETS") == pl.col("TOTALLIABILITIES") + pl.col("TOTALSHAREHOLDEREQUITY"))
    &
      (pl.col("TOTALASSETS") != 0.0)
).select("DATE","TOTALASSETS", "TOTALCURRENTASSETS", "TOTALNONCURRENTASSETS", "TOTALLIABILITIES", "TOTALSHAREHOLDEREQUITY")
currentassets = OVERALL.filter(
    (pl.col("TOTALCURRENTASSETS") == pl.col("CASHANDCASHEQUIVALENTSATCARRYINGVALUE") + pl.col("INVENTORY") + pl.col("CURRENTNETRECEIVABLES") +
    pl.col("OTHERCURRENTASSETS") + pl.col("SHORTTERMINVESTMENTS"))
     &
      (pl.col("TOTALCURRENTASSETS") != 0.0)
    ).select("DATE","TOTALCURRENTASSETS", "CASHANDCASHEQUIVALENTSATCARRYINGVALUE", "INVENTORY", "CURRENTNETRECEIVABLES", "OTHERCURRENTASSETS","SHORTTERMINVESTMENTS" )
currentliabilities = OVERALL.filter(
    (pl.col("TOTALCURRENTLIABILITIES") == pl.col("CURRENTACCOUNTSPAYABLE") + pl.col("DEFERREDREVENUE") +
      pl.col("SHORTTERMDEBT") + pl.col("OTHERCURRENTLIABILITIES"))
      &
      (pl.col("TOTALCURRENTLIABILITIES") != 0.0)
).select("DATE","TOTALCURRENTLIABILITIES", "CURRENTACCOUNTSPAYABLE", "DEFERREDREVENUE", "SHORTTERMDEBT", "OTHERCURRENTLIABILITIES")

completevals = totalassets.join(currentassets, on = "DATE", how = "left")
completevals = completevals.join(currentliabilities, on = "DATE", how = "left")
print(completevals.head(5))
try:
    x = completevals["DATE"].to_list()
    y = completevals["TOTALASSETS"].to_list()

    plt.plot(x, y)
    plt.xlabel("DATE")
    plt.ylabel("ASSETS")
    plt.title("ASSETS OVER TIME")
    plt.show()
except Exception as e:
    print(e)


try:
    x = completevals["DATE"].to_list()
    y = completevals["TOTALSHAREHOLDEREQUITY"].to_list()

    plt.plot(x, y)
    plt.xlabel("DATE")
    plt.ylabel("ASSETS")
    plt.title("ASSETS OVER TIME")
    plt.show()
except Exception as e:
    print(e)

