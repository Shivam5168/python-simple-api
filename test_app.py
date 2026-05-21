import requests

BASE_URL = "http://127.0.0.1:8000"

def test_azure_api_flow():
    print("Step 1: Testing POST (Creating database row inside Azure SQL)...")
    payload = {"name": "Azure Managed Mouse", "price": 45.50, "in_stock": True}
    response = requests.post(f"{BASE_URL}/items/", json=payload)
    
    assert response.status_code == 200, f"Failed creation: {response.text}"
    data = response.json()
    generated_id = data["id"]
    print(f"✓ Success! Item added to Azure SQL with generated ID: {generated_id}\n")

    print(f"Step 2: Testing GET (Fetching Row ID {generated_id} from Azure SQL)...")
    get_response = requests.get(f"{BASE_URL}/items/{generated_id}")
    
    assert get_response.status_code == 200, f"Failed fetching: {get_response.text}"
    fetched_data = get_response.json()
    assert fetched_data["name"] == "Azure Managed Mouse"
    print("✓ Success! Verified database data accuracy seamlessly.\n")

if __name__ == "__main__":
    print("=== STARTING LIVE AZURE SQL API TESTS ===\n")
    try:
        test_azure_api_flow()
        print("=== ALL TESTS PASSED AGAINST LIVE DATABASE ===")
    except AssertionError as e:
        print(f"❌ TEST FAILED: {e}")
    except requests.exceptions.ConnectionError:
        print("❌ FAILED TO CONNECT: Is your local uvicorn server running?")