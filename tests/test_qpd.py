# ==================================================================================
#       Copyright (c) 2020 AT&T Intellectual Property.
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
import json
import time
from contextlib import suppress
from qpdriver import main
from ricxappframe.xapp_frame import Xapp

test_sender = None


def test_flow():
    """
    just a skeleton for now.. this will evolve when qpd evolves
    """

    # start qpd
    main.start(thread=True)

    # define a test sender
    def entry(self):

        val = json.dumps({"test send 30000": 1}).encode()
        self.rmr_send(val, 30000)

        val = json.dumps({"test send 60001": 2}).encode()
        self.rmr_send(val, 60001)

    global test_sender
    test_sender = Xapp(entrypoint=entry, rmr_port=4564, use_fake_sdl=True)
    test_sender.run()

    time.sleep(1)

    assert main.get_stats() == {"DefCalled": 1, "SteeringRequests": 1}


def teardown_module():
    """
    this is like a "finally"; the name of this function is pytest magic
    safer to put down here since certain failures above can lead to pytest never returning
    for example if an exception gets raised before stop is called in any test function above, pytest will hang forever
    """
    with suppress(Exception):
        test_sender.stop()
    with suppress(Exception):
        main.stop()
