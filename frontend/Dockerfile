FROM python:3.7

WORKDIR /usr/src/

COPY ./requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

CMD ["streamlit", "run", "index.py"]
