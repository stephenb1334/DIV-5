# Upload Dataset

## Endpoint Overview
- **Base URL**: `https://api-atlas.nomic.ai`
- **Endpoint Path**: `/v1/datasets/upload`
- **HTTP Method**: `POST`
- **Description**: Uploads a new dataset to the system, allowing further analysis, tagging, and querying.

## Parameters
### Body Parameters
- **name** (string, required):
  - Description: The name of the dataset.
- **description** (string, optional):
  - Description: A brief description of the dataset.
- **file** (file, required):
  - Description: The dataset file to upload. Supported formats include `.csv`, `.json`, `.parquet`, etc.
- **metadata** (object, optional):
  - Description: Additional metadata about the dataset.
  - Example:
    ```json
    {
      "source": "user_upload",
      "tags": ["finance", "2025"]
    }
    ```

## Responses
### 200 OK
- **Description**: Indicates the dataset was successfully uploaded.
- **Schema**:
  - **dataset_id** (string):
    - Description: The unique identifier of the uploaded dataset.
  - **status** (string):
    - Description: The status of the upload (e.g., `processing` or `completed`).
- **Example Response**:
  ```json
  {
    "dataset_id": "string",
    "status": "processing"
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
curl -L 'https://api-atlas.nomic.ai/v1/datasets/upload' \
-H 'Authorization: Bearer <TOKEN>' \
-F 'name=My Dataset' \
-F 'description=A sample dataset' \
-F 'file=@/path/to/file.csv' \
-F 'metadata={"source": "user_upload", "tags": ["finance", "2025"]}'
```

### Python
```python
import requests

url = "https://api-atlas.nomic.ai/v1/datasets/upload"

files = {
    'file': open('/path/to/file.csv', 'rb')
}
data = {
    'name': 'My Dataset',
    'description': 'A sample dataset',
    'metadata': '{"source": "user_upload", "tags": ["finance", "2025"]}'
}
headers = {
    'Authorization': 'Bearer <TOKEN>'
}

response = requests.request("POST", url, headers=headers, data=data, files=files)

print(response.text)
```

## Notes
- Ensure the `Authorization` header contains a valid Bearer token.
- The dataset file should adhere to the supported formats to avoid upload errors.
- Metadata can be used to provide additional context for the dataset.

---
**Next Steps**:
- Monitor the dataset's processing status using the returned `dataset_id`.
- Perform additional operations such as tagging or querying once the dataset is processed.