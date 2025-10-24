"""Discovers and displays all entity types available in your Fibery workspace."""

from fibery_api_client import get_fibery_schema


def discover_types():
    """Discovers and displays all entity types in Fibery workspace."""
    print("\n" + "="*60)
    print("DISCOVERING FIBERY ENTITY TYPES")
    print("="*60)

    result = get_fibery_schema()

    schema = result.get('result', result)

    types = schema['fibery/types']

    system_types = []
    custom_types = []

    for entity_type in types:
        type_name = entity_type.get('fibery/name', 'Unknown')
        type_meta = entity_type.get('fibery/meta', {})

        if type_meta.get('fibery/primitive?', False):
            continue

        if type_meta.get('fibery/platform?', False) or type_name.startswith('fibery/'):
            system_types.append(type_name)
        else:
            custom_types.append({
                'name': type_name,
                'fields': entity_type.get('fibery/fields', [])
            })

    print(f"\n📦 CUSTOM ENTITY TYPES (Can be synced):")
    print("-" * 60)

    if not custom_types:
        print("  No custom types found yet.")
        print("  You may need to create types in Fibery first.")
    else:
        for entity_type in custom_types:
            print(f"\n  🔹 {entity_type['name']}")

            fields = entity_type['fields']
            if fields:
                print(f"     Fields ({len(fields)}):")
                for field in fields[:10]:
                    field_name = field.get('fibery/name', 'Unknown')
                    field_type = field.get('fibery/type', 'Unknown')

                    if not field_name.startswith('fibery/'):
                        print(f"       • {field_name} ({field_type})")

    print(f"\n\n📊 SUMMARY:")
    print(f"  Custom types: {len(custom_types)}")
    print(f"  System types: {len(system_types)}")

    print("\n" + "="*60)
    print("NEXT STEPS:")
    print("="*60)
    print("1. Identify which entity type contains your contacts")
    print("2. Update sync_fibery_to_hubspot.py with the correct type name")
    print("3. Update the field mappings (Name, Email, Phone, etc.)")
    print("4. Run the sync!")

    return custom_types


if __name__ == "__main__":
    discover_types()
