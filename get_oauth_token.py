import requests
from urllib.parse import urlencode, parse_qs, urlparse

# OAuth credentials


# Scopes (exact scopes from your app)
SCOPES = "crm.objects.companies.read crm.objects.companies.write crm.objects.contacts.read crm.objects.contacts.write oauth"

def get_authorization_url():
    """Generate the OAuth authorization URL"""
    params = {
        "client_id": CLIENT_ID,
        "redirect_uri": REDIRECT_URI,
        "scope": SCOPES
    }
    auth_url = f"https://app-na3.hubspot.com/oauth/authorize?{urlencode(params)}"
    return auth_url

def exchange_code_for_token(code):
    """Exchange authorization code for access token"""
    token_url = "https://api.hubapi.com/oauth/v1/token"

    data = {
        "grant_type": "authorization_code",
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "redirect_uri": REDIRECT_URI,
        "code": code
    }

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    response = requests.post(token_url, data=data, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.json())
        return None

def main():
    print("HubSpot OAuth Token Setup")
    print("=" * 80)
    print("\n📋 STEP 1: Visit this URL in your browser:\n")
    print(get_authorization_url())
    print("\n" + "=" * 80)
    print("\n📋 STEP 2: Authorize the app in your browser")
    print("   - You'll be redirected to localhost (the page won't load - that's OK!)")
    print("   - Copy the ENTIRE URL from your browser's address bar")
    print("   - It will look like: http://localhost?code=XXXXX\n")

    redirect_url = input("📋 STEP 3: Paste the redirect URL here: ").strip()

    # Extract the code from the redirect URL
    parsed_url = urlparse(redirect_url)
    params = parse_qs(parsed_url.query)

    if 'code' not in params:
        print("\n❌ Error: No authorization code found in URL")
        return

    code = params['code'][0]
    print(f"\n✓ Authorization code found: {code[:20]}...")
    print("\n📋 STEP 4: Exchanging code for access token...")

    token_data = exchange_code_for_token(code)

    if token_data:
      

        # Update config.py
        print("\n💾 Updating config.py...")
        with open("config.py", "w") as f:
            f.write("# HubSpot API Configuration\n")
            f.write("# All HubSpot credentials in one place\n\n")
            f.write("# OAuth Credentials\n")
            f.write(f'HUBSPOT_ACCESS_TOKEN = "{token_data["access_token"]}"\n')
            f.write(f'HUBSPOT_CLIENT_ID = "{CLIENT_ID}"\n')
            f.write(f'HUBSPOT_CLIENT_SECRET = "{CLIENT_SECRET}"\n')
            f.write(f'HUBSPOT_REFRESH_TOKEN = "{token_data["refresh_token"]}"\n\n')
            f.write("# Fibery API Configuration (for future use)\n")
            f.write('FIBERY_API_KEY = ""\n')
            f.write('FIBERY_WORKSPACE = ""\n')
        print("✓ Updated config.py")

        # Save to token.txt
        print("💾 Saving token to token.txt...")
        with open("token.txt", "w") as f:
            f.write(f"ACCESS_TOKEN={token_data['access_token']}\n")
            f.write(f"REFRESH_TOKEN={token_data['refresh_token']}\n")
        print("✓ Token saved to token.txt")

        print("\n✅ All done! You can now use hubspot_contacts.py")
    else:
        print("\n❌ Failed to get access token")

if __name__ == "__main__":
    main()
