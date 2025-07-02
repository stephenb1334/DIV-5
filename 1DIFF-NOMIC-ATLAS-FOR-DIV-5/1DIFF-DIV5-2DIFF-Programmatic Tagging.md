# Programmatic Tagging

## Endpoint Overview
- **Base URL**: `https://api-atlas.nomic.ai`
- **Endpoint Path**: `/v1/tags/programmatic`
- **HTTP Method**: `POST`
- **Description**: Allows programmatic tagging of datasets based on user-defined rules or conditions.

## Parameters
### Body Parameters
- **dataset_id** (string, required):
  - Description: The unique identifier of the dataset to which the tags will be applied.
- **tags** (array of objects, required):
  - Description: A list of tags to be applied programmatically.
  - **Items**:
    - **tag_name** (string):
      - Description: The name of the tag.
    - **conditions** (object):
      - Description: The conditions for applying the tag.
      - **Properties**:
        - **column** (string): The column within the dataset to evaluate.
        - **value** (string): The value to match for the condition.

## Responses
### 200 OK
- **Description**: Indicates the tags were successfully applied.
- **Schema**:
  - **tags_applied** (array of strings):
    - Description: A list of tags that were successfully applied.
- **Example Response**:
  ```json
  {
    "tags_applied": ["tag1", "tag2"]
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
curl -L 'https://api-atlas.nomic.ai/v1/tags/programmatic' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{
  "dataset_id": "string",
  "tags": [
    {
      "tag_name": "important",
      "conditions": {
        "column": "priority",
        "value": "high"
      }
    }
  ]
}'
```

### Python
```python
import requests
import json

url = "https://api-atlas.nomic.ai/v1/tags/programmatic"

payload = json.dumps({
  "dataset_id": "string",
  "tags": [
    {
      "tag_name": "important",
      "conditions": {
        "column": "priority",
        "value": "high"
      }
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
- The `dataset_id` must match an existing dataset in the system.
- The `conditions` object should be tailored to the dataset's schema for accurate tagging.

---
**Next Steps**:
- Validate the dataset and tags before sending the request.
- Log the applied tags for future reference.