import os
import unittest
import pytest
from unittest.mock import patch, Mock
import datetime as dt
from src.joesTime.utils.entry import get_entry_by_id, get_entry_by_timestamp
from src.joesTime.api import login, logout



def test_logout(token):
    # Test that logout function returns 'success'
    assert logout(token) == "success"


class TestAPIFunctions(unittest.TestCase):
    @patch("requests.request")
    @patch("getpass.getpass")
    def test_get_entry_by_id(self, mock_request, mock_getpass):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.text = {"id": "12345", "description": "test entry"}
        mock_request.return_value = mock_response

        mock_getpass.side_effect = [os.environ['MY_APIKEY'], os.environ['MY_APISECRET']]

        # Call the login function to get the token
        token = login()

        # Check that the token is not None
        assert token is not None

        # Call the function with mock data
        data = get_entry_by_id("12345", token["token"])

        # Check that the mock request was called with the correct arguments
        mock_request.assert_called_with(
            "GET",
            "https://api.timeular.com/api/v3/time-entries/12345",
            headers={"Authorization": token["token"]},
            data={},
        )

        # Check that the function returns the expected data
        expected_data = {"id": "12345", "description": "test entry"}
        self.assertEqual(data, expected_data)

        # Call the logout function to invalidate the token
        assert logout(token["token"]) == {"apiKey": os.environ['MY_APIKEY'], "apiSecret":os.environ['MY_APISECRET']}


    @patch("requests.request")
    @patch("getpass.getpass")
    def test_get_entry_by_timestamp(self, mock_request, mock_getpass):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.text = [{"id": "12345", "description": "test entry 1"}, {"id": "67890", "description": "test entry 2"}]
        mock_request.return_value = mock_response

        mock_getpass.side_effect = [os.environ['MY_APIKEY'], os.environ['MY_APISECRET']]

        # Call the login function to get the token
        token = login()

        # Check that the token is not None
        assert token is not None

        # Call the function with mock data
        start_time = dt.datetime(2023, 3, 30, 0, 0, 0)
        end_time = dt.datetime(2023, 3, 31, 0, 0, 0)
        data = get_entry_by_timestamp(
            start_time, end_time, token["token"], "America/New_York"
        )

        # Check that the mock request was called with the correct arguments
        expected_url = "https://api.timeular.com/api/v3/time-entries/2023-03-30T04:00:00.000/2023-03-31T04:00:00.000"
        mock_request.assert_called_with(
            "GET",
            expected_url,
            headers={"Authorization": token["token"]},
            data={},
        )

        # Check that the function returns the expected data
        expected_data = [
            {"id": "12345", "description": "test entry 1"},
            {"id": "67890", "description": "test entry 2"},
        ]
        self.assertEqual(data, expected_data)

        assert logout(token["token"]) == {"apiKey": os.environ['MY_APIKEY'], "apiSecret":os.environ['MY_APISECRET']}
