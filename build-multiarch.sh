#!/bin/sh

docker buildx build --platform linux/amd64,linux/arm64\
 -t rdomloge/catholicon-agg-clubfixture:latest . --push