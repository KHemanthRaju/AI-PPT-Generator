#!/bin/bash

# Build Lambda layer using Docker for Linux compatibility
docker run --rm --entrypoint /bin/sh -v "$PWD":/var/task "public.ecr.aws/lambda/python:3.9" -c "
    yum install -y zip &&
    mkdir -p /tmp/layer/python &&
    pip install python-pptx matplotlib pandas openpyxl -t /tmp/layer/python/ &&
    cd /tmp/layer &&
    zip -r /var/task/pptx-layer-linux.zip . &&
    echo 'Lambda layer created successfully'
"

echo ""
echo "✅ Linux-compatible layer created: pptx-layer-linux.zip"
echo "📦 Includes: python-pptx, matplotlib, pandas, openpyxl"
echo "📊 Size: $(ls -lh pptx-layer-linux.zip | awk '{print $5}')"