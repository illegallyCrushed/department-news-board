FROM rabbitmq:3.10.5


RUN apt-get update -y\
    && apt-get upgrade -y\
    && apt-get install python -y\
    && apt-get install python3-pip -y


COPY python-requirements.txt /python-requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /python-requirements.txt


EXPOSE 8000


COPY . .


CMD [ "python", "test.py" ]