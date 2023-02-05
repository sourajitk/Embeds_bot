FROM python:3.11-slim-buster

WORKDIR /app

COPY . .
RUN apt-get update; apt-get install -y git
RUN pip install -U setuptools setuptools_scm wheel
RUN pip3 install .

CMD ["python3", "src/embeds_bot/app.py"]
