import requests

class FetcherError(RuntimeError):
    pass

class FetcherClient:
    def __init__(self, timeout: float = 30.0):
        self.timeout = timeout

    def fetch_text(self, url: str) -> str:
        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise FetcherError(f"HTTP error while fetching '{url}': {exc}") from exc
        except requests.RequestException as exc:
            raise FetcherError(f"Network error while fetching '{url}': {exc}") from exc
        
        if not response.text.strip():
            raise FetcherError(f"Empty response from {url}")
        
        return response.text