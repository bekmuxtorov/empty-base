import requests
import json

BASE_URL = "http://127.0.0.1:8000/api/records/"

def test_crud():
    # 1. CREATE (POST)
    print("--- Testing CREATE ---")
    payload = {
        "device_id": "DEV-001",
        "meter_id": "MTR-123",
        "phone": "+998901234567",
        "pressure": 1.2,
        "temperature": 25.5,
        "volume": 100.0,
        "signal": 80,
        "battery": 95.5,
        "status": "online",
        "timestamp": "2024-03-28T21:00:00Z"
    }
    response = requests.post(BASE_URL, json=payload)
    print(f"Status: {response.status_code}")
    record = response.json()
    print(json.dumps(record, indent=2))
    record_id = record['id']

    # 2. READ (GET List)
    print("\n--- Testing READ (List) ---")
    response = requests.get(BASE_URL)
    print(f"Status: {response.status_code}")
    print(f"Records found: {len(response.json())}")

    # 3. READ (GET Detail)
    print(f"\n--- Testing READ (Detail ID: {record_id}) ---")
    response = requests.get(f"{BASE_URL}{record_id}/")
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

    # 4. UPDATE (PUT/PATCH)
    print(f"\n--- Testing UPDATE (ID: {record_id}) ---")
    update_payload = {"status": "offline", "temperature": 30.0}
    response = requests.patch(f"{BASE_URL}{record_id}/", json=update_payload)
    print(f"Status: {response.status_code}")
    print(json.dumps(response.json(), indent=2))

    # 5. DELETE
    print(f"\n--- Testing DELETE (ID: {record_id}) ---")
    response = requests.delete(f"{BASE_URL}{record_id}/")
    print(f"Status: {response.status_code}")
    if response.status_code == 204:
        print("Successfully deleted!")

if __name__ == "__main__":
    try:
        test_crud()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to the server. Make sure 'python manage.py runserver' is running.")
