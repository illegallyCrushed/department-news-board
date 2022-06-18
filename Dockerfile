FROM python:3.10.5


COPY python-requirements.txt /python-requirements.txt
RUN pip install --upgrade pip
RUN pip install -r /python-requirements.txt


COPY . .