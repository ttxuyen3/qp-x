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
from qpdriver import data


def test_merge(monkeypatch, ue_metrics, cell_metrics_1, cell_metrics_2, cell_metrics_3, qpd_to_qp):

    # monkeypatch
    def fake_ue(ueid):
        if ueid == 12345:
            return ue_metrics

    def fake_cell(cellid):
        if cellid == "310-680-200-555001":
            return cell_metrics_1
        if cellid == "310-680-200-555002":
            return cell_metrics_2
        if cellid == "310-680-200-555003":
            return cell_metrics_3

    monkeypatch.setattr("qpdriver.data._fetch_ue_metrics", fake_ue)
    monkeypatch.setattr("qpdriver.data._fetch_cell_metrics", fake_cell)

    assert data.form_qp_pred_req(12345) == qpd_to_qp
