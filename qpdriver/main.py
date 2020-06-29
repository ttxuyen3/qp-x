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
"""
qpdriver entrypoint module

RMR Messages
 #define TS_UE_LIST 30000
 #define TS_QOE_PRED_REQ 30001
 #define TS_QOE_PREDICTION 30002
30000 is the message type QPD receives; sends out type 30001, which should be routed to QP.
"""

import json
from os import getenv
from ricxappframe.xapp_frame import RMRXapp, rmr
from ricxappframe.alarm import alarm
from qpdriver import data
from qpdriver.exceptions import UENotFound


# pylint: disable=invalid-name
rmr_xapp = None


def post_init(self):
    """
    Function that runs when xapp initialization is complete
    """
    self.def_hand_called = 0
    self.traffic_steering_requests = 0
    self.alarm_mgr = alarm.AlarmManager(self._mrc, "ric-xapp", "qp-driver")
    self.alarm_sdl = None


def handle_config_change(self, config):
    """
    Function that runs at start and on every configuration file change.
    """
    self.logger.debug("handle_config_change: config: {}".format(config))


def default_handler(self, summary, sbuf):
    """
    Function that processes messages for which no handler is defined
    """
    self.def_hand_called += 1
    self.logger.warning("default_handler unexpected message type {}".format(summary[rmr.RMR_MS_MSG_TYPE]))
    self.rmr_free(sbuf)


def steering_req_handler(self, summary, sbuf):
    """
    This is the main handler for this xapp, which handles traffic steering requests.
    Traffic steering requests predictions on a set of UEs.
    This app fetches a set of data from SDL, merges it together in a deterministic way,
    then sends a new message to the QP predictor Xapp.

    The incoming message that this function handles looks like:
        {"UEPredictionSet" : ["UEId1","UEId2","UEId3"]}
    """
    self.traffic_steering_requests += 1
    # we don't use rts here; free the buffer
    self.rmr_free(sbuf)

    ue_list = []
    try:
        req = json.loads(summary[rmr.RMR_MS_PAYLOAD])  # input should be a json encoded as bytes
        ue_list = req["UEPredictionSet"]
        self.logger.debug("steering_req_handler processing request for UE list {}".format(ue_list))
    except (json.decoder.JSONDecodeError, KeyError):
        self.logger.warning("steering_req_handler failed to parse request: {}".format(summary[rmr.RMR_MS_PAYLOAD]))
        return

    if self._sdl.healthcheck():
        # healthy, so clear the alarm if it was raised
        if self.alarm_sdl:
            self.logger.debug("steering_req_handler clearing alarm")
            self.alarm_mgr.clear_alarm(self.alarm_sdl)
            self.alarm_sdl = None
    else:
        # not healthy, so (re-)raise the alarm
        self.logger.debug("steering_req_handler connection to SDL is not healthy, raising alarm")
        if self.alarm_sdl:
            self.alarm_mgr.reraise_alarm(self.alarm_sdl)
        else:
            self.alarm_sdl = self.alarm_mgr.create_alarm(1, alarm.AlarmSeverity.CRITICAL, "SDL failure")
            self.alarm_mgr.raise_alarm(self.alarm_sdl)
        self.logger.warning("steering_req_handler dropping request!")
        return

    # iterate over the UEs and send a request for each, if it is a valid UE, to QP
    for ueid in ue_list:
        try:
            to_qpp = data.form_qp_pred_req(self, ueid)
            payload = json.dumps(to_qpp).encode()
            success = self.rmr_send(payload, 30001)
            if not success:
                self.logger.warning("steering_req_handler failed to send to QP!")
        except UENotFound:
            self.logger.warning("steering_req_handler received a TS Request for a UE that does not exist!")


def start(thread=False):
    """
    This is a convenience function that allows this xapp to run in Docker
    for "real" (no thread, real SDL), but also easily modified for unit testing
    (e.g., use_fake_sdl). The defaults for this function are for the Dockerized xapp.
    """
    global rmr_xapp
    fake_sdl = getenv("USE_FAKE_SDL", None)
    rmr_xapp = RMRXapp(default_handler,
                       config_handler=handle_config_change,
                       rmr_port=4560,
                       post_init=post_init,
                       use_fake_sdl=bool(fake_sdl))
    rmr_xapp.register_callback(steering_req_handler, 30000)
    rmr_xapp.run(thread)


def stop():
    """
    can only be called if thread=True when started
    TODO: could we register a signal handler for Docker SIGTERM that calls this?
    """
    rmr_xapp.stop()


def get_stats():
    """
    hacky for now, will evolve
    """
    return {"DefCalled": rmr_xapp.def_hand_called,
            "SteeringRequests": rmr_xapp.traffic_steering_requests}
