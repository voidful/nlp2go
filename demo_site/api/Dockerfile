FROM pytorch/pytorch:latest

# utf-8 zh_TW
RUN apt-get -y update

# Create app directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Install Python dependencies
RUN pip install gevent

# Copy source project
COPY . /usr/src/app/

RUN pip install nlprep tfkit nlp2go -U
RUN nlp2go-preload --json config.json
CMD PYTHONIOENCODING=utf8 nlp2go --json config.json --api_port ${PORT}
