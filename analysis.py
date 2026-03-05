import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import seaborn as sns

# ================================================
# LOAD DATA
# ================================================
df = pd.read_csv("Walmart.csv")

# ================================================
# DATA CLEANING
# ================================================
df['unit_price'] = df['unit_price'].str.replace('$', '', regex=False).astype(float)
df = df.dropna()
df['total_sales'] = df['unit_price'] * df['quantity']

# ================================================
# CONNECT TO POSTGRESQL
# ================================================
engine = create_engine('postgresql+psycopg2://postgres:admin123@localhost:5432/walmart_db')
df.to_sql('walmart_sales', engine, if_exists='replace', index=False)
print("✅ Data pushed to PostgreSQL!")

# ================================================
# SQL QUERY 1 - Top 10 Cities by Revenue
# ================================================
# SQL QUERY 1 - Top 10 Cities by Revenue
query1 = """
    SELECT "City", 
           ROUND(SUM(total_sales)::numeric, 2) as total_revenue
    FROM walmart_sales
    GROUP BY "City"
    ORDER BY total_revenue DESC
    LIMIT 10;
"""
result1 = pd.read_sql_query(query1, engine)
print("\nTop 10 Cities by Revenue:")
print(result1)

# SQL QUERY 2 - Revenue by Category
query2 = """
    SELECT category,
           ROUND(SUM(total_sales)::numeric, 2) as total_revenue,
           ROUND(AVG(rating)::numeric, 2) as avg_rating
    FROM walmart_sales
    GROUP BY category
    ORDER BY total_revenue DESC;
"""
result2 = pd.read_sql_query(query2, engine)
print("\nRevenue by Category:")
print(result2)

# SQL QUERY 3 - Payment Method Analysis
query3 = """
    SELECT payment_method,
           COUNT(*) as total_transactions,
           ROUND(SUM(total_sales)::numeric, 2) as total_revenue
    FROM walmart_sales
    GROUP BY payment_method
    ORDER BY total_transactions DESC;
"""
result3 = pd.read_sql_query(query3, engine)
print("\nPayment Method Analysis:")
print(result3)

# SQL QUERY 4 - Best Profit Margin by Category
query4 = """
    SELECT category,
           ROUND(AVG(profit_margin)::numeric, 2) as avg_profit_margin,
           ROUND(SUM(total_sales)::numeric, 2) as total_revenue
    FROM walmart_sales
    GROUP BY category
    ORDER BY avg_profit_margin DESC;
"""
result4 = pd.read_sql_query(query4, engine)
print("\nProfit Margin by Category:")
print(result4)

# SQL QUERY 5 - Monthly Sales Trend
query5 = """
    SELECT 
           TO_CHAR(TO_DATE(date, 'DD/MM/YY'), 'YYYY-MM') as month,
           ROUND(SUM(total_sales)::numeric, 2) as monthly_revenue,
           COUNT(*) as total_transactions
    FROM walmart_sales
    GROUP BY month
    ORDER BY month;
"""
result5 = pd.read_sql_query(query5, engine)
print("\nMonthly Sales Trend:")
print(result5)
# ================================================
# VISUALIZATIONS
# ================================================
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Chart 1 - Top 10 Cities by Revenue
city_sales = result1.set_index('City')['total_revenue']
plt.figure()
sns.barplot(x=city_sales.values, y=city_sales.index,
            hue=city_sales.index, palette='Blues_r', legend=False)
plt.title('Top 10 Walmart Cities by Revenue', fontsize=16, fontweight='bold')
plt.xlabel('Total Sales ($)')
plt.ylabel('City')
plt.tight_layout()
plt.savefig('top_cities.png')
plt.show()

# Chart 2 - Revenue by Category
category_sales = result2.set_index('category')['total_revenue']
plt.figure()
sns.barplot(x=category_sales.values, y=category_sales.index,
            hue=category_sales.index, palette='Greens_r', legend=False)
plt.title('Revenue by Product Category', fontsize=16, fontweight='bold')
plt.xlabel('Total Sales ($)')
plt.ylabel('Category')
plt.tight_layout()
plt.savefig('category_sales.png')
plt.show()

# Chart 3 - Payment Method Distribution
payment_counts = result3.set_index('payment_method')['total_transactions']
plt.figure(figsize=(8, 8))
plt.pie(payment_counts.values, labels=payment_counts.index,
        autopct='%1.1f%%', colors=['#2196F3','#4CAF50','#FF9800'])
plt.title('Payment Method Distribution', fontsize=16, fontweight='bold')
plt.tight_layout()
plt.savefig('payment_methods.png')
plt.show()

# Chart 4 - Monthly Sales Trend
plt.figure()
plt.plot(result5['month'], result5['monthly_revenue'], 
         marker='o', linewidth=2, color='#2196F3')
plt.title('Monthly Sales Trend', fontsize=16, fontweight='bold')
plt.xlabel('Month')
plt.ylabel('Total Revenue ($)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('monthly_trend.png')
plt.show()