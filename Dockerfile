# set base image (host OS)
FROM python:3.8

# set the working directory in the container
WORKDIR /home/dnl

# copy the dependencies file to the working directory
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

# copy the directory structure to working dir
COPY . .

# set environment path
ENV PYTHONPATH "$PYTHONPATH:/home/dnl"

# command to run on container start
CMD ["python3", "-m", "uvicorn", "main:app", "--host=0.0.0.0"]