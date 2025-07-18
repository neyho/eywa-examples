# OAuth 2.1 Client Credentials Flow Test

This directory contains Python scripts to test the OAuth 2.1 client credentials flow implementation in EYWA.

## Files

- `test_client_credentials.py` - Main test script for client credentials flow
- `setup_test_client.py` - Setup script to create test client configuration  
- `requirements.txt` - Python dependencies
- `README.md` - This file

## Quick Start

### 1. Install Dependencies

```bash
cd /path/to/EYWA/core/examples/py
pip install -r requirements.txt
```

### 2. Setup Test Client

First, run the setup script to get the client configuration:

```bash
python setup_test_client.py
```

This will print Clojure code that you need to run in your EYWA REPL.

### 3. Configure EYWA

In your EYWA REPL, run the provided Clojure code to create the test client:

```clojure
;; The setup script will give you the exact code to run
(require '[neyho.eywa.iam.oauth.core :as oauth-core])
(require '[buddy.hashers :as hashers])

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

(swap! oauth-core/*clients* assoc (:euuid test-client-config) test-client-config)
```

### 4. Run Tests

Run the comprehensive test suite:

```bash
python test_client_credentials.py
```

Or run a single test:

```bash
python test_client_credentials.py http://localhost:8080 single
```

## Test Cases

The test script includes these test cases:

1. **Valid Client Credentials** - Tests successful token generation
2. **Invalid Client ID** - Tests error handling for non-existent client  
3. **Invalid Client Secret** - Tests authentication failure
4. **No Scope Specified** - Tests default scope handling

## Expected Output

### Successful Test Output

```
🧪 OAUTH 2.1 CLIENT CREDENTIALS FLOW TEST
============================================================

🧪 Test 1: Valid Client Credentials
----------------------------------------
🔑 Testing Client Credentials Flow...
   Client ID: test-client-credentials-app
   Endpoint: http://localhost:8080/oauth/token
   Scope: read:data write:data

📤 Making token request...
📥 Response Status: 200
📥 Response Body: {
  "access_token": "eyJhbGciOiJSUzI1NiIs...",
  "type": "Bearer",
  "scope": "read:data write:data", 
  "expires_in": 3600
}
✅ Test PASSED (Expected: True, Got: True)

🚀 Testing access token with GraphQL request...
📥 GraphQL Response Status: 200
✅ Access token is valid and working!
```

### Error Test Output

```
🧪 Test 2: Invalid Client ID
----------------------------------------
🔑 Testing Client Credentials Flow...
   Client ID: nonexistent-client
   Endpoint: http://localhost:8080/oauth/token

📤 Making token request...
📥 Response Status: 401
📥 Response Body: {
  "error": "invalid_client",
  "error_description": "Client authentication failed"
}
✅ Test PASSED (Expected: False, Got: False)
```

## Troubleshooting

### Common Issues

1. **Connection Refused**
   - Make sure EYWA server is running on http://localhost:8080
   - Check if the server port is correct

2. **Invalid Client Error** 
   - Verify the test client was created in EYWA REPL
   - Check that client ID and secret match the configuration

3. **Unsupported Grant Type**
   - Ensure the client credentials implementation is loaded
   - Verify the `allowed-grants` includes "client_credentials"

### Debugging

Enable debug logging by modifying the test script:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Manual Testing

You can also test manually with curl:

```bash
curl -X POST http://localhost:8080/oauth/token \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "grant_type=client_credentials&client_id=test-client-credentials-app&client_secret=super-secret-key-123&scope=read:data"
```

Expected response:
```json
{
  "access_token": "eyJhbGciOiJSUzI1NiIs...",
  "type": "Bearer", 
  "scope": "read:data",
  "expires_in": 3600
}
```

## Security Notes

- The test client uses a weak password for demonstration purposes
- In production, use strong, randomly generated client secrets
- Store client secrets securely and never commit them to version control
- Consider using client certificate authentication for enhanced security
