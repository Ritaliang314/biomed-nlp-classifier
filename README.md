# Biomed NLP classifier

這是一個用來自動分類醫療筆記的專案。使用 BioBERT 預訓練模型，輸入一句簡單的症狀描述，給予建議的看診疾病科別。

---

## 專案功能

- 使用者輸入醫療紀錄（像是：咳嗽、胸痛等敘述）
- 模型會判斷這屬於哪一種疾病分類（例如：呼吸系統、消化系統）
- 做成一個網頁小工具，用 Streamlit 製作

---

## 使用到的工具

- Python
- Hugging Face Transformers（BioBERT）
- Pandas、Scikit-learn
- Streamlit

---

## 專案結構
biomed-nlp-classifier/ ├── app.py # Streamlit UI 主程式 ├── classifier.py # 分類邏輯 ├── requirements.txt # 所需 Python 套件 └── README.md # 就是你現在看的這個檔案
## 部署說明

目前尚未部署至雲端，原因如下：

### 問題說明：
- 1.
- Streamlit Cloud 無法順利下載 Hugging Face 上的大型模型，部署過程會出現 `OSError` 或逾時錯誤
- 像 `facebook/bart-large-mnli` 和 `valhalla/distilbart-mnli-12-3` 這類模型，對於免費帳戶來說可能過大或限制存取
- 2.原先想要使用現有台灣言語工具模型(itaigi)將語音輸出的text生成台語語音(TTS)，但目前版本已將相關功能移除，另外將中文翻譯成台羅拼音模型[Bohanlu/Taigi-Llama-2-Translator-7B](https://github.com/lbh0830/TW-Hokkien-LLM/blob/main/README.md)會用到大量記憶體空間，以目前環境會發生crash。若是想輸出台語語音可以考慮自己訓練小型語料庫+針對看診科別的特定模型。

### 暫時解法：
- 專案可在本地端順利執行，指令如下（見下方）


---

## 🧪 本地執行方式

```bash
git clone https://github.com/Ritaliang314/biomed-nlp-classifier.git
cd biomed-nlp-classifier
pip install -r requirements.txt
streamlit run app.py
