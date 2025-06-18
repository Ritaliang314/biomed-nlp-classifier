import streamlit as st
import pandas as pd
from classifier import classify_medical_note
import streamlit.components.v1 as components
from 臺灣言語工具.語音合成.HTS工具.語音合成 import 語音合成

# 疾病英文→中文名稱對照
label_translation = {
    "Allergy and Immunology": "過敏與免疫科",
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
    "Pulmonology": "胸腔科",
    "Radiology": "放射科",
    "Rheumatology": "風濕免疫科",
    "Surgery": "外科",
    "Urology": "泌尿科"
}

合成器 = 語音合成("models/nan-pau-1.0.htsvoice")

def speak_taiwanese(text):
    st.components.v1.html(f"""
        <button onclick="speak()">🔊 用中文唸出來</button>
        <script>
            function speak() {{
                var msg = new SpeechSynthesisUtterance("{text}");
                msg.lang = "zh-tw";  // 使用台語語音（部分瀏覽器可能 fallback）
                window.speechSynthesis.speak(msg);
            }}
        </script>
    """, height=100)
def speak_taiwanese_audio(text, path="output.wav"):
    合成器.合成(text, path)
    st.audio(path, format="audio/wav")
def speak_taiwanese_audio_button(text, label="🔈 播放台語語音", path="output.wav"):
    if st.button(label):
        speak_taiwanese_audio(text, path)
st.title("🩺 症狀分類模型：BioBERT for Medical Specialities")

st.write("你可以輸入單句症狀描述，或上傳包含多筆症狀的 CSV 檔案。")

# 單句輸入
st.subheader("🔹 單筆輸入")
user_input = st.text_input("請輸入一段症狀描述：")

if user_input:
    label, confidence = classify_medical_note(user_input)
    st.write(f"預測分類：{label}（信心度：{confidence}%)")
    zh_label = label_translation.get(label, label)

    st.write(f"建議看診科別（中文）：{zh_label}")
    speak_taiwanese_audio_button(zh_label)
    speak_taiwanese(zh_label)

# 多筆輸入
st.subheader("📄 批次輸入（CSV）")
uploaded_file = st.file_uploader("請上傳包含 symptom 欄位的 CSV 檔", type=["csv"])

if uploaded_file is not None:
    try:
        df = pd.read_csv(uploaded_file)
        if "symptom" not in df.columns:
            st.error("❗ 檔案中缺少 'symptom' 欄位，請確認格式正確。")
        else:
            st.write("預測中...")
            df["Prediction"], df["Confidence"] = zip(*df["symptom"].map(classify_medical_note))
            st.success("✅ 預測完成！")
            st.dataframe(df)

            # 提供下載
            csv_download = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 下載預測結果 CSV", data=csv_download, file_name="predictions.csv", mime='text/csv')

    except Exception as e:
        st.error(f"讀取或預測發生錯誤：{e}")





