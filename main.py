from fastapi import FastAPI, HTTPException
import requests
from pydantic import BaseModel, Field
from typing import List

app = FastAPI()

# Model for API responses
class APIResponse(BaseModel):
    oop_max: int = Field(..., description="Out-of-pocket max in cents")
    remaining_oop_max: int = Field(..., description="Remaining out-of-pocket max in cents")
    copay: int = Field(..., description="Copay in cents")

# Strategy to coalesce data (simple average, most common, or highest)
class CoalescingStrategy:
    @staticmethod
    def average(values: List[int]) -> int:
        return sum(values) // len(values)

    @staticmethod
    def most_common(values: List[int]) -> int:
        return max(set(values), key=values.count)

    @staticmethod
    def highest(values: List[int]) -> int:
        return max(values)

# Main function to get the final combined response
def coalesce_data(responses: List[APIResponse], strategy="average"):
    if strategy == "average":
        oop_max = CoalescingStrategy.average([resp.oop_max for resp in responses])
        remaining_oop_max = CoalescingStrategy.average([resp.remaining_oop_max for resp in responses])
        copay = CoalescingStrategy.average([resp.copay for resp in responses])
    elif strategy == "most_common":
        oop_max = CoalescingStrategy.most_common([resp.oop_max for resp in responses])
        remaining_oop_max = CoalescingStrategy.most_common([resp.remaining_oop_max for resp in responses])
        copay = CoalescingStrategy.most_common([resp.copay for resp in responses])
    elif strategy == "highest":
        oop_max = CoalescingStrategy.highest([resp.oop_max for resp in responses])
        remaining_oop_max = CoalescingStrategy.highest([resp.remaining_oop_max for resp in responses])
        copay = CoalescingStrategy.highest([resp.copay for resp in responses])
    else:
        raise ValueError("Invalid strategy")
    
    return APIResponse(oop_max=oop_max, remaining_oop_max=remaining_oop_max, copay=copay)

# Function to call external APIs
def call_api(url: str, member_id: int):
    try:
        response = requests.get(f"{url}?member_id={member_id}")
        response.raise_for_status()
        return APIResponse(**response.json())
    except requests.exceptions.RequestException:
        raise HTTPException(status_code=502, detail=f"Error calling {url}")
    except ValueError:
        raise HTTPException(status_code=500, detail=f"Invalid data from {url}")

# Main route
@app.get("/coalesce/{member_id}", response_model=APIResponse)
def get_coalesced_data(member_id: int, strategy: str = "average"):
    api_urls = [
        "https://api1.com",
        "https://api2.com",
        "https://api3.com"
    ]

    responses = []
    
    # Call APIs
    for url in api_urls:
        responses.append(call_api(url, member_id))

    # Coalesce the data
    return coalesce_data(responses, strategy)
