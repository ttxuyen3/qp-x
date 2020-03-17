# ==================================================================================
#       Copyright (c) 2018-2020 AT&T Intellectual Property.
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#          http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
# ==================================================================================
FROM python:3.7-alpine

# RMR setup
RUN mkdir -p /opt/route/
COPY --from=nexus3.o-ran-sc.org:10004/bldr-alpine3-go:1-rmr1.13.1 /usr/local/lib64/libnng.so /usr/local/lib64/libnng.so
COPY --from=nexus3.o-ran-sc.org:10004/bldr-alpine3-go:1-rmr1.13.1 /usr/local/lib64/librmr_nng.so /usr/local/lib64/librmr_nng.so
ENV LD_LIBRARY_PATH /usr/local/lib/:/usr/local/lib64

# sdl needs gcc
RUN apk update && apk add gcc musl-dev bash

# Install
COPY setup.py /tmp
COPY LICENSE.txt /tmp/
COPY qpdriver/ /tmp/qpdriver
RUN pip install /tmp

# Run
ENV PYTHONUNBUFFERED 1
CMD start.py
