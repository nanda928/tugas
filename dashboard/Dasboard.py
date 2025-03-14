import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Load data
day_df = pd.read_csv('data/day.csv')
hour_df = pd.read_csv('data/hour.csv')

# Konversi kolom 'dteday' ke tipe datetime
day_df['dteday'] = pd.to_datetime(day_df['dteday'])
hour_df['dteday'] = pd.to_datetime(hour_df['dteday'])

# Judul Dashboard
st.title('Analisis Data Peminjaman Sepeda')

# Sidebar untuk navigasi
st.sidebar.title('Navigasi')
options = st.sidebar.radio('Pilih Analisis:', 
                           ['Pola Penggunaan Sepeda', 'Pengaruh Cuaca', 'Tren Penggunaan Sepeda'])

# Filter interaktif di sidebar
st.sidebar.header('Filter Data')
selected_season = st.sidebar.selectbox('Pilih Musim:', ['Semua', 'Musim Semi (1)', 'Musim Panas (2)', 'Musim Gugur (3)', 'Musim Dingin (4)'])
selected_weather = st.sidebar.selectbox('Pilih Kondisi Cuaca:', ['Semua', 'Cerah (1)', 'Berkabut (2)', 'Hujan Ringan (3)', 'Hujan Lebat (4)'])
date_range = st.sidebar.date_input('Pilih Rentang Tanggal:', 
                                   [day_df['dteday'].min(), day_df['dteday'].max()])

# Fungsi untuk memfilter data berdasarkan pilihan pengguna
def filter_data(df, season, weather, date_range):
    if season != 'Semua':
        season_num = int(season.split('(')[1].replace(')', ''))
        df = df[df['season'] == season_num]
    if weather != 'Semua':
        weather_num = int(weather.split('(')[1].replace(')', ''))
        df = df[df['weathersit'] == weather_num]
    df = df[(df['dteday'] >= pd.to_datetime(date_range[0])) & (df['dteday'] <= pd.to_datetime(date_range[1]))]
    return df

# Terapkan filter ke dataset
filtered_day_df = filter_data(day_df, selected_season, selected_weather, date_range)
filtered_hour_df = filter_data(hour_df, selected_season, selected_weather, date_range)

# Fungsi untuk visualisasi pola penggunaan sepeda
def pola_penggunaan():
    st.header('Pola Penggunaan Sepeda')
    
    # Pola penggunaan berdasarkan musim
    st.subheader('Pola Penggunaan Berdasarkan Musim')
    seasonal_avg_day = filtered_day_df.groupby('season')['cnt'].mean()
    fig, ax = plt.subplots()
    seasonal_avg_day.plot(kind='bar', ax=ax)
    ax.set_ylabel('Rata-rata Peminjaman')
    ax.set_xlabel('Musim')
    st.pyplot(fig)
    
    # Pola penggunaan berdasarkan bulan
    st.subheader('Pola Penggunaan Berdasarkan Bulan')
    monthly_avg_day = filtered_day_df.groupby('mnth')['cnt'].mean()
    fig, ax = plt.subplots()
    monthly_avg_day.plot(kind='bar', ax=ax)
    ax.set_ylabel('Rata-rata Peminjaman')
    ax.set_xlabel('Bulan')
    st.pyplot(fig)
    
    # Pola penggunaan berdasarkan jam
    st.subheader('Pola Penggunaan Berdasarkan Jam')
    hourly_avg = filtered_hour_df.groupby('hr')['cnt'].mean()
    fig, ax = plt.subplots()
    hourly_avg.plot(kind='line', ax=ax)
    ax.set_ylabel('Rata-rata Peminjaman')
    ax.set_xlabel('Jam')
    st.pyplot(fig)

# Fungsi untuk visualisasi pengaruh cuaca
def pengaruh_cuaca():
    st.header('Pengaruh Cuaca Terhadap Jumlah Peminjaman Sepeda')
    
    # Korelasi cuaca dengan jumlah peminjaman
    st.subheader('Korelasi Cuaca dengan Jumlah Peminjaman')
    weather_avg_day = filtered_day_df.groupby('weathersit')['cnt'].mean()
    fig, ax = plt.subplots()
    weather_avg_day.plot(kind='bar', ax=ax)
    ax.set_ylabel('Rata-rata Peminjaman')
    ax.set_xlabel('Kondisi Cuaca')
    st.pyplot(fig)
    
    # Scatter plot suhu vs jumlah peminjaman
    st.subheader('Scatter Plot Suhu vs Jumlah Peminjaman')
    fig, ax = plt.subplots()
    sns.scatterplot(x='temp', y='cnt', data=filtered_day_df, ax=ax)
    ax.set_ylabel('Jumlah Peminjaman')
    ax.set_xlabel('Suhu')
    st.pyplot(fig)

# Fungsi untuk visualisasi tren penggunaan sepeda
def tren_penggunaan():
    st.header('Tren Penggunaan Sepeda dari Tahun ke Tahun')
    
    # Tren penggunaan sepeda per tahun
    st.subheader('Tren Penggunaan Sepeda per Tahun')
    yearly_avg_day = filtered_day_df.groupby('yr')['cnt'].mean()
    fig, ax = plt.subplots()
    yearly_avg_day.plot(kind='line', ax=ax)
    ax.set_ylabel('Rata-rata Peminjaman')
    ax.set_xlabel('Tahun')
    st.pyplot(fig)
    
    # Tren penggunaan sepeda per bulan dalam setahun
    st.subheader('Tren Penggunaan Sepeda per Bulan dalam Setahun')
    monthly_trend = filtered_day_df.groupby(['yr', 'mnth'])['cnt'].mean().unstack()
    fig, ax = plt.subplots(figsize=(12, 6))
    monthly_trend.plot(ax=ax)
    ax.set_ylabel('Rata-rata Peminjaman')
    ax.set_xlabel('Bulan')
    st.pyplot(fig)

# Pilih analisis berdasarkan pilihan pengguna
if options == 'Pola Penggunaan Sepeda':
    pola_penggunaan()
elif options == 'Pengaruh Cuaca':
    pengaruh_cuaca()
elif options == 'Tren Penggunaan Sepeda':
    tren_penggunaan()
