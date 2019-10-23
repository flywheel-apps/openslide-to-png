FROM python:3-slim
MAINTAINER Flywheel <support@flywheel.io>

# Make directory for flywheel spec (v0)
ENV FLYWHEEL /flywheel/v0
RUN mkdir -p ${FLYWHEEL}
COPY run.py ${FLYWHEEL}/run.py
RUN chmod +x ${FLYWHEEL}/run.py
COPY manifest.json ${FLYWHEEL}/manifest.json

RUN apt-get update && apt-get install -y build-essential python3-openslide

RUN pip install openslide-python