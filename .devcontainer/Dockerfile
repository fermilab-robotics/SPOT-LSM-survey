FROM python:3.7-bullseye

WORKDIR /home/SPOT-LSM-survey

# pip install
COPY requirements.txt /tmp/pip-tmp/
RUN pip3 --disable-pip-version-check --no-cache-dir install -r /tmp/pip-tmp/requirements.txt \
   && rm -rf /tmp/pip-tmp

#libusb is required for exodriver 
#see https://github.com/labjack/exodriver/blob/master/INSTALL.Linux
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive && export DEBIAN_FRONTEND=noninteractive \
   && apt-get -y install --no-install-recommends libusb-1.0-0-dev  

#exodriver
RUN git clone --depth=1 --verbose https://github.com/labjack/exodriver.git \
   && cd exodriver && ./install.sh

COPY . . 


