# List Datasets

## Endpoint Overview
- **Base URL**: `https://api-atlas.nomic.ai`
- **Endpoint Path**: `/v1/datasets`
- **HTTP Method**: `GET`
- **Description**: Retrieves a list of datasets available to the user, including metadata and status information.

## Parameters
- **No parameters required.**

## Responses
### 200 OK
- **Description**: Successfully retrieves a list of datasets.
- **Schema**:
  - **datasets** (array of objects):
    - Description: List of datasets with their details.
    - **Items**:
      - **dataset_id** (string): The unique identifier of the dataset.
      - **name** (string): The name of the dataset.
      - **description** (string): A brief description of the dataset.
      - **status** (string): The current status of the dataset (e.g., `available`, `processing`).
      - **created_at** (string): The timestamp of when the dataset was created.
      - **metadata** (object): Additional metadata about the dataset.
- **Example Response**:
  ```json
  {
    "datasets": [
      {
        "dataset_id": "string",
        "name": "Dataset Name",
        "description": "A brief description",
        "status": "available",
        "created_at": "2025-06-27T17:00:00Z",
        "metadata": {
          "source": "user_upload",
          "tags": ["finance", "2025"]
        }
      }
    ]
  }
  ```

### 401 Unauthorized
- **Description**: Indicates that the request lacks valid authentication credentials.
- **Schema**:
  - **detail** (string): Error message indicating authentication failure.
- **Example Response**:
  ```json
  {
    "detail": "Authentication credentials were not provided."
  }
  ```

## Example Usage
### CURL
```bash
curl -L 'https://api-atlas.nomic.ai/v1/datasets' \
-H 'Authorization: Bearer <TOKEN>'
```

### Python
```python
import requests

url = "https://api-atlas.nomic.ai/v1/datasets"

headers = {
    'Authorization': 'Bearer <TOKEN>'
}

response = requests.request("GET", url, headers=headers)

print(response.text)
```

## Notes
- Ensure the `Authorization` header contains a valid Bearer token.
- Use the `dataset_id` from the response to perform further operations on specific datasets.

---
**Next Steps**:
- Analyze the list of datasets to identify ones for further processing or analysis.
- Use the metadata to filter datasets based on specific criteria.