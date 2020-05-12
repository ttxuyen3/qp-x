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
from ricxappframe.xapp_frame import Xapp, RMRXapp

mock_traffic_steering = None
mock_qp_predictor = None

"""
 these tests are not currently parallelizable (do not use this tox flag)
 I would use setup_module, however that can't take monkeypatch fixtures
 Currently looking for the best way to make this better:
 https://stackoverflow.com/questions/60886013/python-monkeypatch-in-pytest-setup-module
"""


def test_init_xapp(monkeypatch, ue_metrics, cell_metrics_1, cell_metrics_2, cell_metrics_3, ue_metrics_with_bad_cell):
    # monkeypatch post_init to set the data we want in SDL
    # the metrics arguments are JSON (dict) objects
    def fake_post_init(self):
        self.def_hand_called = 0
        self.traffic_steering_requests = 0
        self.sdl_set(data.UE_NS, "12345", json.dumps(ue_metrics).encode(), usemsgpack=False)
        self.sdl_set(data.UE_NS, "8675309", json.dumps(ue_metrics_with_bad_cell).encode(), usemsgpack=False)
        self.sdl_set(data.CELL_NS, "310-680-200-555001", json.dumps(cell_metrics_1).encode(), usemsgpack=False)
        self.sdl_set(data.CELL_NS, "310-680-200-555002", json.dumps(cell_metrics_2).encode(), usemsgpack=False)
        self.sdl_set(data.CELL_NS, "310-680-200-555003", json.dumps(cell_metrics_3).encode(), usemsgpack=False)

    # patch
    monkeypatch.setattr("qpdriver.main.post_init", fake_post_init)

    # start qpd
    main.start(thread=True)


def test_rmr_flow(monkeypatch, qpd_to_qp, qpd_to_qp_bad_cell):
    """
    this flow mocks out the xapps on both sides of QP driver.
    It first stands up a mock qp predictor, then it starts up a
    mock traffic steering which will immediately send requests
    to the running qp driver]
    """

    expected_result = {}

    # define a mock qp predictor
    def default_handler(self, summary, sbuf):
        pass

    def qp_driver_handler(self, summary, sbuf):
        nonlocal expected_result  # closures ftw
        pay = json.loads(summary["payload"])
        expected_result[pay["PredictionUE"]] = pay

    global mock_qp_predictor
    mock_qp_predictor = RMRXapp(default_handler, rmr_port=4666, use_fake_sdl=True)
    mock_qp_predictor.register_callback(qp_driver_handler, 30001)
    mock_qp_predictor.run(thread=True)

    time.sleep(1)

    # define a mock traffic steering xapp
    def entry(self):

        # make sure a bad steering request doesn't blow up in qpd
        val = "notevenjson".encode()
        self.rmr_send(val, 30000)
        val = json.dumps({"bad": "tothebone"}).encode()  # json but missing UEPredictionSet
        self.rmr_send(val, 30000)

        # valid request body but missing cell id
        val = json.dumps({"UEPredictionSet": ["VOIDOFLIGHT"]}).encode()
        self.rmr_send(val, 30000)

        # good traffic steering request
        val = json.dumps({"UEPredictionSet": ["12345", "8675309"]}).encode()
        self.rmr_send(val, 30000)

        # should trigger the default handler and do nothing
        val = json.dumps({"test send 60001": 2}).encode()
        self.rmr_send(val, 60001)

    global mock_traffic_steering
    mock_traffic_steering = Xapp(entrypoint=entry, rmr_port=4564, use_fake_sdl=True)
    mock_traffic_steering.run()  # this will return since entry isn't a loop

    time.sleep(1)

    assert expected_result == {"12345": qpd_to_qp, "8675309": qpd_to_qp_bad_cell}
    assert main.get_stats() == {"DefCalled": 1, "SteeringRequests": 4}


def teardown_module():
    """
    this is like a "finally"; the name of this function is pytest magic
    safer to put down here since certain failures above can lead to pytest never returning
    for example if an exception gets raised before stop is called in any test function above, pytest will hang forever
    """
    with suppress(Exception):
        mock_traffic_steering.stop()
    with suppress(Exception):
        mock_qp_predictor.stop()
    with suppress(Exception):
        main.stop()
