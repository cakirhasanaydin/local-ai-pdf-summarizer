FROM python:3.10-slim

WORKDIR /app

# Gerekli sistem paketlerini güncelle
RUN apt-get update && apt-get install -y --no-install-recommends build-essential

# Bağımlılık dosyasını kopyala ve yükle
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Kodları kopyala
COPY . .

EXPOSE 8501

# Doğrudan python modülü olarak çalıştırarak PATH sorunlarını tamamen ortadan kaldırıyoruz
CMD ["python", "-m", "streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]