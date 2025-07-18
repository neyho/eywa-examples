#!/usr/bin/env python3
"""
Test GraphQL with a valid access token

This script uses a valid access token obtained from the REPL to test GraphQL queries.
"""

import requests
import json


def test_with_known_token():
    """
    Test GraphQL with a token that we know works from REPL testing
    """
    print("🔑 Testing GraphQL with Known Valid Token")
    print("=" * 50)
    
    # This is a token that was generated successfully in our REPL tests
    # Note: In production, tokens should be obtained through the OAuth flow
    access_token = "eyJhbGciOiJSUzI1NiIsImtpZCI6InZOaUJrY1dZUnJOUTViSHl0U1VEa29hMG41U0RsdGJ1cG9HTUVMSHB1dXMiLCJ0eXBlIjoiSldUIn0.eyJhdWQiOm51bGwsInN1YiI6bnVsbCwiaXNzIjoiaHR0cDovL2xvY2FsaG9zdDo4MDgwIiwiZXhwIjoxNzUyODM3NTQxLCJzY29wZSI6InIgZSBhIGQgOiBkIGEgdCBhIiwiY2xpZW50X2lkIjoidGVzdC1jbGllbnQtY3JlZGVudGlhbHMtYXBwIiwiaWF0IjoxNzUyODMzOTQxLCJzaWQiOm51bGwsInNlc3Npb24iOm51bGx9.oTMUu1YQGqwlQYreBl--akIYv_ycoH-lOd6_VCPhFZd35uI5o3c9L4DV7ue0ACCH_1cdisdduMGsxilKuKUxevSxEwt9tnxrgv5UDeuQm3aCF0oqO9PlWx2EuLqbnEnH9uB35QvupFRlDiLjUe-D_2XFm8_1vqU85DxT1qq7urqMRRKOd3hcYHUocZVKyfHrxlh4Bn-WLNO3iLqFMH891afuAveu_Bvnv4Ehql-t12IMx5nYsAupILZIaYg-8_6FRLWE2nD7cWmXHUS26Wdp0WsJtr1losgahieQ5zSglbYbSRg3G4b2dxuecmwpEEvGnk2XQm80JnD2p0bhi9HVvg"
    
    print(f"🎫 Token: {access_token[:50]}...")
    
    graphql_url = "http://localhost:8080/graphql"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Test 1: Simple introspection
    print("\n🧪 Test 1: Schema Introspection")
    query1 = {
        "query": """
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
    }
    
    try:
        response = requests.post(graphql_url, json=query1, headers=headers, timeout=10)
        print(f"📥 Status: {response.status_code}")
        print(f"📥 Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            if "errors" not in data:
                print("✅ Introspection successful!")
                print(f"📊 Schema: {json.dumps(data['data'], indent=2)}")
            else:
                print(f"❌ GraphQL Errors: {data['errors']}")
    except Exception as e:
        print(f"❌ Request failed: {e}")
    
    # Test 2: List available queries
    print("\n🧪 Test 2: Available Queries")
    query2 = {
        "query": """
        {
          __type(name: "Query") {
            fields {
              name
              description
              type {
                name
                kind
              }
            }
          }
        }
        """
    }
    
    try:
        response = requests.post(graphql_url, json=query2, headers=headers, timeout=10)
        print(f"📥 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if "errors" not in data and data.get("data", {}).get("__type"):
                print("✅ Query types retrieved!")
                fields = data["data"]["__type"]["fields"]
                print(f"📊 Available queries ({len(fields)} total):")
                for field in fields[:10]:  # Show first 10
                    print(f"   - {field['name']}: {field['type']['name']}")
                if len(fields) > 10:
                    print(f"   ... and {len(fields) - 10} more")
            else:
                print(f"❌ Error or no data: {response.text}")
        else:
            print(f"❌ HTTP Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Request failed: {e}")
    
    # Test 3: Try a simple data query
    print("\n🧪 Test 3: Simple Data Query")
    query3 = {
        "query": """
        {
          searchUser(limit: 3) {
            euuid
            name
            active
          }
        }
        """
    }
    
    try:
        response = requests.post(graphql_url, json=query3, headers=headers, timeout=10)
        print(f"📥 Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if "errors" not in data:
                print("✅ User query successful!")
                users = data.get("data", {}).get("searchUser", [])
                print(f"📊 Found {len(users)} users:")
                for user in users:
                    print(f"   - {user.get('name', 'Unknown')} ({user.get('euuid', 'No ID')})")
            else:
                print(f"❌ GraphQL Errors: {data['errors']}")
        else:
            print(f"❌ HTTP Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Request failed: {e}")


def test_token_endpoint_again():
    """
    Try the token endpoint one more time to see current status
    """
    print("\n🔄 Testing Token Endpoint Status")
    print("=" * 40)
    
    url = "http://localhost:8080/oauth/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": "test-client-credentials-app",
        "client_secret": "super-secret-key-123",
        "scope": "read:data"
    }
    
    try:
        response = requests.post(url, data=data, timeout=5)
        print(f"📥 Token endpoint status: {response.status_code}")
        print(f"📥 Response: {response.text}")
        
        if response.status_code == 200:
            token_data = response.json()
            print("🎉 NEW TOKEN OBTAINED!")
            return token_data.get("access_token")
        else:
            print("❌ Still getting authentication error")
            return None
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return None


def main():
    print("🧪 GRAPHQL TESTING WITH ACCESS TOKEN")
    print("=" * 50)
    
    # First, try to get a fresh token
    fresh_token = test_token_endpoint_again()
    
    if fresh_token:
        print(f"\n✅ Using fresh token: {fresh_token[:50]}...")
        # Use the fresh token for testing
        # ... (add GraphQL tests here)
    else:
        print("\n🔄 Using known working token from REPL tests...")
        test_with_known_token()


if __name__ == "__main__":
    main()
