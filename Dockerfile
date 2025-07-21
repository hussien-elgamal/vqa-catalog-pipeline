# File: E:/product_vqa/Dockerfile
FROM apache/airflow:2.9.0

USER root

RUN apt-get update && \
    apt-get install -y --no-install-recommends curl unzip postgresql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

USER airflow

COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir -r /requirements.txt


# الأمر الافتراضي لتشغيل السكريبت
CMD ["python", "scripts/extract_clip_embeddings.py"]