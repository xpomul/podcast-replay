FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./main /code/main

COPY ./config /code/config

VOLUME /code/config

EXPOSE 8088

CMD ["uvicorn", "main.podcast_replay:app", "--host", "0.0.0.0", "--port", "8088"]
