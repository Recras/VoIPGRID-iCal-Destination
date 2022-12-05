FROM python:3.10

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

RUN useradd --system flask

EXPOSE 5000

USER flask

CMD [ "python", "/usr/src/app/main.py" ]
