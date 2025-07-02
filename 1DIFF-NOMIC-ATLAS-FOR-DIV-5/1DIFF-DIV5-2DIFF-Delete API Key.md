# Delete API Key

## Endpoint Overview
- **Base URL**: `https://api-atlas.nomic.ai`
- **Endpoint Path**: `/v1/user/authorization/keys/:organization_id/delete`
- **HTTP Method**: `POST`
- **Description**: Deletes an existing API key scoped to an organization, dataset, or user.

## Parameters
### Path Parameters
- **organization_id** (string, required):
  - Description: The unique identifier of the organization to which the API key belongs.

### Body Parameters
- **key_id** (string, required):
  - Description: The unique identifier of the API key to be deleted.

## Responses
### 200 OK
- **Description**: Indicates the API key was successfully deleted.
- **Example Response**:
  ```json
  {
    "message": "API key deleted successfully."
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
curl -L 'https://api-atlas.nomic.ai/v1/user/authorization/keys/:organization_id/delete' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{
  "key_id": "string"
}'
```

### Python
```python
import requests
import json

url = "https://api-atlas.nomic.ai/v1/user/authorization/keys/:organization_id/delete"

payload = json.dumps({
  "key_id": "string"
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
- The `organization_id` and `key_id` must match an existing organization and API key in the system.
- Use this endpoint with caution as deleted API keys cannot be recovered.

---
**Next Steps**:
- Verify the `key_id` before deletion.
- Log the deletion action for audit purposes.