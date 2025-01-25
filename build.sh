#!/bin/bash
# Create a clean build directory
rm -rf .aws-sam/build

# Create package directory
mkdir -p package/src

# Copy source files
cp -r src/* package/src/

# Install dependencies
pip install -r requirements-prod.txt -t package/

# Build with SAM
sam build
