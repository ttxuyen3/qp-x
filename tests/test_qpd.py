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
from qpdriver import main, data
from ricxappframe.xapp_frame import Xapp

test_sender = None

"""
 these tests are not currently parallelizable (do not use this tox flag)
 I would use setup_module, however that can't take monkeypatch fixtures
 Currently looking for the best way to make this better: https://stackoverflow.com/questions/60886013/python-monkeypatch-in-pytest-setup-module
"""


def test_init_xapp(monkeypatch, ue_metrics, cell_metrics_1, cell_metrics_2, cell_metrics_3, qpd_to_qp):
    # monkeypatch post_init to set the data we want in SDL
    def fake_post_init(self):
        self.def_hand_called = 0
        self.traffic_steering_requests = 0
        self.sdl_set(data.UE_NS, "12345", ue_metrics, usemsgpack=False)
        self.sdl_set(data.CELL_NS, "310-680-200-555001", cell_metrics_1, usemsgpack=False)
        self.sdl_set(data.CELL_NS, "310-680-200-555002", cell_metrics_2, usemsgpack=False)
        self.sdl_set(data.CELL_NS, "310-680-200-555003", cell_metrics_3, usemsgpack=False)

    # patch
    monkeypatch.setattr("qpdriver.main.post_init", fake_post_init)

    # start qpd
    main.start(thread=True, use_fake_sdl=True)


def test_data_merge(qpd_to_qp):
    """
    test the merge (basically tests all of the code in data.py in this one line)
    TODO: this will go away when the full E2E flow is implemented as we can just look at the final result
    """
    assert data.form_qp_pred_req(main.rmr_xapp, 12345) == qpd_to_qp


def test_rmr_flow(monkeypatch, ue_metrics, cell_metrics_1, cell_metrics_2, cell_metrics_3, qpd_to_qp):
    """
    just a skeleton for now.. this will evolve when qpd evolves
    """

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
