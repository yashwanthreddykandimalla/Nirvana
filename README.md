# FastAPI - Coalescing Data from Multiple APIs

This project is a FastAPI application that takes a `member_id` as a parameter and makes calls to three different APIs to retrieve `oop_max`, `remaining_oop_max`, and `copay` values. The application then "coalesces" or combines the data from these APIs based on a chosen strategy, which can be configured by the user.

## Features

- Calls three external APIs with the same `member_id`.
- Combines the results using one of the following coalescing strategies:
  - **Average**: Takes the average of the values returned by the APIs.
  - **Most Common**: Picks the value that appears most frequently across the APIs.
  - **Highest**: Selects the highest value from the APIs.
- Handles common error cases like invalid API responses.
- Allows configurable coalescing strategy through a query parameter.
- Unit tests and integration tests are included for validation.

## Requirements

- **Python 3.10+**
- **FastAPI**
- **httpx**
- **pytest**
- **requests**
- **pydantic**

You can install all necessary dependencies using the following command:

```bash
pip install fastapi uvicorn requests pydantic httpx pytest requests_mock
```

Project Structure
.
├── main.py # Main FastAPI application
├── test_main.py # Unit and integration tests
├── README.md # Project documentation
└── requirements.txt # List of dependencies (optional)

Running the Application
Install dependencies:

```bash
pip install -r requirements.txt
```

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

The API will be available at http://127.0.0.1:8000.

Endpoints
/coalesce/{member_id}
This endpoint takes a member_id as a path parameter and an optional strategy query parameter to choose the coalescing strategy. It makes API calls to three external services and returns the coalesced data.

HTTP Method: GET
Path Parameter:
member_id (integer): The ID of the member.
Query Parameter (optional):
strategy (string): The coalescing strategy to use (average, most_common, highest). Defaults to average.

Example:

```bash
GET /coalesce/1?strategy=average
```

Sample Response:

```json
{
  "oop_max": 13333,
  "remaining_oop_max": 8666,
  "copay": 17333
}
```

Running Tests
The project includes unit tests for the coalescing logic and integration tests for the FastAPI endpoints. Tests are written using pytest and requests_mock.

To run the tests, simply execute:

```bash
pytest test_main.py
```
