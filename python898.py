import streamlit as st
import pandas as pd
import investpy
from datetime import date, timedelta

# ==============================
# 🔹 تحميل قائمة الشركات التونسية (الاسم + الرمز)
# ==============================
@st.cache_data
def get_tunisian_companies():
    try:
        companies = investpy.stocks.get_stocks(country="tunisia")
        return companies[["name", "symbol"]]
    except Exception as e:
        st.error(f"حدث خطأ أثناء جلب قائمة الشركات: {e}")
        return pd.DataFrame()

# ==============================
# 🔹 تحميل البيانات التاريخية لشركة معينة عبر رمزها
# ==============================
def get_stock_data_tunisia(symbol, from_date, to_date):
    try:
        data = investpy.get_stock_historical_data(
            stock=symbol,
            country="tunisia",
            from_date=from_date.strftime("%d/%m/%Y"),
            to_date=to_date.strftime("%d/%m/%Y")
        )
        return data
    except Exception as e:
        st.error(f"حدث خطأ أثناء تحميل بيانات {symbol}: {e}")
        return pd.DataFrame()

# ==============================
# 🔹 واجهة Streamlit
# ==============================
st.set_page_config(page_title="تحليل الشركات التونسية", layout="wide")

st.title("📊 تحليل الشركات المدرجة في بورصة تونس 🇹🇳")
st.markdown("---")

df_companies = get_tunisian_companies()

if not df_companies.empty:
    st.success("✅ تم تحميل قائمة الشركات التونسية بنجاح.")
    
    company_name = st.selectbox("اختر الشركة:", df_companies["name"].sort_values().unique())

    if company_name:
        # الحصول على رمز الشركة
        company_symbol = df_companies.loc[df_companies["name"] == company_name, "symbol"].values[0]
        
        st.markdown(f"**رمز السهم:** `{company_symbol}`")

        st.markdown("### 🗓️ اختر فترة التحليل")

        today = date.today()
        start_date = st.date_input("من تاريخ:", today - timedelta(days=180))
        end_date = st.date_input("إلى تاريخ:", today)

        if st.button("عرض البيانات"):
            with st.spinner("⏳ جاري تحميل بيانات السهم..."):
                data = get_stock_data_tunisia(company_symbol, start_date, end_date)
                if not data.empty:
                    st.success(f"✅ تم تحميل بيانات {company_name}")
                    st.dataframe(data.tail(), use_container_width=True)
                    st.line_chart(data["Close"], use_container_width=True)
                else:
                    st.warning("⚠️ لم يتم العثور على بيانات للسهم المحدد.")
else:
    st.error("❌ تعذّر تحميل قائمة الشركات التونسية من المصدر.")




