FROM python:3.12.6-slim
WORKDIR /app

COPY api/ ./api
RUN pip install --root-user-action=ignore --no-cache-dir --upgrade -r api/requirements.txt

CMD ["fastapi", "run", "api/main.py"]