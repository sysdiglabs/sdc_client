FROM python:3-alpine
WORKDIR /sdc_client
COPY sdc_client *.py requirements.txt LICENSE /sdc_client/
COPY cli /sdc_client/cli
COPY sdc /sdc_client/sdc
COPY sdc_client.sh /bin/sdc_client
RUN chmod +x /bin/sdc_client
RUN pip install -r /sdc_client/requirements.txt
ENTRYPOINT ["sdc_client"]
