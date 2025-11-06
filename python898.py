import investpy
import datetime

# 1️⃣ تحديد اسم السهم والدولة
stock_name = "SIAME"
country_name = "tunisia"

# 2️⃣ تحديد فترة البيانات (من إلى)
from_date = datetime.date(2023, 1, 1)
to_date = datetime.date.today()  # اليوم الحالي

# تأكد أن التاريخ الأخير أكبر من الأول
if to_date <= from_date:
    raise ValueError("⚠️ يجب أن يكون التاريخ الأخير بعد التاريخ الأول!")

# 3️⃣ تحميل البيانات من Investing
data = investpy.get_stock_historical_data(
    stock=stock_name,
    country=country_name,
    from_date=from_date.strftime("%d/%m/%Y"),
    to_date=to_date.strftime("%d/%m/%Y")
)

# 4️⃣ عرض أول 5 أسطر من البيانات
print("✅ تم تحميل البيانات بنجاح:\n")
print(data.head())

# 5️⃣ حفظ البيانات في ملف CSV
data.to_csv(f"{stock_name}_data.csv")
print(f"\n💾 تم حفظ الملف: {stock_name}_data.csv")

