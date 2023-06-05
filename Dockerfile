FROM ubuntu:latest
RUN apt-get update && apt-get install -y \
    net-tools \
    curl \
    tcpdump \
    python3-pip
COPY requirements.txt .
RUN pip3 install -r requirements.txt
COPY flow.py /usr/local/lib/python3.10/dist-packages/cicflowmeter/
COPY flow_session.py /usr/local/lib/python3.10/dist-packages/cicflowmeter/
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
