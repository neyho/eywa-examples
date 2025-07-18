#!/usr/bin/env python3
"""
Simple Client Credentials Flow Test

This script demonstrates how to get an access token using the OAuth 2.1 
client credentials flow with EYWA.
"""

import requests
import json
import sys
from urllib.parse import urlencode


def get_access_token(eywa_url, client_id, client_secret, scope=None):
    """
    Get an access token using client credentials flow
    
    Args:
        eywa_url: Base URL of EYWA server (e.g., http://localhost:8080)
        client_id: OAuth client ID
        client_secret: OAuth client secret  
        scope: Optional scope parameter
        
    Returns:
        dict: Token response or error
    """
    token_endpoint = f"{eywa_url}/oauth/token"
    
    # Prepare request data
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }
    
    if scope:
        data["scope"] = scope
    
    # Set headers
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    
    try:
        print(f"🔑 Requesting access token from {token_endpoint}")
        print(f"📋 Client ID: {client_id}")
        if scope:
            print(f"📋 Scope: {scope}")
        
        response = requests.post(
            token_endpoint,
            data=urlencode(data),
            headers=headers,
            timeout=10
        )
        
        print(f"📥 Response Status: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            print("✅ SUCCESS! Access token received:")
            print(f"   Token Type: {token_data.get('type', 'Bearer')}")
            print(f"   Expires In: {token_data.get('expires_in')} seconds")
            print(f"   Scope: {token_data.get('scope', 'N/A')}")
            print(f"   Access Token: {token_data.get('access_token', '')[:50]}...")
            
            return {
                "success": True,
                "access_token": token_data.get("access_token"),
                "token_type": token_data.get("type", "Bearer"),
                "expires_in": token_data.get("expires_in"),
                "scope": token_data.get("scope")
            }
        else:
            error_data = response.json()
            print("❌ ERROR: Failed to get access token")
            print(f"   Error: {error_data.get('error')}")
            print(f"   Description: {error_data.get('error_description')}")
            
            return {
                "success": False,
                "error": error_data.get("error"),
                "error_description": error_data.get("error_description")
            }
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error: {e}")
        return {"success": False, "error": str(e)}
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON response: {e}")
        return {"success": False, "error": "Invalid JSON response"}


def test_access_token(eywa_url, access_token):
    """
    Test the access token by making a GraphQL request
    
    Args:
        eywa_url: Base URL of EYWA server
        access_token: The access token to test
    """
    graphql_endpoint = f"{eywa_url}/graphql"
    
    # Simple introspection query
    query = """
    {
      __schema {
        queryType {
          name
        }
        mutationType {
          name
        }
      }
    }
    """
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    try:
        print(f"\n🚀 Testing access token with GraphQL request...")
        response = requests.post(
            graphql_endpoint,
            json={"query": query},
            headers=headers,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Access token is valid!")
            print(f"📊 GraphQL Schema Info: {json.dumps(data.get('data', {}), indent=2)}")
            return True
        else:
            print(f"❌ GraphQL request failed with status {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ GraphQL request failed: {e}")
        return False


def main():
    """
    Main function - demonstrates client credentials flow usage
    """
    print("🔐 OAUTH 2.1 CLIENT CREDENTIALS FLOW DEMO")
    print("=" * 50)
    
    # Configuration - modify these values for your setup
    EYWA_URL = "http://localhost:8080"
    CLIENT_ID = "test-client-credentials-app"
    CLIENT_SECRET = "super-secret-key-123"
    SCOPE = "read:data"
    
    # Allow override from command line
    if len(sys.argv) >= 2:
        EYWA_URL = sys.argv[1]
    if len(sys.argv) >= 3:
        CLIENT_ID = sys.argv[2]
    if len(sys.argv) >= 4:
        CLIENT_SECRET = sys.argv[3]
    if len(sys.argv) >= 5:
        SCOPE = sys.argv[4]
    
    print(f"🎯 Target EYWA Server: {EYWA_URL}")
    print()
    
    # Step 1: Get access token
    result = get_access_token(EYWA_URL, CLIENT_ID, CLIENT_SECRET, SCOPE)
    
    if not result["success"]:
        print("\n💡 Troubleshooting Tips:")
        print("1. Make sure EYWA server is running")
        print("2. Verify client credentials are correct")
        print("3. Check that client is configured for 'client_credentials' grant")
        print("\nTo create a test client, run this in your EYWA REPL:")
        print("""
        (require '[neyho.eywa.iam.oauth.core :as oauth-core])
        (require '[buddy.hashers :as hashers])
        (require '[neyho.eywa.iam :as iam])
        
        ;; Mock iam/get-client for testing
        (defn mock-get-client [id]
          (when (= id "test-client-credentials-app")
            {:euuid "550e8400-e29b-41d4-a716-446655440001"
             :name "Test Client"
             :id "test-client-credentials-app"
             :type "confidential"
             :secret (hashers/derive "super-secret-key-123")
             :active true
             :settings {"allowed-grants" ["client_credentials"]
                        "token-expiry" {"access" 3600}}}))
        
        ;; Apply the mock
        (alter-var-root #'iam/get-client (constantly mock-get-client))
        """)
        return
    
    # Step 2: Test the access token
    access_token = result["access_token"]
    test_access_token(EYWA_URL, access_token)
    
    print(f"\n🎉 Demo completed successfully!")
    print(f"💰 You now have a valid access token that expires in {result['expires_in']} seconds")
    print(f"🔑 Use it in API requests with: Authorization: Bearer {access_token[:30]}...")


if __name__ == "__main__":
    main()
