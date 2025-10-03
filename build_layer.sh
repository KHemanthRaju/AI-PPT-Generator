#!/bin/bash

# Build Lambda layer using Docker for Linux compatibility
docker run --rm -v "$PWD":/var/task "public.ecr.aws/lambda/python:3.9" /bin/sh -c "
    mkdir -p /tmp/layer/python
    pip install python-pptx -t /tmp/layer/python/
    cd /tmp/layer
    zip -r /var/task/pptx-layer-linux.zip .
"

echo "Linux-compatible layer created: pptx-layer-linux.zip"