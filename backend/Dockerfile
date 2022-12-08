FROM python:3.8.5-slim

WORKDIR /search

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY emails.mbox .
COPY app.py .
COPY clean_mbox.py .
COPY create_index.py .
COPY index_search.py .

RUN python clean_mbox.py
RUN python create_index.py

EXPOSE 5000

CMD ["python", "app.py", "flask run"]