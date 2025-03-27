FROM ubuntu:20.04 as builder 
RUN apt-get update && apt-get install -y git
WORKDIR /git-install
RUN git clone --depth 1 https://github.com/fermilab-robotics/AccuRad-PRD.git /git-install


FROM python:3.9-alpine as base
WORKDIR /dependencies
COPY --from=builder /git-install /dependencies
RUN pip install --no-cache-dir bosdyn-client==3.3.2 bosdyn-mission==3.3.2  --target /install  \ 
   && pip install . --target /install

FROM python:3.9-alpine as run-time 
COPY --from=base /install /usr/local/lib/python3.9/site-packages/ 
WORKDIR /SPOT-LSM-survey
COPY . . 
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/bin/sh","-c"]
CMD ["./entrypoint.sh"]


  



