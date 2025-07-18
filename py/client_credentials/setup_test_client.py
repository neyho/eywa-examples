#!/usr/bin/env python3
"""
Setup script to create a test client for client credentials flow testing.

This script creates the necessary client configuration in EYWA
for testing the client_credentials grant type.
"""

import json
import sys


def create_test_client_config():
    """
    Create a test client configuration for client credentials flow
    """
    client_config = {
        "euuid": "550e8400-e29b-41d4-a716-446655440001",
        "name": "Client Credentials Test Client", 
        "id": "test-client-credentials-app",
        "type": "confidential",
        "secret": "$2a$12$rWc3LvhqJ8Y7U.6f3XBFO.vn8c8F9vF5y.xGJhBa8qQv8LzN1rOO2",  # hashed "super-secret-key-123"
        "description": "Test client for OAuth 2.1 client credentials flow",
        "active": True,
        "settings": {
            "token-expiry": {
                "access": 3600
            },
            "allowed-grants": [
                "client_credentials"
            ],
            "refresh-tokens": False
        }
    }
    
    return client_config


def save_client_config(filename="test_client_config.json"):
    """
    Save the client configuration to a JSON file
    """
    config = create_test_client_config()
    
    with open(filename, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Test client configuration saved to: {filename}")
    print("\n📋 Client Details:")
    print(f"   Client ID: {config['id']}")
    print(f"   Client Secret: super-secret-key-123")
    print(f"   Allowed Grants: {config['settings']['allowed-grants']}")
    print(f"   Token Expiry: {config['settings']['token-expiry']['access']} seconds")
    
    print("\n🔧 To use this client:")
    print("1. Import this configuration into your EYWA system")
    print("2. Run the test script: python test_client_credentials.py")
    
    return config


def print_clojure_setup():
    """
    Print Clojure code to set up the test client in EYWA
    """
    print("\n" + "=" * 60)
    print("🔧 CLOJURE SETUP CODE FOR EYWA REPL")
    print("=" * 60)
    
    clojure_code = '''
;; Run this in your EYWA REPL to create the test client
(require '[neyho.eywa.iam.oauth.core :as oauth-core])
(require '[buddy.hashers :as hashers])

;; Create test client configuration
(def test-client-config
  {:euuid "550e8400-e29b-41d4-a716-446655440001"
   :name "Client Credentials Test Client"
   :id "test-client-credentials-app"
   :type "confidential"
   :secret (hashers/derive "super-secret-key-123")
   :description "Test client for OAuth 2.1 client credentials flow"
   :active true
   :settings {"token-expiry" {"access" 3600}
              "allowed-grants" ["client_credentials"]
              "refresh-tokens" false}})

;; Add the client to the system
(swap! oauth-core/*clients* assoc (:euuid test-client-config) test-client-config)

;; Verify the client was added
(println "Test client created:")
(println "Client ID:" (:id test-client-config))
(println "Allowed grants:" (get-in test-client-config [:settings "allowed-grants"]))

;; Test the client lookup
(oauth-core/get-client "test-client-credentials-app")
'''
    
    print(clojure_code)


def main():
    """
    Main function
    """
    print("🏗️  CLIENT CREDENTIALS TEST SETUP")
    print("=" * 50)
    
    # Save client configuration
    config = save_client_config()
    
    # Print Clojure setup instructions
    print_clojure_setup()
    
    print("\n🚀 Next Steps:")
    print("1. Start your EYWA server (if not already running)")
    print("2. Run the Clojure setup code in your EYWA REPL")
    print("3. Run: python test_client_credentials.py")
    print("4. Verify the client credentials flow works!")


if __name__ == "__main__":
    main()
