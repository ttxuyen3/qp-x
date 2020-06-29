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
import pytest


@pytest.fixture
def ue_metrics():
    return {
        "UEID": "12345",
        "ServingCellID": "310-680-200-555002",
        "MeasTimestampUEPDCPBytes": "2020-03-18 02:23:18.220",
        "MeasPeriodUEPDCPBytes": 20,
        "UEPDCPBytesDL": 250000,
        "UEPDCPBytesUL": 100000,
        "MeasTimestampUEPRBUsage": "2020-03-18 02:23:18.220",
        "MeasPeriodUEPRBUsage": 20,
        "UEPRBUsageDL": 10,
        "UEPRBUsageUL": 30,
        "MeasTimestampRF": "2020-03-18 02:23:18.210",
        "MeasPeriodRF": 40,
        "ServingCellRF": {"RSRP": -115, "RSRQ": -16, "RSSINR": -5},
        "NeighborCellRF": [
            {"CID": "310-680-200-555001", "CellRF": {"RSRP": -90, "RSRQ": -13, "RSSINR": -2.5}},
            {"CID": "310-680-200-555003", "CellRF": {"RSRP": -140, "RSRQ": -17, "RSSINR": -6}},
        ],
        "FAKE_BAD_DATA_TEST": "THIS SHOULD GET DELETED",
    }


@pytest.fixture
def ue_metrics_with_bad_cell():
    return {
        "UEID": "8675309",
        "ServingCellID": "310-680-200-555002",
        "MeasTimestampUEPDCPBytes": "2020-03-18 02:23:18.220",
        "MeasPeriodUEPDCPBytes": 20,
        "UEPDCPBytesDL": 250000,
        "UEPDCPBytesUL": 100000,
        "MeasTimestampUEPRBUsage": "2020-03-18 02:23:18.220",
        "MeasPeriodUEPRBUsage": 20,
        "UEPRBUsageDL": 10,
        "UEPRBUsageUL": 30,
        "MeasTimestampRF": "2020-03-18 02:23:18.210",
        "MeasPeriodRF": 40,
        "ServingCellRF": {"RSRP": -115, "RSRQ": -16, "RSSINR": -5},
        "NeighborCellRF": [
            {"CID": "310-680-200-555001", "CellRF": {"RSRP": -90, "RSRQ": -13, "RSSINR": -2.5}},
            {"CID": "CANTTOUCHTHIS", "CellRF": {"RSRP": -140, "RSRQ": -17, "RSSINR": -6}},
        ],
    }


@pytest.fixture
def cell_metrics_1():
    return {
        "CellID": "310-680-200-555001",
        "MeasTimestampPDCPBytes": "2020-03-18 02:23:18.220",
        "MeasPeriodPDCPBytes": 20,
        "PDCPBytesDL": 2000000,
        "PDCPBytesUL": 1200000,
        "MeasTimestampAvailPRB": "2020-03-18 02:23:18.220",
        "MeasPeriodAvailPRB": 20,
        "AvailPRBDL": 30,
        "AvailPRBUL": 50,
    }


@pytest.fixture
def cell_metrics_2():
    return {
        "CellID": "310-680-200-555002",
        "MeasTimestampPDCPBytes": "2020-03-18 02:23:18.220",
        "MeasPeriodPDCPBytes": 20,
        "PDCPBytesDL": 800000,
        "PDCPBytesUL": 400000,
        "MeasTimestampAvailPRB": "2020-03-18 02:23:18.220",
        "MeasPeriodAvailPRB": 20,
        "AvailPRBDL": 30,
        "AvailPRBUL": 45,
        "FAKE_BAD_DATA_TEST": "THIS SHOULD GET DELETED",
    }


@pytest.fixture
def cell_metrics_3():
    return {
        "CellID": "310-680-200-555003",
        "MeasTimestampPDCPBytes": "2020-03-18 02:23:18.220",
        "MeasPeriodPDCPBytes": 20,
        "PDCPBytesDL": 1900000,
        "PDCPBytesUL": 1000000,
        "MeasTimestampAvailPRB": "2020-03-18 02:23:18.220",
        "MeasPeriodAvailPRB": 20,
        "AvailPRBDL": 60,
        "AvailPRBUL": 80,
    }


@pytest.fixture
def qpd_to_qp():
    return {
        "PredictionUE": "12345",
        "UEMeasurements": {
            "ServingCellID": "310-680-200-555002",
            "MeasTimestampUEPDCPBytes": "2020-03-18 02:23:18.220",
            "MeasPeriodUEPDCPBytes": 20,
            "UEPDCPBytesDL": 250000,
            "UEPDCPBytesUL": 100000,
            "MeasTimestampUEPRBUsage": "2020-03-18 02:23:18.220",
            "MeasPeriodUEPRBUsage": 20,
            "UEPRBUsageDL": 10,
            "UEPRBUsageUL": 30,
        },
        "CellMeasurements": [
            {
                "CellID": "310-680-200-555001",
                "MeasTimestampPDCPBytes": "2020-03-18 02:23:18.220",
                "MeasPeriodPDCPBytes": 20,
                "PDCPBytesDL": 2000000,
                "PDCPBytesUL": 1200000,
                "MeasTimestampAvailPRB": "2020-03-18 02:23:18.220",
                "MeasPeriodAvailPRB": 20,
                "AvailPRBDL": 30,
                "AvailPRBUL": 50,
                "MeasTimestampRF": "2020-03-18 02:23:18.210",
                "MeasPeriodRF": 40,
                "RFMeasurements": {"RSRP": -90, "RSRQ": -13, "RSSINR": -2.5},
            },
            {
                "CellID": "310-680-200-555003",
                "MeasTimestampPDCPBytes": "2020-03-18 02:23:18.220",
                "MeasPeriodPDCPBytes": 20,
                "PDCPBytesDL": 1900000,
                "PDCPBytesUL": 1000000,
                "MeasTimestampAvailPRB": "2020-03-18 02:23:18.220",
                "MeasPeriodAvailPRB": 20,
                "AvailPRBDL": 60,
                "AvailPRBUL": 80,
                "MeasTimestampRF": "2020-03-18 02:23:18.210",
                "MeasPeriodRF": 40,
                "RFMeasurements": {"RSRP": -140, "RSRQ": -17, "RSSINR": -6},
            },
            {
                "CellID": "310-680-200-555002",
                "MeasTimestampPDCPBytes": "2020-03-18 02:23:18.220",
                "MeasPeriodPDCPBytes": 20,
                "PDCPBytesDL": 800000,
                "PDCPBytesUL": 400000,
                "MeasTimestampAvailPRB": "2020-03-18 02:23:18.220",
                "MeasPeriodAvailPRB": 20,
                "AvailPRBDL": 30,
                "AvailPRBUL": 45,
                "MeasTimestampRF": "2020-03-18 02:23:18.210",
                "MeasPeriodRF": 40,
                "RFMeasurements": {"RSRP": -115, "RSRQ": -16, "RSSINR": -5},
            },
        ],
    }


@pytest.fixture
def qpd_to_qp_bad_cell():
    return {
        "PredictionUE": "8675309",
        "UEMeasurements": {
            "ServingCellID": "310-680-200-555002",
            "MeasTimestampUEPDCPBytes": "2020-03-18 02:23:18.220",
            "MeasPeriodUEPDCPBytes": 20,
            "UEPDCPBytesDL": 250000,
            "UEPDCPBytesUL": 100000,
            "MeasTimestampUEPRBUsage": "2020-03-18 02:23:18.220",
            "MeasPeriodUEPRBUsage": 20,
            "UEPRBUsageDL": 10,
            "UEPRBUsageUL": 30,
        },
        "CellMeasurements": [
            {
                "CellID": "310-680-200-555001",
                "MeasTimestampPDCPBytes": "2020-03-18 02:23:18.220",
                "MeasPeriodPDCPBytes": 20,
                "PDCPBytesDL": 2000000,
                "PDCPBytesUL": 1200000,
                "MeasTimestampAvailPRB": "2020-03-18 02:23:18.220",
                "MeasPeriodAvailPRB": 20,
                "AvailPRBDL": 30,
                "AvailPRBUL": 50,
                "MeasTimestampRF": "2020-03-18 02:23:18.210",
                "MeasPeriodRF": 40,
                "RFMeasurements": {"RSRP": -90, "RSRQ": -13, "RSSINR": -2.5},
            },
            {
                "CellID": "310-680-200-555002",
                "MeasTimestampPDCPBytes": "2020-03-18 02:23:18.220",
                "MeasPeriodPDCPBytes": 20,
                "PDCPBytesDL": 800000,
                "PDCPBytesUL": 400000,
                "MeasTimestampAvailPRB": "2020-03-18 02:23:18.220",
                "MeasPeriodAvailPRB": 20,
                "AvailPRBDL": 30,
                "AvailPRBUL": 45,
                "MeasTimestampRF": "2020-03-18 02:23:18.210",
                "MeasPeriodRF": 40,
                "RFMeasurements": {"RSRP": -115, "RSRQ": -16, "RSSINR": -5},
            },
        ],
    }
