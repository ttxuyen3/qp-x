"""
qpdriver module responsible for SDL queries and data merging
"""
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

# list of keys in ue metrics that we want to carry over to qp pred
UE_KEY_LIST = set(
    [
        "ServingCellID",
        "MeasTimestampUEPDCPBytes",
        "MeasPeriodUEPDCPBytes",
        "UEPDCPBytesDL",
        "UEPDCPBytesUL",
        "MeasTimestampUEPRBUsage",
        "MeasPeriodUEPRBUsage",
        "UEPRBUsageDL",
        "UEPRBUsageUL",
    ]
)

# list of keys in cell metrics we want to carry
CELL_KEY_LIST = set(
    [
        "CellID",
        "MeasTimestampPDCPBytes",
        "MeasPeriodPDCPBytes",
        "PDCPBytesDL",
        "PDCPBytesUL",
        "MeasTimestampAvailPRB",
        "MeasPeriodAvailPRB",
        "AvailPRBDL",
        "AvailPRBUL",
    ]
)


def _fetch_ue_metrics(ueid):
    """fetch ue metrics for ueid"""
    return {}


def _fetch_cell_metrics(cellid):
    """fetch cell metrics for a cellid"""
    return {}


def form_qp_pred_req(ueid):
    """
    this function takes in a single ueid and:
        - fetches the current ue data
        - for the serving cell id, and for each neighboring cell id, fetches the cell data for those cells
        - returns the message that should be sent to the QP Predictor
    Note that a single request to qp driver may have many UEs in a list, however since a new message needs to be sent for each one,
    the calling function iterates over that list, rather than doing it here.
    """
    ue_data = _fetch_ue_metrics(ueid)

    serving_cid = ue_data["ServingCellID"]

    # a dict is better than a list for what we need to do here
    n_cell_info = {}
    for ncell in ue_data["NeighborCellRF"]:
        n_cell_info[ncell["CID"]] = ncell["CellRF"]

    # form the cell_id list
    # qp prediction team does not have a preference as to order; we deterministically put the serving cell last
    cell_ids = list(n_cell_info.keys())
    cell_ids.append(serving_cid)

    # form the qp req
    qp_pred_req = {"PredictionUE": ueid}  # top level key
    qp_pred_req["UEMeasurements"] = {k: ue_data[k] for k in UE_KEY_LIST}  # take ue keys we want
    qp_pred_req["CellMeasurements"] = []

    # form the CellMeasurements
    for cid in cell_ids:
        cellm = _fetch_cell_metrics(cid)
        # if we were really under performance strain here we could delete from the orig instead of copying but this code is far simpler
        cell_data = {k: cellm[k] for k in CELL_KEY_LIST}

        # these keys get dropped into *each* cell
        cell_data["MeasTimestampRF"] = ue_data["MeasTimestampRF"]
        cell_data["MeasPeriodRF"] = ue_data["MeasPeriodRF"]

        # add the RF
        cell_data["RFMeasurements"] = ue_data["ServingCellRF"] if cid == serving_cid else n_cell_info[cid]

        # add to our array
        qp_pred_req["CellMeasurements"].append(cell_data)

    return qp_pred_req
