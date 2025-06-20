import streamlit as st
import pandas as pd
import requests
from taibun import Converter
from classifier import classify_medical_note  
from tailo import chinese_to_tailo

# 初始化臺羅轉換器
conv = Converter(system="Tailo", dialect="south", format="number", delimiter="-", sandhi="auto")

# 疾病英文→中文名稱對照表
label_translation = {
    "Allergy and Immunology": "過敏與免疫科",
    "Allergy": "過敏與免疫科",
    "Anesthesiology": "麻醉科",
    "Cardiology": "心臟科",
    "Dermatology": "皮膚科",
    "Emergency Medicine": "急診醫學科",
    "Endocrinology": "內分泌科",
    "Gastroenterology": "胃腸科",
    "General Practice": "一般醫學",
    "Geriatrics": "老年醫學",
    "Hematology": "血液科",
    "Infectious Disease": "感染科",
    "Internal Medicine": "內科",
    "Nephrology": "腎臟科",
    "Neurology": "神經科",
    "Obstetrics and Gynecology": "婦產科",
    "Oncology": "腫瘤科",
    "Ophthalmology": "眼科",
    "Orthopedics": "骨科",
    "Otolaryngology": "耳鼻喉科",
    "Pediatrics": "小兒科",
    "Psychiatry": "精神科",
    "Pulmonology": "肺臟科",
    "Radiology": "放射科",
    "Rheumatology": "風濕免疫科",
    "Surgery": "外科",
    "Urology": "泌尿科"
}

# 語音播放函式（使用瀏覽器語音合成）
def speak_tailo(tailo_text):
    if tailo_text:
        #tailo_text='sim-tsōng-kho'
        st.components.v1.html(f"""
            <button onclick="speak()">🔈 用台羅唸出台語</button>
            <script>
                function speak() {{
                    var msg = new SpeechSynthesisUtterance("{tailo_text}");
                    msg.lang = "zh-TW";
                    window.speechSynthesis.speak(msg);
                }}
            </script>
        """, height=100)
    else:
        st.warning("⚠️ 無法轉換為台羅發音。")

# 中文→臺羅
def get_tailo(text):
    try:
        return chinese_to_tailo(text)
    except Exception:
        return None

# UI 開始
st.title("🏪 病狀分類模型：BioBERT + 臺語語音")

st.write("輸入一段病狀描述，我們會預測看診科別並用臺語唸出來！")

# 單筆輸入
st.subheader("🔹 單筆輸入")
user_input = st.text_input("請輸入一段病狀描述（英文）：")

if user_input:
    label, confidence = classify_medical_note(user_input)
    zh_label = label_translation.get(label, label)
    st.write(f"預測科別：**{label}**（信心度：{confidence:.2f}%）")
    
    tailo_text = get_tailo(zh_label)
    st.write(f"建議看診科別（中文）：**{zh_label}**,**{tailo_text}**")
    speak_tailo(tailo_text)

# 批次輸入
st.subheader("📄 批次輸入（CSV）")
uploaded_file = st.file_uploader("請上傳包含 symptom 欄位的 CSV 檔案", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)
        if "symptom" not in df.columns:
            st.error("❗ 檔案中須包含 symptom 欄位")
        else:
            st.write("預測中，請稍候...")
            df["Prediction"], df["Confidence"] = zip(*df["symptom"].map(classify_medical_note))
            df["中文科別"] = df["Prediction"].map(label_translation)
            df["臺羅發音"] = df["中文科別"].map(get_tailo)
            st.success("✅ 完成！")
            st.dataframe(df)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📅 下載結果 CSV", data=csv, file_name="predicted_labels.csv", mime="text/csv")
    except Exception as e:
        st.error(f"❌ 發生錯誤：{e}")
