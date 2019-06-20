FROM python:3.7-alpine
LABEL maintainer="Farhan Arshad"

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
# It uses package manager comes with alpine nae 'apk' 'add' a package, and
# before this '--update' updates the registry but '--no-cache' don't store the
# registry index on the docker file to minimize the number of extra files and
# packages that are included in the docker container. so that docker container
# have smallest footprint(space occupied) and don't include extra dependencies
# which may cause unexpected effects and create security vulnerabilities in 
# the system. 
RUN apk add --update --no-cache postgresql-client
# Add some temporary packages and remove it after instaling the python 
# requirements. '--virtual' is a alias for our dependencies so we can easily 
# remove them. '.temp-build-deps' name of the alias that means we temporary 
# build the dependencies.
RUN apk add --update --no-cache --virtual .temp-build-deps \
    gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt

# Remove all temporary added packages
RUN apk del .temp-build-deps

#  create a new directory in docker image
RUN mkdir /src
WORKDIR /src
# Copy souce code of the project in the docker image
COPY ./src /src

# create a user name 'user', -D allow to run process from the project and limitize the user scope
RUN adduser -D user
# switch to new created user
USER user
