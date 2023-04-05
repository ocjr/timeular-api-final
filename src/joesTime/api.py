import requests
import json
import getpass
import logging

logger = logging.getLogger(__name__)


def login() -> dict:
    """
    Logs into the Timeular API and returns an access token.

    This function sends a POST request to the Timeular API with the user's API
    key and secret to log in and receive an access token. The access token is
    returned as a dictionary.

    Returns:
        A dictionary containing the access token.
    """
    # url for login
    url = "https://api.timeular.com/api/v3/developer/sign-in"

    # get apiKey
    apiKey = getpass.getpass(prompt="Provide apiKey: ")

    # get apiSecret
    apiSecret = getpass.getpass(prompt="Provide apiSecret: ")

    # Build payload
    payload = json.dumps({"apiKey": apiKey, "apiSecret": apiSecret})

    # Build Headers
    headers = {"Content-Type": "application/json"}

    # log some information about the request
    logger.info("Sending login request to %s", url)
    logger.debug("Payload: %s", payload)
    logger.debug("Headers: %s", headers)

    # make request
    response = requests.request("POST", url, headers=headers, data=payload)

    # log the response status code and text
    logger.info("Received response %s", response)
    if hasattr(response, 'text'): 
        logger.debug("Response text: %s", response.text)

    token = json.loads(response.text)

    return token


def logout(token: str) -> str:
    """
    Logs out of the Timeular API using the provided access token.

    This function sends a POST request to the Timeular API to log out using
    the provided access token. The response text is returned as a string.

    Args:
        token: A string containing the access token.

    Returns:
        A string containing the response text from the logout request.
    """
    logger.info("Logging out of the Timeular API")

    # url for logout
    url = "https://api.timeular.com/api/v3/developer/api-access"

    # Build payload
    payload = ""

    # build headers
    headers = {"Authorization": "Bearer " + token}

    response = requests.request("POST", url, headers=headers, data=payload)

    logger.debug("Logout response: %s", response)

    return response.text
