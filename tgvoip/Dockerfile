ARG BUILD_FROM=hassioaddons/base:2.0.1
FROM ${BUILD_FROM}

ARG BUILD_ARCH
RUN apk add --update \
              ca-certificates \
              musl \
              python3 \
              bash \
              openssl \
              pulseaudio \
              opus \
              alsa-lib \
 && pip3.6 install --upgrade pip \
 && rm /var/cache/apk/*

# Install tgvoip binaries
ADD ${BUILD_ARCH}/tgvoip.tar.bz2 /

# If no binaries available (i.e. tgvoip.tar.bz is a dummy file), build from source
WORKDIR /usr/src
COPY build_dependencies.sh build.sh
COPY python3_symlinks.sh .
RUN sh build.sh

# After clean up the symlinks are lost, fix them up again
WORKDIR /usr/src
COPY python3_symlinks.sh .
RUN sh python3_symlinks.sh

# Python Dependencies
RUN pip install paho-mqtt

COPY tgmqtt.py /
COPY run.sh /
RUN chmod a+x /run.sh
CMD ["/run.sh"]

ARG VCS_REF
ARG VCS_URL
ARG BUILD_DATE
LABEL org.label-schema.vcs-ref=${VCS_REF} \
      org.label-schema.vcs-url=${VCS_URL} \
      org.label-schema.build-date=${BUILD_DATE}
