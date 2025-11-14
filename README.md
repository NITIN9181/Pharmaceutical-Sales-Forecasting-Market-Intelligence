# **Pharma Sales Analysis & Forecasting**

## **Project Overview**

This project performs a comprehensive, end-to-end analysis of a pharmaceutical sales dataset. Starting from raw CSV files, it runs an automated Python script (Pharmaceutical_Sales_Forecasting_and_Market_Intelligence.py) to perform:

  1. **Data Loading & Preparation**: Reading and preparing all raw data.

  2. **Exploratory Data Analysis (EDA)**: Discovering hidden trends, patterns, and seasonality.

  3. **Time Series Forecasting**: Building a predictive model for future sales.

  4. **Market & Pattern Analysis**: Understanding market composition and daily sales habits.

The script automates the entire process, generating a series of plots and insights that can be used for inventory management, marketing strategy, and staff scheduling.

## Dataset

The project uses the [Pharma Sales Data](https://www.kaggle.com/datasets/milanzdravkovic/pharma-sales-data) dataset from Kaggle, downloaded via kagglehub.

The dataset consists of four CSV files, each providing sales data aggregated at a different time granularity. The columns represent different drug classes (e.g., M01AB, M01AE, N02BA, N02BE, etc.).

  * salesmonthly.csv: Aggregated sales per month.

  * salesdaily.csv: Aggregated sales per day.

  * saleshourly.csv: Aggregated sales per hour.

  * salesweekly.csv: Aggregated sales per week.

## **Requirements**

The analysis script requires the following Python libraries:

  * pandas: For data manipulation and analysis.

  * matplotlib: For data visualization and plotting.

  * statsmodels: For advanced time series forecasting (specifically, the SARIMAX model).

## **How to Run**

  1. Ensure you have the required libraries installed (e.g., pip install pandas matplotlib statsmodels).

  2. Make sure the dataset path variable in load_sales_data.py is correct.

  3. Execute the script from your terminal:

    python load_sales_data.py


The script will run the entire analysis pipeline, printing its progress to the console and generating all the output plots in the same directory.

## **Analysis Pipeline & Key Findings**

The script is structured into five distinct phases.

**Phase 1: Data Loading & Preparation (Step 1)**

This foundational phase involves loading all four raw CSV files (daily, hourly, monthly, weekly) into a structured dictionary of pandas DataFrames. It also handles converting date columns and sorting time-series data to prepare it for analysis.

**Phase 2: Exploratory Analysis (Steps 2-4)**

This phase explores the prepared data to identify high-level trends and choose a focus for deeper analysis.

* **Step 2: Monthly Sales Trends**

  * **Analyzes**: salesmonthly.csv

  * **Output**: monthly_sales_trends.png

  * **Finding**: The sales for drug class N02BE are significantly higher and far more volatile (seasonal) than other classes like M01AB. This identifies N02BE as our high-priority-high-impact product line.

* **Step 3: Seasonality Analysis**

  * **Analyzes**: salesmonthly.csv (focusing on N02BE)

  * **Output**: seasonal_sales_plot.png

  * **Finding**: N02BE sales are strongly seasonal. Sales peak in the fall and winter (October, December) and hit their lowest point in the summer (June, July). This suggests a link to seasonal ailments (e.g., cold, flu, pain associated with colder weather).

* **Step 4: Hourly Sales Trends**

  * **Analyzes**: saleshourly.csv (focusing on N02BE)

  * **Output**: hourly_sales_plot.png

  * **Finding**: Sales are not uniform throughout the day. There are two distinct peaks: a large one around 12:00 PM (noon) and a second, even larger peak around 7:00 PM (19:00). This suggests customers visit pharmacies most often during their lunch break and after work.

**Phase 3: Time Series Forecasting (Step 5)**

This phase uses our seasonality finding to build a predictive model.

* **Step 5: Forecasting N02BE Sales**

  * **Analyzes**: salesmonthly.csv (N02BE sales data)

  * **Output**: forecast_plot.png

  * **Finding**: A SARIMA (Seasonal AutoRegressive Integrated Moving Average) model, chosen specifically for its ability to handle seasonality, successfully captures the historical pattern. The model generates a 12-month forecast, predicting the upcoming summer dip and winter recovery, which is crucial for inventory planning.

**Phase 4: Market Share Analysis (Step 6)**

This phase broadens the scope to see how our main product fits into the entire market.

* **Step 6: Market Share (2019)**

  * **Analyzes**: salesmonthly.csv (all drug classes for 2019)

  * **Output**: market_share_2019.png

  * **Finding**: N02BE is the dominant market leader, responsible for 46.4% of all sales in 2019. This confirms that its performance is critical to the entire business and justifies our deep-dive analysis.

**Phase 5: Daily Pattern Analysis (Step 7)**

This final phase drills down into daily sales behavior to inform staffing and operations.

* **Step 7: Weekday vs. Weekend Sales**

  * **Analyzes**: salesdaily.csv (focusing on N02BE)

  * **Output**: weekday_vs_weekend_sales.png

  * **Finding**: On average, sales for N02BE are noticeably higher on weekends than on weekdays. This is a valuable insight, as one might incorrectly assume sales drop when people are not commuting for work.

## **Actionable Business Implications**

The findings from this analysis lead to several concrete, data-driven recommendations:

1. **Inventory Management:**

    * **Action**: Use the forecast_plot.png and seasonal_sales_plot.png to manage N02BE stock.

    * **Recommendation**: Begin significantly increasing stock levels of N02BE in late summer (Aug-Sep) to prepare for the peak demand that begins in October. Avoid overstocking in late spring (Apr-May) when demand is about to fall.

2. Staff Scheduling:

    * **Action**: Use hourly_sales_plot.png and weekday_vs_weekend_sales.png.

    * **Recommendation**: Ensure maximum staff coverage during peak hours (11 AM - 1 PM and 6 PM - 8 PM). Schedule more staff on weekends than on weekdays to handle the higher sales volume, rather than assuming weekends are slower.

3. **Marketing & Promotions:**

    * **Action**: Use seasonal_sales_plot.png.

    * **Recommendation**: Launch marketing campaigns for N02BE in late September, just before the sales curve begins its sharp rise. Running promotions in June or July would be inefficient as demand is at its seasonal low.

## **Generated Files (Outputs)**

Running Pharmaceutical_Sales_Forecasting_and_Market_Intelligence.py will produce the following six analysis plots:

1. monthly_sales_trends.png

2. seasonal_sales_plot.png

3. hourly_sales_plot.png

4. forecast_plot.png

5. market_share_2019.png

6. weekday_vs_weekend_sales.png
