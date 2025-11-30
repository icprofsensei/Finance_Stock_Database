import requests
import polars as pl
import duckdb
import seaborn as sns
import matplotlib.pyplot as plt
from itertools import islice

greenstocks = {'TICKER_RUN': 7.936507936507942, 'TICKER_SUN': -8.50, 'TICKER_SOLAR': 7, 'TICKER_RUN1': 1.936507936507942, 'TICKER_SUN2': -1.50, 'TICKER_SOLAR3': 1
               ,'TICKER_RUN2': 2.936507936507942, 'TICKER_SUN4': -2.50, 'TICKER_SOLAR6': 2, 'TICKER_RUN3': 3.936507936507942, 'TICKER_SUN5': -3.50, 'TICKER_SOLAR7': 3}
top3 = dict(islice(dict(sorted(greenstocks.items(), reverse = True )).items(), 3))
bottom3 = dict(islice(dict(sorted(greenstocks.items(), reverse = False )).items(), 3))
greenstocks_processed = top3 | bottom3
greenstocks_processed = dict(sorted(greenstocks_processed.items()))
tickers = list(greenstocks_processed.keys())
values = list(greenstocks_processed.values())
sns.set_style("whitegrid")

ax = sns.barplot(x=tickers, y=values, palette="pastel", legend = False)
ax.axhline(0, color="black", linewidth=1.2)
for i, t in enumerate(tickers):
    ax.text(i, -1, t, ha = "center", va = "top")
ax.set_title("Green Stock Performance")
ax.set_ylabel("Percentage Change (%)")
ax.set_xticklabels([]) 
ax.set_xlabel("")


plt.show()
