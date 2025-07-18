#!/usr/bin/env python3
"""
OAuth 2.1 Client Credentials Flow Test Script

This script tests the client_credentials grant type implementation
by making direct HTTP requests to the EYWA OAuth token endpoint.
"""

import requests
import json
import sys
from urllib.parse import urlencode


class ClientCredentialsTest:
    def __init__(self, eywa_url="http://localhost:8080"):
        self.eywa_url = eywa_url
        self.token_endpoint = f"{eywa_url}/oauth/token"
        
    def create_test_client(self):
        """
        Create a test client configuration for client credentials flow.
        This would normally be done through EYWA admin interface.
        """
        return {
            "client_id": "test-client-credentials-app",
            "client_secret": "super-secret-key-123",
            "settings": {
                "allowed-grants": ["client_credentials"],
                "token-expiry": {
                    "access": 3600
                }
            }
        }
    
    def test_client_credentials_flow(self, client_id, client_secret, scope=None):
        """
        Test the client credentials OAuth 2.1 flow
        
        Args:
            client_id: The client identifier
            client_secret: The client secret
            scope: Optional scope parameter
            
        Returns:
            dict: Response from token endpoint
        """
        print(f"🔑 Testing Client Credentials Flow...")
        print(f"   Client ID: {client_id}")
        print(f"   Endpoint: {self.token_endpoint}")
        
        # Prepare the request data
        data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret
        }
        
        if scope:
            data["scope"] = scope
            print(f"   Scope: {scope}")
        
        # Set headers
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"
        }
        
        try:
            print("\n📤 Making token request...")
            response = requests.post(
                self.token_endpoint,
                data=urlencode(data),
                headers=headers,
                timeout=10
            )
            
            print(f"📥 Response Status: {response.status_code}")
            print(f"📥 Response Headers: {dict(response.headers)}")
            
            # Parse response
            try:
                response_data = response.json()
                print(f"📥 Response Body: {json.dumps(response_data, indent=2)}")
                
                return {
                    "success": response.status_code == 200,
                    "status_code": response.status_code,
                    "data": response_data,
                    "headers": dict(response.headers)
                }
            except json.JSONDecodeError:
                print(f"📥 Raw Response: {response.text}")
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "error": "Invalid JSON response",
                    "raw_response": response.text
                }
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Request failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def test_with_access_token(self, access_token):
        """
        Test using the access token to make a GraphQL request
        
        Args:
            access_token: The access token obtained from client credentials flow
        """
        print("\n🚀 Testing access token with GraphQL request...")
        
        graphql_endpoint = f"{self.eywa_url}/graphql"
        
        # Simple GraphQL query to test authentication
        query = """
        {
          __schema {
            queryType {
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
            response = requests.post(
                graphql_endpoint,
                json={"query": query},
                headers=headers,
                timeout=10
            )
            
            print(f"📥 GraphQL Response Status: {response.status_code}")
            
            if response.status_code == 200:
                print("✅ Access token is valid and working!")
                data = response.json()
                print(f"📥 GraphQL Response: {json.dumps(data, indent=2)}")
            else:
                print(f"❌ GraphQL request failed: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ GraphQL request failed: {e}")
    
    def run_comprehensive_test(self):
        """
        Run a comprehensive test suite for client credentials flow
        """
        print("=" * 60)
        print("🧪 OAUTH 2.1 CLIENT CREDENTIALS FLOW TEST")
        print("=" * 60)
        
        # Test cases
        test_cases = [
            {
                "name": "Valid Client Credentials",
                "client_id": "test-client-credentials-app",
                "client_secret": "super-secret-key-123",
                "scope": "read:data write:data",
                "expected_success": True
            },
            {
                "name": "Invalid Client ID",
                "client_id": "nonexistent-client",
                "client_secret": "super-secret-key-123",
                "scope": "read:data",
                "expected_success": False
            },
            {
                "name": "Invalid Client Secret",
                "client_id": "test-client-credentials-app",
                "client_secret": "wrong-secret",
                "scope": "read:data",
                "expected_success": False
            },
            {
                "name": "No Scope Specified",
                "client_id": "test-client-credentials-app",
                "client_secret": "super-secret-key-123",
                "scope": None,
                "expected_success": True
            }
        ]
        
        results = []
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"\n🧪 Test {i}: {test_case['name']}")
            print("-" * 40)
            
            result = self.test_client_credentials_flow(
                test_case["client_id"],
                test_case["client_secret"],
                test_case["scope"]
            )
            
            success = result.get("success", False)
            expected = test_case["expected_success"]
            
            if success == expected:
                print(f"✅ Test PASSED (Expected: {expected}, Got: {success})")
            else:
                print(f"❌ Test FAILED (Expected: {expected}, Got: {success})")
            
            results.append({
                "test": test_case["name"],
                "expected": expected,
                "actual": success,
                "passed": success == expected,
                "result": result
            })
            
            # If we got a valid token, test it
            if success and "access_token" in result.get("data", {}):
                access_token = result["data"]["access_token"]
                self.test_with_access_token(access_token)
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for r in results if r["passed"])
        total = len(results)
        
        print(f"✅ Passed: {passed}/{total}")
        
        if passed == total:
            print("🎉 ALL TESTS PASSED!")
        else:
            print("❌ Some tests failed:")
            for result in results:
                if not result["passed"]:
                    print(f"   - {result['test']}")
        
        return results


def main():
    """
    Main function to run the client credentials test
    """
    # Parse command line arguments
    if len(sys.argv) > 1:
        eywa_url = sys.argv[1]
    else:
        eywa_url = "http://localhost:8080"
    
    print(f"🎯 Testing against EYWA server: {eywa_url}")
    
    # Create test instance
    tester = ClientCredentialsTest(eywa_url)
    
    # Check if user wants to run specific test or comprehensive suite
    if len(sys.argv) > 2 and sys.argv[2] == "single":
        # Single test with hardcoded values
        result = tester.test_client_credentials_flow(
            client_id="test-client-credentials-app",
            client_secret="super-secret-key-123",
            scope="read:data"
        )
        
        if result.get("success") and "access_token" in result.get("data", {}):
            access_token = result["data"]["access_token"]
            tester.test_with_access_token(access_token)
    else:
        # Run comprehensive test suite
        tester.run_comprehensive_test()


if __name__ == "__main__":
    main()
