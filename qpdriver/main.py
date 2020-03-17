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
from ricxappframe.xapp_frame import RMRXapp


"""
This is only a stencil for now, will be filled in!
What is currently here was only for initial skeleton and test creation.
"""


def post_init(self):
    self.def_hand_called = 0
    self.traffic_steering_requests = 0


def default_handler(self, summary, sbuf):
    self.def_hand_called += 1
    print(summary)
    self.rmr_free(sbuf)


def steering_req_handler(self, summary, sbuf):
    self.traffic_steering_requests += 1
    print(summary)
    self.rmr_free(sbuf)


# obv some of these flags have to change
rmr_xapp = RMRXapp(default_handler, post_init=post_init, rmr_port=4562, use_fake_sdl=True)
rmr_xapp.register_callback(steering_req_handler, 60000)  # no idea (yet) what the real int is here


def start(thread=False):
    rmr_xapp.run(thread)


def stop():
    """can only be called if thread=True when started"""
    rmr_xapp.stop()


def get_stats():
    # hacky for now, will evolve
    return {"DefCalled": rmr_xapp.def_hand_called, "SteeringRequests": rmr_xapp.traffic_steering_requests}
