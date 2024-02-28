FROM ubuntu:20.04

WORKDIR /home/SPOT-LSM-survey
#Our current spot is only compatible with python3.7
RUN apt-get update && apt-get install -y pip python3.7

# pip install
COPY requirements.txt /tmp/pip-tmp/
RUN apt-get install -y git
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
   && rm -rf /tmp/pip-tmp

#libusb is required for exodriver 
#see https://github.com/labjack/exodriver/blob/master/INSTALL.Linux
RUN export DEBIAN_FRONTEND=noninteractive && export DEBIAN_FRONTEND=noninteractive \
   && apt-get -y install --no-install-recommends libusb-1.0-0-dev  

#exodriver
RUN git clone --depth=1 --verbose https://github.com/labjack/exodriver.git \
   && cd exodriver && ./install.sh

COPY . . 

# WORKDIR /home/SPOT-LSM-survey/src/data_acquisitions/
# RUN cp data_export.py tocsv && chmod +x tocsv && cp tocsv /usr/sbin

# WORKDIR /home/SPOT-LSM-survey

ENTRYPOINT [ "python3","src/main.py" ]





