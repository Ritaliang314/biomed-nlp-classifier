# Biomed NLP classifier

這是一個用來自動分類醫療筆記的專案。使用 BioBERT 預訓練模型，輸入一句簡單的症狀描述，就能預測出可能的疾病類別。

---

## 專案功能

- 使用者輸入醫療紀錄（像是：咳嗽、胸痛等敘述）
- 模型會判斷這屬於哪一種疾病分類（例如：呼吸系統、消化系統）
- 預計會做成一個網頁小工具，用 Streamlit 製作

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
- Streamlit Cloud 無法順利下載 Hugging Face 上的大型模型，部署過程會出現 `OSError` 或逾時錯誤
- 像 `facebook/bart-large-mnli` 和 `valhalla/distilbart-mnli-12-3` 這類模型，對於免費帳戶來說可能過大或限制存取

### 暫時解法：
- 專案可在本地端順利執行，指令如下（見下方）
- 為了避免把時間花在無止盡的部署錯誤排除，目前暫緩上雲端

> 📌 特意保留此部署記錄，以展示對雲端限制的理解、錯誤排除的過程，以及做出務實選擇的能力。

---

## 🧪 本地執行方式

```bash
git clone https://github.com/Ritaliang314/biomed-nlp-classifier.git
cd biomed-nlp-classifier
pip install -r requirements.txt
streamlit run app.py
