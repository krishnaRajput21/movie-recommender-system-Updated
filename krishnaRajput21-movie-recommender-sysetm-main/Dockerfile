FROM python:3.10-slim

WORKDIR /app

# System dependencies install karna
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*


COPY requirements_v2.txt* ./
COPY requirements.txt* ./


RUN if [ -f requirements_v2.txt ]; then pip install --no-cache-dir -r requirements_v2.txt; \
    elif [ -f requirements.txt ]; then pip install --no-cache-dir -r requirements.txt; \
    fi


RUN pip install --no-cache-dir uvicorn streamlit fastapi chromadb sentence-transformers


COPY . .

EXPOSE 8000
EXPOSE 8501


CMD uvicorn backend.main:app --host 0.0.0.0 --port 8000 & sleep 3 && streamlit run frontend/app.py --server.port 7860 --server.address 0.0.0.0 --server.enableCORS false --server.enableXsrfProtection false