FROM ubuntu:20.04

WORKDIR /home/SPOT-LSM-survey
ENV TZ="America/Chicago"

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
   python3.9-venv  && apt-get clean 

RUN python3.9 -m venv /venv
ENV PATH=/venv/bin:$PATH

COPY requirements.txt /tmp/pip-tmp/
RUN apt-get install -y git udev
RUN pip --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
   && rm -rf /tmp/pip-tmp

COPY . . 
RUN chmod +x port_detection.sh entrypoint.sh

ENTRYPOINT ["bash","-c","source ./entrypoint.sh"]



  



