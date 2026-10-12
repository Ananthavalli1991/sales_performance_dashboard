import pandas as pd

df = pd.read_excel("C:\Users\DELL\Desktop\sales_performance_portfolio_dataset")

df.head()

df.tail()

df.shape

df.info()

df.describe()

df.columns

df.isnull().sum()

df.duplicated().sum()

"""##**cleaning**"""

clean_df = df.copy()

clean_df.to_csv("cleaned_sales_data.csv", index=False)

import os

print(os.getcwd())

"""## Handling null values"""

(clean_df.isnull().sum() / len(clean_df) * 100).round(2)

clean_df["Customer"] = clean_df["Customer"].fillna("Unknown")

clean_df["Salesperson"] = clean_df["Salesperson"].fillna("Unknown")

clean_df["Discount"].median()

clean_df["Discount"] = clean_df["Discount"].fillna(
    clean_df["Discount"].median()
)

"""##**Handling duplicates**"""

clean_df[clean_df.duplicated()]

clean_df = clean_df.drop_duplicates()

clean_df.duplicated().sum()

"""## Check Datatypes"""

clean_df["Order_Date"] = pd.to_datetime(clean_df["Order_Date"])

clean_df.dtypes

"""##**Check for impossible values**"""

(clean_df["Quantity"] <= 0).sum()

(clean_df["Sales"] < 0).sum()

(clean_df["Profit"] < 0).sum()

"""## **After cleaning**"""

clean_df.shape

clean_df.isnull().sum()

"""## **Exploratory Data Analysis (EDA)**"""

## total sales
total_sales = clean_df["Sales"].sum()
print(total_sales)

## total profit
total_profit = clean_df["Profit"].sum()
print(total_profit)

## profit_margin
profit_margin = (total_profit / total_sales) * 100
print(profit_margin)

## total quantity sold
total_quantity = clean_df["Quantity"].sum()
print(total_quantity)

## average_order value
average_order = clean_df["Sales"].mean()
print(average_order)

## sales_byRegion
region_sales = clean_df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
print(region_sales)

##Top_5products
top_products = (
    clean_df.groupby("Product")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

print(top_products)

##profit_bycategory
category_profit = (
    clean_df.groupby("Category")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

print(category_profit)

"""## **Data Visualization**"""

## totalsales_by region with bar chart
import matplotlib.pyplot as plt

region_sales = clean_df.groupby("Region")["Sales"].sum().sort_values(ascending=False)

region_sales.plot(kind="bar")

plt.title("Sales by Region")
plt.xlabel("Region")
plt.ylabel("Total Sales")
plt.xticks(rotation=0)
plt.tight_layout()
plt.show()

## totalsales_byproduct
product_sales = (
    clean_df.groupby("Product")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

product_sales.plot(kind="bar")

plt.title("Sales by Product")
plt.xlabel("Product")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

## profit by category
category_profit = (
    clean_df.groupby("Category")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

category_profit.plot(kind="bar")

plt.title("Profit by Category")
plt.xlabel("Category")
plt.ylabel("Total Profit")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

"""##**Monthly Sales Trend**"""

## Create a Month column
clean_df["Month"] = clean_df["Order_Date"].dt.to_period("M")

## Calculate monthly sales
monthly_sales = clean_df.groupby("Month")["Sales"].sum()

print(monthly_sales)

## Create the trend chart
monthly_sales.plot(kind="line", figsize=(12, 5))

plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Total Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

## Find the best and worst months
print("Best month:")
print(monthly_sales.idxmax(), monthly_sales.max())

print("\nLowest month:")
print(monthly_sales.idxmin(), monthly_sales.min())

"""Best month: November 2024 — 257,935.63
Lowest month: June 2024 — 152,562.35

That means November sales were about 69% higher than June sales. This is a useful business observation.

Sales showed a fluctuating monthly pattern during the two-year period, with noticeable peaks and dips. November 2024 recorded the highest monthly sales at 257,935.63, while June 2024 recorded the lowest at 152,562.35. Overall, 2025 showed stronger sales performance compared with 2024.

## **Profitability Analysis**
"""

## Profit by Product
product_profit = (
    clean_df.groupby("Product")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

print(product_profit)

## Find the top 5 most profitable products
print(product_profit.head(5))

## Find the bottom 5
product_summary = clean_df.groupby("Product").agg(
    Sales=("Sales", "sum"),
    Profit=("Profit", "sum")
)

product_summary["Profit_Margin"] = (
    product_summary["Profit"] / product_summary["Sales"] * 100
)

product_summary = product_summary.sort_values(
    "Profit_Margin", ascending=False
)

print(product_summary)

product_summary.sort_values("Profit_Margin").head()

"""A product with high sales or high total profit does not necessarily have the highest profit margin.

For example, Laptop generates the highest total profit, while Headset has the highest profit margin. This distinction is valuable in a real Data Analyst portfolio.

## **Region + Category together**

The product with the highest sales isn't necessarily the product with the highest profitability.

Then we'll analyze Region + Category together and start building insights that look much more like real business analysis.
"""

region_category_profit = (
    clean_df.groupby(["Region", "Category"])["Profit"]
    .sum()
    .sort_values(ascending=False)
)

print(region_category_profit)

"""##**Key findings**

-🏆 Highest profit: Electronics in the South region — 269,563.28.

-📉 Lowest profit: Office Equipment in the West region — 19,703.16.

-💻 Strongest category: Electronics generates the highest profit in all four regions.

-🪑 Furniture: The South region generates the highest profit from Furniture.

-⚠️ Office Equipment: It is a relatively weak profit contributor across all four regions.

**Maintain Electronics performance:** Investigate which products and sales strategies are contributing to its strong profits.

**Investigate the South region:** Understand why Electronics and Furniture perform particularly well there.

**Review Office Equipment:** Examine its pricing, costs, discounts, and sales volume to identify opportunities to improve profitability.

**Avoid assumptions:** Low profit alone does not prove that a category is performing badly. Compare its sales, costs, and profit margin before making a final recommendation.

**Regional Profitability Analysis:** Electronics was the strongest profit-generating category across all four regions. The South region recorded the highest profit from Electronics, at 269,563.28, while Office Equipment in the West recorded the lowest profit, at 19,703.16. These findings suggest that the business should investigate the factors driving Electronics profitability and examine opportunities to improve Office Equipment performance.
"""

region_profit = (
    clean_df.groupby("Region")["Profit"]
    .sum()
    .sort_values(ascending=False)
)

print(region_profit)

"""The analysis shows that the South region has the highest total sales and the highest total profit in this synthetic dataset.

## **Customer Analysis**
"""

customer_sales = (
    clean_df.groupby("Customer")
    .agg(
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Profit", "sum"),
        Total_Orders=("Order_ID", "nunique")
    )
    .sort_values("Total_Sales", ascending=False)
)

print(customer_sales.head(10))

"""**Results**

Based on answers:

-Highest total sales: Customer_0318

-Highest profit among the top 10 customers: Customer_0231

-Does the customer with the highest sales also generate the highest profit? No.

💡 **Business Insight**

The customer generating the highest sales is not necessarily the customer generating the highest profit.

This can happen because customers may purchase different products, receive different discounts, or generate different costs.

**Business recommendation:** The company should evaluate both sales and profit when identifying its most valuable customers, rather than ranking customers by sales alone.

You can include this finding in your portfolio, but remember that the dataset contains synthetic sample data.

## **Customer Segmentation**
"""

customer_segments = customer_sales.copy()

customer_segments["Customer_Segment"] = pd.cut(
    customer_segments["Total_Sales"],
    bins=[-float("inf"), 500, 1500, float("inf")],
    labels=["Low Value", "Medium Value", "High Value"]
)

print(customer_segments["Customer_Segment"].value_counts())

"""The dataset has 5,000 cleaned sales records, and the original dataset was designed with 500 customer IDs. The result totals 501 customers, which may mean a missing customer value was handled differently than expected.

Also, 497 out of 501 customers are classified as High Value. This suggests that spending thresholds may not be appropriate for this dataset.

Let's investigate before drawing conclusions.

### **Step 1: Check the customer sales distribution**
"""

print(customer_sales["Total_Sales"].describe())

"""### **Step 2: Check the spending thresholds**"""

print(customer_sales["Total_Sales"].sort_values().head(10))
print(customer_sales["Total_Sales"].sort_values(ascending=False).head(10))

"""**Average vs. median:** Average customer sales are higher than median sales, suggesting that some high-spending customers pull the average upward.

**Spending variation:** Customer sales range from 1,152.51 to 29,644.86.

**Segmentation thresholds:** Our original thresholds of 500 and 1,500 were too low for this dataset.
"""

print("Number of unique customer groups:", clean_df["Customer"].nunique())
print(clean_df[clean_df["Customer"] == "Unknown"].shape[0])

"""**Improve customer segmentation**

Instead of choosing arbitrary spending thresholds, let's divide customers into three groups based on their actual spending distribution.
"""

known_customers = customer_sales[
    ~customer_sales.index.isin(["Unknown"])
].copy()

known_customers["Customer_Segment"] = pd.qcut(
    known_customers["Total_Sales"],
    q=3,
    labels=["Low Value", "Medium Value", "High Value"]
)

print(known_customers["Customer_Segment"].value_counts())

"""**Customer Segmentation Results**

There found 12 records with an unknown customer.

These records were created when missing customer names were replaced with "Unknown". Excluding that group from individual customer segmentation is appropriate because we cannot identify the actual customers.

These results show that your known customers have been divided into three approximately equal groups based on total sales.

Customer segmentation helps businesses develop targeted marketing strategies.

For example:

Low Value: Explore ways to encourage repeat purchases and increase order value.
Medium Value: Offer relevant product recommendations and bundles to encourage additional purchases.
High Value: Consider loyalty programs and personalized service to maintain customer relationships.

These are potential strategies, not proven recommendations. Additional analysis would be needed to determine which actions are likely to work.

Let's investigate whether high-value customers also generate the highest profits.
"""

segment_analysis = known_customers.groupby(
    "Customer_Segment",
    observed=True
).agg(
    Total_Sales=("Total_Sales", "sum"),
    Total_Profit=("Total_Profit", "sum"),
    Customer_Count=("Total_Sales", "count")
)

segment_analysis["Profit_Margin"] = (
    segment_analysis["Total_Profit"]
    / segment_analysis["Total_Sales"]
    * 100
)

print(segment_analysis.round(2))

print(segment_analysis.sort_values("Profit_Margin", ascending=False))

"""If the Low Value segment has the highest profit margin, it suggests that these customers generate more profit relative to their sales.

Remember the difference:

**Total profit** measures the amount of profit generated.

**Profit margin** measures profit as a percentage of sales.

A customer segment can generate less total profit but have a higher profit margin.
"""
