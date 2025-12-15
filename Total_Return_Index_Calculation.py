import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Define the start dates and investment period (15 years)
start_dates = ['1995-01-01', '2000-01-01', '2005-01-01', '2008-01-01']
investment_amount = 1000000  # $1,000,000 investment

# Download the SPY adjusted close data for the past 15 years
spy_data = yf.download('SPY', start='1995-01-01', end='2023-01-01', adjusted=True)

# Function to calculate the total return index and final investment value
def calculate_total_return_index(start_date, investment_amount, data):
    # Filter the data starting from the given date
    data_start = data.loc[start_date:]
    
    # Calculate the monthly returns
    data_start['monthly_return'] = data_start['Adj Close'].pct_change()

    # Calculate the total return index starting from 1.0
    data_start['total_return_index'] = (1 + data_start['monthly_return']).cumprod()
    data_start['total_return_index'] = data_start['total_return_index'].fillna(1.0)  # Fill NaNs for the first value
    
    # Calculate the final investment value after 15 years
    final_value = investment_amount * data_start['total_return_index'].iloc[-1]
    
    return data_start[['total_return_index']], final_value

# Store results
results = {}

# Iterate over the start dates and calculate results
for start_date in start_dates:
    total_return_index, final_value = calculate_total_return_index(start_date, investment_amount, spy_data)
    results[start_date] = {
        'total_return_index': total_return_index,
        'final_value': final_value
    }

# Plot the total return index for each start date
plt.figure(figsize=(12, 6))
for start_date in start_dates:
    plt.plot(results[start_date]['total_return_index'], label=f"Start Date: {start_date}")

plt.title("SPY Total Return Index (Monthly) - Different Start Dates")
plt.xlabel("Date")
plt.ylabel("Total Return Index")
plt.legend()
plt.grid(True)
plt.show()

# Display the final values for each start date
final_values = {start_date: results[start_date]['final_value'] for start_date in start_dates}
print("Final Investment Values ($1,000,000 initial investment):")
for start_date, final_value in final_values.items():
    print(f"{start_date}: ${final_value:,.2f}")

# Determine the best and worst performing start date
best_start_date = max(final_values, key=final_values.get)
worst_start_date = min(final_values, key=final_values.get)

print(f"\nBest Performing Start Date: {best_start_date}")
print(f"Worst Performing Start Date: {worst_start_date}")
