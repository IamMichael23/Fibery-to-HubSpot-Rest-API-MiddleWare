"""Fibery API client with token authentication."""

from api_client import make_get_request, make_post_request, make_patch_request, make_delete_request
from config import FIBERY_API_KEY, FIBERY_WORKSPACE


def get_fibery_headers():
    """Returns headers for Fibery API requests with token authentication."""
    return {
        "Authorization": f"Token {FIBERY_API_KEY}",
        "Content-Type": "application/json"
    }


def get_base_url():
    """Returns the base URL for Fibery API."""
    return f"https://{FIBERY_WORKSPACE}/api"


def fibery_command(command, args=None):
    """Executes a Fibery API command. Fibery uses command-based API architecture."""
    url = f"{get_base_url()}/commands"
    headers = get_fibery_headers()

    data = [{
        "command": command,
        "args": args or {}
    }]

    result = make_post_request(url, headers, data)

    if isinstance(result, list) and len(result) > 0:
        return result[0]
    return result


def get_fibery_schema():
    """Gets the Fibery workspace schema (all types/databases)."""
    return fibery_command("fibery.schema/query")


def query_entities(entity_type, fields=None, limit=100):
    """Queries entities from a Fibery database."""
    if fields is None:
        fields = ["fibery/id", "fibery/public-id"]
    else:
        if "fibery/id" not in fields:
            fields.insert(0, "fibery/id")
        if "fibery/public-id" not in fields:
            fields.insert(1, "fibery/public-id")

    query = {
        "q/from": entity_type,
        "q/select": fields,
        "q/limit": limit
    }

    result = fibery_command("fibery.entity/query", {"query": query})

    if "result" in result:
        return result["result"]
    return result


def create_entity(entity_type, fields):
    """Creates a new entity in Fibery."""
    entity_data = {
        "type": entity_type,
        "entity": fields
    }

    return fibery_command("fibery.entity/create", entity_data)


def update_entity(entity_type, entity_id, fields):
    """Updates an existing entity in Fibery."""
    entity_data = {
        "type": entity_type,
        "entity": {
            "fibery/id": entity_id,
            **fields
        }
    }

    return fibery_command("fibery.entity/update", entity_data)


def delete_entity(entity_type, entity_id):
    """Deletes an entity from Fibery."""
    entity_data = {
        "type": entity_type,
        "entity": {
            "fibery/id": entity_id
        }
    }

    return fibery_command("fibery.entity/delete", entity_data)


def test_connection():
    """Tests the connection to Fibery API."""
    get_fibery_schema()
    return "Connected - Fibery API is working!"
