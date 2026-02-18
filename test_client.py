"""
Example client script for testing the AG-UI agent endpoint.

This script demonstrates how to interact with the deployed agent
using simple HTTP requests.
"""

import json
import requests


def test_agent_endpoint(base_url: str = "http://localhost:8000"):
    """
    Test the AG-UI agent endpoint with a sample query.
    
    Args:
        base_url: Base URL of the agent server
    """
    print("=" * 70)
    print("Testing AG-UI Agent Endpoint")
    print("=" * 70)
    print(f"\nBase URL: {base_url}")
    
    # Test 1: Basic connectivity
    print("\n1. Testing basic connectivity...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✓ Endpoint is reachable")
        else:
            print(f"   ⚠ Unexpected status code: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Connection failed: {e}")
        return
    
    # Test 2: Send a test message to the agent
    print("\n2. Sending test message to agent...")
    test_message = {
        "messages": [
            {
                "role": "user",
                "content": "Hello! Can you help me with an intake form?"
            }
        ]
    }
    
    try:
        response = requests.post(
            f"{base_url}/chat",
            json=test_message,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✓ Agent responded successfully")
            data = response.json()
            if "response" in data:
                print(f"\n   Agent response: {data['response'][:100]}...")
        else:
            print(f"   Response: {response.text[:200]}")
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Request failed: {e}")
    except json.JSONDecodeError as e:
        print(f"   ✗ Failed to parse response: {e}")
    
    # Test 3: Query with knowledge base requirement
    print("\n3. Testing knowledge base query...")
    kb_query = {
        "messages": [
            {
                "role": "user",
                "content": "What projects are in the knowledge base that I can reference for this intake form?"
            }
        ]
    }
    
    try:
        response = requests.post(
            f"{base_url}/chat",
            json=kb_query,
            headers={"Content-Type": "application/json"}
        )
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✓ Knowledge base query successful")
            data = response.json()
            if "response" in data:
                print(f"\n   Agent response: {data['response'][:200]}...")
    except requests.exceptions.RequestException as e:
        print(f"   ✗ Request failed: {e}")
    
    print("\n" + "=" * 70)
    print("Testing Complete")
    print("=" * 70)


if __name__ == "__main__":
    import sys
    
    # Allow custom base URL as command line argument
    base_url = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:8000"
    test_agent_endpoint(base_url)
