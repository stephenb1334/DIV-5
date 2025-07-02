# Create API Key

## Endpoint Overview
- **Base URL**: `https://api-atlas.nomic.ai`
- **Endpoint Path**: `/v1/user/authorization/keys/:organization_id/create`
- **HTTP Method**: `POST`
- **Description**: Creates a new API key scoped to an organization, dataset, or user with specific permissions.

## Parameters
### Path Parameters
- **organization_id** (string, required):
  - Description: The unique identifier of the organization for which the API key is being created.

### Body Parameters
- **name** (string, required):
  - Description: A descriptive name for the API key.
- **permissions** (array of strings, required):
  - Description: A list of permissions to assign to the API key.
  - Example: `["read", "write"]`.
- **expiration** (string, optional):
  - Description: The expiration date for the API key in ISO 8601 format.
  - Example: `"2025-12-31T23:59:59Z"`.
- **scopes** (array of objects, optional):
  - Description: Defines the scope of the API key.
  - **Items**:
    - **scope_type** (string): The type of scope, e.g., `dataset` or `organization`.
    - **scope_id** (string): The unique identifier of the scope.

## Responses
### 200 OK
- **Description**: Indicates the API key was successfully created.
- **Schema**:
  - **key_id** (string):
    - Description: The unique identifier of the created API key.
  - **key** (string):
    - Description: The actual API key.
- **Example Response**:
  ```json
  {
    "key_id": "string",
    "key": "string"
  }
  ```

### 422 Validation Error
- **Description**: Indicates a validation error occurred.
- **Schema**:
  - **detail** (array of objects):
    - **loc** (array of strings): The location of the error.
    - **msg** (string): The error message.
    - **type** (string): The type of error.
- **Example Response**:
  ```json
  {
    "detail": [
      {
        "loc": ["string", 0],
        "msg": "string",
        "type": "string"
      }
    ]
  }
  ```

## Example Usage
### CURL
```bash
curl -L 'https://api-atlas.nomic.ai/v1/user/authorization/keys/:organization_id/create' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{
  "name": "My API Key",
  "permissions": ["read", "write"],
  "expiration": "2025-12-31T23:59:59Z",
  "scopes": [
    {
      "scope_type": "dataset",
      "scope_id": "dataset123"
    }
  ]
}'
```

### Python
```python
import requests
import json

url = "https://api-atlas.nomic.ai/v1/user/authorization/keys/:organization_id/create"

payload = json.dumps({
  "name": "My API Key",
  "permissions": ["read", "write"],
  "expiration": "2025-12-31T23:59:59Z",
  "scopes": [
    {
      "scope_type": "dataset",
      "scope_id": "dataset123"
    }
  ]
})
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer <TOKEN>'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
```

## Notes
- Ensure the `Authorization` header contains a valid Bearer token.
- The `permissions` should align with the intended use case of the API key.
- Use the `expiration` field to limit the lifespan of the key for security purposes.

---
**Next Steps**:
- Store the returned API key securely.
- Monitor API key usage and rotate keys periodically for security.