FROM python:3.7

WORKDIR /usr/src/home-test

COPY . /usr/src/home-test

EXPOSE 5000

RUN pip install -r requirements.txt

CMD ["flask", "run", "--host=0.0.0.0"]
