import requests

class SimpleFlaskClientWithHeaders:
    def __init__(self, base_url='http://localhost:5000/api/v1'):
        self.base_url = base_url

    def get(self, endpoint, headers=None):
        """Send a GET request with optional custom headers."""
        response = requests.get(f'{self.base_url}/{endpoint}', headers=headers)
        return response

    def post(self, endpoint, data=None, headers=None):
        """Send a POST request with JSON data and optional custom headers."""
        response = requests.post(f'{self.base_url}/{endpoint}', json=data, headers=headers)
        return response

    def put(self, endpoint, data=None, headers=None):
        """Send a PUT request with JSON data and optional custom headers."""
        response = requests.put(f'{self.base_url}/{endpoint}', json=data, headers=headers)
        return response

    def delete(self, endpoint, headers=None):
        """Send a DELETE request with optional custom headers."""
        response = requests.delete(f'{self.base_url}/{endpoint}', headers=headers)
        return response

# Example usage (commented out to prevent execution here):
# client = SimpleFlaskClientWithHeaders()
# custom_headers = {'Authorization': 'Bearer YOUR_ACCESS_TOKEN'}
# response = client.get('some_endpoint', headers=custom_headers)
# print(response.status_code, response.json())

