FROM python
ENV PYTHONUNBUFFERED 1
WORKDIR /usr/src/RSD
COPY requirements.txt /usr/src/RSD
RUN pip install -r requirements.txt
COPY . /usr/src/RSD