#!/usr/bin/env python
# * coding: utf8 *
"""
test_checks.py
A module that contains tests for the checks module.
"""

import json
from collections import namedtuple
from os import environ
from pathlib import Path

import psycopg2
import pytest
from conductor.checks import (
    ArcGisOnlineChecker,
    GSheetChecker,
    MetaTableChecker,
    MSSqlTableChecker,
    OpenDataChecker,
    PGSqlTableChecker,
    TableChecker,
)
from pygsheets import Cell

secret_path = Path(__file__).parent.parent / "src" / "conductor" / "secrets" / "db" / "connections"

if "CI" in environ:
    secret_path = Path.cwd() / "secrets" / "db" / "connections"

SECRETS = json.loads(secret_path.read_text(encoding="utf-8"))
CONNECTION_STRING = ""


def test_imports():
    assert True


def test_checker_raises_for_table_without_schema():
    with pytest.raises(ValueError):
        table = "city"
        TableChecker(table, CONNECTION_STRING)


def test_checker_parses_table_with_schema():
    table = "location.city"
    patient = TableChecker(table, CONNECTION_STRING)

    assert patient.table == "city"
    assert patient.schema == "location"


def test_checker_parses_table_with_schema_and_db():
    table = "dbo.location.city"
    patient = TableChecker(table, CONNECTION_STRING)

    assert patient.table == "city"
    assert patient.schema == "location"


def test_checker_raises_with_too_many_parts():
    table = "some.very.long.table.name"

    with pytest.raises(ValueError):
        TableChecker(table, CONNECTION_STRING)


def test_checker_raises_with_empty_connection_string():
    with pytest.raises(ValueError):
        TableChecker("schema.table", "").connect()


def test_checker_raises_with_no_connection_string():
    with pytest.raises(ValueError):
        TableChecker("schema.table", None).connect()


def test_open_sgid_can_connect():
    patient = PGSqlTableChecker("boundaries.municipal_boundaries", SECRETS["opensgid"])

    cursor = patient.connect()

    assert cursor.connection.status == psycopg2.extensions.STATUS_READY

    cursor.close()
    patient.connection.close()


def test_pgsql_postgresize():
    assert PGSqlTableChecker.postgresize("Utah County Boundaries") == "county_boundaries"
    assert PGSqlTableChecker.postgresize("") == ""


@pytest.mark.vpn
def test_mssql_table_can_connect():
    patient = MSSqlTableChecker("boundaries.municipalities", SECRETS["sgid10"])

    cursor = patient.connect()

    assert cursor is not None


def test_pgsql_table_exists_returns_true():
    patient = PGSqlTableChecker("boundaries.municipal_boundaries", SECRETS["opensgid"])

    assert patient.exists() is True

    patient.connection.close()


@pytest.mark.vpn
def test_mssql_table_exists_returns_true():
    patient = MSSqlTableChecker("boundaries.municipalities", SECRETS["sgid10"])

    assert patient.exists() is True

    patient.connection.close()


def test_pgsql_table_does_not_exist_returns_false():
    patient = PGSqlTableChecker("fake.table", SECRETS["opensgid"])

    assert patient.exists() is False

    patient.connection.close()


@pytest.mark.vpn
def test_mssql_table_does_not_exist_returns_false():
    patient = MSSqlTableChecker("fake.table", SECRETS["sgid10"])

    assert patient.exists() is False

    patient.connection.close()


@pytest.mark.vpn
def test_metatable_response_returns_true_when_exists():
    patient = MetaTableChecker("sgid.boundaries.municipalities", SECRETS["internalsgid"])
    response = patient.exists()

    assert response.exists is True
    assert patient.data.item_id == "543fa1f073714198a3dbf8a292bdf30c"
    assert patient.data.item_name == "Utah Municipal Boundaries"


@pytest.mark.vpn
def test_response_returns_completely_missing_for_fake_table():
    patient = MetaTableChecker("sgid.fake.table", SECRETS["internalsgid"])
    response = patient.exists()

    assert response.exists is False


def test_empty_row_returns_false(mocker):
    mocker.patch("conductor.checks.TableChecker.get_data")

    patient = MetaTableChecker("sgid.fake.table", SECRETS["internalsgid"])
    response = patient.exists()

    assert response.exists is False


def test_missing_item_id_returns_correct_string(mocker):
    mocker.patch("conductor.checks.TableChecker.get_data")

    patient = MetaTableChecker("sgid.fake.table", SECRETS["internalsgid"])
    patient.data = (None, "Agol Published Name", "geometry type")

    response = patient.exists()

    assert response.exists == "missing item id"


def test_missing_item_name_returns_correct_string(mocker):
    mocker.patch("conductor.checks.TableChecker.get_data")

    patient = MetaTableChecker("sgid.fake.table", SECRETS["internalsgid"])
    patient.data = ("some-guid", None, "geometry type")

    response = patient.exists()

    assert response.exists == "missing item name"


def test_missing_geometry_type_returns_correct_string(mocker):
    mocker.patch("conductor.checks.TableChecker.get_data")

    patient = MetaTableChecker("sgid.fake.table", SECRETS["internalsgid"])
    patient.data = ("some-guid", "agol name", None)

    response = patient.exists()

    assert response.exists == "missing geometry type"


def test_missing_all_returns_correct_string(mocker):
    mocker.patch("conductor.checks.TableChecker.get_data")
    patient = MetaTableChecker("sgid.fake.table", SECRETS["internalsgid"])
    patient.data = (None, None, None)

    response = patient.exists()

    assert response.exists is False


def test_arcgis_online_url_creation():
    patient = ArcGisOnlineChecker("item_id")

    assert patient.url == "https://www.arcgis.com/sharing/rest/content/items/item_id"


def test_arcgis_online_exists_when_json_contains_owner(mocker):
    mocker.patch("conductor.checks.UrlChecker.get_data")
    patient = ArcGisOnlineChecker("item_id")
    patient.data = mocker.Mock(
        **{
            "json.return_value": {
                "id": "3080c0a2859a4d23a279e17e17c703c8",
                "owner": "UtahAGRC",
                "orgId": "123",
                "created": 1593230216000,
                "modified": 1594153455000,
                "guid": None,
                "name": "TrailsAndPathways",
                "title": "Utah Trails and Pathways",
                "type": "Feature Service",
            }
        }
    )

    assert patient.exists() is True


def test_arcgis_online_does_not_exist(mocker):
    mocker.patch("conductor.checks.ArcGisOnlineChecker.get_data")
    patient = ArcGisOnlineChecker("item_id")
    patient.data = mocker.Mock(
        **{
            "json.return_value": {
                "error": {
                    "code": 400,
                    "messageCode": "CONT_0001",
                    "message": "Item does not exist or is inaccessible.",
                    "details": [],
                }
            }
        }
    )

    assert patient.exists() is False


def test_open_data_url_creation():
    patient = OpenDataChecker("UPPER CASED Name")

    assert patient.url == "https://opendata.gis.utah.gov/datasets/upper-cased-name"


def test_open_data_raises_for_empty_url():
    with pytest.raises(ValueError):
        OpenDataChecker(None)


def test_open_data_for_existence_with_200(mocker):
    mocker.patch("conductor.checks.UrlChecker.get_data")

    patient = OpenDataChecker("found layer name")
    patient.data = mocker.Mock()
    patient.data.status_code = 200

    assert patient.exists() is True


def test_open_data_for_missing_with_301(mocker):
    mocker.patch("conductor.checks.UrlChecker.get_data")

    patient = OpenDataChecker("missing layer name")
    patient.data = mocker.Mock()
    patient.data.status_code = 301

    assert patient.exists() is False


header_row = [
    "id",
    "indexStatus",
    "displayName",
    "description",
    "justification",
    "category",
    "categorySecondary",
    "productType",
    "refreshCycle",
    "storageType",
    "tableName",
    "productPage",
    "inActionUrl",
    "ugrcSteward",
    "hostedBy",
    "hostContactName",
    "hostContactEmail",
    "dataSource",
    "dataContactEmail",
    "dataContactName",
    "itemId",
    "hubName",
    "hubOrganization",
    "serverHost",
    "serverServiceName",
    "serverLayerId",
    "arcGisOnline",
    "openSgid",
    "openSgidTableName",
    "confidenceRating",
    "porterUrl",
]


def test_sheets_build_header_row_index():
    patient = GSheetChecker("fake.table", "sheet_id", "worksheet_name", "TESTING")

    patient.required_fields = [
        "displayName",
        "productPage",
        "porterUrl",
    ]  #: shorten the list to make the testing simpler
    patient.build_header_row_index(header_row)

    assert patient.field_index == {"displayName": 2, "productPage": 11, "porterUrl": 30}


def test_sheets_with_duplicate_cells_returns_false(mocker):
    patient = GSheetChecker("fake.table", "sheet_id", "worksheet_name", "TESTING")
    mocker.patch("pygsheets.Cell.link")
    patient._get_data = mocker.Mock(return_value=[Cell("A1", val="fake.table"), Cell("A2", val="fake.table")])

    response = patient.exists()

    assert response.valid is False
    assert response.messages == "There are multiple items with this name on rows 1, 2. Please remove the duplicates."


def test_sheets_with_no_matches_returns_false(mocker):
    patient = GSheetChecker("fake.table", "sheet_id", "worksheet_name", "TESTING")
    patient._get_data = mocker.Mock(return_value=[])

    response = patient.exists()

    assert response.valid is False
    assert response.messages == "Did not find fake.table in the worksheet"


def test_sheets_returns_false_for_empty_values(mocker):
    patient = GSheetChecker("fake.table", "sheet_id", "worksheet_name", "TESTING")
    patient.build_header_row_index(header_row)
    patient._get_data = mocker.Mock(return_value=[Cell("A1", "table")])
    mocker.patch("pygsheets.Cell.link")
    mocker.patch("pygsheets.Cell.neighbour", return_value=Cell("A2"))

    response = patient.exists()

    assert response.valid is True
    assert response.messages == {
        "displayName": False,
        "description": False,
        "justification": False,
        "category": False,
        "productType": False,
        "ugrcSteward": False,
        "dataContactEmail": False,
        "dataContactName": False,
        "porterUrl": False,
        "productPage": False,
        "itemId": False,
    }


def test_sheets_requires_product_page_or_item_id(mocker):
    patient = GSheetChecker("fake.table", "sheet_id", "worksheet_name", "TESTING")
    patient.build_header_row_index(header_row)
    patient._get_data = mocker.Mock(return_value=[Cell("A1", "table")])
    mocker.patch("pygsheets.Cell.link")
    mocker.patch("pygsheets.Cell.neighbour", return_value=Cell("A2"))

    response = patient.exists()

    assert response.valid is True
    assert response.messages["productPage"] is False
    assert response.messages["itemId"] is False


def test_sheets_handles_partial_values(mocker):
    patient = GSheetChecker("fake.table", "sheet_id", "worksheet_name", "TESTING")
    patient.build_header_row_index(header_row)
    patient._get_data = mocker.Mock(return_value=[Cell("A1", "fake.table")])
    mocker.patch("pygsheets.Cell.link")
    mocker.patch(
        "pygsheets.Cell.neighbour",
        side_effect=[
            Cell("A2", val="not empty"),
            Cell("A3", val=" "),
            Cell("A4", val="not empty"),
            Cell("A5", val="   "),
            Cell("A6", val=" true "),
            Cell("A7", val=" "),
            Cell("A8", val=" "),
            Cell("A9", val=" "),
            Cell("A10", val=" "),
            Cell("A11", val=" "),
            Cell("A12", val=" "),
        ],
    )

    response = patient.exists()

    assert response.valid is True
    assert response.messages == {
        "displayName": True,
        "description": False,
        "justification": True,
        "category": False,
        "productType": True,
        "ugrcSteward": False,
        "dataContactEmail": False,
        "dataContactName": False,
        "porterUrl": False,
        "productPage": False,
        "itemId": False,
    }


def test_sheets_returns_true_if_neighbors_all_have_values(mocker):
    patient = GSheetChecker("fake.table", "sheet_id", "worksheet_name", "TESTING")
    patient.build_header_row_index(header_row)
    patient._get_data = mocker.Mock(return_value=[Cell("A1", "fake.table")])
    mocker.patch("pygsheets.Cell.link")
    mocker.patch(
        "pygsheets.Cell.neighbour",
        side_effect=[
            Cell("A2", val="not empty"),
            Cell("A3", val="also not empty"),
            Cell("A4", val="also not empty"),
            Cell("A5", val="also not empty"),
            Cell("A6", val="also not empty"),
            Cell("A7", val="also not empty"),
            Cell("A8", val="also not empty"),
            Cell("A9", val="also not empty"),
            Cell("A10", val="also not empty"),
            Cell("A11", val="also not empty"),
            Cell("A12", val="also not empty"),
            Cell("A13", val="also not empty"),
        ],
    )

    response = patient.exists()

    assert response.valid is True
    assert response.messages == {
        "displayName": True,
        "description": True,
        "justification": True,
        "category": True,
        "productType": True,
        "ugrcSteward": True,
        "dataContactEmail": True,
        "dataContactName": True,
        "porterUrl": True,
    }


@pytest.mark.google
def test_sheets_can_find_workspace():
    patient = GSheetChecker(
        "fake.table",
        "11ASS7LnxgpnD0jN4utzklREgMf1pcvYjcXcIcESHweQ",
        "SGID Stewardship Info",
        SECRETS["sheets-sa"],
    )

    assert len(patient._get_data()) == 0


@pytest.mark.google
def test_sheets_can_find_known_record_in_workspace():
    patient = GSheetChecker(
        "basemap.addresspoints",
        "11ASS7LnxgpnD0jN4utzklREgMf1pcvYjcXcIcESHweQ",
        "SGID Stewardship Info",
        SECRETS["sheets-sa"],
    )

    assert len(patient._get_data()) == 1


@pytest.mark.google
def test_sheets_exists_returns_true_for_known_layer():
    patient = GSheetChecker(
        "boundaries.counties",
        "11ASS7LnxgpnD0jN4utzklREgMf1pcvYjcXcIcESHweQ",
        "SGID Stewardship Info",
        SECRETS["sheets-sa"],
    )

    response = patient.exists()

    assert response.valid is True
    assert response.messages == {
        "displayName": True,
        "description": True,
        "justification": True,
        "category": True,
        "productType": True,
        "ugrcSteward": True,
        "dataContactEmail": True,
        "dataContactName": True,
        "porterUrl": True,
        "productPage": True,
        "itemId": True,
    }


def test_sheet_grade_returns_false_for_no_row_for_add():
    SheetResponse = namedtuple("SheetResponse", "valid messages")
    grade = GSheetChecker("fake.table", "id", "name", "TESTING").grade(
        add=True,
        report_value=SheetResponse(False, "Did not find fake.table in the worksheet"),
    )

    assert grade == ":no_entry: Did not find fake.table in the worksheet"


def test_sheet_grade_returns_false_for_multiple_row_for_add():
    SheetResponse = namedtuple("SheetResponse", "valid messages")
    grade = GSheetChecker("fake.table", "id", "name", "TESTING").grade(
        add=True,
        report_value=SheetResponse(
            False,
            "There are multiple items with this name on rows 1,2. Please remove the duplicates.",
        ),
    )

    assert grade == ":no_entry: There are multiple items with this name on rows 1,2. Please remove the duplicates."


def test_sheet_grade_returns_false_for_missing_field_for_add():
    SheetResponse = namedtuple("SheetResponse", "valid messages")
    grades = {
        "displayName": False,
        "description": True,
    }
    grade = GSheetChecker("fake.table", "id", "name", "TESTING").grade(
        add=True, report_value=SheetResponse(True, grades)
    )

    assert grade == " |\n| - displayName | :no_entry: |\n| - description | :+1:"


def test_sheet_grade_returns_true_for_deprecation_field_for_remove():
    SheetResponse = namedtuple("SheetResponse", "valid messages")
    grades = {
        "displayName": False,
        "description": True,
        "porterUrl": True,
    }
    grade = GSheetChecker("fake.table", "id", "name", "TESTING").grade(
        add=False, report_value=SheetResponse(True, grades)
    )

    assert grade == " |\n| - porter issue link | :+1:"


def test_sheet_grade_returns_false_for_deprecation_field_for_remove():
    SheetResponse = namedtuple("SheetResponse", "valid messages")
    grades = {
        "displayName": False,
        "description": True,
        "porterUrl": False,
    }
    grade = GSheetChecker("fake.table", "id", "name", "TESTING").grade(
        add=False, report_value=SheetResponse(True, grades)
    )

    assert grade == " |\n| - porter issue link | :no_entry:"
    grade = GSheetChecker("fake.table", "id", "name", "TESTING").grade(
        add=False, report_value=SheetResponse(True, grades)
    )

    assert grade == " |\n| - porter issue link | :no_entry:"
