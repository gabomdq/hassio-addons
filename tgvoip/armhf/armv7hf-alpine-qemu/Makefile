src := $(dir $(abspath $(lastword $(MAKEFILE_LIST))))

resin-xbuild: resin-xbuild.go
	GOOS=linux GOARCH=amd64 go build -ldflags "-w -s" resin-xbuild.go

qemu-arm-static: build-qemu.sh
	docker run -v $(src)build-qemu.sh:/tmp/build.sh -v $(src):/host debian:8.7 sh /tmp/build.sh
