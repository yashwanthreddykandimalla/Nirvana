import pytest
from fastapi.testclient import TestClient
from main import app, coalesce_data, APIResponse

client = TestClient(app)

# Unit test for the coalesce_data function
def test_coalesce_data_average():
    responses = [
        APIResponse(oop_max=10000, remaining_oop_max=9000, copay=1000),
        APIResponse(oop_max=20000, remaining_oop_max=9000, copay=50000),
        APIResponse(oop_max=10000, remaining_oop_max=8000, copay=1000)
    ]
    result = coalesce_data(responses, strategy="average")
    
    # Validate the average of the values
    assert result.oop_max == (10000 + 20000 + 10000) // 3  # 13333
    assert result.remaining_oop_max == (9000 + 9000 + 8000) // 3  # 8666
    assert result.copay == (1000 + 50000 + 1000) // 3  # 17333


def test_coalesce_data_most_common():
    responses = [
        APIResponse(oop_max=10000, remaining_oop_max=9000, copay=1000),
        APIResponse(oop_max=20000, remaining_oop_max=9000, copay=50000),
        APIResponse(oop_max=10000, remaining_oop_max=8000, copay=1000)
    ]
    result = coalesce_data(responses, strategy="most_common")
    
    # Validate the most common value
    assert result.oop_max == 10000  # Most common
    assert result.remaining_oop_max == 9000  # Most common
    assert result.copay == 1000  # Most common

def test_coalesce_data_highest():
    responses = [
        APIResponse(oop_max=10000, remaining_oop_max=9000, copay=1000),
        APIResponse(oop_max=20000, remaining_oop_max=9000, copay=50000),
        APIResponse(oop_max=10000, remaining_oop_max=8000, copay=1000)
    ]
    result = coalesce_data(responses, strategy="highest")
    
    # Validate the highest value
    assert result.oop_max == 20000  # Highest
    assert result.remaining_oop_max == 9000  # Highest
    assert result.copay == 50000  # Highest


# Test FastAPI route by mocking external API responses
@pytest.fixture
def mock_api_responses(requests_mock):
    requests_mock.get("https://api1.com?member_id=1", json={"oop_max": 10000, "remaining_oop_max": 9000, "copay": 1000})
    requests_mock.get("https://api2.com?member_id=1", json={"oop_max": 20000, "remaining_oop_max": 9000, "copay": 50000})
    requests_mock.get("https://api3.com?member_id=1", json={"oop_max": 10000, "remaining_oop_max": 8000, "copay": 1000})

# Test the FastAPI endpoint with mocked responses
def test_get_coalesced_data(mock_api_responses):
    response = client.get("/coalesce/1?strategy=average")
    assert response.status_code == 200
    data = response.json()
    
    # Validate average calculation
    assert data['oop_max'] == (10000 + 20000 + 10000) // 3  # 13333
    assert data['remaining_oop_max'] == (9000 + 9000 + 8000) // 3  # 8666
    assert data['copay'] == (1000 + 50000 + 1000) // 3  # 17333


def test_get_coalesced_data_most_common(mock_api_responses):
    response = client.get("/coalesce/1?strategy=most_common")
    assert response.status_code == 200
    data = response.json()

    # Validate most common values
    assert data['oop_max'] == 10000
    assert data['remaining_oop_max'] == 9000
    assert data['copay'] == 1000
