import streamlit as st
import requests

# إعدادات الاتصال بقاعدة البيانات
DB_URL = "https://sheetdb.io/api/v1/snxj7m29yni8q"
ADMIN_SECRET_KEY = "BOSS_2026" # مفتاحك السري للدخول

st.set_page_config(page_title="TDZ ADMIN ENGINE", layout="wide")

st.title("🕹️ TDZ Command Center")
auth_key = st.sidebar.text_input("Enter Master Key", type="password")

if auth_key == ADMIN_SECRET_KEY:
    st.sidebar.success("Welcome, Director.")
    
    # 1. جلب بيانات كل التجار
    try:
        data = requests.get(DB_URL).json()
        
        st.header("📊 Global Merchant Overview")
        # عرض سريع للإحصائيات
        total_debt = sum(float(u.get('debt', 0)) for u in data)
        st.status(f"System Total Debt: {total_debt} DZD", state="error" if total_debt > 20000 else "complete")

        # 2. جدول التحكم بالتجار
        st.subheader("Manage Merchants")
        for user in data:
            with st.expander(f"👤 {user.get('name')} (ID: {user.get('id')})"):
                col1, col2 = st.columns(2)
                current_debt = float(user.get('debt', 0))
                col1.metric("Current Debt", f"{current_debt} DZD")
                
                # أزرار الإجراءات السريعة
                new_debt = col2.number_input(f"Update Debt for {user.get('id')}", value=current_debt)
                if col2.button(f"Confirm Update ID: {user.get('id')}"):
                    # هنا نرسل التحديث لـ SheetDB
                    update_url = f"{DB_URL}/id/{user.get('id')}"
                    response = requests.patch(update_url, json={"data": {"debt": new_debt}})
                    if response.status_code == 200:
                        st.success("Database Updated!")
                    else:
                        st.error("Failed to sync.")

    except Exception as e:
        st.error(f"Error fetching data: {e}")
else:
    st.warning("Unauthorized Access. System Locked.")
