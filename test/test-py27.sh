#!/usr/bin/env bash
alias py27='docker run --rm -it -v $(pwd):/src -w /src python:2-stretch sh ./test/test.sh'

py27 3.0.0
py27 3.2.0
py27 3.3.0
