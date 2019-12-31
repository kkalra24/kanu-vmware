
FROM python:3.7

RUN pip install PyYAML==5.2
RUN pip install pytest==5.3.2
RUN pip install requests==2.22.0

WORKDIR .
COPY . .
CMD [ "pytest", "./test_vmware.py" ]