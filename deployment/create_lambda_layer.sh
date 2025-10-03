#!/bin/bash

# Script to create Lambda layer with required Python packages

echo "Creating Lambda layer for Bedrock PowerPoint Generator..."

# Create directory structure
mkdir -p python

# Install required packages
pip install firecrawl-py python-pptx -t python --platform manylinux2014_x86_64 --only-binary=:all:

# Create ZIP file
zip -r layer.zip python

echo "Lambda layer created: layer.zip"
echo "Upload this file to AWS Lambda Layers in the console"

# Cleanup
rm -rf python

echo "Done!"