import streamlit as st
import pandas as pd
import chardet
from classifier import classify_medical_note

# 疾病英文→中文名稱對照表
label_translation = {
    "Allergy and Immunology": "過敏與免疫科",
    "Allergy": "過敏與免疫科",
    "Anesthesiology": "麻醉科",
    "Cardiology": "心臟科",
    "Dermatology": "皮膚科",
    "Emergency": "急診醫學科",
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
    'Gynecology':'婦科',
    'Obstetrics':'產科',
    "Oncology": "腫瘤科",
    'Otorhinolaryngology':'耳鼻喉科',
    'Odontology':"牙科",
    "Ophthalmology": "眼科",
    "Orthopedics": "骨科",
    "Otolaryngology": "耳鼻喉科",
    "Pediatrics": "小兒科",
    "Psychiatry": "精神科",
    "Pulmonology": "肺臟科",
    "Radiology": "放射科",
    'Respiratory':'呼吸科',
    "Rheumatology": "風濕免疫科",
    "Surgery": "外科",
    'Microbiology':'微生物學',
    "Urology": "泌尿科",
    'Nursing':'護理部',
    'Psychology':'身心科',
    'Pathology':"病理科"
}

# 中文語音播放（瀏覽器 TTS）
def speak_chinese(text):
    if text:
        st.components.v1.html(f"""
            <button onclick="speak()">🔈 播放語音建議</button>
            <script>
                function speak() {{
                    var msg = new SpeechSynthesisUtterance("根據您的症狀描述，建議您掛 {text} 科別");
                    msg.lang = "zh-TW";
                    window.speechSynthesis.speak(msg);
                }}
            </script>
        """, height=100)
    else:
        st.warning("⚠️ 沒有建議科別。")

col1, col2 = st.columns([0.1, 0.9])
with col1:
    st.title("🏪")
with col2:
    st.markdown("<h2 style='margin-bottom:0;'>病狀分類模型：BioBERT + 中文語音</h2>", unsafe_allow_html=True)
    st.markdown("輸入一段病狀描述，我們會預測看診科別並用中文語音說出！")

# 單筆輸入
st.subheader("🔹 單筆輸入")
user_input = st.text_area(
    "請輸入一段病狀描述（英文）：",
    height=100,
    placeholder="例如：Patient experiencing chest pain and shortness of breath for the last two days."
)

if user_input:
    label, confidence = classify_medical_note(user_input)
    zh_label = label_translation.get(label, label)
    st.write(f"預測科別：**{label}**（信心度：{confidence:.2f}%）")
    st.write(f"建議看診科別（中文）：**{zh_label}**")
    speak_chinese(zh_label)

# 批次輸入
st.subheader("📄 批次輸入（CSV）")
uploaded_file = st.file_uploader("請上傳包含 symptom 欄位的 CSV 檔案", type=["csv"])


# 嘗試多種欄位名稱
POSSIBLE_SYMPTOM_COLUMNS = ["symptom",'description', "symptoms", "cleaned_transcription", "transcription", "text"]

if uploaded_file:
    try:
        # 自動偵測檔案編碼
        raw_bytes = uploaded_file.read()
        detected_encoding = chardet.detect(raw_bytes)["encoding"] or "utf-8"
        
        # 用偵測到的編碼讀取
        df = pd.read_csv(pd.io.common.BytesIO(raw_bytes), encoding=detected_encoding, on_bad_lines='skip')

        # 嘗試找到可能的症狀欄位
        symptom_col = None
        for col in POSSIBLE_SYMPTOM_COLUMNS:
            if col in df.columns:
                symptom_col = col
                break

        if symptom_col is None:
            st.error("❗ 檔案中找不到症狀欄位，請確認至少有一欄像是 symptom、transcription、cleaned_transcription。")
        else:
            st.write("預測中，請稍候...")
            df["Prediction"], df["Confidence"] = zip(*df[symptom_col].map(classify_medical_note))
            df["中文科別"] = df["Prediction"].map(label_translation)
            st.success("✅ 完成！")
            st.dataframe(df)

            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📅 下載結果 CSV", data=csv, file_name="predicted_labels.csv", mime="text/csv")
    except Exception as e:
        st.error(f"❌ 發生錯誤：{e}")
