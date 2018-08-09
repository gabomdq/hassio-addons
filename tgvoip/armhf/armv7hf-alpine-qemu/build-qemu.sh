#!/bin/sh

apt-get update
apt-get install -y git build-essential python pkg-config zlib1g-dev libglib2.0 dh-autoreconf

mkdir -p /tmp/qemu
cd /tmp
git clone https://github.com/resin-io/qemu

cd qemu
git submodule update --init pixman

mkdir build
cd build
../configure --target-list=arm-linux-user --static
make

cd arm-linux-user
strip qemu-arm
cp qemu-arm /host/qemu-arm-static
