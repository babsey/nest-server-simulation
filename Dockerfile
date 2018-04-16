FROM ubuntu:16.04

LABEL maintainer="Sebastian Spreizer <spreizer@web.de>"

RUN apt-get update && apt-get install -y \
    build-essential \
    cmake \
    cython \
    libgsl0-dev \
    libltdl7-dev \
    libncurses5-dev \
    libreadline6-dev \
    python-all-dev \
    python-flask \
    python-numpy \
    wget

WORKDIR /tmp
RUN wget https://github.com/nest/nest-simulator/archive/v2.14.0.tar.gz && \
    tar -xvzf v2.14.0.tar.gz && \
    mkdir /tmp/nest-build

WORKDIR /tmp/nest-build
RUN cmake -DCMAKE_INSTALL_PREFIX:PATH=/opt/nest/ ../nest-simulator-2.14.0 && \
    make && \
    make install && \
    rm -rf /tmp/*

COPY ./ /nest-server-simulation
WORKDIR /nest-server-simulation

EXPOSE 5000
RUN chmod 755 entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]
