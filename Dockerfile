FROM python:3.12-slim

WORKDIR /app

# تثبيت أدوات النظام
RUN apt-get update && apt-get install -y \
    git \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# تحسين Python
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# نسخ الاعتماديات أولاً للاستفادة من Docker cache
COPY requirements.txt .

# تحديث pip
RUN pip install --upgrade pip

# تثبيت المكتبات
RUN pip install --no-cache-dir -r requirements.txt

# نسخ المشروع
COPY . .

# فتح المنفذ
EXPOSE 8000

# تشغيل المنصة (بدون --reload)
CMD ["uvicorn", "orchestrator.main:app", "--host", "0.0.0.0", "--port", "8000"]
