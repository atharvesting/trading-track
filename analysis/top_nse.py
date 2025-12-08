from nsetools import Nse

# Initialize the NSE object
nse = Nse()

# Get the list of top gainers
top_gainers = nse.get_top_gainers("ALL")

# Print the results
print("NSE Top Gainers:")
for stock in top_gainers:
    print(f"Symbol: {stock['symbol']}, Last Price: {stock['ltp']}")