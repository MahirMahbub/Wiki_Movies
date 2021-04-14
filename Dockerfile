FROM python:3.8.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /srv/ocr_backend
WORKDIR /srv/ocr_backend
COPY requirements.txt /srv/ocr_backend/
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . /srv/ocr_backend/