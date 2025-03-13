import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Load data
day_df = pd.read_csv('data/day.csv')
hour_df = pd.read_csv('data/hour.csv')

# Judul Dashboard
st.title('Analisis Data Peminjaman Sepeda')

# Sidebar untuk navigasi
st.sidebar.title('Navigasi')
options = st.sidebar.radio('Pilih Analisis:', 
                           ['Pola Penggunaan Sepeda', 'Pengaruh Cuaca', 'Tren Penggunaan Sepeda'])

# Fungsi untuk visualisasi pola penggunaan sepeda
def pola_penggunaan():
    st.header('Pola Penggunaan Sepeda')
    
    # Pola penggunaan berdasarkan musim
    st.subheader('Pola Penggunaan Berdasarkan Musim')
    seasonal_avg_day = day_df.groupby('season')['cnt'].mean()
    fig, ax = plt.subplots()
    seasonal_avg_day.plot(kind='bar', ax=ax)
    ax.set_ylabel('Rata-rata Peminjaman')
    ax.set_xlabel('Musim')
    st.pyplot(fig)
    
    # Pola penggunaan berdasarkan bulan
    st.subheader('Pola Penggunaan Berdasarkan Bulan')
    monthly_avg_day = day_df.groupby('mnth')['cnt'].mean()
    fig, ax = plt.subplots()
    monthly_avg_day.plot(kind='bar', ax=ax)
    ax.set_ylabel('Rata-rata Peminjaman')
    ax.set_xlabel('Bulan')
    st.pyplot(fig)
    
    # Pola penggunaan berdasarkan jam
    st.subheader('Pola Penggunaan Berdasarkan Jam')
    hourly_avg = hour_df.groupby('hr')['cnt'].mean()
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
    weather_avg_day = day_df.groupby('weathersit')['cnt'].mean()
    fig, ax = plt.subplots()
    weather_avg_day.plot(kind='bar', ax=ax)
    ax.set_ylabel('Rata-rata Peminjaman')
    ax.set_xlabel('Kondisi Cuaca')
    st.pyplot(fig)
    
    # Scatter plot suhu vs jumlah peminjaman
    st.subheader('Scatter Plot Suhu vs Jumlah Peminjaman')
    fig, ax = plt.subplots()
    sns.scatterplot(x='temp', y='cnt', data=day_df, ax=ax)
    ax.set_ylabel('Jumlah Peminjaman')
    ax.set_xlabel('Suhu')
    st.pyplot(fig)

# Fungsi untuk visualisasi tren penggunaan sepeda
def tren_penggunaan():
    st.header('Tren Penggunaan Sepeda dari Tahun ke Tahun')
    
    # Tren penggunaan sepeda per tahun
    st.subheader('Tren Penggunaan Sepeda per Tahun')
    yearly_avg_day = day_df.groupby('yr')['cnt'].mean()
    fig, ax = plt.subplots()
    yearly_avg_day.plot(kind='line', ax=ax)
    ax.set_ylabel('Rata-rata Peminjaman')
    ax.set_xlabel('Tahun')
    st.pyplot(fig)
    
    # Tren penggunaan sepeda per bulan dalam setahun
    st.subheader('Tren Penggunaan Sepeda per Bulan dalam Setahun')
    monthly_trend = day_df.groupby(['yr', 'mnth'])['cnt'].mean().unstack()
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
