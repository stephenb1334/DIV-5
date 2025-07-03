# Plan for Data Preparation and Nomic Atlas Interaction

This plan outlines the steps to prepare key case data for upload to Nomic Atlas, provide upload instructions, and guide on maximizing value from Atlas's visualizations and AI capabilities. The focus is on a "short version" of prep work to prioritize speed and immediate value for a test upload.

## Phase 1: Data Identification and Prioritization

Identify critical data points from the `evidence matrix.txt` that would benefit most from Nomic Atlas's embedding and visualization capabilities. This includes:

*   **Financial Contribution data:** Property Expenses, Additional Investments.
*   **Timeline of Events:** Trauma Pivot Point, Pre/Post-Trauma Evidence.
*   **Key legal documents:** e.g., Answer to Complaint, Interrogatories, relevant legal letters.
*   **Communications:** SMS, emails that support claims.

## Phase 2: Data Extraction and Formatting (Short Version)

For each identified data point, extract and format the data for Nomic Atlas ingestion. To prioritize speed, we will focus on extracting the most critical textual content and essential metadata.

*   **Structured Data (Financials, Timelines):**
    *   Extract key figures and descriptions into a simple tabular format (e.g., CSV or JSON array of objects).
    *   Include columns for `text` (e.g., a summary of the financial event or timeline entry) and relevant `metadata` fields such as `date`, `category` (e.g., "Financial Contribution", "Timeline Event"), `source_document`, and `legal_theory_supported`.
*   **Unstructured Data (Documents, Communications):**
    *   For legal documents and communications, extract the most relevant sections or summaries as plain text.
    *   For PDFs, if the text is selectable, copy-paste. If not, we will note this as a limitation for the "short version" and prioritize other data.
    *   Include `metadata` fields such as `document_type` (e.g., "Legal Document", "Communication"), `date`, `sender/recipient`, `relevance` (e.g., "CRITICAL", "HIGH"), and `legal_theory_supported`.

## Phase 3: Nomic Atlas Upload Instructions

Provide step-by-step instructions for uploading the prepared data to Nomic Atlas. We will focus on using the Python SDK for its ease of use and programmatic control.

1.  **Install Nomic:** `pip install nomic`
2.  **Prepare your data:** Create a list of dictionaries, where each dictionary represents a data point. Each dictionary must have a `text` field and can include any number of `metadata` fields.
    ```python
    data = [
        {"text": "Summary of financial contribution...", "date": "2023-10-01", "category": "Financial Contribution", "source_document": "Bank Statement Oct 2023", "legal_theory_supported": "Financial Abandonment"},
        {"text": "Description of trauma pivot point...", "date": "2024-03-26", "category": "Timeline Event", "source_document": "Police Report", "legal_theory_supported": "Disability Impact"},
        # ... more data points
    ]
    ```
3.  **Upload to Atlas:**
    ```python
    from nomic import atlas
    import os

    # Ensure your NOMIC_API_KEY is set as an environment variable
    # os.environ['NOMIC_API_KEY'] = 'YOUR_API_KEY'

    project = atlas.map_text(
        data=data,
        id_field="id_field_if_you_have_one", # Optional: unique ID for each data point
        text_field="text",
        name="Stephen Boerner Divorce Case Data - Test Upload",
        colorable_fields=["category", "legal_theory_supported"], # Fields to color by in Atlas UI
        description="Test upload of key case data for Stephen Boerner's divorce case.",
        reset_project_if_exists=True # Set to True for testing to overwrite existing project
    )
    print(f"Atlas project created: {project.maps[0].map_link}")
    ```
4.  **Access your project:** The `map_link` printed in the console will take you directly to your project in the Nomic Atlas UI.

## Phase 4: Maximizing Value from Visualizations and AI

Once the data is in Nomic Atlas, you can immediately start exploring and gaining insights.

*   **Visualizations:**
    *   **Explore the Map:** The Nomic Atlas map will visually cluster your data points based on their semantic similarity. Documents and events related to similar topics will appear close together.
    *   **Filter and Select:** Use the filters on the left sidebar to narrow down data points by `category`, `legal_theory_supported`, `date`, or any other metadata field you included.
    *   **Color by Metadata:** Use the "Color by" option to color data points based on fields like `category` or `legal_theory_supported` to quickly identify patterns.
    *   **Search:** Use the search bar to find specific keywords or phrases. The semantic search will also find related content even if the exact words aren't present.
    *   **Custom Views:** Create and save custom views to highlight specific aspects, such as all documents supporting "Financial Abandonment" or a timeline of "Trauma Pivot Point" events.
*   **AI Layer (Semantic Search & Insights):**
    *   **Semantic Search:** When you search within Nomic Atlas, it's not just keyword matching. It understands the meaning of your query and finds semantically similar documents or data points, even if they use different words. This is crucial for finding relevant legal precedents or evidence.
    *   **Clustering for Insights:** Observe the clusters on the map. Each cluster represents a group of semantically similar data points. This can help you identify new connections, recurring themes, or gaps in your evidence. For example, a cluster of communications around a specific date might reveal a pattern of behavior.
    *   **Query Embeddings (Advanced):** For more advanced AI integration, you can use the Nomic Atlas API to query embeddings programmatically. This allows you to build custom AI agents that can ask questions and retrieve the most relevant information from your case data.

This plan prioritizes getting your data into Nomic Atlas quickly to allow for immediate interaction and value discovery.