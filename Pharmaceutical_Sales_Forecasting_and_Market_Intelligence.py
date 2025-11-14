import pandas as pd
import os
import matplotlib.pyplot as plt


try:
    from statsmodels.tsa.statespace.sarimax import SARIMAX
    STATSMODELS_INSTALLED = True
    print("Successfully imported SARIMAX for forecasting.")
except ImportError:
    STATSMODELS_INSTALLED = False
    print("\n--- WARNING ---")
    print("Library 'statsmodels' not found. Forecasting (Step 5) will be skipped.")
    print("To enable forecasting, please install it (e.g., 'pip install statsmodels') and run the script again.\n")


# This is the path you got from kagglehub in your screenshot.
# In your notebook, you could just re-use the 'path' variable
# from the previous cell.
path = "/root/.cache/kagglehub/datasets/milanzdravkovic/pharma-sales-data/versions/1"

# 1. Define the names of all the files you want to load
csv_file_names = [
    "salesdaily.csv",
    "saleshourly.csv",
    "salesmonthly.csv",
    "salesweekly.csv"
]

print(f"Loading data from directory: {path}\n")

# A dictionary to hold all our dataframes
dataframes = {}

# 2. Loop through each file name in the list
for csv_file in csv_file_names:
    # 3. Create the full file path for the current file
    full_file_path = os.path.join(path, csv_file)
    
    print(f"--- Loading file: {csv_file} ---")
    
    try:
        # 4. Load the current CSV into a pandas DataFrame
        df = pd.read_csv(full_file_path)

        # 5. Store the dataframe in our dictionary
        dataframes[csv_file] = df
        
        print(f"Successfully loaded {csv_file}")
        print("="*30 + "\n") # Add a separator

    except FileNotFoundError:
        print(f"Error: File not found at {full_file_path}")
        print("Please check that the path and filename are correct.\n")
    except Exception as e:
        print(f"An error occurred while loading {csv_file}: {e}\n")


# --- FIX: Initialize n02be_sales to None ---
# This ensures the variable always exists, even if Step 2/3 fails
n02be_sales = None


# --- STEP 2: Analyze and Plot Monthly Sales Trends ---

if "salesmonthly.csv" in dataframes:
    print("\n--- STEP 2: Analyzing Monthly Sales Trends ---")
    
    # Get the monthly dataframe
    df_monthly = dataframes["salesmonthly.csv"]

    # 1. Convert the 'datum' column to datetime objects
    # This is crucial for plotting time series data correctly
    df_monthly['datum'] = pd.to_datetime(df_monthly['datum'])
    
    # 2. Set the 'datum' column as the index
    # We will also use the datetime index to extract month/year
    df_monthly.set_index('datum', inplace=True)
    
    # --- FIX: Sort the index ---
    # Sorting the index is crucial for time-based slicing to work reliably
    df_monthly.sort_index(inplace=True)

    print("Converted 'datum' to datetime, set as index, and sorted index.")

    # 3. Plot the sales of a few drug classes
    plt.figure(figsize=(12, 6))
    plt.plot(df_monthly.index, df_monthly['M01AB'], label='M01AB')
    plt.plot(df_monthly.index, df_monthly['N02BE'], label='N02BE')
    
    plt.title('Monthly Sales Trends (M01AB vs N02BE)')
    plt.xlabel('Year')
    plt.ylabel('Sales')
    plt.legend()
    plt.grid(True)
    
    # 4. Save the plot to a file
    plot_filename = "monthly_sales_trends.png"
    plt.savefig(plot_filename)
    
    print(f"Successfully created plot and saved it as '{plot_filename}'")
    
    # To display the plot in a notebook, you would just run:
    # plt.show()
    
    # --- NEXT STEP (STEP 3): Analyze Seasonality of N02BE ---
    print("\n--- STEP 3: Analyzing Seasonality of N02BE ---")

    # 1. Create a new column 'month' from the index
    df_monthly['month'] = df_monthly.index.month
    
    # 2. Group by this 'month' column and calculate the mean sales for N02BE
    seasonal_sales = df_monthly.groupby('month')['N02BE'].mean()
    
    # 3. Create month names for a nicer plot
    month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                   'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
    seasonal_sales.index = month_names
    
    print("Calculated average sales per month for N02BE.")

    # 4. Plot the seasonal sales as a bar chart
    plt.figure(figsize=(10, 5))
    seasonal_sales.plot(kind='bar', color='skyblue')
    
    plt.title('Average Monthly Sales for N02BE (Seasonality)')
    plt.xlabel('Month')
    plt.ylabel('Average Sales')
    plt.xticks(rotation=0) # Keep month names horizontal
    plt.grid(axis='y', linestyle='--')
    
    # 5. Save the new plot to a file
    seasonal_plot_filename = "seasonal_sales_plot.png"
    plt.savefig(seasonal_plot_filename)
    
    print(f"Successfully created seasonality bar chart and saved it as '{seasonal_plot_filename}'")
    
    # --- (This is part of STEP 2/3, we need the original df_monthly) ---
    # We'll use the 'N02BE' data from the original monthly df
    n02be_sales = df_monthly['N02BE']
    
else:
    print("\nCould not perform analysis: 'salesmonthly.csv' was not loaded.")
    # This line is still correct, n02be_sales will be None
    # n02be_sales = None # (This is already handled by our initializer)
    

# --- NEXT STEP (STEP 4): Analyze Hourly Sales Trends ---
if "saleshourly.csv" in dataframes:
    print("\n--- STEP 4: Analyzing Hourly Sales Trends ---")
    
    # 1. Get the hourly dataframe
    df_hourly = dataframes["saleshourly.csv"]

    # 2. Group by the 'Hour' column and calculate the mean sales for N02BE
    # We'll focus on N02BE again to see if its pattern is different
    hourly_sales = df_hourly.groupby('Hour')['N02BE'].mean()
    
    print("Calculated average sales per hour for N02BE.")

    # 3. Plot the hourly sales as a bar chart
    plt.figure(figsize=(12, 6))
    hourly_sales.plot(kind='bar', color='lightgreen')
    
    plt.title('Average Hourly Sales for N02BE')
    plt.xlabel('Hour of the Day (0-23)')
    plt.ylabel('Average Sales')
    plt.xticks(rotation=0)
    plt.grid(axis='y', linestyle='--')
    
    # 4. Save the new plot to a file
    hourly_plot_filename = "hourly_sales_plot.png"
    plt.savefig(hourly_plot_filename)
    
    print(f"Successfully created hourly sales bar chart and saved it as '{hourly_plot_filename}'")

else:
    print("\nCould not perform analysis: 'saleshourly.csv' was not loaded.")


# --- PHASE 2 / STEP 5: Time Series Forecasting ---
# Check if both data (n02be_sales) and the library (STATSMODELS_INSTALLED) are ready
if n02be_sales is not None and STATSMODELS_INSTALLED:
    print("\n--- STEP 5: Forecasting N02BE Sales ---")
    
    try:
        # 1. Define the SARIMA model
        # We're using a common (p,d,q)(P,D,S,m) model for monthly seasonal data
        # (1,1,1) for non-seasonal part
        # (1,1,1,12) for seasonal part (12 months)
        model = SARIMAX(n02be_sales, 
                        order=(1, 1, 1), 
                        seasonal_order=(1, 1, 1, 12))
        
        # 2. Fit the model to the data
        # This may take a few seconds
        print("Fitting the SARIMA model... (This may take a moment)")
        model_fit = model.fit(disp=False) # disp=False turns off verbose logging
        
        # 3. Generate a forecast for the next 12 months
        forecast = model_fit.forecast(steps=12)
        
        print("Model fitting complete. Forecast generated.")

        # 4. Plot the original data and the forecast
        plt.figure(figsize=(12, 6))
        plt.plot(n02be_sales, label='Original Sales')
        plt.plot(forecast, label='Forecasted Sales', color='red', linestyle='--')
        
        plt.title('N02BE Sales Forecast (Next 12 Months)')
        plt.xlabel('Date')
        plt.ylabel('Sales')
        plt.legend()
        plt.grid(True)
        
        # 5. Save the forecast plot
        forecast_plot_filename = "forecast_plot.png"
        plt.savefig(forecast_plot_filename)
        
        print(f"Successfully created forecast plot and saved it as '{forecast_plot_filename}'")
        
    except Exception as e:
        print(f"\nAn error occurred during Step 5 (Forecasting): {e}")

elif n02be_sales is None:
    print("\nSkipping Step 5 (Forecasting) because monthly sales data was not loaded.")
else: # This means STATSMODELS_INSTALLED is False
    print("\nSkipping Step 5 (Forecasting) because 'statsmodels' library is not installed.")


# --- PHASE 3 / STEP 6: Market Share Analysis (Pie Chart) ---
if "salesmonthly.csv" in dataframes:
    print("\n--- STEP 6: Analyzing Market Share (2019) ---")
    
    try:
        # 1. Filter the data to get only 2019
        # Using .loc for robust time-based slicing
        df_2019 = df_monthly.loc['2019']
        
        # 2. Calculate the total sales for the year for each drug class
        # We drop the 'month' column we added earlier
        yearly_sales = df_2E019.drop(columns=['month']).sum()
        
        # 3. Filter out any classes with zero or negative sales to make a clean pie chart
        yearly_sales = yearly_sales[yearly_sales > 0]
        
        print("Calculated total sales for each drug class in 2019.")

        # 4. Create the pie chart
        plt.figure(figsize=(10, 10))
        plt.pie(
            yearly_sales, 
            labels=yearly_sales.index, 
            autopct='%1.1f%%', # Show percentage
            startangle=140
        )
        
        plt.title('Drug Class Market Share (2019)')
        plt.axis('equal') # Ensures the pie is a circle
        
        # 5. Save the pie chart
        pie_chart_filename = "market_share_2019.png"
        plt.savefig(pie_chart_filename)
        
        print(f"Successfully created market share pie chart and saved it as '{pie_chart_filename}'")
        
    except Exception as e:
        print(f"\nAn error occurred during Step 6 (Market Share): {e}")

else:
    print("\nSkipping Step 6 (Market Share) because monthly sales data was not loaded.")


# --- PHASE 4 / STEP 7: Weekday vs. Weekend Analysis ---
if "salesdaily.csv" in dataframes:
    print("\n--- STEP 7: Analyzing Weekday vs. Weekend Sales ---")
    
    try:
        # 1. Get the daily sales dataframe
        df_daily = dataframes["salesdaily.csv"]
        
        # 2. Define a function to classify day type
        def get_day_type(weekday_name):
            if weekday_name in ['Saturday', 'Sunday']:
                return 'Weekend'
            else:
                return 'Weekday'
                
        # 3. Apply the function to create a new 'Day Type' column
        # The 'Weekday Name' column already exists in the CSV
        df_daily['Day Type'] = df_daily['Weekday Name'].apply(get_day_type)
        
        # 4. Group by 'Day Type' and calculate the mean sales for N02BE
        daily_sales_comparison = df_daily.groupby('Day Type')['N02BE'].mean()
        
        print("Calculated average sales for N02BE on weekdays vs. weekends.")

        # 5. Plot the comparison as a bar chart
        plt.figure(figsize=(7, 5))
        daily_sales_comparison.plot(kind='bar', color=['dodgerblue', 'orange'])
        
        plt.title('Average N02BE Sales: Weekday vs. Weekend')
        plt.xlabel('Day Type')
        plt.ylabel('Average Sales')
        plt.xticks(rotation=0)
        plt.grid(axis='y', linestyle='--')
        
        # 6. Save the new plot
        weekday_plot_filename = "weekday_vs_weekend_sales.png"
        plt.savefig(weekday_plot_filename)
        
        print(f"Successfully created comparison plot and saved it as '{weekday_plot_filename}'")
        
    except Exception as e:
        print(f"\nAn error occurred during Step 7 (Weekday Analysis): {e}")

else:
    print("\nSkipping Step 7 (Weekday Analysis) because salesdaily.csv was not loaded.")