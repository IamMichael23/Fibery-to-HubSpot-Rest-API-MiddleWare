"""Simple functions to manage HubSpot contacts."""

from hubspot_api_client import get_hubspot, post_hubspot, patch_hubspot, delete_hubspot


def get_all_contacts(limit=100):
    """Gets all contacts from HubSpot (max 100)."""
    result = get_hubspot('/crm/v3/objects/contacts', params={'limit': limit})
    contacts = result.get('results', [])
    return contacts


def get_contact(contact_id):
    """Gets a single contact by ID."""
    result = get_hubspot(f'/crm/v3/objects/contacts/{contact_id}')
    return result


def create_contact(email, firstname, lastname, phone=None, company=None):
    """Creates a new contact in HubSpot."""
    properties = {
        "email": email,
        "firstname": firstname,
        "lastname": lastname
    }

    if phone:
        properties["phone"] = phone
    if company:
        properties["company"] = company

    data = {"properties": properties}
    result = post_hubspot('/crm/v3/objects/contacts', data)
    return result


def update_contact(contact_id, **properties):
    """Updates an existing contact in HubSpot."""
    data = {"properties": properties}
    result = patch_hubspot(f'/crm/v3/objects/contacts/{contact_id}', data)
    return result


def delete_contact(contact_id):
    """Deletes a contact from HubSpot."""
    result = delete_hubspot(f'/crm/v3/objects/contacts/{contact_id}')
    return result


def test_connection():
    """Tests the connection to HubSpot API."""
    get_hubspot('/crm/v3/objects/contacts', params={'limit': 1})
    return "Connected - HubSpot API is working!"
