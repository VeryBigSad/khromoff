# pull official base image
FROM python:3.9.5-slim-buster

# set work directory
RUN mkdir /code
WORKDIR /code

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /code/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY . /code
# remove the static folder if it exists so that we can recreate it on the machine
CMD ["rm", "-rf", "static"]
# that will not be used so we remove it
CMD ["rm", "-rf", "services"]
RUN python manage.py collectstatic --noinput
