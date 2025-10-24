"""Simple functions to manage Fibery entities."""

from fibery_api_client import (
    get_fibery_schema,
    query_entities,
    create_entity,
    update_entity,
    delete_entity,
    test_connection
)


def get_all_types():
    """Gets all entity types (databases) in Fibery workspace."""
    result = get_fibery_schema()

    if 'fibery/types' in result:
        types = result['fibery/types']
        return types
    return result


def get_entities(entity_type, fields=None, limit=100):
    """Gets entities from a specific Fibery database/type."""
    return query_entities(entity_type, fields, limit)


def get_entity_by_id(entity_type, entity_id):
    """Gets a single entity by its ID."""
    entities = query_entities(entity_type, fields=None, limit=1)

    for entity in entities:
        if entity.get('fibery/id') == entity_id:
            return entity
    return None


def create_fibery_entity(entity_type, **fields):
    """Creates a new entity in Fibery."""
    return create_entity(entity_type, fields)


def update_fibery_entity(entity_type, entity_id, **fields):
    """Updates an existing entity in Fibery."""
    return update_entity(entity_type, entity_id, fields)


def delete_fibery_entity(entity_type, entity_id):
    """Deletes an entity from Fibery."""
    return delete_entity(entity_type, entity_id)


def find_entity_by_field(entity_type, field_name, field_value, fields=None):
    """Finds an entity by a specific field value."""
    entities = get_entities(entity_type, fields, limit=1000)

    for entity in entities:
        if entity.get(field_name) == field_value:
            return entity
    return None
