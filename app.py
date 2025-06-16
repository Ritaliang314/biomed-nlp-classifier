import streamlit as st
import pandas as pd
from classifier import classify_medical_note
import streamlit.components.v1 as components

def speak_taiwanese(text):
    st.components.v1.html(f"""
        <button onclick="speak()">🔊 用台語唸出來</button>
        <script>
            function speak() {{
                var msg = new SpeechSynthesisUtterance("{text}");
                msg.lang = "nan-tw";  // 使用台語語音（部分瀏覽器可能 fallback）
                window.speechSynthesis.speak(msg);
            }}
        </script>
    """, height=100)

st.title("🩺 症狀分類模型：BioBERT for Medical Specialities")

st.write("你可以輸入單句症狀描述，或上傳包含多筆症狀的 CSV 檔案。")

# 單句輸入
st.subheader("🔹 單筆輸入")
user_input = st.text_input("請輸入一段症狀描述：")

if user_input:
    label, confidence = classify_medical_note(user_input)
    st.write(f"預測分類：{label}（信心度：{confidence}%)")
    speak_taiwanese(label)

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


