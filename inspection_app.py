import streamlit as st
import pandas as pd
import json
from datetime import datetime
import base64
import os
file_name = "inspection_plan.json"

# ✅ ระบบล็อกอิน
# =============================
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if username != st.secrets["AUTH_USER"] or password != st.secrets["AUTH_PASS"]:
    st.warning("กรุณาเข้าสู่ระบบก่อน")
    st.stop()
else:
    st.success("เข้าสู่ระบบสำเร็จ ✅")

# ใช้ st.secrets เพื่อความปลอดภัย (ต้องสร้างไฟล์ .streamlit/secrets.toml)
# ตัวอย่างไฟล์ secrets.toml:
# [auth]
# user = "itbkd"
# pass = "M1nd@t:62"

# โหลดข้อมูล
with open("inspection_plan.json", "r", encoding="utf-8") as f:
    data = json.load(f)
df = pd.DataFrame(data)

st.set_page_config(page_title="ระบบตรวจสอบอุปกรณ์", layout="wide")
st.title("📋 ระบบตรวจสอบอุปกรณ์อิเล็กทรอนิกส์")

# สร้าง Tabs
tab1, tab2, tab3, tab4 = st.tabs(["➕ เพิ่มข้อมูล", "📷 อัปโหลดรูปภาพ", "📆 คำนวณอายุการใช้งาน", "📊 ข้อมูลทั้งหมด"])

# ✅ Tab 1: ฟอร์มกรอกข้อมูล
with tab1:
    st.subheader("กรอกข้อมูลการตรวจสอบ")
    with st.form("inspection_form"):
        col1, col2 = st.columns(2)
        with col1:
            location = st.selectbox("สถานที่ตรวจสอบ", ["1.บ้านพักพนักงาน", "2.เสาทางเข้าโรงงาน", "3.ตู้ CCTV โรงรถ", "4.ตู้ CCTV ข้างป้อมรปภ.2",
    "5.ข้างในป้อมรปภ.2", "6.ตู้ CCTV หมักส่าฝั่งทางเข้าโรงงาน", "7.ตู้ CCTV ฝั่งติดกลั่น",
    "8.ตู้ CCTV Ro", "9.ตู้ CCTV กลั่น", "10.ตู้ CCTV แพลนปรับสภาพน้ำ", "11.CCTV ต้นกำลัง",
    "12.CCTV Server room", "13.CCTV ห้องหัวหน้าบรรจุ", "14.CCTV ตู้หน้าลิฟฟ์บรรจุ",
    "15.ท่าน้ำปรับสภาพน้ำ", "16.ท่าน้ำตรงตู้ไฟใหญ่", "17.TBL ตู้ CCTV", "18.สิ่งแวดล้อมตู้หน้าแผนก",
    "19.ตู้อาคารพักขยะ", "20.สิ่งแวดล้อมตู้กลางบ่อ", "21.ปรุงสุราอาคาร 1", "22.ปรุงสุราอาคาร 2",
    "23.โรงบรมบริเวณหัวโค้งไปศาล", "24.โรงบรมบริเวณหัวโค้งไปศาล2(ป้อมยาม)", "25.HOM internet",
    "26.พัสดุ internet", "27.โรงงานอาหาร internet", "28.ซ่อมบำรุง internet", "29.อาคารวิทยาศาสตร์ internet",
    "30.บรรจุ internet", "31.Serverroom internet", "32.กลั่น internet", "33.บักพักเรืองรับรอง internet",
    "34.HOM เครื่องเสียงชั่น 2", "35.HOM เครื่องเสียงชั่น 1", "36.ตึกอำนวยการ ประชุม1 เครื่องเสียง",
    "37.ตึกอำนวยการ ประชุม4 เครื่องเสียง"
])
            date = st.date_input("วันที่ตรวจสอบ", value=datetime.today())
            inspection_method = st.selectbox("วิธีตรวจเช็ค", ["กายภาพ", "Infrared", "กายภาพ + Infrared"])
            wire_condition = st.selectbox("สภาพสายไฟ", ["ปกติ", "ผุพัง"])
            wire_temperature = st.selectbox("อุณหภูมิสายไฟ", ["ปกติ", "ร้อน"])
        with col2:
            equipment_quality = st.selectbox("คุณภาพอุปกรณ์", ["ดีมาก", "ควรเปลี่ยน"])
            equipment_temperature = st.number_input("อุณหภูมิอุปกรณ์ (°C)", min_value=0)
            ups_status = st.text_input("สถานะ UPS")
            internet_status = st.text_input("สถานะอินเทอร์เน็ต")
        recommendation = st.text_area("คำแนะนำเพิ่มเติม")
        submitted = st.form_submit_button("✅ บันทึกข้อมูล")
        if submitted:
            new_entry = {
                "location": location,
                "date": str(date),
                "inspection_method": inspection_method,
                "wire_condition": wire_condition,
                "wire_temperature": wire_temperature,
                "equipment_quality": equipment_quality,
                "equipment_temperature": equipment_temperature,
                "ups_status": ups_status,
                "internet_status": internet_status,
                "recommendation": recommendation
            }
            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
            with open("inspection_plan.json", "w", encoding="utf-8") as f:
                json.dump(df.to_dict(orient="records"), f, ensure_ascii=False, indent=4)
            st.success("✅ บันทึกข้อมูลเรียบร้อยแล้ว")

# ✅ Tab 2: อัปโหลดรูปภาพ
with tab2:
    st.subheader("อัปโหลดรูปภาพ")
    upload_option = st.radio("เลือกวิธี:", ["ถ่ายภาพด้วยกล้อง", "อัปโหลดไฟล์"])
    images = []
    if upload_option == "ถ่ายภาพด้วยกล้อง":
        photo = st.camera_input("ถ่ายภาพ")
        if photo:
            st.image(photo)
    else:
        uploaded_files = st.file_uploader("เลือกไฟล์", type=["jpg", "png"], accept_multiple_files=True)
        if uploaded_files:
            for file in uploaded_files:
                st.image(file)

# ✅ Tab 3: คำนวณอายุการใช้งาน
with tab3:
    st.subheader("คำนวณอายุการใช้งาน")
    num_items = st.number_input("จำนวนรายการ", min_value=1, max_value=10, value=3)
    items = []
    for i in range(num_items):
        name = st.text_input(f"ชื่อของชิ้นที่ {i+1}", key=f"name_{i}")
        purchase_date = st.date_input(f"วันที่ซื้อของชิ้นที่ {i+1}", key=f"date_{i}")
        items.append({"name": name, "purchase_date": purchase_date})
    if st.button("คำนวณ"):
        today = datetime.today()
        for item in items:
            if item["name"] and item["purchase_date"]:
                delta = today - datetime.combine(item["purchase_date"], datetime.min.time())
                years = delta.days // 365
                months = (delta.days % 365) // 30
                days = (delta.days % 365) % 30
                st.write(f"**{item['name']}** ใช้งานมาแล้ว {years} ปี {months} เดือน {days} วัน")

with tab4:
    st.subheader("📊 ข้อมูลการตรวจสอบทั้งหมด")
    if data:
        # ✅ แสดงข้อมูลดิบ
        df = pd.DataFrame(data)
        st.dataframe(df)

        # ✅ ฟีเจอร์ลบข้อมูล
        st.subheader("🗑 ลบข้อมูลการตรวจสอบ")
        index_to_delete = st.selectbox(
            "เลือกรายการที่จะลบ",
            range(len(data)),
            format_func=lambda i: f"{data[i]['location']} | {data[i]['date']}"
        )

        col_del1, col_del2 = st.columns(2)
        with col_del1:
            if st.button("ลบรายการนี้"):
                data.pop(index_to_delete)
                with open(file_name, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                st.success("✅ ลบข้อมูลเรียบร้อยแล้ว")
                st.rerun()
        with col_del2:
            if st.button("ล้างข้อมูลทั้งหมด"):
                data.clear()
                with open(file_name, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                st.success("✅ ล้างข้อมูลทั้งหมดเรียบร้อยแล้ว")
                st.experimental_rerun()

        # ✅ ตาราง Dashboard
        st.subheader("📅 ตารางแผนการตรวจสอบ (เดือน × สัปดาห์)")
        months = ["ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.", "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."]
        weeks = ["สัปดาห์1", "สัปดาห์2", "สัปดาห์3", "สัปดาห์4"]
        columns = [f"{m}-{w}" for m in months for w in weeks]
        locations = [
            "1.บ้านพักพนักงาน", "2.เสาทางเข้าโรงงาน", "3.ตู้ CCTV โรงรถ", "4.ตู้ CCTV ข้างป้อมรปภ.2",
            "5.ข้างในป้อมรปภ.2", "6.ตู้ CCTV หมักส่าฝั่งทางเข้าโรงงาน", "7.ตู้ CCTV ฝั่งติดกลั่น",
            "8.ตู้ CCTV Ro", "9.ตู้ CCTV กลั่น", "10.แพลนปรับสภาพน้ำ", "11.ต้นกำลัง",
            "12.CCTV Server room", "13.CCTV ห้องหัวหน้าบรรจุ", "14.CCTV ตู้หน้าลิฟฟ์บรรจุ",
            "15.ท่าน้ำปรับสภาพน้ำ", "16.ท่าน้ำตรงตู้ไฟใหญ่", "17.TBL ตู้ CCTV", "18.สิ่งแวดล้อมตู้หน้าแผนก",
            "19.ตู้อาคารพักขยะ", "20.สิ่งแวดล้อมตู้กลางบ่อ", "21.ปรุงสุราอาคาร 1", "22.ปรุงสุราอาคาร 2",
            "23.โรงบรมบริเวณหัวโค้งไปศาล", "24.โรงบรมบริเวณหัวโค้งไปศาล2(ป้อมยาม)", "25.HOM internet",
            "26.พัสดุ internet", "27.โรงงานอาหาร internet", "28.ซ่อมบำรุง internet", "29.อาคารวิทยาศาสตร์ internet",
            "30.บรรจุ internet", "31.Serverroom internet", "32.กลั่น internet", "33.บักพักเรืองรับรอง internet",
            "34.HOM เครื่องเสียงชั่น 2", "35.HOM เครื่องเสียงชั่น 1", "36.ตึกอำนวยการ ประชุม1 เครื่องเสียง",
            "37.ตึกอำนวยการ ประชุม4 เครื่องเสียง"
        ]
        plan_df = pd.DataFrame("", index=locations, columns=columns)

        def get_week(day):
            if 1 <= day <= 7:
                return "สัปดาห์1"
            elif 8 <= day <= 15:
                return "สัปดาห์2"
            elif 16 <= day <= 22:
                return "สัปดาห์3"
            else:
                return "สัปดาห์4"

        for item in data:
            date_obj = datetime.strptime(item["date"], "%Y-%m-%d")
            month_name = months[date_obj.month - 1]
            week_name = get_week(date_obj.day)
            col_name = f"{month_name}-{week_name}"
            if item["location"] in plan_df.index:
                plan_df.loc[item["location"], col_name] = "✅"

        # ✅ สร้างตารางเหมือน Excel
months_full = ["มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
               "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"]
weeks = ["สัปดาห์1", "สัปดาห์2", "สัปดาห์3", "สัปดาห์4"]

# สร้างชื่อคอลัมน์แบบ เดือน-สัปดาห์
columns = [f"{m}-{w}" for m in months_full for w in weeks]

# สร้าง DataFrame ว่าง
plan_df = pd.DataFrame("", index=locations, columns=columns)

# ฟังก์ชันหาสัปดาห์
def get_week(day):
    if 1 <= day <= 7:
        return "สัปดาห์1"
    elif 8 <= day <= 15:
        return "สัปดาห์2"
    elif 16 <= day <= 22:
        return "สัปดาห์3"
    else:
        return "สัปดาห์4"

# เติมข้อมูล ✅ ตามวันที่ตรวจ
for item in data:
    date_obj = datetime.strptime(item["date"], "%Y-%m-%d")
    month_name = months_full[date_obj.month - 1]
    week_name = get_week(date_obj.day)
    col_name = f"{month_name}-{week_name}"
    if item["location"] in plan_df.index:
        plan_df.loc[item["location"], col_name] = "✅"

       # ✅ สร้าง MultiIndex สำหรับหัวตาราง
months_full = ["มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน", "พฤษภาคม", "มิถุนายน",
               "กรกฎาคม", "สิงหาคม", "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"]
weeks = ["สัปดาห์1", "สัปดาห์2", "สัปดาห์3", "สัปดาห์4"]

# MultiIndex columns: (เดือน, สัปดาห์)
multi_cols = pd.MultiIndex.from_product([months_full, weeks], names=["เดือน", "สัปดาห์"])

# สร้าง DataFrame ว่าง
plan_df = pd.DataFrame("", index=locations, columns=multi_cols)

# ฟังก์ชันหาสัปดาห์
def get_week(day):
    if 1 <= day <= 7:
        return "สัปดาห์1"
    elif 8 <= day <= 15:
        return "สัปดาห์2"
    elif 16 <= day <= 22:
        return "สัปดาห์3"
    else:
        return "สัปดาห์4"

# เติมข้อมูล ✅
for item in data:
    date_obj = datetime.strptime(item["date"], "%Y-%m-%d")
    month_name = months_full[date_obj.month - 1]
    week_name = get_week(date_obj.day)
    if item["location"] in plan_df.index:
        plan_df.loc[item["location"], (month_name, week_name)] = "✅"

        # ✅ ปรับสีและขนาดช่อง
        styled_plan = plan_df.style.applymap(lambda val: "background-color: lightgreen" if val == "✅" else "")
        styled_plan.set_table_styles([
            {"selector": "th", "props": [("font-size", "12px"), ("text-align", "center")]},
            {"selector": "td", "props": [("width", "40px"), ("text-align", "center"), ("font-size", "12px")]}
        ])

        st.dataframe(styled_plan, use_container_width=True)

        # ✅ ปุ่มดาวน์โหลด
        st.download_button(
            "📥 ดาวน์โหลดตารางแผนเป็น CSV",
            plan_df.to_csv(index=True).encode('utf-8-sig'),
            file_name="inspection_schedule.csv",
            mime="text/csv"
        )
    else:

        st.warning("ยังไม่มีข้อมูลการตรวจสอบ")

