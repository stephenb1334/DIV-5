# Query Embeddings

## Endpoint Overview
- **Base URL**: `https://api-atlas.nomic.ai`
- **Endpoint Path**: `/v1/query/embeddings`
- **HTTP Method**: `POST`
- **Description**: Queries the embedding space for similar items based on a provided query vector or text.

## Parameters
### Body Parameters
- **query** (string | array, required):
  - Description: The query text or vector to search for similar embeddings.
- **map_id** (string, required):
  - Description: The unique identifier of the map to query.
- **top_k** (integer, optional):
  - Description: The number of top similar results to return.
  - Default: `10`.

## Responses
### 200 OK
- **Description**: Indicates the query was successfully processed, returning the most similar embeddings.
- **Schema**:
  - **results** (array of objects):
    - Description: List of items matching the query.
    - **Items**:
      - **item_id** (string): The ID of the matched item.
      - **score** (number): Similarity score of the matched item.
      - **metadata** (object): Additional metadata about the matched item.
- **Example Response**:
  ```json
  {
    "results": [
      {
        "item_id": "string",
        "score": 0.98,
        "metadata": {
          "key": "value"
        }
      }
    ]
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
curl -L 'https://api-atlas.nomic.ai/v1/query/embeddings' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer <TOKEN>' \
-d '{
  "query": "search text or vector",
  "map_id": "string",
  "top_k": 10
}'
```

### Python
```python
import requests
import json

url = "https://api-atlas.nomic.ai/v1/query/embeddings"

payload = json.dumps({
  "query": "search text or vector",
  "map_id": "string",
  "top_k": 10
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
- The `map_id` must match an existing map in the system.
- The `query` can be either plain text or a vector representation.

---
**Next Steps**:
- Preprocess the query input to improve similarity results.
- Analyze the returned metadata for further insights.