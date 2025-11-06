import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# ===============================
# واجهة التطبيق
# ===============================
st.set_page_config(page_title="📈 بيانات الأسهم", layout="centered")

st.title("📊 تحميل بيانات الأسهم")

# ===============================
# الدول والأسهم المتاحة
# ===============================
stocks_by_country = {
    "🇺🇸 الولايات المتحدة": {
        "Apple (AAPL)": "AAPL",
        "Microsoft (MSFT)": "MSFT",
        "Tesla (TSLA)": "TSLA",
        "Nvidia (NVDA)": "NVDA"
    },
    "🇫🇷 فرنسا": {
        "Airbus (AIR.PA)": "AIR.PA",
        "LVMH (MC.PA)": "MC.PA",
        "Renault (RNO.PA)": "RNO.PA"
    },
    "🇩🇪 ألمانيا": {
        "BMW (BMW.DE)": "BMW.DE",
        "Siemens (SIE.DE)": "SIE.DE",
        "Volkswagen (VOW3.DE)": "VOW3.DE"
    },
    "🇬🇧 المملكة المتحدة": {
        "HSBC (HSBA.L)": "HSBA.L",
        "BP (BP.L)": "BP.L",
        "AstraZeneca (AZN.L)": "AZN.L"
    },
    "🇯🇵 اليابان": {
        "Toyota (7203.T)": "7203.T",
        "Sony (6758.T)": "6758.T",
        "Honda (7267.T)": "7267.T"
    },
    "🇨🇦 كندا": {
        "Shopify (SHOP.TO)": "SHOP.TO",
        "Royal Bank (RY.TO)": "RY.TO",
        "TD Bank (TD.TO)": "TD.TO"
    },
    "🇮🇳 الهند": {
        "Reliance (RELIANCE.NS)": "RELIANCE.NS",
        "Tata Motors (TATAMOTORS.NS)": "TATAMOTORS.NS",
        "Infosys (INFY.NS)": "INFY.NS"
    }
}

# ===============================
# اختيار الدولة
# ===============================
country = st.selectbox("🌍 اختر الدولة:", list(stocks_by_country.keys()))

# ===============================
# اختيار الشركة
# ===============================
companies = stocks_by_country[country]
company_name = st.selectbox("🏢 اختر الشركة:", list(companies.keys()))
stock_symbol = companies[company_name]

# ===============================
# تحميل البيانات (دائمًا لفترة شهر)
# ===============================
if st.button("تحميل البيانات"):
    try:
        data = yf.download(stock_symbol, period="1mo")

        if data.empty:
            st.error("⚠️ لم يتم العثور على بيانات لهذا السهم.")
        else:
            st.success(f"✅ تم تحميل بيانات {company_name} بنجاح!")

            # عرض آخر 10 أيام من البيانات
            st.dataframe(data.tail(10))

            # ===============================
            # رسم بياني بالشموع اليابانية
            # ===============================
            fig = go.Figure(
                data=[
                    go.Candlestick(
                        x=data.index,
                        open=data['Open'],
                        high=data['High'],
                        low=data['Low'],
                        close=data['Close']
                    )
                ]
            )

            fig.update_layout(
                title=f"رسم بياني لسهم {company_name}",
                xaxis_title="📅 التاريخ",
                yaxis_title="💲 السعر",
                xaxis_rangeslider_visible=False
            )

            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"حدث خطأ أثناء تحميل البيانات: {e}")


