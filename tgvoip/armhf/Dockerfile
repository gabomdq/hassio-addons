#FROM alpine:3.8
FROM arm32v6/alpine:3.8

ENV QEMU_EXECVE 1

COPY armv7hf-alpine-qemu/qemu-arm-static /usr/bin
COPY armv7hf-alpine-qemu/resin-xbuild /usr/bin

RUN [ "/usr/bin/qemu-arm-static", "/bin/sh", "-c", "ln -s /usr/bin/resin-xbuild /usr/bin/cross-build-start; ln -s /usr/bin/resin-xbuild /usr/bin/cross-build-end; ln /bin/sh /bin/sh.real" ]

RUN ["cross-build-start"]
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

WORKDIR /usr/src
COPY build.sh .
COPY python3_symlinks.sh .
RUN /bin/sh build.sh

WORKDIR /dist
RUN mkdir -p usr/local
RUN cp -r /usr/local/include usr/local
RUN cp -r /usr/local/lib usr/local
RUN rm -rf usr/local/lib/perl5
RUN rm -rf usr/local/lib/libtgvoip.a
RUN mkdir -p root/.local
RUN cp -r /root/.local root

ARG VCS_REF
ARG VCS_URL
ARG BUILD_DATE
LABEL org.label-schema.vcs-ref=${VCS_REF} \
      org.label-schema.vcs-url=${VCS_URL} \
      org.label-schema.build-date=${BUILD_DATE}

RUN ["cross-build-end"]
