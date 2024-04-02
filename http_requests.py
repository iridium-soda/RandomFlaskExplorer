import requests


class SimpleFlaskClientWithHeaders:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url

    def get(self, endpoint, headers=None, params=None):
        """Send a GET request and return status code and parsed JSON."""
        response = requests.get(
            f"{self.base_url}/{endpoint}", headers=headers, params=params
        )
        return response.status_code, self._resolve_response(response)

    def post(self, endpoint, data=None, headers=None):
        """Send a POST request and return status code and parsed JSON."""
        """Use data for form-encoded data (application/x-www-form-urlencoded or multipart/form-data).
Use json for JSON-encoded data (application/json)."""
        response = requests.post(
            f"{self.base_url}/{endpoint}", data=data, headers=headers
        )
        return response.status_code, self._resolve_response(response)

    def put(self, endpoint, data=None, headers=None, params=None):
        """Send a PUT request and return status code and parsed JSON."""
        response = requests.put(
            f"{self.base_url}/{endpoint}", json=data, headers=headers, params=params
        )
        return response.status_code, self._resolve_response(response)

    def delete(self, endpoint, headers=None, params=None):
        """Send a DELETE request and return status code and parsed JSON."""
        response = requests.delete(
            f"{self.base_url}/{endpoint}", headers=headers, params=params
        )
        return response.status_code, self._resolve_response(response)

    def patch(self, endpoint, data=None, json=None, params=None, headers=None):
        """Send a PATCH request with optional data, JSON payload, query parameters, and headers."""
        response = requests.patch(
            endpoint, data=data, json=json, params=params, headers=headers
        )
        return response.status_code, self._resolve_response(response)

    @staticmethod
    def _resolve_response(response):
        """Attempt to parse JSON content from a response."""
        try:
            return response.json()
        except ValueError:
            # Return None or raise an error if the response doesn't contain JSON
            return None


def handle_response(self, response):
    """Handle the HTTP response, checking for error codes and taking appropriate action."""
    if response.status_code == 401:
        # Handle Unauthorized Error
        print("Unauthorized (401): Check your credentials.")
        # Here, you might log the error, refresh the token, or raise an exception
    elif 400 <= response.status_code < 500:
        # Handle client errors
        print(f"Client Error ({response.status_code}): {response.text}")
        # Log or raise an exception
    elif 500 <= response.status_code:
        # Handle server errors
        print(f"Server Error ({response.status_code}): {response.text}")
        # Log or raise an exception
    return response


# Example usage (commented out to prevent execution here):
# client = SimpleFlaskClientWithHeaders()
# custom_headers = {'Authorization': 'Bearer YOUR_ACCESS_TOKEN'}
# response = client.get('some_endpoint', headers=custom_headers)
# print(response.status_code, response.json())
