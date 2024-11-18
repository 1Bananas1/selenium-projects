import pandas as pd
import os

current_dir = os.path.dirname(os.path.realpath(__file__))
csv_path = os.path.join(current_dir, "downloads", "stocktrading.csv")
output_path = os.path.join(current_dir, "downloads", "daily_stats.csv")

try:
    # Read the CSV
    df = pd.read_csv(csv_path)
    
    # Clean the percentreturn column by removing '%' and converting to float
    df['percentreturn'] = df['percentreturn'].str.rstrip('%').astype('float')
    
    # Calculate statistics per day
    daily_stats = df.groupby('day').agg({
        'stockprice': ['mean', 'min', 'max', 'std', 'count'],
        'percentreturn': 'mean',
        'balance': 'mean'
    }).round(2)
    
    # Flatten column names to make them CSV-friendly
    daily_stats.columns = ['avg_price', 'min_price', 'max_price', 'price_std', 'trades_count', 
                          'avg_return', 'avg_balance']
    
    # Reset index to make 'day' a column
    daily_stats = daily_stats.reset_index()
    
    # Save to CSV
    daily_stats.to_csv(output_path, index=False)
    
    print(f"Daily statistics saved to {output_path}")
    print("\nFirst few rows of the statistics:")
    print(daily_stats.head())
    
except FileNotFoundError:
    print(f"Could not find stocktrading.csv at {csv_path}")
except Exception as e:
    print(f"An error occurred: {e}")