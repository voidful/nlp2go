FROM python:3.9.16

# nodejs
RUN apt-get -y update
RUN curl -fsSL https://deb.nodesource.com/setup_19.x | bash -
RUN apt install -y nodejs

# Create app directory
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# Copy Python dependencies
COPY requirements.txt /usr/src/app/
RUN pip3 install -r /usr/src/app/requirements.txt

# Copy source project
COPY . /usr/src/app/

RUN npm install --global yarn
RUN yarn install
RUN yarn build

CMD python3 server.py --port 80 --static ./build