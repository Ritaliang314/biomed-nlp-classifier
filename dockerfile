# 使用 Python 簡潔版映像
FROM python:3.10-slim

# 安裝系統相依套件與工具
RUN apt-get update && apt-get install -y \
    build-essential \
    espeak \
    curl \
    wget \
    git \
    libsndfile1 \
    && apt-get clean

# 安裝 Python 套件（包含台語語音工具）
RUN pip install --upgrade pip
RUN pip install \
    streamlit \
    pandas \
    transformers \
    torch \
    tai5-uan5_gian5-gi2_kang1-ku7 \
    htsengine

# 下載 HTS 台語語音模型（含 .htsvoice）
RUN python3 -m 臺灣言語工具.語音合成.HTS工具.安裝HTS語音辨識程式

# 建立應用程式工作目錄
WORKDIR /app
COPY . /app

# 對外開放 port（Streamlit 使用）
EXPOSE 8501

# 啟動 Streamlit App
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
