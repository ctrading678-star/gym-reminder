# app.py
import streamlit as st
import pandas as pd
import datetime

st.set_page_config(page_title="📊 Investing Data Fetcher", layout="centered")

st.title("📈 تحميل بيانات سهم من Investing.com")
st.markdown("أدخل المعطيات التالية لتحميل البيانات التاريخية وحفظها في ملف CSV")

# --- إدخال البيانات من المستخدم ---
stock_name = st.text_input("🔸 اسم السهم كما في Investing.com (مثال: SIAME)")
country = st.text_input("🌍 الدولة بالإنجليزية (مثال: tunisia)")
from_date = st.date_input("📅 من تاريخ", datetime.date(2025, 5, 1))
to_date = st.date_input("📅 إلى تاريخ", datetime.date.today())
out_csv = st.text_input("💾 اسم ملف CSV الناتج", "stock_data.csv")

# --- عند الضغط على الزر ---
if st.button("🚀 تحميل البيانات"):
    if not stock_name or not country:
        st.warning("الرجاء إدخال اسم السهم والدولة قبل المتابعة.")
    else:
        with st.spinner("⏳ جاري جلب البيانات من Investing.com ..."):
            try:
                import investpy

                data = investpy.get_stock_historical_data(
                    stock=stock_name,
                    country=country,
                    from_date=from_date.strftime("%d/%m/%Y"),
                    to_date=to_date.strftime("%d/%m/%Y")
                )

                # حفظ البيانات
                data.to_csv(out_csv, encoding="utf-8-sig")

                st.success(f"✅ تم تحميل البيانات وحفظها في الملف: {out_csv}")
                st.dataframe(data.tail(10))  # عرض آخر 10 أسطر
                st.download_button("📥 تحميل CSV", data.to_csv().encode('utf-8-sig'), out_csv, "text/csv")

            except Exception as e:
                import traceback
                st.error("❌ حدث خطأ أثناء تحميل البيانات:")
                st.text(traceback.format_exc())

