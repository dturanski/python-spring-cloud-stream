FROM python:2.7.11-alpine
COPY . /src
RUN apk add --no-cache git
RUN pip install -r src/requirements.txt
CMD [ "python", "src/consumer.py" ]
