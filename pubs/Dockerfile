FROM python:3.13.2-bookworm

WORKDIR /app

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY ./shared /app/shared
RUN pip install -e /app/shared

# Correct path to the app directory
COPY ./pubs/app /app 

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
