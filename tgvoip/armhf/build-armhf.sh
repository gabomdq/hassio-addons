#!/bin/bash
# Cross compile armhf binaries using docker

rm -rf dist
cp -f ../build_dependencies.sh build.sh
cp -f ../python3_symlinks.sh .
docker build --no-cache -t tgvoip-cross .
docker run -v $PWD:/out --rm -ti tgvoip-cross  cp -r /dist /out
sudo chown -R $USER:$USER dist
cd dist
tar -cvjSf ../tgvoip.tar.bz2 *
cd ..
rm -rf dist
rm build.sh
rm python3_symlinks.sh