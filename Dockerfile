FROM python:3-slim
MAINTAINER Flywheel <support@flywheel.io>

RUN apt-get update && apt-get install -y \
    build-essential \
    python3-openslide

# Make directory for flywheel spec (v0)
ENV FLYWHEEL /flywheel/v0
RUN mkdir -p ${FLYWHEEL}
COPY run.py ${FLYWHEEL}/run.py
RUN chmod +x ${FLYWHEEL}/run.py
COPY manifest.json ${FLYWHEEL}/manifest.json

# Install python package dependencies
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt