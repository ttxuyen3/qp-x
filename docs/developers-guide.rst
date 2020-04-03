.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0
.. Copyright (C) 2020 AT&T Intellectual Property


Developers Guide
=================

.. contents::
   :depth: 3
   :local:

Testing RMR Healthcheck
-----------------------
The following instructions should deploy the QP Driver container in bare docker, and allow you to test that the rmr healthcheck is working

::

    docker build -t qpd:latest -f  Dockerfile .
    docker run -d --net=host -e USE_FAKE_SDL=1 qpd:latest
    docker exec -it CONTAINER_ID /usr/local/bin/health_ck -h 127.0.0.1:4562


