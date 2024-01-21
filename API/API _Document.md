# API Documentation
## 1. Start ExpandReduceFlow Job

**Endpoint**: `/start-expand-reduce`  
**Method**: POST  
**Request Format**:
    ```json
    {
        "input_data": { /* Input Data */ }
    }   
    ```
**Response Format**:
    ```json
    {
        "job_id": "unique-job-id",
        "message": "Job started successfully"
    }
    ```
**Exapmle**:
    **Request**:
        ```json
        {
            "input_data": {"key1": "value1", "key2": "value2"}
        }
        ```
    
    **Response**:
        ```json
        {
            "job_id": <job_id>,
            "message": "Job started successfully"
        }
        ```
        
## 2. Check ExpandReduceFlow Job Status

**Endpoint**: `/check-status/<job_id>`
**Method**: GET
**Response Format**:
    ```json
    {
        "job_id": "unique-job-id",
        "status": "pending|completed|error"
    }
    ```
**Exapmle**:
    **Request**: `GET /check-status/<job_id>`
    
    **Response**:
        ```json
        {
            "job_id": <job_id>,
            "status": "completed"
        }
        ```
        
## 3. Query ExpandReduceFlow Job Results

**Endpoint**: `/check-status/<job_id>`
**Method**: GET
**Response Format**:
    ```json
    {
        "job_id": "unique-job-id",
        "results": [ /* Results Data */ ]
    }
    ```
**Exapmle**:
    **Request**: `GET /results/<job_id>`
    
    **Response**:
        ```json
        {
            "job_id": "123e4567-e89b-12d3-a456-426614174000",
            "results": [
                /* Results Data */
            ]
        }
        ```
