#!/usr/bin/env python3
"""
Manual Client Credentials Token Test and GraphQL Query

This script manually tests the client credentials flow and then 
uses the token to make GraphQL queries.
"""

import requests
import json
import sys
from urllib.parse import urlencode


def get_access_token_manual():
    """
    Manually get an access token by making the exact request
    """
    print("🔑 Manual Client Credentials Token Request")
    print("=" * 50)
    
    # Use curl-like approach
    url = "http://localhost:8080/oauth/token"
    
    data = {
        "grant_type": "client_credentials",
        "client_id": "test-client-credentials-app", 
        "client_secret": "super-secret-key-123",
        "scope": "read:data"
    }
    
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json"
    }
    
    print(f"📤 POST {url}")
    print(f"📋 Data: {data}")
    
    try:
        response = requests.post(url, data=data, headers=headers, timeout=10)
        
        print(f"📥 Status: {response.status_code}")
        print(f"📥 Headers: {dict(response.headers)}")
        print(f"📥 Raw Response: {response.text}")
        
        if response.status_code == 200:
            try:
                token_data = response.json()
                return token_data
            except json.JSONDecodeError:
                print("❌ Failed to parse JSON response")
                return None
        else:
            print(f"❌ Request failed with status {response.status_code}")
            return None
            
    except Exception as e:
        print(f"❌ Request failed: {e}")
        return None


def test_graphql_queries(access_token):
    """
    Test various GraphQL queries with the access token
    """
    print("\n🚀 Testing GraphQL Queries with Access Token")
    print("=" * 50)
    
    graphql_url = "http://localhost:8080/graphql"
    
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Test queries from simple to more complex
    test_queries = [
        {
            "name": "Schema Introspection",
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
        },
        {
            "name": "Available Types",
            "query": """
            {
              __schema {
                types {
                  name
                  kind
                }
              }
            }
            """
        },
        {
            "name": "Simple Query - Check if User query exists",
            "query": """
            {
              __type(name: "Query") {
                fields {
                  name
                  type {
                    name
                  }
                }
              }
            }
            """
        }
    ]
    
    for i, test in enumerate(test_queries, 1):
        print(f"\n🧪 Test {i}: {test['name']}")
        print("-" * 30)
        
        try:
            response = requests.post(
                graphql_url,
                json={"query": test["query"]},
                headers=headers,
                timeout=10
            )
            
            print(f"📥 Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if "errors" in data:
                        print(f"❌ GraphQL Errors: {data['errors']}")
                    else:
                        print("✅ Success!")
                        # Print first few items of response
                        result = data.get("data", {})
                        if result:
                            print(f"📊 Data preview: {json.dumps(result, indent=2)[:200]}...")
                        else:
                            print("📊 Empty data response")
                except json.JSONDecodeError:
                    print(f"❌ Invalid JSON: {response.text}")
            else:
                print(f"❌ HTTP Error: {response.status_code}")
                print(f"📥 Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Request failed: {e}")


def test_simple_data_query(access_token):
    """
    Test a simple data query if available
    """
    print("\n🔍 Testing Simple Data Queries")
    print("=" * 40)
    
    graphql_url = "http://localhost:8080/graphql"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    
    # Try some common EYWA queries
    simple_queries = [
        {
            "name": "Health Check", 
            "query": "{ __typename }"
        },
        {
            "name": "Search Users (if available)",
            "query": """
            {
              searchUser(limit: 1) {
                euuid
                name
              }
            }
            """
        }
    ]
    
    for query_test in simple_queries:
        print(f"\n🔹 {query_test['name']}:")
        
        try:
            response = requests.post(
                graphql_url,
                json={"query": query_test["query"]},
                headers=headers,
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                if "errors" in data:
                    print(f"❌ GraphQL Error: {data['errors'][0].get('message', 'Unknown error')}")
                else:
                    print(f"✅ Success: {json.dumps(data.get('data', {}), indent=2)}")
            else:
                print(f"❌ HTTP {response.status_code}: {response.text[:100]}")
                
        except Exception as e:
            print(f"❌ Request failed: {e}")


def main():
    """
    Main test function
    """
    print("🧪 COMPREHENSIVE CLIENT CREDENTIALS + GRAPHQL TEST")
    print("=" * 60)
    
    # Step 1: Get access token
    token_data = get_access_token_manual()
    
    if not token_data:
        print("\n❌ Could not obtain access token. Exiting.")
        return
    
    access_token = token_data.get("access_token")
    if not access_token:
        print("\n❌ No access token in response. Exiting.")
        return
    
    print(f"\n✅ Access Token Obtained!")
    print(f"🎫 Token Type: {token_data.get('type', 'Bearer')}")
    print(f"⏰ Expires In: {token_data.get('expires_in')} seconds")
    print(f"🔍 Scope: {token_data.get('scope', 'N/A')}")
    print(f"🔑 Token Preview: {access_token[:50]}...")
    
    # Step 2: Test GraphQL queries
    test_graphql_queries(access_token)
    
    # Step 3: Test simple data queries
    test_simple_data_query(access_token)
    
    print(f"\n🎉 Test completed!")
    print(f"💡 Your access token: {access_token}")


if __name__ == "__main__":
    main()
