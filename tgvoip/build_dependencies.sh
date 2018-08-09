#!/bin/sh
if [ -f /usr/local/lib/libtgvoip.so ]; then
  exit 0
fi

# Build dependencies
apk add \
              build-base \
              python3-dev \
              bash \
              git \
              libxml2-dev \
              libxslt-dev \
              openssl-dev \
              opus-dev \
              pulseaudio-dev \
              alsa-lib-dev \
              cmake \
              gperf \
              automake \
              autoconf \
              libtool \

sh python3_symlinks.sh

mkdir -p /usr/src
cd /usr/src
git clone https://github.com/gabomdq/libtgvoip.git
cd libtgvoip
CXXFLAGS="-DMIN_UDP_PORT=20000 -DMAX_UDP_PORT=20001" ./configure
make -j4
make install
cd ..

# Build tdlib
git clone https://github.com/tdlib/td.git
mkdir -p td/build
cd td/build
cmake -DCMAKE_BUILD_TYPE=Release .. 
cmake --build . -- -j4
cd ../..

# python-telegram
git clone https://github.com/gabomdq/python-telegram.git
mkdir -p python-telegram/telegram/lib/linux
cp td/build/libtdjson.so python-telegram/telegram/lib/linux
cd python-telegram
python3 setup.py install --user
cd ..

# pytgvoip
git clone https://github.com/gabomdq/pytgvoip.git
cd pytgvoip
python3 setup.py install --user
cd ..

rm -rf /usr/src

# Fix up dependencies for runtime
apk del \
              build-base \
              python3-dev \
              git \
              libxml2-dev \
              libxslt-dev \
              openssl-dev \
              opus-dev \
              pulseaudio-dev \
              alsa-lib-dev \
              cmake \
              gperf \
              automake \
              autoconf \
              libtool \

apk add --update \
              ca-certificates \
              musl \
              bash \
              openssl \
              pulseaudio \
              opus \
              alsa-lib \
