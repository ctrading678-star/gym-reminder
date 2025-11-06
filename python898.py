import streamlit as st
import investpy
import datetime
import pandas as pd

# عنوان التطبيق
st.title("📈 تحميل بيانات الأسهم من Investing.com (تونس)")

# --- الخطوة 1: جلب قائمة الأسهم المتاحة في تونس ---
try:
    stocks_list = investpy.stocks.get_stocks_list(country='tunisia')
except Exception as e:
    st.error(f"حدث خطأ أثناء تحميل قائمة الأسهم: {e}")
    st.stop()

# --- الخطوة 2: اختيار السهم ---
selected_stock = st.selectbox("🔍 اختر اسم السهم من القائمة:", stocks_list)

# --- الخطوة 3: تحديد الفترة الزمنية ---
col1, col2 = st.columns(2)
with col1:
    start_date = st.date_input("من تاريخ:", datetime.date(2023, 1, 1))
with col2:
    end_date = st.date_input("إلى تاريخ:", datetime.date.today())

# --- الخطوة 4: زر التحميل ---
if st.button("📥 تحميل البيانات"):
    if start_date >= end_date:
        st.error("❌ يجب أن يكون تاريخ النهاية أكبر من تاريخ البداية.")
    else:
        try:
            data = investpy.get_stock_historical_data(
                stock=selected_stock,
                country='tunisia',
                from_date=start_date.strftime("%d/%m/%Y"),
                to_date=end_date.strftime("%d/%m/%Y")
            )

            st.success(f"✅ تم تحميل بيانات السهم: {selected_stock}")
            st.dataframe(data)

            # حفظ البيانات في ملف CSV
            file_name = f"{selected_stock}_data.csv"
            data.to_csv(file_name)
            st.download_button("💾 تحميل الملف CSV", data.to_csv().encode('utf-8'), file_name, "text/csv")

        except Exception as e:
            st.error(f"⚠️ حدث خطأ أثناء تحميل البيانات: {e}")


