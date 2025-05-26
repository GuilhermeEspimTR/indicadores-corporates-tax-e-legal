import requests

class Requests:

    auth: tuple

    def run(self, url: str) -> requests.Response | None:
        response = requests.get(url, auth=self.auth)
        if response.status_code == 200:
            # Process the JSON data
            return response
        else:
            print("error on request")
            return None