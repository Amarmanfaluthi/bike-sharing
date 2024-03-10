import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_daily_rent_df(df):
    daily_rent_df = df.resample(rule='D', on='dteday').agg({
        "cnt": "sum"
    })
    daily_rent_df = daily_rent_df.reset_index()
    daily_rent_df.rename(columns={
        "cnt": "rent_count"
    }, inplace=True)
    return daily_rent_df

def create_byseason_df(df):
    # Mengubah nilai numerik musim menjadi nama musim
    season_name = {1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'}
    df['season_name'] = df['season'].map(season_name)
    
    # Mengelompokkan berdasarkan nama musim dan menghitung jumlah cnt untuk setiap musim
    byseason_df = df.groupby('season_name').agg({'cnt': 'sum'}).reset_index()
    
    return byseason_df

all_df = pd.read_csv("all_data.csv")
if 'season_x' in all_df.columns and 'season_y' in all_df.columns:
    # Jika ada, gabungkan nilai dari kedua kolom menjadi satu kolom
    all_df['season'] = all_df['season_x'].fillna(all_df['season_y'])
    # Setelah menggabungkan nilai, Anda bisa menghapus kolom season_x dan season_y
    all_df.drop(['season_x', 'season_y'], axis=1, inplace=True)

if 'cnt_x' in all_df.columns and 'cnt_y' in all_df.columns:
    # Jika ada, gabungkan nilai dari kedua kolom menjadi satu kolom
    all_df['cnt'] = all_df['cnt_x'].fillna(all_df['cnt_y'])
    # Setelah menggabungkan nilai, Anda bisa menghapus kolom cnt_x dan cnt_y
    all_df.drop(['cnt_x', 'cnt_y'], axis=1, inplace=True)


all_df['dteday'] = pd.to_datetime(all_df['dteday'])

all_df.sort_values(by='dteday', inplace=True)
all_df.reset_index(inplace=True)


min_date = all_df["dteday"].min()
max_date = all_df["dteday"].max()
 
with st.sidebar:

    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu', min_value=min_date,
        max_value=max_date, value=[min_date, max_date]
    )

main_df = all_df[(all_df["dteday"] >= str(start_date)) & 
                (all_df["dteday"] <= str(end_date)) & 
                (all_df["season"].notnull())]

daily_rent_df = create_daily_rent_df(main_df)
byseason_df = create_byseason_df(main_df)


st.header('Bike Sharing :sparkles:')

st.subheader('daily Rent')
 
col1, col2 = st.columns(2)
 
with col1:
    total_rent = daily_rent_df.rent_count.sum()
    st.metric("Total Rents", value=total_rent)
 
with col2:
    fig, ax = plt.subplots(figsize=(16, 8))
    ax.plot(
        daily_rent_df["dteday"],
        daily_rent_df["rent_count"],
        marker='o', 
        linewidth=2,
        color="#90CAF9"
    )
    ax.tick_params(axis='y', labelsize=20)
    ax.tick_params(axis='x', labelsize=15)
    st.pyplot(fig)

st.subheader("Customer Demographics by Season")

fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3"]

sns.barplot(
    x="cnt", 
    y="season_name",
    data=byseason_df.sort_values(by="cnt", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("Number of Customers by Season", loc="center", fontsize=30)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
st.pyplot(fig)