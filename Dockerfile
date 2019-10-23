FROM python:3-slim
COPY . /src
WORKDIR /src
RUN apt-get update && apt-get install -y build-essential python3-openslide

RUN pip install openslide-python