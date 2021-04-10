FROM pytorch/pytorch:latest

# utf-8 zh_TW
RUN apt-get -y update

# Create app directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Install Python dependencies
COPY requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

# Copy source project
COPY . /usr/src/app/

RUN nlp2go-preload --json config.json
CMD PYTHONIOENCODING=utf8 nlp2go --json config.json --api_port ${PORT}
