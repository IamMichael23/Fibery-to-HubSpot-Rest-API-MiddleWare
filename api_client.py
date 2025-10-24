"""Generic reusable API client for REST APIs."""

import requests


def make_get_request(url, headers, params=None):
    """Makes HTTP GET request."""
    response = requests.get(url, headers=headers, params=params, timeout=10)
    return response.json()


def make_post_request(url, headers, data):
    """Makes HTTP POST request."""
    response = requests.post(url, headers=headers, json=data, timeout=10)
    return response.json()


def make_patch_request(url, headers, data):
    """Makes HTTP PATCH request to update resources."""
    response = requests.patch(url, headers=headers, json=data, timeout=10)
    return response.json()


def make_delete_request(url, headers):
    """Makes HTTP DELETE request to remove resources."""
    requests.delete(url, headers=headers, timeout=10)
    return "Resource deleted successfully"
