import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# ================================================
# PAGE CONFIG
# ================================================
st.set_page_config(
    page_title="Walmart Sales Dashboard",
    page_icon="🛒",
    layout="wide"
)


# ================================================
# LOAD DATA
# ================================================
@st.cache_data
def load_data():
    df = pd.read_csv("Walmart.csv")
    df['unit_price'] = df['unit_price'].str.replace('$', '', regex=False).astype(float)
    df = df.dropna()
    df['total_sales'] = df['unit_price'] * df['quantity']
    return df

df = load_data()

# ================================================
# SIDEBAR FILTERS
# ================================================
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/c/ca/Walmart_logo.svg", width=200)
st.sidebar.title("Filters")

# City filter
all_cities = ["All"] + sorted(df["City"].unique().tolist())
selected_city = st.sidebar.selectbox("Select City", all_cities)

# Category filter
all_categories = ["All"] + sorted(df["category"].unique().tolist())
selected_category = st.sidebar.multiselect("Select Category", all_categories, default="All")

# Payment filter
all_payments = ["All"] + sorted(df["payment_method"].unique().tolist())
selected_payment = st.sidebar.selectbox("Select Payment Method", all_payments)

# Apply filters
filtered_df = df.copy()
if selected_city != "All":
    filtered_df = filtered_df[filtered_df["City"] == selected_city]
if "All" not in selected_category and selected_category:
    filtered_df = filtered_df[filtered_df["category"].isin(selected_category)]
if selected_payment != "All":
    filtered_df = filtered_df[filtered_df["payment_method"] == selected_payment]

# ================================================
# HEADER
# ================================================
st.title("🛒 Walmart Sales Analytics Dashboard")
st.markdown("**End-to-End Data Analysis using Python & PostgreSQL**")
st.markdown("---")

# ================================================
# KPI METRICS ROW
# ================================================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Revenue", f"${filtered_df['total_sales'].sum():,.2f}")
with col2:
    st.metric("Total Transactions", f"{len(filtered_df):,}")
with col3:
    st.metric("Avg Transaction Value", f"${filtered_df['total_sales'].mean():,.2f}")
with col4:
    st.metric("Avg Rating", f"{filtered_df['rating'].mean():,.2f}")

st.markdown("---")

# ================================================
# ROW 1 - Revenue by Category & Payment Methods
# ================================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("📦 Revenue by Category")
    cat_sales = filtered_df.groupby("category")["total_sales"].sum().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    cat_sales.plot(kind="barh", ax=ax, color="#2196F3")
    ax.set_xlabel("Total Sales ($)")
    ax.set_ylabel("")
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    st.subheader("💳 Payment Method Distribution")
    payment_counts = filtered_df["payment_method"].value_counts()
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.pie(payment_counts.values, labels=payment_counts.index,
           autopct='%1.1f%%', colors=['#2196F3', '#4CAF50', '#FF9800'])
    plt.tight_layout()
    st.pyplot(fig)

# ================================================
# ROW 2 - Top Cities & Monthly Trend
# ================================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("🏙️ Top 10 Cities by Revenue")
    city_sales = filtered_df.groupby("City")["total_sales"].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(8, 5))
    city_sales.plot(kind="bar", ax=ax, color="#4CAF50")
    ax.set_xlabel("")
    ax.set_ylabel("Total Sales ($)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    st.subheader("📈 Monthly Sales Trend")
    filtered_df["date"] = pd.to_datetime(filtered_df["date"], format='mixed', dayfirst=True)
    monthly = filtered_df.groupby(filtered_df["date"].dt.to_period("M"))["total_sales"].sum()
    fig, ax = plt.subplots(figsize=(8, 5))
    monthly.plot(kind="line", ax=ax, marker="o", color="#FF9800", linewidth=2)
    ax.set_xlabel("Month")
    ax.set_ylabel("Total Sales ($)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

# ================================================
# ROW 3 - Rating Analysis & Raw Data
# ================================================
col1, col2 = st.columns(2)

with col1:
    st.subheader("⭐ Average Rating by Category")
    avg_rating = filtered_df.groupby("category")["rating"].mean().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    avg_rating.plot(kind="barh", ax=ax, color="#9C27B0")
    ax.set_xlabel("Average Rating")
    plt.tight_layout()
    st.pyplot(fig)

with col2:
    st.subheader("📊 Profit Margin by Category")
    avg_profit = filtered_df.groupby("category")["profit_margin"].mean().sort_values(ascending=True)
    fig, ax = plt.subplots(figsize=(8, 5))
    avg_profit.plot(kind="barh", ax=ax, color="#F44336")
    ax.set_xlabel("Avg Profit Margin")
    plt.tight_layout()
    st.pyplot(fig)

# ================================================
# RAW DATA TABLE
# ================================================
st.markdown("---")
st.subheader("📋 Raw Data")
st.dataframe(filtered_df.head(100), use_container_width=True)

st.markdown("---")
st.markdown("Built with ❤️ by Anitha Morampudi | Python + PostgreSQL + Streamlit")