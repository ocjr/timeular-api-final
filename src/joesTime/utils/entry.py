from typing import Dict, List
import requests
import json
import datetime as dt
import pytz
import logging

logger = logging.getLogger(__name__)


def get_entry_by_id(id: str, token: str) -> Dict[str, any]:
    """
    Retrieves a time entry from the Timeular API by its ID.

    Args:
        id (str): The ID of the time entry to retrieve.
        token (str): An access token for the Timeular API.

    Returns:
        dict: A dictionary containing information about the time entry.

    Raises:
        requests.exceptions.RequestException: If an error occurs while making the request to the API.

    """
    # url for get entry by id
    url = f"https://api.timeular.com/api/v3/time-entries/{id}"

    # build headers
    headers = {"Authorization": "Bearer " + token}

    try:
        # make request
        response = requests.get(url, headers=headers)

        response.raise_for_status() # raise an exception for any unsuccessful response codes
    except requests.exceptions.RequestException as e:
        logger.exception(f"An error occurred while making the request to {url}: {e}")
        raise

    data = response.json()

    logger.info(f"Retrieved time entry with ID '{id}'")

    return data


def get_entry_by_timestamp(
    start_timestamp: dt.datetime,
    end_timestamp: dt.datetime,
    token=str,
    timezone: str = "America/Chicago",
) -> List[Dict[str, any]]:
    """
    Retrieves time entries between two timestamps in the specified timezone.
    
    Parameters:
        start_timestamp (datetime): The start timestamp for the time entries.
        end_timestamp (datetime): The end timestamp for the time entries.
        token (str): The user's Timeular API token.
        timezone (str): The timezone to use for the timestamps. Defaults to "America/Chicago".
    
    Returns:
        List[Dict[str, any]]: A list of time entries between the two timestamps.
    """
    logger.info("Retrieving time entries between %s and %s in timezone %s", start_timestamp, end_timestamp, timezone)
    # url for get entry by id
    url = entry_by_timestamp_url_constructer(
        start_time=start_timestamp, end_time=end_timestamp, timezone=timezone
    )

    # build headers
    headers = {"Authorization": "Bearer " + token}

    try:
        # make request
        response = requests.get(url, headers=headers)

        response.raise_for_status() # raise an exception for any unsuccessful response codes
    except requests.exceptions.RequestException as e:
        logger.exception(f"An error occurred while making the request to {url}: {e}")
        raise

    data = response.json()

    logger.info("Retrieved %d time entries", len(data))

    return data


def entry_by_timestamp_url_constructer(
    start_time: dt.datetime, end_time: dt.datetime, timezone: str = "America/Chicago"
) -> str:
    """
    Construct the URL for getting entries by timestamp for a specified timezone.

    Args:
        start_time (datetime.datetime): Start time for the entries in the specified timezone.
        end_time (datetime.datetime): End time for the entries in the specified timezone.
        timezone (str, optional): Timezone to use for the start and end times. Defaults to "America/Chicago".

    Returns:
        str: URL for getting entries by timestamp.

    """
    # set local timezone and UTC
    local_tz = pytz.timezone(timezone)  # Replace with your local timezone
    utc_tz = pytz.timezone("UTC")

    # build url format
    url_format = "https://api.timeular.com/api/v3/time-entries/{}/{}"

    # Attach timezone to the times
    start_time_local = local_tz.localize(start_time, is_dst=None)
    end_time_local = local_tz.localize(end_time, is_dst=None)

    # convert to UTC
    start_time_utc = start_time_local.astimezone(utc_tz)
    end_time_utc = end_time_local.astimezone(utc_tz)

    # create strings with right format
    start_time_str = start_time_utc.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
    end_time_str = end_time_utc.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]

    logging.info(f"Constructing URL for entries between {start_time} and {end_time} in timezone {timezone}")

    # return the url in the correct format.
    return url_format.format(start_time_str, end_time_str)
