# HubSpot API - Clean & Simple

## What is an API?
An **API** (Application Programming Interface) is like a waiter at a restaurant:
- You (Python code) tell the waiter (API) what you want
- The waiter goes to the kitchen (HubSpot server)
- The waiter brings back your food (data)

## Project Structure

This project is organized for **reusability** - you can use the same code for HubSpot AND Fibery APIs!

### Core Files:

1. **`config.py`** - All your API credentials (tokens, keys, secrets)
   - HubSpot credentials
   - Fibery credentials (for future use)

2. **`api_client.py`** - Generic API functions
   - Works with ANY REST API
   - Reusable for HubSpot, Fibery, etc.
   - Functions: GET, POST, PATCH, DELETE

3. **`hubspot_api_client.py`** - HubSpot-specific API client
   - Uses `api_client.py` functions
   - Handles HubSpot authentication
   - Token refresh functionality

4. **`hubspot_contacts.py`** - HubSpot contact operations
   - Simple functions you can call
   - Get, create, update, delete contacts
   - Returns: `(success, data_or_error)`

### Helper Files:

- **`get_oauth_token.py`** - First-time OAuth setup (auto-updates config.py)
- **`token.txt`** - Stores your tokens

## Quick Start

### 1. Test Your Connection

```python
from hubspot_contacts import test_connection

success, message = test_connection()
if success:
    print(message)  # "Connected - HubSpot API is working!"
else:
    print(f"Error: {message}")
```

### 2. Get All Contacts (Limited to 100)

```python
from hubspot_contacts import get_all_contacts

success, contacts = get_all_contacts()
if success:
    print(f"Found {len(contacts)} contacts")
    for contact in contacts:
        email = contact['properties'].get('email', 'No email')
        firstname = contact['properties'].get('firstname', 'No name')
        print(f"- {firstname} ({email})")
else:
    print(f"Error: {contacts}")
```

### 3. Get a Single Contact

```python
from hubspot_contacts import get_contact

success, contact = get_contact("162367203291")
if success:
    print(f"Email: {contact['properties']['email']}")
    print(f"Name: {contact['properties']['firstname']} {contact['properties']['lastname']}")
else:
    print(f"Error: {contact}")  # e.g., "Contact not found"
```

### 4. Create a Contact

```python
from hubspot_contacts import create_contact

success, contact = create_contact(
    email="jane.doe@example.com",
    firstname="Jane",
    lastname="Doe",
    phone="+1-555-1234",
    company="ABC Corp"
)

if success:
    print(f"Created contact ID: {contact['id']}")
else:
    print(f"Error: {contact}")  # e.g., "Contact with email 'jane.doe@example.com' already exists"
```

### 5. Update a Contact

```python
from hubspot_contacts import update_contact

success, contact = update_contact(
    "162367203291",
    phone="+1-555-9999",
    company="New Company Name"
)

if success:
    print("Contact updated!")
else:
    print(f"Error: {contact}")  # e.g., "Contact not found"
```

### 6. Delete a Contact

```python
from hubspot_contacts import delete_contact

success, message = delete_contact("162367203291")
if success:
    print(message)  # "Contact deleted (ID: 162367203291)"
else:
    print(f"Error: {message}")  # e.g., "Contact not found"
```

## Token Management

### Token Expired?

If you see: `"Token expired - update HUBSPOT_ACCESS_TOKEN in config.py"`

**Option 1: Refresh Token (Recommended)**
```python
from hubspot_api_client import refresh_token

token_data = refresh_token()
if token_data:
    print("Token refreshed! Copy the new token and update config.py")
else:
    print("Token refresh failed")
```

**Option 2: Get New Token via OAuth**
Run the OAuth setup script:
```bash
python3 get_oauth_token.py
```
This will automatically update `config.py` with the new token.

## Error Handling

All functions return `(success, data_or_error_message)`:

```python
success, result = get_contact("12345")

if success:
    # result is the contact data
    print(result['properties']['email'])
else:
    # result is an error message
    print(f"Error: {result}")
```

### Common Error Messages:

- `"Token expired - update HUBSPOT_ACCESS_TOKEN in config.py"`
- `"Contact not found (ID: 12345)"`
- `"Contact with email 'test@example.com' already exists"`
- `"Connection error - check your internet connection"`
- `"Request timeout - server took too long to respond"`

## Complete Example

```python
from hubspot_contacts import *

# Test connection
success, message = test_connection()
if not success:
    print(f"Connection failed: {message}")
    exit()

# Get all contacts
success, contacts = get_all_contacts()
if success:
    print(f"You have {len(contacts)} contacts")

# Create a new contact
success, contact = create_contact(
    email="john.smith@example.com",
    firstname="John",
    lastname="Smith",
    phone="+1-555-7890",
    company="Tech Startup"
)

if success:
    contact_id = contact['id']
    print(f"Created contact ID: {contact_id}")

    # Update the contact
    success, updated = update_contact(contact_id, company="Updated Company")
    if success:
        print("Contact updated!")

    # Delete the contact
    success, message = delete_contact(contact_id)
    if success:
        print(message)
else:
    print(f"Create failed: {contact}")
```

## File Organization

```
project/
├── config.py                  # All API credentials
├── api_client.py              # Generic API functions (reusable!)
├── hubspot_api_client.py      # HubSpot-specific client
├── hubspot_contacts.py        # Contact operations (use this!)
├── get_oauth_token.py         # First-time OAuth setup
├── token.txt                  # Token storage
└── README.md                  # This guide
```

## Benefits of This Structure

✓ **Reusable** - `api_client.py` works for HubSpot AND Fibery
✓ **Clean** - Each file has one clear purpose
✓ **Simple** - All functions return `(success, data_or_error)`
✓ **Organized** - All credentials in one place (`config.py`)
✓ **Extendable** - Easy to add more APIs (Fibery, etc.)

## Next Steps

### For Fibery API (Future):
1. Add Fibery credentials to `config.py`
2. Create `fibery_api_client.py` (similar to `hubspot_api_client.py`)
3. Create `fibery_entities.py` (similar to `hubspot_contacts.py`)
4. Reuse `api_client.py` functions - no duplication!

## Need Help?

### Token Issues:
- Token expires every 30 minutes
- Use `refresh_token()` or run `get_oauth_token.py`
- Tokens are automatically saved to `config.py`

### Connection Issues:
- Check internet connection
- Verify `config.py` has correct credentials
- Run `test_connection()` to check API access

### Questions?
- All functions have docstrings with examples
- Check error messages - they explain what went wrong
- Read the function comments in each file
