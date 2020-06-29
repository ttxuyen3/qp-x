.. This work is licensed under a Creative Commons Attribution 4.0 International License.
.. SPDX-License-Identifier: CC-BY-4.0
.. Copyright (C) 2020 AT&T Intellectual Property

Release Notes
===============

All notable changes to this project will be documented in this file.

The format is based on `Keep a Changelog <http://keepachangelog.com/>`__
and this project adheres to `Semantic Versioning <http://semver.org/>`__.


[1.1.0] - 2020-06-29
--------------------
* Send alarm on SDL failure (`RICAPP-117 <https://jira.o-ran-sc.org/browse/RICAPP-117>`_)
* Requires RMR at version 4.1.2 or later
* Requires xapp-frame-py at version 1.2.0 or later


[1.0.9] - 2020-06-02
--------------------
* Change RMR listen port to 4560 (`RICAPP-112 <https://jira.o-ran-sc.org/browse/RICAPP-112>`_)


[1.0.8] - 2020-05-22
--------------------
* Revise static route table (`RICAPP-108 <https://jira.o-ran-sc.org/browse/RICAPP-108>`_)


[1.0.7] - 2020-05-15
--------------------
* Include xapp descriptor json in repo (`RICAPP-97 <https://jira.o-ran-sc.org/browse/RICAPP-97>`_)
  

[1.0.6] - 2020-05-12
--------------------
* Decode values from SDL as JSON (`RICAPP-104 <https://jira.o-ran-sc.org/browse/RICAPP-104>`_)


[1.0.5] - 2020-05-08
--------------------

* Upgrade to RMR version 4.0.5
* Upgrade to framework version 1.1.0
* Use constants from rmr module instead of hardcoded strings
* Add Dockerfile-Unit-Test to support testing


[1.0.4] - 2020-05-05
--------------------

* Upgrade to RMR version 4.0.2


[1.0.3] - 2020-04-22
--------------------

* Upgrade to RMR version 3.8.2


[1.0.2] - 4/8/2020
------------------

* Upgrade to xapp frame 1.0.0 which includes rmr python


[1.0.1] - 4/3/2020
------------------

* Docker now builds with an empty route file so rmr starts; it will not even start properly without this
* Change how fake_sdl is activated for docker convienence
* Create dev guide file
* Add instructions on how to test the rmr healthcheck in a running container
* Update to xapp frame 0.7.0 (which has rmr healthchecks)


[1.0.0] - 4/1/2020
------------------

* This release is seen as the first complete implementation of QPD, although likely fixes and enhancements are needed
* Implement the rmr messaging
* Add tests for various bad scenarios like UE IDs not existing and Cell data not existing
* Fix UE IDs to be strings as they are in the req slides


[0.2.0] - 3/27/2020
-------------------

* Implement SDL calls and testing
* Small cleanups


[0.1.0] - 3/26/2020
-------------------

* Implement the core business logic of the data merge


[0.0.2] - 3/25/2020
-------------------

* Move to SI95
* Move to Xapp frame 0.6.0
* Move to py38
* Remove unneeded stuff from setup.py since this is a docker component and not a pypi library
* Add some mock data for future development


[0.0.1] - 3/17/2020
-------------------

* inital skeleton creation
