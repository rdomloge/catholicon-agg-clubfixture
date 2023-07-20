FROM python:3.9-slim
RUN pip install --upgrade pip
RUN pip3 install flask requests
COPY endpoint.py /endpoint.py
ENTRYPOINT [ "python", "/endpoint.py" ] 