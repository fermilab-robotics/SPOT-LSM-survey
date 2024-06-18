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

#libusb is required for exodriver 
#see https://github.com/labjack/exodriver/blob/master/INSTALL.Linux
# RUN export DEBIAN_FRONTEND=noninteractive && export DEBIAN_FRONTEND=noninteractive \
#    && apt-get -y install --no-install-recommends libusb-1.0-0-dev  

#exodriver
# RUN git clone --depth=1 --verbose https://github.com/labjack/exodriver.git \
#    && cd exodriver && ./install.sh

COPY . . 
RUN chmod +x port_detection.sh entrypoint.sh

ENTRYPOINT ["bash","-c","source ./entrypoint.sh"]




  



