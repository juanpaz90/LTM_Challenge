#!/bin/bash

TAG_01=api

docker build -t "$TAG_01" -f 'build/FastAPI.Dockerfile' .

docker run \
  -e .env \
  -p 8000:8000 \
  -d "$TAG_01"
