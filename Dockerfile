FROM python:3.7-alpine
LABEL maintainer="Farhan Arshad"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

#  create a new directory in docker image
RUN mkdir /src
WORKDIR /src
# Copy souce code of the project in the docker image
COPY ./src /src

# create a user name 'user', -D allow to run process from the project and limitize the user scope
RUN adduser -D user
# switch to new created user
USER user