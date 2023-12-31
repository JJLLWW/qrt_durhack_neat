FROM python:3.12
ENV IN_DOCKER_CONTAINER='yes'
COPY src/ src/
COPY requirements_ugh.txt .
RUN pip install -r requirements_ugh.txt
CMD python src/server.py