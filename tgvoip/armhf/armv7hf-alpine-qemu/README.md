# armv7hf-alpine-qemu

Alpine ARM Docker base image with built-in QEMU cross-build support.

This is a base image to enable ARM-based images to be built with x86-64 CI systems as well as Docker Hub's automated build system. See [Resin.io's blog post](https://resin.io/blog/building-arm-containers-on-any-x86-machine-even-dockerhub/) for details.

## Tags

`schmich/armv7hf-alpine-qemu:3.5`: Alpine 3.5 ARM

## Usage

To create your own ARM images that can be cross-built on x86-64 systems:

1. Derive from this image
2. Surround program invocations with `cross-build-start` and `cross-build-end` (you *must* use the exec form seen below)

```Dockerfile
FROM schmich/armv7hf-alpine-qemu:3.5

RUN ["cross-build-start"]

# RUN apk add --no-cache ...
# RUN curl ...
# RUN ...

RUN ["cross-build-end"]
```

## Credits

- Based on [Resin.io's armv7hf-debian-qemu](https://github.com/resin-io-projects/armv7hf-debian-qemu)
- Built with the [armhf/alpine](https://hub.docker.com/r/armhf/alpine/) base image

## License

Copyright &copy; 2017 Resin, Inc &amp; Chris Schmich  
Apache 2.0 License. See [LICENSE](LICENSE) for details.
