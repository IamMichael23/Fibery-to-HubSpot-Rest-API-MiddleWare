"""HubSpot-specific API client with OAuth 2.0 token management."""

import requests
from config import HUBSPOT_ACCESS_TOKEN, HUBSPOT_CLIENT_ID, HUBSPOT_CLIENT_SECRET, HUBSPOT_REFRESH_TOKEN
from api_client import make_get_request, make_post_request, make_patch_request, make_delete_request

HUBSPOT_API_BASE = "https://api.hubapi.com"


def get_access_token():
    """Returns the current HubSpot access token from config."""
    return HUBSPOT_ACCESS_TOKEN


def refresh_token():
    """Refreshes the HubSpot OAuth token."""
    response = requests.post(
        f"{HUBSPOT_API_BASE}/oauth/v1/token",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data={
            "grant_type": "refresh_token",
            "client_id": HUBSPOT_CLIENT_ID,
            "client_secret": HUBSPOT_CLIENT_SECRET,
            "refresh_token": HUBSPOT_REFRESH_TOKEN
        },
        timeout=10
    )
    token_data = response.json()
    print("✓ Token refreshed successfully!")
    print(f"\nNew Access Token: {token_data['access_token']}")
    print(f"New Refresh Token: {token_data['refresh_token']}")
    print("\nUpdate config.py with the new HUBSPOT_ACCESS_TOKEN")
    return token_data


def make_hubspot_request(method, endpoint, data=None, params=None):
    """Makes authenticated request to HubSpot API."""
    url = f"{HUBSPOT_API_BASE}{endpoint}"
    headers = {
        "Authorization": f"Bearer {get_access_token()}",
        "Content-Type": "application/json"
    }

    if method.upper() == 'GET':
        return make_get_request(url, headers, params)
    elif method.upper() == 'POST':
        return make_post_request(url, headers, data)
    elif method.upper() == 'PATCH':
        return make_patch_request(url, headers, data)
    elif method.upper() == 'DELETE':
        return make_delete_request(url, headers)


def get_hubspot(endpoint, params=None):
    """Makes GET request to HubSpot."""
    return make_hubspot_request('GET', endpoint, params=params)


def post_hubspot(endpoint, data):
    """Makes POST request to HubSpot."""
    return make_hubspot_request('POST', endpoint, data=data)


def patch_hubspot(endpoint, data):
    """Makes PATCH request to HubSpot to update resources."""
    return make_hubspot_request('PATCH', endpoint, data=data)


def delete_hubspot(endpoint):
    """Makes DELETE request to HubSpot to remove resources."""
    return make_hubspot_request('DELETE', endpoint)
