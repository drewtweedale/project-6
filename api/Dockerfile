FROM python:3.8
LABEL Drew Tweedale="dtweedal@uoregon.edu"
RUN apt-get update -y
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
