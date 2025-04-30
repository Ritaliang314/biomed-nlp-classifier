# MEDI-TAG

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

## ⚠️ 部署說明

由於 Streamlit Cloud 對 Hugging Face 模型存取有限，本專案在嘗試載入 zero-shot 分類模型（如 `facebook/bart-large-mnli` 與 `valhalla/distilbart-mnli-12-3`）時，會發生持續性的 `OSError`。

### 常見問題：
- 無法匿名下載模型  
- 模型體積過大導致逾時  
- Streamlit 雲端容器限制模型存取權限  

因此，目前 **無法提供線上部署版本**。

🛠️ 不過，本專案可透過以下指令於 **本機正常執行**：

```bash
streamlit run app.py
```

此部署限制已被紀錄，以展示對環境限制的理解與實務除錯經驗。
