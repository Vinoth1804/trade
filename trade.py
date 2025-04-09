import pandas as pd

# Set float display format
pd.set_option('display.float_format', '{:.8f}'.format)

# Column names for the raw CSV
columns = [
    "agg_trade_id",
    "price",
    "quantity",
    "quote_quantity",
    "timestamp",
    "is_buyer_maker",
    "is_best_match"
]

# Load the two CSV files and combine them
df = pd.read_csv("trades.csv", names=columns)
  

# Time filter: Jan 20, 5 PM to Jan 21, 5 PM
start_time = pd.Timestamp("2025-01-20 17:00:00")
end_time = start_time + pd.Timedelta(hours=24)

# Convert microsecond timestamp to datetime
df["datetime"] = pd.to_datetime(df["timestamp"], unit="us")

# Filter by time
filtered = df[(df["datetime"] >= start_time) & (df["datetime"] < end_time)]

# Sort by quote_quantity (USDT) to get top 5 biggest trades
top5 = filtered.sort_values("quote_quantity", ascending=False).head(5)

# Prepare output
output = pd.DataFrame({
    "Timestamp (μs)": top5["timestamp"],
    "Amount (BTC)": top5["quantity"],
    "Amount (USDT)": top5["quote_quantity"],
    "Side": top5["is_buyer_maker"].apply(lambda x: "SELL" if x else "BUY")
})

# Save to Excel
output.to_excel("top-5-trade.xlsx", index=False)

# Display the results
print("Top 5 biggest trades (BTC/USDT):")
print(output)
