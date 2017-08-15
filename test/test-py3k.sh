#!/usr/bin/env bash
alias py3k='docker run --rm -it -v $(pwd):/src -w /src python:3-stretch sh ./test/test.sh'

py3k 3.0.0
py3k 3.2.0
py3k 3.3.0
