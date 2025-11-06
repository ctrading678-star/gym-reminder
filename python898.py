import streamlit as st
import yfinance as yf
import pandas as pd
import datetime

st.title("📊 تحميل بيانات الأسهم من Yahoo Finance")

# --- قائمة رموز الأسهم التونسية أو العالمية ---
stocks = {
    "SIAME (Tunisia)": "SIAME.TN",
    "BT (Banque de Tunisie)": "BT.TN",
    "BIAT": "BIAT.TN",
    "TUNISAIR": "TAIR.TN",
    "SFBT": "SFBT.TN",
    "Office Plast": "PLS.TN"
}

# --- اختيار السهم ---
selected_name = st.selectbox("🔍 اختر السهم:", list(stocks.keys()))
ticker_symbol = stocks[selected_name]

# --- اختيار الفترة الزمنية ---
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("من تاريخ:", datetime.date(2023, 1, 1))
with col2:
    end_date = st.date_input("إلى تاريخ:", datetime.date.today())

# --- زر التحميل ---
if st.button("📥 تحميل البيانات"):
    if start_date >= end_date:
        st.error("❌ يجب أن يكون تاريخ النهاية أكبر من تاريخ البداية.")
    else:
        data = yf.download(ticker_symbol, start=start_date, end=end_date)

        if data.empty:
            st.warning("⚠️ لا توجد بيانات في هذه الفترة للسهم المحدد.")
        else:
            st.success(f"✅ تم تحميل بيانات {selected_name}")
            st.dataframe(data)

            # حفظ الملف CSV
            csv = data.to_csv().encode('utf-8')
            file_name = f"{ticker_symbol}_data.csv"
            st.download_button("💾 تحميل الملف CSV", csv, file_name, "text/csv")


