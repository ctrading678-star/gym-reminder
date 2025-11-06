# fetch_investing.py
# مثال بسيط: تحميل بيانات تاريخية لسهم وحفظها في CSV
import investpy
import datetime

def fetch_stock_history(stock_name, country, from_date, to_date, out_csv):
    """
    stock_name: اسم السهم كما يظهر في Investing.com (مثال: "SIAME")
    country: اسم الدولة بالانجليزية (مثال: "tunisia")
    from_date, to_date: بصيغة "dd/mm/yyyy" (مثال: "01/05/2025")
    out_csv: اسم ملف الإخراج (مثال: "SIAME_data.csv")
    """
    try:
        data = investpy.get_stock_historical_data(
            stock=stock_name,
            country=country,
            from_date=from_date,
            to_date=to_date
        )
        data.to_csv(out_csv, encoding="utf-8-sig")
        print(f"✅ تم حفظ البيانات في: {out_csv}")
        return True
    except Exception as e:
        print("❌ حدث خطأ أثناء تحميل البيانات:")
        print(e)
        return False

if __name__ == "__main__":
    # مثال استخدام:
    stock_name = "SIAME"         # غيّر حسب الاسم الفعلي في Investing.com
    country = "tunisia"         # الدولة باللغة الانجليزية
    from_date = "01/05/2025"    # من تاريخ (يوم/شهر/سنة)
    to_date = "06/11/2025"      # الى تاريخ
    out_csv = "SIAME_data.csv"

    fetch_stock_history(stock_name, country, from_date, to_date, out_csv)
