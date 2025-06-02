FROM python:3.12
MAINTAINER TR1GUN-D
ADD . /app
WORKDIR /app
COPY . /app
RUN pip3 install --upgrade -r requirements.txt
EXPOSE 8000
CMD [ "python3", "app.py"]

