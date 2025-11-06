import streamlit as st
import pandas as pd
import requests

# ==============================
# 🟢 دالة جلب بيانات بورصة تونس
# ==============================
def get_tunisian_stocks_data():
    url = "https://www.bvmt.com.tn/fr/cours"
    try:
        tables = pd.read_html(url)
        df = tables[0]
        df.columns = [col.strip() for col in df.columns]
        # تنظيف الأعمدة
        df = df.rename(columns={
            'Valeurs': 'الشركة',
            'Cours de clôture': 'سعر الإغلاق',
            'Variation (%)': 'نسبة التغير',
            'Ouverture': 'سعر الافتتاح',
            'Plus haut': 'أعلى سعر',
            'Plus bas': 'أدنى سعر',
            'Volume': 'حجم التداول',
            'Capitalisation (en DT)': 'القيمة السوقية'
        }, errors='ignore')
        return df
    except Exception as e:
        st.error(f"حدث خطأ أثناء تحميل البيانات: {e}")
        return pd.DataFrame()

# ==============================
# 🟢 واجهة Streamlit
# ==============================
st.set_page_config(page_title="تحليل الشركات التونسية - بورصة تونس", layout="wide")

st.title("📊 تحليل بيانات الشركات المدرجة في بورصة تونس (BVMT)")
st.markdown("---")

st.info("يتم جلب البيانات مباشرة من الموقع الرسمي لبورصة تونس (www.bvmt.com.tn).")

# زر لتحديث البيانات
if st.button("🔄 تحديث البيانات الآن"):
    df = get_tunisian_stocks_data()
    if not df.empty:
        st.success("✅ تم تحميل البيانات بنجاح.")
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("⚠️ لم يتم العثور على بيانات.")
else:
    st.write("اضغط على الزر أعلاه لجلب أحدث البيانات.")

# ==============================
# 🟢 قسم التحليل الإحصائي
# ==============================
st.markdown("## 🔍 التحليل الإحصائي")

if 'df' in locals() and not df.empty:
    # تحويل القيم الرقمية
    numeric_cols = ['سعر الإغلاق', 'سعر الافتتاح', 'أعلى سعر', 'أدنى سعر', 'نسبة التغير']
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', '.').str.replace('%', ''), errors='coerce')

    # اختيار شركة للتحليل
    company = st.selectbox("اختر الشركة:", df['الشركة'].unique())

    if company:
        selected = df[df['الشركة'] == company].iloc[0]
        st.subheader(f"📈 تحليل: {company}")
        st.write(f"- **سعر الإغلاق:** {selected.get('سعر الإغلاق', 'غير متوفر')}")
        st.write(f"- **نسبة التغير:** {selected.get('نسبة التغير', 'غير متوفر')} %")
        st.write(f"- **سعر الافتتاح:** {selected.get('سعر الافتتاح', 'غير متوفر')}")
        st.write(f"- **أعلى سعر:** {selected.get('أعلى سعر', 'غير متوفر')}")
        st.write(f"- **أدنى سعر:** {selected.get('أدنى سعر', 'غير متوفر')}")
        st.write(f"- **القيمة السوقية:** {selected.get('القيمة السوقية', 'غير متوفر')}")
else:
    st.warning("لم يتم تحميل أي بيانات بعد.")

st.markdown("---")
st.caption("🟢 المصدر: الموقع الرسمي لبورصة تونس BVMT – تم التطوير بواسطة Python و Streamlit.")



