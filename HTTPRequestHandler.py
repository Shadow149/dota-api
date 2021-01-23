import requests
from requests.exceptions import HTTPError

class HTTPRequestHandler:   
    def get(self, request: str) -> str:
        """
        Get a response from an HTTP get request

        Args:
            request (str): get request
        """
        # https://realpython.com/python-requests/
        try:
            response = requests.get(request)
            # If the response was successful, no Exception will be raised
            response.raise_for_status()
        except HTTPError as http_err:
            print(f'HTTP error occurred: {http_err}')  # Python 3.6
        except Exception as err:
            print(f'Other error occurred: {err}')  # Python 3.6
        else:
            print('Request successful')
            return response.text
