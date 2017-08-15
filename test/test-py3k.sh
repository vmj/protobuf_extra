#!/usr/bin/env bash
alias py3k='docker run --rm -it -v $(pwd):/src -w /src python:3-alpine sh ./test.sh'

py3k 3.0.0
py3k 3.2.0
py3k 3.3.0
