FROM hysds/pge-base:latest
MAINTAINER torresal "alexander.p.torres@jpl.nasa.gov"
LABEL description="Smart Tasking query & evaluation base image"

USER ops
# copy packages
COPY . /home/ops/verdi/ops/smarttasking_listener
RUN set -ex \
 && source /home/ops/verdi/bin/activate \
 && sudo chown -R ops:ops /home/ops/verdi/ops/smarttasking_listener

WORKDIR /home/ops
CMD ["/bin/bash", "--login"]
