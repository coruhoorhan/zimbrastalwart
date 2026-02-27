FROM python:3.11-slim
RUN apt-get update && apt-get install -y --no-install-recommends wget && rm -rf /var/lib/apt/lists/*
RUN echo '#!/bin/bash\necho "Simulating imapsync done"' > /usr/bin/imapsync && chmod +x /usr/bin/imapsync
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV PYTHONPATH=/
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
