FROM python:3.7

WORKDIR /usr/src/home_app

COPY . /usr/src/home_app

EXPOSE 5000

RUN pip install -r requirements.txt

CMD ["flask", "run", "--host=0.0.0.0"]
