#!/usr/bin/env bash
docker run --rm -v $(pwd)/test:/src -w /src znly/protoc --python_out=. -I. Person.proto
